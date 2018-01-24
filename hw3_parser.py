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

term = {} # dictionary of termanal symbols
termInd = []
nonTerm = {} # dictionary of nonterminal symbols
nonTermInd = []

rulecount = 0
for inLine in inputCFG.productions(): # use grammar from nltk to auto handle  rules with '|'
	rule = str(inLine) # GET A STRING OF THE RULE
	# print(rule)
	pieces = rule.split()
	lhs = pieces[0] # lefthand side of rule
	rhs = "" # righthand side of rule
	if pieces[-1] == '':
		pieces = pieces[:-1]

	termCheck = False # check if rule is terminal
	if len(pieces) > 3: # check if rule is binary
		rhs = pieces[2] + " " + pieces[3]
	else:
		if pieces[2][0] == "\'" and pieces[2][-1] == "\'": # check for terminals
			termCheck = True
		rhs = pieces[2]

	if termCheck == True:
		if rhs in term:
			termInd[term[rhs]].append(lhs)
		else:
			term[rhs] = len(termInd)
			termInd.append([lhs])
	else:
		if rhs in nonTerm:
			nonTermInd[nonTerm[rhs]].append(lhs)

		else:
			nonTerm[rhs] = len(nonTermInd)
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
	neo = [ [ [None] for x in range(len(words)+1)] for y in range(len(words)+1)] # neo because the Matrix

	numParses = 0
	treeStr = ""
	c = 1
	while c < len(neo):
		r = c - 1
		addFirst = False # Check that diagonal cells replace Null and add all

		for symbol in termInd[term[words[r]]]:
			pathStr = "(" + symbol + " " + words[r] + ")"
			if addFirst == False:
				neo[r][c] = [[symbol, pathStr]]
				addFirst = True
			else:
				neo[r][c].append([symbol, pathStr])
		r-=1
		while r >= 0:
			move = 1 # number of spaces to backtrack left

			while move < c:

				current = "current[" + str(r) + "," + str(c) + "]"
				left_cell = "left[" + str(r) + "," + str(move) + "]"
				down_cell = "down[" + str(move) + "," + str(c) + "]"

				down_symbs = ""
				left_symbs = ""
				addNew = False
				if neo[r][move] != [None] and neo[move][c] != [None]:
					for left_sub in neo[r][move]:
						left_symbs += left_sub[0] + "|"

						for right_sub in neo[move][c]:
							down_symbs += right_sub[0] + "|"

							sub = left_sub[0] + " " + right_sub[0]
							if sub in nonTerm:
								symbols = nonTermInd[nonTerm[sub]]
								for symbol in symbols:
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
