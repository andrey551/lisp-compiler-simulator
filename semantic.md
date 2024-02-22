<!-- only expression can hold undefined multi node, and they an be anything -->
<expression> ::= "(" <literal> | <identifier> | <expression>* ")" 
<integer-literal> ::= [0-9]+
<string-literal> ::= "\"" [a-zA-Z]+ "\""
<boolean-literal> ::= "true"|"false"
<EOL> ::= "/"
<identifier > ::= [a-zA-Z]+
<literal> ::= <integer-literal> | <string-literal> | <boolean-literal>
<data> ::= <literal> | <identifier > | <expression>
<defun-expression> ::= "(" "defun" <identifier> <expression> <expression> ")"
<func-call-expression> ::= "(" call <identifier> <expression> ")"
<return> ::= return <data>
<from-expression> ::= from <literal>
<to-expression> ::= "to" <literal>
<for-expression> ::= "for" <identifier> <from-expression> <to-expression>
<loop-expression> ::= "(" "loop"  <for-expression> <expression> ")" 
<while-expresison> ::= while <expression> <expression>
<set-expression> ::= "(" "set" <identifier> <literal>|<expressions> ")"
<if-expression> ::= "(" "if" <condition_expression> <true_expression> | <true_expression> <false_expression> ")"
<print-expression> ::= "(" "format"  <literal> | <identifier> | <expression> ")"
<logical-operator> ::= "<" | "=" | ">" | "<=" | ">=" | "\=" | "|" | "&" | "~"
<logical-expression> ::= <logical-operator> <data> <data>
<mathematic-operator> ::= "+" | "-" | "*" | "/"
<mathematic-expression> ::= <mathematic-operator> <expresision>
