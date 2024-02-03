<!-- only expression can hold undefined multi node, and they an be anything -->
<expression> ::= "(" <literal> | <identifier> | <expression>* ")" 
<integer-literal> ::= [0-9]+
<string-literal> ::= "\"" [a-zA-Z]+ "\""
<boolean-literal> ::= "true"|"false"
<literal> ::= <integer-literal> | <string-literal> | <boolean-literal> | <expression>

<defun-expression> ::= "(" "defun" <identifier> <expression> <expression> ")"

<func-call-expression> ::= "(" call <identifier> <expression> ")"

<from-expression> ::= from <literal>
<to-expression> ::= "to" <literal>
<for-expression> ::= "for" <identifier> <from-expression> <to-expression>
<loop-expression> ::= "(" "loop"  <for-expression> <expression> ")" 
<set-expression> ::= "(" "setq" <identifier> <literal>|<expressions> ")"
<if-expression> ::= "(" "if" <expression> <expression> ")"

<print-expression> ::= "(" "format" "t" <literal> ")"

<logical-operator> ::= "<" | "=" | ">" | "<=" | ">=" | "\=" | "|" | "&" | "~"
<logical-expression> ::= <logical-operator> <literal> <literal>

<mathematic-operator> ::= "+" | "-" | "*" | "/"
<mathematic-expression> ::= <mathematic-operator> <expresision>
