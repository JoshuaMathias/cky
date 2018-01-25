# HW 3: Cocke–Younger–Kasami algorithm.

Joshua Mathias & Kekoa Riggin - LING 571 - January 24, 2018

## Problems & Solutions
Problem: Checking whether a symbol is a terminal.
Solution: One option is checking for ' surrounding the symbol. We decided to use nltk's function is_terminal() to be sure to cover all cases (such as double quotes).

## Insights
Looping efficiently through cells: For simplicity, our implementation checks whether cells are empty instead of not looping through them in the first place. We could use a stack or queue to know where to start/end each inner loop, to speed up the algorithm.

## Special Features
We check at the beginning whether the input grammar is in Chomsky Normal Form and output a warning if it's not.

## Learned
We learned how an converting a CFG to a binary form allows efficient parsing using dynamic programming. Dealing with subtrees and grammars is a good way to conceptualize the main idea behind dynamic programming, which is to reuse previous results/paths and do as little checking as possible while progressively moving through the search space.

## Division of Labor

**Read Grammar** - Joshua

**CYK Algorithm** - Joshua & Kekoa

**Output** - Joshua & Kekoa

<!--END-->
