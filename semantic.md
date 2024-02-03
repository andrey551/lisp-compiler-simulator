<!-- <expression> ::= <*-expression> | <literal> | <identifier>
<expressions> ::= <expression> | <expression> <expressions>

<multi-expression> ::= "(" <expressions> ")"

<load-by-ptr-expression> ::= "(" "@" <identifier> ")"

<if-expression> ::= "(" "if" <expression> <if-body> ")"
<if-body> ::= <expression> | <expression> <expression>

<alloc-str-expression> ::= "(" "alloc_str" <identifier> <int-literal> ")"

<set-ptr-expression> ::= "(" "set_ptr" <identifier> <expression> ")"

<set-expression> ::= "(" "set" <identifier> <expression> ")"

<loop-while-expression> ::= "(" "loop" "while" <expression> "do" <expressions> ")"

<put-char-expression> ::= "(" "put_char" <expression> ")"
<get-char-expression> ::= "(" "get_char" ")"

<let-var> ::= "(" <identifier> <expression> ")"
<let-vars> ::= <let-var> | <let-var> <let-vars>
<let-expression> ::= "(" "let" "(" <let-vars> ")" <expressions> ")"

<math-expression> ::= "(" <math-op> <expression> <expression> ")"
<math-op> ::= ">" | ">=" | "<" | "<=" | "=" | "!=" | "+" | "-" | "<<" | ">>"

<defun-expression> ::= "(" "defun" <identifier> "(" <identifiers> ")" <expressions> ")"

<func-call-expression> ::= "(" <identifier> <expressions> ")"

<identifiers> ::= <identifier> | <identifier> <identifiers>
<identifier> ::= [a-zA-Z]+

<literal> ::= <string-literal> | <int-literal> | <bool-literal>
<string-literal> ::= "\"" [a-zA-Z]+ "\""
<int-literal> ::= [0-9]+
<bool-literal> ::= "true" | "false"

<macro> :: "#include " .+ <EOL> -->


<expression> ::= <literal> | <identifier> | <expression>
<expressions> ::= <expression> <expressions> | <None>
<integer-literal> ::= [0-9]+
<string-literal> ::= "\"" [a-zA-Z]+ "\""
<boolean-literal> ::= "true"|"false"
<literal> ::= <integer-literal> | <string-literal> | <boolean-literal>

<defun-expression> ::= "(" "defun" <identifier> "(" <identifiers> ")" <expressions> ")"
<func-call-expression> ::= "(" <identifier> <expressions> ")"

<loop-expression> ::= "(" "loop" ":" "for" <identifier> ":" "from" <identifier> ":" "to" <identifier> ":" "do" <expressions> ")" 
<set-expression> ::= "(" "setq" <identifier> <literal>|<expressions> ")"
<if-expression> ::= "(" "if" "(" <expression> ")" "(" <expressions> ")" ")"

<print-expression> ::= "(" "format" "t" <literal> ")"

<logical-operator> ::= "<" | "=" | ">" | "<=" | ">=" | "\=" | "|" | "&" | "~"
<logical-expression> ::= <logical-operator> <expresision> <expression>

<mathematic-operator> ::= "+" | "-" | "*" | "/"
<mathematic-expression> ::= <mathematic-operator> <expresision> <expression>
