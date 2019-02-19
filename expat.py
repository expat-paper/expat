import enum
import re
import argparse
import calendar
import time
import csv
import codecs
from os import path
from antlr4 import *
from lib.OPOLLexer import OPOLLexer
from lib.OPOLParser import OPOLParser
from lib.OPOLVisitor import OPOLVisitor
from z3 import *

OPENHAB_POLICY_VARIABLES = []
REGEX_DICT = {
    'rule': re.compile(r'rule\s+\"(?P<rule_name>.*)\"\s*', re.IGNORECASE),
    'trigger': re.compile(
        r'\s*item\s+(?P<item_name>.[^\s]*)\s+(received)?\s*(?P<cmd_type>(command|update|changed))\s*(from)?\s*(.[^\s]*)?\s*(to)?\s*(?P<cmd>.[^\s]*)?\s*',
        re.IGNORECASE),
    'then': re.compile(r'\s*then\s*', re.IGNORECASE),
    'action': re.compile(
        r'\s*(?P<action_item>.[^\s]*)\s*\.\s*(sendCommand|postUpdate)\s*\(\s*(?P<action_cmd>.[^\s]*)\s*\)\s*',
        re.IGNORECASE),
}


class Policy:
    pass


class Invariant:
    pass


class Desire(enum.Enum):
    NOT_EXPECT = 0
    EXPECT = 1


class Analysis:
    pass


class ConditionAST:
    def __init__(self):
        self.type = None
        self.value = None
        self.children = []

    def get_reverse_children(self):
        children = self.children[:]
        children.reverse()
        return children


class CustomVisitorOH(OPOLVisitor):
    def __init__(self):
        self.policies = []

    def visitPolicy_statement(self, ctx: OPOLParser.Policy_statementContext):
        pol = Policy()
        pol.name = ctx.STRING()
        invs = []
        for c in ctx.invariant():
            invs.append(c.accept(self))
        pol.invariants = invs
        self.policies.append(pol)

    def visitInvariant(self, ctx: OPOLParser.InvariantContext):
        inv = Invariant()
        inv.name = ctx.STRING()
        inv.situation, inv.desire, inv.expectation = ctx.invariant_body().accept(self)
        return inv

    def visitInvariant_body(self, ctx: OPOLParser.Invariant_bodyContext):
        sit = ctx.situation_block().accept(self)
        des = ctx.desire_block().accept(self)
        exp = ctx.expectation_block().accept(self)
        return sit, des, exp

    def visitSituation_condition(self, ctx: OPOLParser.Situation_conditionContext):
        if ctx.ANY():
            any_ast_node = ConditionAST()
            any_ast_node.type = 'any'
            any_ast_node.value = 'true'
            return any_ast_node
        else:
            return ctx.condition().accept(self)

    def visitDesire_value(self, ctx: OPOLParser.Desire_valueContext):
        if ctx.NOT():
            return Desire.NOT_EXPECT
        else:
            return Desire.EXPECT

    def visitBoolean_expression(self, ctx: OPOLParser.Boolean_expressionContext):
        if ctx.key_name():
            atomic_ast_node = ConditionAST()
            atomic_ast_node.type = 'atomic'
            atomic_ast_node.value = ctx.operator().getText()
            key_name_ast_node = ctx.key_name().accept(self)
            atomic_ast_node.children.append(key_name_ast_node)
            value_ast_node = ctx.value().accept(self)
            if value_ast_node.type == 'string':
                if not (key_name_ast_node.type in ['drk', 'ark']):
                    if not (key_name_ast_node.value in ['triggered_event', 'triggered_event_device']):
                        value_ast_node.value = "'" + value_ast_node.value + "'"
            atomic_ast_node.children.append(value_ast_node)
            return atomic_ast_node
        if ctx.NOT():
            not_ast_node = ConditionAST()
            not_ast_node.type = 'not'
            not_ast_node.value = 'not'
            not_ast_node.children.append(ctx.getChild(1).accept(self))
            return not_ast_node
        else:
            bexp_ast_node = ConditionAST()
            bexp_ast_node.type = 'bexp'
            bexp_ast_node.value = ctx.boolean_operator().getText().lower()
            bexp_ast_node.children.append(ctx.getChild(0).accept(self))
            bexp_ast_node.children.append(ctx.getChild(2).accept(self))
            return bexp_ast_node

    def visitTriggered_source_key(self, ctx: OPOLParser.Triggered_source_keyContext):
        tsk_ast_node = ConditionAST()
        tsk_ast_node.type = 'tsk'
        tsk_ast_node.value = ctx.getText()
        return tsk_ast_node

    def visitTriggered_event_key(self, ctx: OPOLParser.Triggered_event_keyContext):
        tek_ast_node = ConditionAST()
        tek_ast_node.type = 'tek'
        tek_ast_node.value = ctx.getText()
        return tek_ast_node

    def visitDevice_related_key(self, ctx: OPOLParser.Device_related_keyContext):
        drk_ast_node = ConditionAST()
        drk_ast_node.type = 'drk'
        drk_ast_node.value = ctx.getChild(0).getText().lower()
        device_ast_node = ConditionAST()
        device_ast_node.type = 'device'
        device_ast_node.value = ctx.STRING().getText()
        drk_ast_node.children.append(device_ast_node)
        return drk_ast_node

    def visitAction_related_key(self, ctx: OPOLParser.Action_related_keyContext):
        ark_ast_node = ConditionAST()
        ark_ast_node.type = 'ark'
        ark_ast_node.value = ctx.getText()
        return ark_ast_node

    def visitSystem_related_key(self, ctx: OPOLParser.System_related_keyContext):
        srk_ast_node = ConditionAST()
        srk_ast_node.type = 'srk'
        srk_ast_node.value = ctx.getText()
        return srk_ast_node

    def visitDate_time_related_key(self, ctx: OPOLParser.Date_time_related_keyContext):
        dtrk_ast_node = ConditionAST()
        dtrk_ast_node.type = 'dtrk'
        dtrk_ast_node.value = ctx.getText()
        return dtrk_ast_node

    def visitValue(self, ctx: OPOLParser.ValueContext):
        value_ast_node = ConditionAST()
        if ctx.NUMBER():
            value_ast_node.type = 'number'
            value_ast_node.value = ctx.getText()
        elif ctx.BOOLEAN():
            value_ast_node.type = 'boolean'
            value_ast_node.value = ctx.getText().lower()
        elif ctx.TIME():
            value_ast_node.type = 'time'
            value_ast_node.value = ctx.getText()
        elif ctx.DATE():
            value_ast_node.type = 'date'
            value_ast_node.value = ctx.getText()
        else:
            value_ast_node.type = 'string'
            value_ast_node.value = ctx.getText()
        return value_ast_node


