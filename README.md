# HW 3: Cocke–Younger–Kasami algorithm.

Joshua Mathias & Kekoa Riggin - LING 571 - January 24, 2018

## Problems & Solutions
Problem: Checking whether a symbol is a terminal.  
Solution: One option is checking for ' surrounding the symbol. We decided to use nltk's function is_terminal() to be sure to cover all cases (such as double quotes).
Problem: Passing multiple features up through the matrix as one tree.
Solution: Rather than making a class, we stored subtree instances as an array of length-2 with symbol and bracket structure at those indexes.
Problem: Handling multiple trees and multiple head nodes for subtrees at one location in the matrix.
Solution: By storing the grammar in a dictionary with a index value, we could store the real key value as an array for possible multiple head nodes for one sub tree. Although most cases only resulted in one head node and few cells had many trees, we account for all possible trees through this iteration (even if that iteration happens only once for most trees).

## Insights
Looping efficiently through cells: For simplicity, our implementation checks whether cells are empty instead of not looping through them in the first place. We could use a stack or queue to know where to start/end each inner loop, to speed up the algorithm.
For the inner loop when passing all subtrees to the current cell in the matrix, only one variable is needed to keep track of both the right-hand and left-hand child. Once we figured this out, that loop became much easier to implement and read.

## Special Features
We check at the beginning whether the input grammar is in Chomsky Normal Form and output a warning if it's not. By using nltk to import the grammar, our script can read any standard grammar format for a CNF grammar that nltk supports, including rules that have multiple right hand side rules on one line.

## Learned
We learned how an converting a CFG to a binary form allows efficient parsing using dynamic programming. Dealing with subtrees and grammars is a good way to conceptualize the main idea behind dynamic programming, which is to reuse previous results/paths and do as little checking as possible while progressively moving through the search space.

## Division of Labor

**Read Grammar** - Joshua

**Grammar Data Structure** - Kekoa

**CYK Algorithm** - Joshua & Kekoa

**Output** - Joshua & Kekoa

<!--END-->
