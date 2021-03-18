grammar Grammar;

file: (variable_definition SEMICOLON | function_definition)*;

function_definition: type identifier parameters body;

parameters: '(' (type identifier ','?)* ')';

body: '{' statement* '}';

statement:
	if_statement
	| for_statement
	| expression SEMICOLON
	| variable_definition SEMICOLON
	| variable_assignment SEMICOLON
	| RETURN expression SEMICOLON;

if_statement:
	'if' expression body else_statement*
	| 'if' expression statement;

else_statement: 'else' body | 'else' if_statement;

for_statement:
	'for' '(' init_for_variable SEMICOLON conditional_for_variable SEMICOLON counter_for_variable
		')' body;

init_for_variable: variable_assignment | variable_definition;

conditional_for_variable: expression;

counter_for_variable: variable_assignment;

variable_definition:
	type (identifier '=' expression ','?)+
	| type (array '=' array_unit? ','?)+;

variable_assignment:
	identifier '=' expression
	| identifier ('+=' | '-=') expression
	| identifier ('/=' | '*=') expression
	| identifier ('++' | '--')
	| ('++' | '--') identifier;

expression:
	string
	| int_var
	| float_var
	| function
	| array
	| identifier
	| expression ('<' | '>' | '<=' | '>=') expression
	| expression ('!=' | '==') expression
	| expression ('/' | '*') expression
	| expression ('+' | '-') expression
	| ('-') expression
	| '(' expression ')';

array: identifier '[' expression ']';
array_unit: '{' (expression ','?)* '}';
function: identifier '(' (expression ','?)* ')';

type: TYPE;
identifier: IDENTIFIER;
string: STRING;
int_var: INT;
float_var: FLOAT;

WHITESPACE: [ \t]+ -> skip;
NEWLINE: ('\r' '\n'? | '\n') -> skip;
BLOCKCOMMENT: '/*' .*? '*/' -> skip;
LINECOMMENT: '//' ~[\r\n]* -> skip;
PRE_PROCESSING_DIRECTIVES: '#' ~[\r\n]* -> skip;
SEMICOLON: (';');
RETURN: ('return');
TYPE: ('int' | 'float');
STRING: '"' .*? '"';
INT: [0-9]+;
FLOAT: [0-9]+ '.'? [0-9]*;
IDENTIFIER: ([a-zA-Z_]+ [0-9]*);