class CustomVisitorZ3(OPOLVisitor):
    def __init__(self):
        self.solver = Solver()
        self.solver.set(unsat_core=True)
        self.triggered_event_used = False
        self.action_command_used = False
        self.action_device_used = False
        self.triggered_event_device_used = False
        self.current_date_used = False
        self.current_time_used = False
        self.device_state_list = []
        self.invariants = []
        self.analysis = []

        # rule_name
        rule_name_list = ['a', 'b', 'c', 'none']
        self.RuleNameSpace = Datatype('RuleNameSpace')
        for rule in rule_name_list:
            self.RuleNameSpace.declare(rule)
        self.RuleNameSpace = self.RuleNameSpace.create()
        self.rule_name = Const('rule_name', self.RuleNameSpace)

        # device_item
        self.device_list = {}
        try:
            device_list_csv = csv.reader(codecs.open('device_list.csv', 'rU'))
            next(device_list_csv)
            for row in device_list_csv:
                self.device_list[row[0].strip()] = row[1].strip()
        except:
            self.logger.debug('An error occurred in loading device list info.\n')
            sys.exit(1)
        self.Device = Datatype('Device')
        for item in self.device_list.keys():
            self.Device.declare(item)
        self.Device = self.Device.create()
        self.triggered_event_device = Const('triggered_event_device', self.Device)
        self.action_device = Const('action_device', self.Device)

        # event type
        trigger_type_list = ['command', 'update', 'changed', 'None']
        self.TriggerTypeSpace = Datatype('TriggerTypeSpace')
        for type in trigger_type_list:
            self.TriggerTypeSpace.declare(type)
        self.TriggerTypeSpace = self.TriggerTypeSpace.create()
        self.trigger_type = Const('trigger_type', self.TriggerTypeSpace)

        self.switch_command_list = ['ON', 'OFF']
        self.contact_command_list = ['OPEN', 'CLOSED']
        self.rollershutter_command_list = ['UP', 'DOWN', 'STOP', 'MOVE']

        self.Command = Datatype('Command')
        for cmd in self.switch_command_list + self.contact_command_list + self.rollershutter_command_list:
            self.Command.declare(cmd)
        self.Command = self.Command.create()
        self.triggered_event = Const('triggered_event', self.Command)
        self.action_command = Const('action_command', self.Command)

    def visitPolicy_statement(self, ctx: OPOLParser.Policy_statementContext):
        invs = []
        for c in ctx.invariant():
            invs.append(Bool(c.accept(self)))
        if len(invs) == 1:
            self.solver.add(Bool(ctx.STRING().getText()) == invs[0])
        elif len(invs) > 1:
            self.solver.add(Bool(ctx.STRING().getText()) == And(invs))

    def visitInvariant(self, ctx: OPOLParser.InvariantContext):
        self.solver.add(Bool(ctx.STRING().getText()) == ctx.invariant_body().accept(self))
        # self.solver.assert_and_track(ctx.invariant_body().accept(self), ctx.STRING().getText())
        self.invariants.append(ctx.STRING().getText())
        return ctx.STRING().getText()

    def visitInvariant_body(self, ctx: OPOLParser.Invariant_bodyContext):
        expect = ctx.desire_block().accept(self)
        return Implies(ctx.situation_block().accept(self), expect(ctx.expectation_block().accept(self)))

    def visitSituation_condition(self, ctx: OPOLParser.Situation_conditionContext):
        if ctx.ANY():
            return True
        else:
            return ctx.condition().accept(self)

    def visitDesire_value(self, ctx: OPOLParser.Desire_valueContext):
        if ctx.NOT():
            return lambda x: Not(x)
        else:
            return lambda x: x

    def visitBoolean_expression(self, ctx: OPOLParser.Boolean_expressionContext):
        if ctx.key_name():
            op = self.visit(ctx.getChild(1))
            key = self.visit(ctx.getChild(0))
            value, value_type = self.visit(ctx.getChild(2))
            if value_type == 'string':
                if key == 'rule_name':
                    r_name = value.lower().replace('-', '_')
                    x = self.rule_name
                    y = getattr(self.RuleNameSpace, r_name)
                elif key == 'triggered_event_device':
                    x = self.triggered_event_device
                    y = getattr(self.Device, value)
                    self.triggered_event_device_used = True
                elif key == 'trigger_type':
                    x = self.trigger_type
                    y = getattr(self.TriggerTypeSpace, value)
                elif key == 'triggered_event':
                    x = self.triggered_event
                    y = getattr(self.Command, value.upper())
                    self.triggered_event_used = True
                elif key == 'action_device':
                    x = self.action_device
                    y = getattr(self.Device, value)
                    self.action_device_used = True
                elif key == 'action_command':
                    x = self.action_command
                    y = getattr(self.Command, value.upper())
                    self.action_command_used = True
                elif '_state' in key:
                    if key not in self.device_state_list:
                        self.device_state_list.append(key)
                    x = Const(key, self.Command)
                    y = getattr(self.Command, value.upper())
            elif value_type == 'number':
                if '_state' in key:
                    x = Int(key)
                    y = int(value)
            elif value_type == 'boolean':
                if '_state' in key:
                    x = Bool(key)
                    y = bool(value)
            elif value_type == 'date':
                self.current_date_used = True
                x = Int(key)
                modified_value = value.replace('_','-')
                y = calendar.timegm(time.strptime(modified_value, '%Y-%m-%d'))
            elif value_type == 'time':
                self.current_time_used = True
                x = Int(key)
                tm = value.strip().split(':')
                y = int(tm[0]) * 3600 + int(tm[1]) * 60 + int(tm[2])

            return op(x, y)
        if ctx.NOT():
            return Not(ctx.getChild(1).accept(self))
        else:
            op = self.visit(ctx.getChild(1))
            x = self.visit(ctx.getChild(0))
            y = self.visit(ctx.getChild(2))
            return op(x, y)

    def visitOperator(self, ctx:OPOLParser.OperatorContext):
        return {
            "=":  lambda x,y: x == y,
            "!=": lambda x,y: x != y,
            ">":  lambda x,y: x > y,
            ">=": lambda x,y: x >= y,
            "<":  lambda x,y: x < y,
            "<=": lambda x,y: x <= y,
        }[ctx.getText()]

    def visitBoolean_operator(self, ctx:OPOLParser.Boolean_operatorContext):
        return {
            "and": lambda x, y: And(x, y),
            "or": lambda x, y: Or(x, y),
        }[ctx.getText()]

    def visitTriggered_source_key(self, ctx: OPOLParser.Triggered_source_keyContext):
        return ctx.getText()

    def visitTriggered_event_key(self, ctx: OPOLParser.Triggered_event_keyContext):
        return ctx.getText()

    def visitDevice_related_key(self, ctx: OPOLParser.Device_related_keyContext):
        return ctx.STRING().getText() + "_" + ctx.getChild(0).getText().lower()

    def visitAction_related_key(self, ctx: OPOLParser.Action_related_keyContext):
        return ctx.getText()

    def visitDate_time_related_key(self, ctx: OPOLParser.Date_time_related_keyContext):
        return ctx.getText()

    def visitValue(self, ctx: OPOLParser.ValueContext):
        if ctx.NUMBER():
            return ctx.getText(), 'number'
        elif ctx.BOOLEAN():
            return ctx.getText(), 'boolean'
        elif ctx.TIME():
            return ctx.getText(), 'time'
        elif ctx.DATE():
            return ctx.getText(), 'date'
        else:
            return ctx.getText(), 'string'

    def visitPolicy_analysis(self, ctx: OPOLParser.Policy_analysisContext):
        ana = Analysis()
        ana.type = ctx.analysis_command().getText().lower()
        if ctx.analysis_expression().getText().strip():
            ana.lhs, ana.opr, ana.rhs = ctx.analysis_expression().accept(self)
        self.analysis.append(ana)

    def visitAnalysis_expression(self, ctx: OPOLParser.Analysis_expressionContext):
        if ctx.analysis_operator():
            return ctx.getChild(0).getText(), ctx.getChild(1).getText(), ctx.getChild(2).getText()


