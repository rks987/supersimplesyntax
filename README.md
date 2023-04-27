# Super Simple Syntax
The objective of SSS (super simple syntax) was to allow user defined operators, 
in a programming language, that were sufficiently powerful that the programming 
language would not need much builtin syntax at all. So this includes multi token 
operators such as if-then-else, and includes optional and repeating subgroups and 
subsub groups.

This library separates SSS out so that it can be used for other applications.

## Overview
Suppose we want a standard notation for lists: square brackets with
- either a comma separated sequence of values, or
- `[ hd | tl ]` to represent prepending `hd` to `tl` (commonly used to unpack a list).

In SSS we need to define 3 operators:
- `[ ]` for the empty list;
- `[ 1, 2, 3 ]` has a required operand, then a "`, x`" repeating group;
- `[ 1 | [2,3] ]` defines a different operator because the `|` is not `,` or `]`. 

In SSS terminology: `[`, `,`, `|` and `]` are called suboperators. Suboperators 
are one of: mandatory, optional, or repeating (0 or more times). If you want 
repeating one or more times then just have the first occurrence as mandatory 
then a repeating group. The first suboperator is, of course, mandatory. 

Before the first suboperator, and then after each suboperator, there is a 
slot for an operand. Before the first suboperator and after each mandatory 
suboperator we can specify that an operand is required or not permitted, 
and we can distinguish operators based on this. In the simplest case, the 
minus in `( - 3 )` is a different operator from the minus is `( 7 - 3 )`. We 
saw above that `[ ]` is a different operator from `[ 1 ]`.

So our operator is defined by the sequence of `n` mandatory suboperators, 
plus the boolean for each of the `n+1` operand positions saying whether an 
operand is required or forbidden in that position for that operator.
### Precedence
A left operand and any operand which might be rightmost (since there is 
no following mandatory suboperator) will have a precedence. A precedence 
is just a decimal number that is only used for its ordering, as with the 
Dewey decimal library system. In the expression `1 + 2 * 3` the right 
precedence of `+` and the left precedence of `*` will determine which 
gets the `2` and which has to wait. But this also applies with just one 
operator: `1 * 2 * 3` will associate to left or right depending on whether 
the left precedence of `*` is higher or lower than the right.
### Subsubs
A common convention in programming languages is to write `i,j,k:Int`. 
This is something you can't do with SSS because you don't know what 
comma means till you get to the `:`. Backtracking is not allowed. So, 
in my language, I have to write `i:,j:,k:Int`. What's happening here is 
that the `:` operator has a (0 or more) repeating group: `, operand :`. 
This is called a subsub, and the 2 suboperators are mandatory in the 
subsub, even though they are part of an optional group at the top level 
(so the operand does have a following mandatory, and hence doesn't have 
a precedence).

The main use of subsubs is when you have an optional (or repeated) 
suboperator, and there are other things that must or might go along 
with it when it is present. In the case above the subsub only adds 
the `:`s that are there for syntactic reasons.

Of course subsubs can have subsubsubs ...
### Identifiers and constants
As we saw with brackets, `[ ]`, an operator might have no left or 
right operand. Identifiers and constants fit into this operator 
scheme as just operators with no left or right. They don't need special 
handling.
### Special suboperators
When an operator with no right is followed by one with no left then a 
special suboperator is created. It will be "juxtaposition" is there is 
no whitespace, as in `f(x)`, or "space" is there is an actual gap. 
Juxtaposition is not allowed to be a secondary suboperator to some other 
operator, but space is. In my language procedure calls use either of 
these as infix operators: `f(x)` or `f x`.

SSS can also keep track of indentation so that changes in indentation 
can act as suboperators.
### Default operand
When an operand is required but not found then a default operand can 
be inserted. Typically this will be `unit`, which is a 0-tuple, which 
can thus be written `()`.
## The Gory Details
Operator declarations occur, hopefully before they are needed, then 
a stream of tokens is processed according to the operator specifications, 
building an AST, Abstract Syntax Tree. Your program will then do something 
useful with that.

The tokens are just text in SSS. If you want tokens with more complex 
structure then you can modify the code, but the easy answer is to just 
encode the structure in text, as I do. I prefix the text with a single 
character saying what sort of token it is, which is good enough for my 
application. However, for clarity, in the examples here I will just 
show incoming text. Also, any token that is not on the current list of 
possible suboperators will be treated as an indentifier or constant, 
which is an operator with no left or right for syntactic purposes.
### Specifying operators
In all the following, when I say "quoted text" I mean: in double 
quotes and, if `"` or backslash is required in the text then precede 
it with a backslash.

An operator specification consists of:
1. A value to tell the AST building code what to do with the operands. 
For example it might say what function to apply to them.
2. A text specification of the sequence of suboperators and operands.

The latter specification consists of suboperator and operand information, 
with no consecutive operand specifications:
1. An operand spec is in parentheses (`()`) and has the following:
- Optional precedence decimal number. Required for a left operand or 
an operand with no following mandatory suboperator.
- Optional subsub, which is just the same as our operator spec, except 
that it has to start with a suboperator spec (in `[]`s). This can only 
occur if the prior (controlling) suboperator is optional or repeating, 
in which case that suboperator token also starts the subsub but mandatory 
this time.
2. A suboperator spec is in square brackets (`[]`) and has the following:
- The quoted text of the suboperator. This can be ommitted, leaving a 
bare `[]`, in the unusual case that it follows an operand with a subsub 
that ends in a suboperator.
- Optional occurence specification: mandatory|optional|repeating. Default 
is mandatory.

There are compatibility constraints. 
- If multiple operators start with the same suboperator, and they have a 
left, then those lefts have to have the same precedence.
- More generally operators are determined by their mandatory suboperators 
and associated operands, and until those diverge they have to agree.
- ...

### API
`sssInit(tokenStream,astCallback,errorCallback)` to start:
- `tokenStream` is a generator of tuples consisting of a token (just text) 
and an opaque value that will be passed to the errorCallback, and might 
contain information like the filename, linenumber and character position.
- `astCallback(operator,operands)` is a routine that will be called whenever
an operator instance is complete. It will return an opaque value (presumably 
an ast tree) that will be
the data when that bit of ast is included in an outer operator instance. The 
operands come in a list as described later.
- `errorCallback(msg,partAst,token)` will be called when an error 
occurs, providing an error
message, the partial ast that can't be finished, the current token. If the
error callback returns then an exception will be thrown. It would be nice
if there was some way to cooperatively fix the error to allow more errors
to be found.

`doOperatorCmd(operator,specification)` is called to define operators. The 
`operator` parameter is an opaque value that is passed to `astCallback`. The
`specification` is text defining the operator syntax, as described previously.

The `doOperatorCmd` can be called before ever calling `sssInit`. However
if you want to have user defined operators then you can call `doOperatorCmd`
at any time. It will, of course, only apply to following tokens. Behaviour
is undefined if the operator being defined partially overlaps with an
existing operator whose operand is being processed. This is avoided by
only allowing operator definitions at "statement level" in some sense, e.g.
after a semicolon (`;`) operator in traditional style programming languages.
### Operands
The `operands` parameter to `astCallback`