# Generated from OPOL.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .OPOLParser import OPOLParser
else:
    from OPOLParser import OPOLParser

# This class defines a complete listener for a parse tree produced by OPOLParser.
class OPOLListener(ParseTreeListener):

    # Enter a parse tree produced by OPOLParser#policy_language.
    def enterPolicy_language(self, ctx:OPOLParser.Policy_languageContext):
        pass

    # Exit a parse tree produced by OPOLParser#policy_language.
    def exitPolicy_language(self, ctx:OPOLParser.Policy_languageContext):
        pass


    # Enter a parse tree produced by OPOLParser#policy_statement.
    def enterPolicy_statement(self, ctx:OPOLParser.Policy_statementContext):
        pass

    # Exit a parse tree produced by OPOLParser#policy_statement.
    def exitPolicy_statement(self, ctx:OPOLParser.Policy_statementContext):
        pass


    # Enter a parse tree produced by OPOLParser#invariant.
    def enterInvariant(self, ctx:OPOLParser.InvariantContext):
        pass

    # Exit a parse tree produced by OPOLParser#invariant.
    def exitInvariant(self, ctx:OPOLParser.InvariantContext):
        pass


    # Enter a parse tree produced by OPOLParser#invariant_body.
    def enterInvariant_body(self, ctx:OPOLParser.Invariant_bodyContext):
        pass

    # Exit a parse tree produced by OPOLParser#invariant_body.
    def exitInvariant_body(self, ctx:OPOLParser.Invariant_bodyContext):
        pass


    # Enter a parse tree produced by OPOLParser#situation_block.
    def enterSituation_block(self, ctx:OPOLParser.Situation_blockContext):
        pass

    # Exit a parse tree produced by OPOLParser#situation_block.
    def exitSituation_block(self, ctx:OPOLParser.Situation_blockContext):
        pass


    # Enter a parse tree produced by OPOLParser#situation_condition.
    def enterSituation_condition(self, ctx:OPOLParser.Situation_conditionContext):
        pass

    # Exit a parse tree produced by OPOLParser#situation_condition.
    def exitSituation_condition(self, ctx:OPOLParser.Situation_conditionContext):
        pass


    # Enter a parse tree produced by OPOLParser#desire_block.
    def enterDesire_block(self, ctx:OPOLParser.Desire_blockContext):
        pass

    # Exit a parse tree produced by OPOLParser#desire_block.
    def exitDesire_block(self, ctx:OPOLParser.Desire_blockContext):
        pass


    # Enter a parse tree produced by OPOLParser#desire_value.
    def enterDesire_value(self, ctx:OPOLParser.Desire_valueContext):
        pass

    # Exit a parse tree produced by OPOLParser#desire_value.
    def exitDesire_value(self, ctx:OPOLParser.Desire_valueContext):
        pass


    # Enter a parse tree produced by OPOLParser#expectation_block.
    def enterExpectation_block(self, ctx:OPOLParser.Expectation_blockContext):
        pass

    # Exit a parse tree produced by OPOLParser#expectation_block.
    def exitExpectation_block(self, ctx:OPOLParser.Expectation_blockContext):
        pass


    # Enter a parse tree produced by OPOLParser#condition.
    def enterCondition(self, ctx:OPOLParser.ConditionContext):
        pass

    # Exit a parse tree produced by OPOLParser#condition.
    def exitCondition(self, ctx:OPOLParser.ConditionContext):
        pass


    # Enter a parse tree produced by OPOLParser#boolean_expression.
    def enterBoolean_expression(self, ctx:OPOLParser.Boolean_expressionContext):
        pass

    # Exit a parse tree produced by OPOLParser#boolean_expression.
    def exitBoolean_expression(self, ctx:OPOLParser.Boolean_expressionContext):
        pass


    # Enter a parse tree produced by OPOLParser#boolean_operator.
    def enterBoolean_operator(self, ctx:OPOLParser.Boolean_operatorContext):
        pass

    # Exit a parse tree produced by OPOLParser#boolean_operator.
    def exitBoolean_operator(self, ctx:OPOLParser.Boolean_operatorContext):
        pass


    # Enter a parse tree produced by OPOLParser#key_name.
    def enterKey_name(self, ctx:OPOLParser.Key_nameContext):
        pass

    # Exit a parse tree produced by OPOLParser#key_name.
    def exitKey_name(self, ctx:OPOLParser.Key_nameContext):
        pass


    # Enter a parse tree produced by OPOLParser#triggered_source_key.
    def enterTriggered_source_key(self, ctx:OPOLParser.Triggered_source_keyContext):
        pass

    # Exit a parse tree produced by OPOLParser#triggered_source_key.
    def exitTriggered_source_key(self, ctx:OPOLParser.Triggered_source_keyContext):
        pass


    # Enter a parse tree produced by OPOLParser#triggered_event_key.
    def enterTriggered_event_key(self, ctx:OPOLParser.Triggered_event_keyContext):
        pass

    # Exit a parse tree produced by OPOLParser#triggered_event_key.
    def exitTriggered_event_key(self, ctx:OPOLParser.Triggered_event_keyContext):
        pass


    # Enter a parse tree produced by OPOLParser#device_related_key.
    def enterDevice_related_key(self, ctx:OPOLParser.Device_related_keyContext):
        pass

    # Exit a parse tree produced by OPOLParser#device_related_key.
    def exitDevice_related_key(self, ctx:OPOLParser.Device_related_keyContext):
        pass


    # Enter a parse tree produced by OPOLParser#action_related_key.
    def enterAction_related_key(self, ctx:OPOLParser.Action_related_keyContext):
        pass

    # Exit a parse tree produced by OPOLParser#action_related_key.
    def exitAction_related_key(self, ctx:OPOLParser.Action_related_keyContext):
        pass


    # Enter a parse tree produced by OPOLParser#system_related_key.
    def enterSystem_related_key(self, ctx:OPOLParser.System_related_keyContext):
        pass

    # Exit a parse tree produced by OPOLParser#system_related_key.
    def exitSystem_related_key(self, ctx:OPOLParser.System_related_keyContext):
        pass


    # Enter a parse tree produced by OPOLParser#date_time_related_key.
    def enterDate_time_related_key(self, ctx:OPOLParser.Date_time_related_keyContext):
        pass

    # Exit a parse tree produced by OPOLParser#date_time_related_key.
    def exitDate_time_related_key(self, ctx:OPOLParser.Date_time_related_keyContext):
        pass


    # Enter a parse tree produced by OPOLParser#operator.
    def enterOperator(self, ctx:OPOLParser.OperatorContext):
        pass

    # Exit a parse tree produced by OPOLParser#operator.
    def exitOperator(self, ctx:OPOLParser.OperatorContext):
        pass


    # Enter a parse tree produced by OPOLParser#value.
    def enterValue(self, ctx:OPOLParser.ValueContext):
        pass

    # Exit a parse tree produced by OPOLParser#value.
    def exitValue(self, ctx:OPOLParser.ValueContext):
        pass


    # Enter a parse tree produced by OPOLParser#policy_analysis.
    def enterPolicy_analysis(self, ctx:OPOLParser.Policy_analysisContext):
        pass

    # Exit a parse tree produced by OPOLParser#policy_analysis.
    def exitPolicy_analysis(self, ctx:OPOLParser.Policy_analysisContext):
        pass


    # Enter a parse tree produced by OPOLParser#analysis_command.
    def enterAnalysis_command(self, ctx:OPOLParser.Analysis_commandContext):
        pass

    # Exit a parse tree produced by OPOLParser#analysis_command.
    def exitAnalysis_command(self, ctx:OPOLParser.Analysis_commandContext):
        pass


    # Enter a parse tree produced by OPOLParser#analysis_expression.
    def enterAnalysis_expression(self, ctx:OPOLParser.Analysis_expressionContext):
        pass

    # Exit a parse tree produced by OPOLParser#analysis_expression.
    def exitAnalysis_expression(self, ctx:OPOLParser.Analysis_expressionContext):
        pass


    # Enter a parse tree produced by OPOLParser#analysis_operator.
    def enterAnalysis_operator(self, ctx:OPOLParser.Analysis_operatorContext):
        pass

    # Exit a parse tree produced by OPOLParser#analysis_operator.
    def exitAnalysis_operator(self, ctx:OPOLParser.Analysis_operatorContext):
        pass