def perform_analysis(visitor):
    if visitor.current_time_used:
        visitor.solver.add(And(Int('current_time') <= 86399, Int('current_time') >= 0))
    if visitor.current_date_used:
        visitor.solver.add(Int('current_date') >= calendar.timegm(time.gmtime()))
    for a in visitor.analysis:
        print('\n\nEncoding of input policy in SMT-LIB2 format for {} analysis:'.format(a.type.lower()))
        print('-'*70)
        if a.type.upper() == 'CONSISTENCY':
            inv_list = []
            for inv in visitor.invariants:
                inv_list.append(Bool(inv))
            print(visitor.solver.sexpr())
            print('\n\nResult:')
            print('-' * 70)
            res = visitor.solver.check(inv_list)
        elif a.type.upper() == 'ENTAILMENT':
            entailment = Implies(Bool(a.lhs), Bool(a.rhs))
            visitor.solver.add(Not(entailment))
            print(visitor.solver.sexpr())
            print('\n\nResult:')
            print('-' * 70)
            res = visitor.solver.check()
        elif a.type.upper() == 'EQUIVALENCE':
            equivalence = Bool(a.lhs) == Bool(a.rhs)
            visitor.solver.add(Not(equivalence))
            print(visitor.solver.sexpr())
            print('\n\nResult:')
            print('-' * 70)
            res = visitor.solver.check()
        if a.type.upper() == 'CONSISTENCY':
            if res == sat:
                print('Invariants are consistent!')
                print('\n\n')
                m = visitor.solver.model()
                print('Model:')
                print('-' * 70)
                show_model(m)
            else:
                print('Invariants are inconsistent!\n')
                print('\n\n')
                print('Conflicting invariants (i.e., Unsat cores):')
                print('-' * 70)
                print(visitor.solver.unsat_core())
                print('\n\n')
        else:
            if res == unsat:
                print('Invariants satisfy {} check!\n'.format(a.type.lower()))
            else:
                print('Invariants violate {} check!\n'.format(a.type.lower()))
                print('\n\n')
                m = visitor.solver.model()
                print('Counterexample:')
                print('-' * 70)
                show_model(m)
        print(('*' * 70) + '\n')

