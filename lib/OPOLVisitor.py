# Generated from OPOL.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .OPOLParser import OPOLParser
else:
    from OPOLParser import OPOLParser

# This class defines a complete generic visitor for a parse tree produced by OPOLParser.

class OPOLVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by OPOLParser#policy_language.
    def visitPolicy_language(self, ctx:OPOLParser.Policy_languageContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPOLParser#policy_statement.
    def visitPolicy_statement(self, ctx:OPOLParser.Policy_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPOLParser#invariant.
    def visitInvariant(self, ctx:OPOLParser.InvariantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPOLParser#invariant_body.
    def visitInvariant_body(self, ctx:OPOLParser.Invariant_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPOLParser#situation_block.
    def visitSituation_block(self, ctx:OPOLParser.Situation_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPOLParser#situation_condition.
    def visitSituation_condition(self, ctx:OPOLParser.Situation_conditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPOLParser#desire_block.
    def visitDesire_block(self, ctx:OPOLParser.Desire_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPOLParser#desire_value.
    def visitDesire_value(self, ctx:OPOLParser.Desire_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPOLParser#expectation_block.
    def visitExpectation_block(self, ctx:OPOLParser.Expectation_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPOLParser#condition.
    def visitCondition(self, ctx:OPOLParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPOLParser#boolean_expression.
    def visitBoolean_expression(self, ctx:OPOLParser.Boolean_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPOLParser#boolean_operator.
    def visitBoolean_operator(self, ctx:OPOLParser.Boolean_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPOLParser#key_name.
    def visitKey_name(self, ctx:OPOLParser.Key_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPOLParser#triggered_source_key.
    def visitTriggered_source_key(self, ctx:OPOLParser.Triggered_source_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPOLParser#triggered_event_key.
    def visitTriggered_event_key(self, ctx:OPOLParser.Triggered_event_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPOLParser#device_related_key.
    def visitDevice_related_key(self, ctx:OPOLParser.Device_related_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPOLParser#action_related_key.
    def visitAction_related_key(self, ctx:OPOLParser.Action_related_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPOLParser#system_related_key.
    def visitSystem_related_key(self, ctx:OPOLParser.System_related_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPOLParser#date_time_related_key.
    def visitDate_time_related_key(self, ctx:OPOLParser.Date_time_related_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPOLParser#operator.
    def visitOperator(self, ctx:OPOLParser.OperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPOLParser#value.
    def visitValue(self, ctx:OPOLParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPOLParser#policy_analysis.
    def visitPolicy_analysis(self, ctx:OPOLParser.Policy_analysisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPOLParser#analysis_command.
    def visitAnalysis_command(self, ctx:OPOLParser.Analysis_commandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPOLParser#analysis_expression.
    def visitAnalysis_expression(self, ctx:OPOLParser.Analysis_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPOLParser#analysis_operator.
    def visitAnalysis_operator(self, ctx:OPOLParser.Analysis_operatorContext):
        return self.visitChildren(ctx)



del OPOLParser