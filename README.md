# Super Simple Syntax
The objective of SSS (super simple syntax) was to allow user defined operators, in a programming language, that were sufficiently powerful that the programming language would not need much builtin syntax at all. So this includes multi token operators such as if-then-else, and includes optional and repeating subgroups and subsub groups.

This library separates SSS out so that it can be used for other applications.

## Overview
Suppose we want a standard notation for lists: square brackets with
- either a comma separated sequence of values, or
- `[ hd | tl ]` to represent prepending `hd` to `tl` (commonly used to unpack a list).

In SSS we need to define 3 operators:
- `[ ]` for the empty list;
- `[ 1, 2, 3 ]` has a required operand, then a "`, x`" repeating group;
- `[ 1 | [2,3] ]` picks a different operator because the `|` is not `,` or `]`. 

In SSS terminology: `[`, `,`, `|` and `]` are called suboperators. Suboperators are one of: mandatory, optional, or repeating (0 or more times). If you want repeating one or more times then just have the first occurrence as mandatory then a repeating group. The first suboperator is, of course, mandatory. 

Before the first suboperator, then after each suboperator, there is a slot for an operand. Before the first suboperator and after each mandatory suboperator we can specify that an operand is required or not permitted, and we can distinguish operators based on this. In the simplest case, the minus in `( - 3 )` is a different operator from the minus is `( 7 - 3 )`. We saw above that `[ ]` is a different operator from `[ 1 ]`.

So our operator is defined by the sequence of `n` mandatory suboperators, plus the boolean for each of the `n+1` operand positions saying whether an operand is required or forbidden in that position for that operator.
### Precedence
A left operand and any operand which might be rightmost (since there is no following mandatory suboperator) will have a precedence. A precedence is just a decimal number that is only used for its ordering, as with the Dewey decimal library system. In the expression `1 + 2 * 3` the right precedence of `+` and the left precedence of `*` will determine which gets the `2` and which has to wait. But this applies with just one operator: `1 * 2 * 3` will associate to left or right depending on whether the left precedence of `*` is higher or lower than the right.
### Subsubs
A common convention in programming languages is to write `i,j,k:Int`. This is something you can't do with SSS because you don't know what comma means till you get to the `:`. Backtracking is not allowed. So, in my language, I have to write `i:,j:,k:Int`. What's happening here is that the `:` operator has a (0 or more) repeating group: `, operand :`. This is called a subsub, and the 2 suboperators are mandatory in the subsub, even though they are part of an optional group at the top level (so the operand does have a following mandatory, and hence doesn't have a precedence).
### Identifiers and constants
As we saw with brackets, `[ ]`, an operator might have no left or right operand. Identifiers and constants fit into this operator scheme as just operators with no left or right. They don't need special handling.
### Special suboperators
When an operator with no right is followed by one with no left then a special suboperator is created. It will be "juxtaposition" is there is no whitespace, as in `f(x)`, or "space" is there is an actual gap. Juxtaposition is not allowed to be a secondary suboperator to some other operator, but space is. In my language procedure calls use either of these as infix operators: `f(x)` or `f x`.

SSS can also keep track of indentation so that changes in indentation can act as suboperators.
### Default operand
When an operand is required but not found then a default operand can be inserted. Typically this will be `unit`, which is a 0-tuple, which can thus be written `()`.
## The Gory Details
Operator declarations occur, hopefully before they are needed, then a stream of tokens is processed according to the operator specifications, building an AST, Abstract Syntax Tree. You program will then do something useful with that.