def show_model(m):
    for decl in m.decls():
        m_decl = m[decl]
        if str(decl) == 'current_date':
            m_decl = time.strftime('%Y-%m-%d', time.gmtime(int(str(m_decl))))
        elif str(decl) == 'current_time':
            seconds = int(str(m_decl))
            m_decl = "%s:%s:%s" % (
                math.floor(seconds / 3600), math.floor(seconds / 60 % 60), math.floor(seconds % 60))
        print("%s: %s" % (decl, m_decl))
    print('\n\n')


def translate_to_dsl(root):
    if root.type in ['tsk', 'tek', 'ark', 'srk', 'dtrk']:
        if root.value not in OPENHAB_POLICY_VARIABLES:
            OPENHAB_POLICY_VARIABLES.append(root.value)
    elif root.type == 'drk':
        value = root.value
        child = root.children[0]
        value = child.value + '_' + value
        if value not in OPENHAB_POLICY_VARIABLES:
            OPENHAB_POLICY_VARIABLES.append(value)

    root_value = root.value
    if root.type == 'atomic':
        if root.value == '=':
            root_value = '=='
        if root.children[1].type == 'date':
            root.children[1].value = "(new DateTime(" + root.children[1].value + "))"
            if root.value == '>':
                root_value = '.isAfter'
            elif root.value == '<':
                root_value = '.isBefore'
            elif root.value == '==':
                root_value = '.equals'

    elif root.type == 'bexp':
        if root.value == 'and':
            root_value = '&&'
        else:
            root_value = '||'
    elif root.type == 'drk':
        root_value = root.value
        root = root.children[0]
        root_value = root.value + '_' + root_value
    elif root.type == 'time':
        time = root.value.split(':')
        root_value = str((int(time[0]) * 3600) + (int(time[1]) * 60) + int(time[2]))

    if not root.children:
        expr_string = root_value + ' '
        return expr_string
    else:
        if len(root.children) == 1:
            expr_string = root_value + ' '
            expr_string += translate_to_dsl(root.children[0])
            return expr_string
        elif len(root.children) == 2:
            expr_string = translate_to_dsl(root.children[0])
            expr_string += root_value + ' '
            expr_string += translate_to_dsl(root.children[1])
            return expr_string


