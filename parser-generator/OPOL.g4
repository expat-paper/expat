grammar OPOL;

policy_language: (policy_statement)+ (policy_analysis)* EOF;

policy_statement: POLICY STRING COLON (invariant)*;

invariant: INVARIANT STRING COLON  invariant_body;

invariant_body: situation_block desire_block expectation_block;

situation_block: SITUATION COLON situation_condition;

situation_condition: ANY 
				   | condition;

desire_block: DESIRE COLON desire_value;

desire_value: EXPECT 
			| NOT EXPECT;

expectation_block: EXPECTATION COLON condition;

condition: boolean_expression;

boolean_expression: key_name operator value																	
				  | NOT boolean_expression 									
				  | boolean_expression boolean_operator boolean_expression;

boolean_operator: AND 
				| OR;


key_name: triggered_source_key 
		| triggered_event_key 
		| device_related_key 
		| action_related_key 
		| system_related_key
		| date_time_related_key;

triggered_source_key: RULE_NAME;

triggered_event_key: TRIGGERED_EVENT_DEVICE 
				   | TRIGGERED_EVENT 
				   | TRIGGER_TYPE;

device_related_key: STATE LPARAN STRING RPARAN;

action_related_key: ACTION_DEVICE 
				  | ACTION_COMMAND;

system_related_key: SYSTEM;

date_time_related_key: CURRENT_TIME
					 | CURRENT_DATE; 

operator: EQ 
		| NEQ
		| GT
		| GTE
		| LT
		| LTE;

value: TIME
	 | DATE
	 | NUMBER
	 | BOOLEAN
	 | STRING;

policy_analysis: CHECK analysis_command analysis_expression;

analysis_command: CONSISTENCY 
				| ENTAILMENT
				| EQUIVALENCE;

analysis_expression: STRING analysis_operator STRING 
				   | ;

analysis_operator: EQUIV_SIGN 
				 | ENTAIL_SIGN;


fragment A:('a'|'A');
fragment B:('b'|'B');
fragment C:('c'|'C');
fragment D:('d'|'D');
fragment E:('e'|'E');
fragment F:('f'|'F');
fragment G:('g'|'G');
fragment H:('h'|'H');
fragment I:('i'|'I');
fragment J:('j'|'J');
fragment K:('k'|'K');
fragment L:('l'|'L');
fragment M:('m'|'M');
fragment N:('n'|'N');
fragment O:('o'|'O');
fragment P:('p'|'P');
fragment Q:('q'|'Q');
fragment R:('r'|'R');
fragment S:('s'|'S');
fragment T:('t'|'T');
fragment U:('u'|'U');
fragment V:('v'|'V');
fragment W:('w'|'W');
fragment X:('x'|'X');
fragment Y:('y'|'Y');
fragment Z:('z'|'Z');

POLICY: P O L I C Y;
INVARIANT: I N V A R I A N T;
SITUATION: S I T U A T I O N;
EXPECTATION: E X P E C T A T I O N;
DESIRE: D E S I R E;
EXPECT: E X P E C T;
NOT: N O T;
ANY: A N Y;
AND: A N D;
OR: O R;
CHECK: C H E C K;
CONSISTENCY: C O N S I S T E N C Y;
ENTAILMENT: E N T A I L M E N T;
EQUIVALENCE: E Q U I V A L E N C E;
BOOLEAN: T R U E
	   | F A L S E;

RULE_NAME: 'rule_name';
TRIGGERED_EVENT_DEVICE: 'triggered_event_device';
TRIGGERED_EVENT: 'triggered_event';
TRIGGER_TYPE: 'trigger_type';
STATE: 'state';
COLON: ':';
LPARAN: '(';
RPARAN: ')';
TYPE: 'type';
ACTION_DEVICE: 'action_device';
ACTION_COMMAND: 'action_command';
SYSTEM: 'system';
CURRENT_TIME: 'current_time';
CURRENT_DATE: 'current_date';

EQUIV_SIGN: '==';
ENTAIL_SIGN: '=>';
EQ: '=';
NEQ: '!=';
GT: '>';
GTE: '>=';
LT: '<';
LTE: '<=';

TIME: DIGIT DIGIT COLON DIGIT DIGIT COLON DIGIT DIGIT;
DATE: DIGIT DIGIT DIGIT DIGIT UNDERSCORE DIGIT DIGIT UNDERSCORE DIGIT DIGIT;
UNDERSCORE: ('_' | '-');
fragment DIGIT: [0-9];
NUMBER: '-'? (DIGIT)+;
STRING: ([a-zA-Z]|UNDERSCORE)([a-zA-Z0-9]|UNDERSCORE)*;
WS: [ \r\n\t]+ -> skip;
ErrorChar : . ;