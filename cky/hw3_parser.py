import sys
import nltk
import re

# USAGE: hw3_parser.sh <grammar_filename> <test_sentence_filename> <output_filename>
grammar_filename = ""
test_sentence_filename = ""
output_filename = ""
if len(sys.argv) > 1:
	grammar_filename = sys.argv[1]
	test_sentence_filename = sys.argv[2]
	output_filename = sys.argv[3]
else:
	print("USAGE: <grammar_filename> <test_sentence_filename> <output_filename>")
	exit()

# --------------------
# CREATE GRAMMAR
# --------------------
inStr = open(grammar_filename, 'r').read()
inputCFG = nltk.CFG.fromstring(inStr)

if not inputCFG.is_chomsky_normal_form():
	print("Input grammar is not in Chomsky normal form.")

start = str(inputCFG.start())

term = {} # dictionary of terminal symbols
termInd = []
nonTerm = {} # dictionary of nonterminal symbols
nonTermInd = []

rulecount = 0
for inLine in inputCFG.productions(): # use grammar from nltk to auto handle rules with '|'
	rule = str(inLine) # GET A STRING OF THE RULE
	# print(rule)
	pieces = rule.split()
	if pieces[-1] == '': # In case the input has an extra space at the end.
		pieces = pieces[:-1]
	lhs = pieces[0] # lefthand side of rule
	rhs = "" # righthand side of rule

	termCheck = False # check if rule is terminal
	if len(pieces) > 3: # is rule binary?
		rhs = pieces[2] + " " + pieces[3]
	else:
		if nltk.grammar.is_terminal(inLine.rhs()): # check for terminals
			termCheck = True
		rhs = pieces[2]

	# Populate lists of terminals and nonterminals with all left hand sides from the rules for each terminal or nonterminal.
	if termCheck == True:
		if rhs in term:
			termInd[term[rhs]].append(lhs)
		else:
			term[rhs] = len(termInd) # Assign terminal the next index.
			termInd.append([lhs])
	else:
		if rhs in nonTerm:
			nonTermInd[nonTerm[rhs]].append(lhs)

		else:
			nonTerm[rhs] = len(nonTermInd)  # Assign nonterminal the next index.
			nonTermInd.append([lhs])

# --------------------
# READ INPUT
# --------------------
sentences = open(test_sentence_filename,'r').readlines()

# --------------------
# PARSER
# --------------------
outStr = ""
for sentence in sentences:
	words = nltk.word_tokenize(sentence) # tokenize input sentence
	if words[-1] == '':
		words = words[:-1]
	m = 0
	for word in words:
		words[m] = "\'" + word + "\'"
		m+=1
	# Embedded array for Row, Column, Tree, [symbol, tree text]
	# (n+1) x (n+1) matrix
	neo = [ [ [None] for x in range(len(words)+1)] for y in range(len(words)+1)] # neo because the Matrix

	numParses = 0
	treeStr = ""
	c = 1 # column
	while c < len(neo):
		r = c - 1
		addFirst = False # Check that diagonal cells replace Null and add all

		# First row
		# For each terminal, populate triangular matrix with its path, represented by the nonterminal pointing to it and the terminal symbol.
		# r represents index of words in sentence (as well as the row)
		for symbol in termInd[term[words[r]]]:
			pathStr = "(" + symbol + " " + words[r] + ")" # Since these are terminals, we know that these are the innermost parentheses/path.
			if addFirst == False: # The first time, initialize with a list.
				neo[r][c] = [[symbol, pathStr]]
				addFirst = True
			else:
				neo[r][c].append([symbol, pathStr])
		r-=1
		# Now start at second row (this time check for subtrees)
		while r >= 0:
			move = 1 # number of spaces to backtrack left

			while move < c:

				# current = "current[" + str(r) + "," + str(c) + "]"
				# left_cell = "left[" + str(r) + "," + str(move) + "]"
				# down_cell = "down[" + str(move) + "," + str(c) + "]"
				down_symbs = ""
				left_symbs = ""
				addNew = False
				if neo[r][move] != [None] and neo[move][c] != [None]: # Don't use the unfilled parts of the matrix (outside of the triangle).
					for left_sub in neo[r][move]: # Each possible subtree for this cell.
						# left_symbs += left_sub[0] + "|"

						for right_sub in neo[move][c]: # Each possible subtree for this cell.
							# down_symbs += right_sub[0] + "|"

							sub = left_sub[0] + " " + right_sub[0] # Represent the combination of both subtrees/nonterminals (possible expansion)
							if sub in nonTerm: # Is there a rule for this expansion?
								symbols = nonTermInd[nonTerm[sub]]
								for symbol in symbols: # What are all the possible left hand sides of the right hand side found for the expansion?
									pathStr = "(" + symbol + " " + left_sub[1] + " " + right_sub[1] + ")"
									if neo[r][c] == [None]:
										neo[r][c] = [[symbol, pathStr]]
										addNew = True
									else:
										neo[r][c].append([symbol, pathStr])
				move += 1
			r-=1
		c+=1


# APPEND OUT TO STRING
	outStr+=sentence
	if neo[0][len(words)] != [None]:
		for tree in neo[0][len(words)]:
			if tree[0] == start:
				outStr+= tree[1]+"\n"
				numParses += 1
	outStr+=treeStr
	outStr+="Number of parses: "+str(numParses)+"\n\n"

outFile = open(output_filename,'w')
outFile.write(outStr)