def get_parse_tree(file_name):
    pol_src_code = FileStream(file_name)
    lexer = OPOLLexer(pol_src_code)
    stream = CommonTokenStream(lexer)
    parser = OPOLParser(stream)
    tree = parser.policy_language()
    return tree, parser.getNumberOfSyntaxErrors()


def parse_line(line):
    for key, rx in REGEX_DICT.items():
        match = rx.search(line)
        if match:
            return key, match
    return None, None


def parse_n_instrument(filepath, inst_file_path):
    with open(filepath, 'r') as file_object:
        with open(inst_file_path, 'a') as tmp_file:
            line = file_object.readline()
            rule_name_stmt = ''
            triggered_event_device_stmt = ''
            triggered_event_stmt = ''
            trigger_type_stmt = ''
            while line:
                key, match = parse_line(line)
                if key == 'rule':
                    rule_name_stmt = "\tval rule_name = '" + match.group('rule_name').lower() + "'\n"
                    tmp_file.write(line)
                elif key == 'trigger':
                    triggered_event_device_stmt = "\tval triggered_event_device = " + match.group('item_name') + "\n"
                    trigger_type_stmt = "\tval trigger_type = '" + match.group('cmd_type') + "'\n"
                    triggered_event_stmt = "\tval triggered_event = NULL\n" if not match.group(
                        'cmd') else match.group('cmd').strip() + "\n"
                    tmp_file.write(line)
                elif key == 'then':
                    tmp_file.write(line)
                    tmp_file.write(rule_name_stmt)
                    tmp_file.write(triggered_event_device_stmt)
                    tmp_file.write(trigger_type_stmt)
                    tmp_file.write(triggered_event_stmt)
                elif key == 'action':
                    action_item = match.group('action_item')
                    action_cmd = match.group('action_cmd')
                    indent = line.split(action_item)
                    tmp_file.write(indent[0] + 'lock.lock()\n')
                    tmp_file.write(indent[0] + 'try {\n')
                    tmp_file.write(indent[
                                       0] + '\tif (policy_check.apply(rule_name, triggered_event_device, triggered_event, trigger_type, ' + action_item + ', ' + action_cmd + ')) {\n')
                    tmp_file.write('\t\t' + line)
                    tmp_file.write(indent[0] + '\t}\n')
                    tmp_file.write(indent[0] + '} finally{\n')
                    tmp_file.write(indent[0] + '\tlock.unlock()\n')
                    tmp_file.write(indent[0] + '}\n')
                else:
                    tmp_file.write(line)
                line = file_object.readline()


def encode_openhab(invs, rule_file_name, inst_rule_file_name):
    invs_dsl_string = []
    permission_string = ""
    for inv in invs:
        name = str(inv.name)
        sit_root_ast = inv.situation
        exp_root_ast = inv.expectation
        sit_string = '( ' + translate_to_dsl(sit_root_ast) + ')'
        des_string = '! ' if inv.desire == Desire.NOT_EXPECT else ''
        exp_string = '( ' + translate_to_dsl(exp_root_ast) + ')'
        inv_string = 'val ' + name + ' = ! ' + sit_string + ' || ' + des_string + exp_string
        invs_dsl_string.append(inv_string)
        permission_string += name + ' && '
    with open(inst_rule_file_name, 'w') as modified:
        modified.write("import java.util.concurrent.locks.ReentrantLock\n")
        modified.write("import org.eclipse.smarthome.core.types.State\n\n")
        modified.write("val ReentrantLock lock  = new ReentrantLock()\n\n")
        modified.write(
            "val policy_check = [String my_rule_name, GenericItem my_triggered_event_device, State my_triggered_event, String my_trigger_type, GenericItem my_action_device, State my_action_command |\n\n")

        for var in OPENHAB_POLICY_VARIABLES:
            if '_state' in var:
                device = var.replace('_state', '')
                declared_var = 'val ' + var + ' = if (' + device + ' == my_action_device) my_action_command else ' + device + '.state'

            else:
                switcher = {
                    'rule_name': "my_rule_name",
                    'triggered_event_device': "my_triggered_event_device",
                    'triggered_event': "my_triggered_event",
                    'trigger_type': "my_trigger_type",
                    'action_device': "my_action_device",
                    'action_command': "my_action_command",
                    'current_time': 'now.getSecondOfDay',
                    'current_date': 'now',
                }
                declared_var = 'val ' + var + ' = ' + switcher.get(var)

            modified.write("\t" + declared_var + "\n")
        modified.write("\n")
        for inv_str in invs_dsl_string:
            modified.write("\t" + inv_str + "\n")
        modified.write("\n\tval permission = " + permission_string[:-3] + "\n")
        modified.write(
            '\n\tlogInfo("PolicyEnforcement", "Action " + my_action_command + ", on device " + my_action_device.getName() + if(permission) " permitted!" else " denied!")\n')
        modified.write("\n\treturn permission\n]\n\n")
    parse_n_instrument(rule_file_name, inst_rule_file_name)


def check_file(filename):
    if path.exists(filename):
        return True
    else:
        print("The file, '%s', does not exist!" % filename)
        return False


def setup_args():
    parser = argparse.ArgumentParser(
        description="PolicyInstrumentator is a research tool enforcing policies on OpenHAB smart home system.")
    parser.add_argument("command", choices=['analysis', 'instrument'])
    parser.add_argument("policy", help="The input file containing user policies.")
    parser.add_argument("rule", help="The input file containing automation rules.", nargs='?')
    parser.add_argument("inst_rule", help="The output file containing instrumented version of automation rules.", nargs='?')
    args = parser.parse_args()
    if args.command == 'instrument' and args.rule is None and args.inst_rule is None:
        parser.error("instrument requires <rule> and <inst_rule> file paths.")
    return args



args = setup_args()
if args.command == 'instrument':
    if check_file(args.policy) and check_file(args.rule):
        tree, err = get_parse_tree(args.policy)
        if err == 0:
            visitor = CustomVisitorOH()
            try:
                tree.accept(visitor)
            except Exception as e:
                print("\nSyntax error occurred in the policy file!\n")
                sys.exit(1)
            invariants = []
            for p in visitor.policies:
                invariants.extend(p.invariants)
            try:
                encode_openhab(invariants, args.rule, args.inst_rule)
            except Exception as e:
                print("\nAn error occurred in encoding policies into openhab rule!\n")
                sys.exit(1)
            print('Done!')
else:
    if check_file(args.policy):
        tree, err = get_parse_tree(args.policy)
        if err == 0:
            visitor = CustomVisitorZ3()
            try:
                tree.accept(visitor)
            except Exception as e:
                print("\nSyntax error occurred in the policy file!\n")
                sys.exit(1)
            perform_analysis(visitor)


