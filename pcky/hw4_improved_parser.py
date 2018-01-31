import sys
import nltk

# USAGE: hw4_parser.sh <input_PCFG_file> <test_sentence_filename> <output_parse_filename>
# Example: export dataDir=~/dropbox/17-18/571/hw4/data
# 	sh hw4_parser.sh hw4_trained.pcfg $dataDir/sentences.txt parses_base.out
# 	sh hw4_parser.sh $dataDir/toy.pcfg $dataDir/toy_sentences.txt toy_output.txt

# <input_PCFG_file> is the name of the file holding the induced PCFG grammar to be read.
# <test_sentence_filename> is the name of the file holding the test sentences to be parsed.
# <output_parse_filename> is the name of the file to which the best parse for each sentence will be written.
# 	Each parse should appear on only one line, and there should be one line per sentence in the output file.
# 	In other words, output a blank line if the sentence does not parse.
input_PCFG_filename = ""
test_sentence_filename = ""
output_parse_filename = ""

if len(sys.argv) > 1:
	input_PCFG_filename = sys.argv[1]
	test_sentence_filename = sys.argv[2]
	output_parse_filename = sys.argv[3]
else:
	print("USAGE: <input_PCFG_filename> <test_sentence_filename> <output_parse_filename>")
	exit()

# Read in a PCFG in NLTK format as generated above
# Read in a set of sentences to parse
# For each sentence:
# Parse the sentences using a PCKY algorithm that you implement
# Print the highest scoring parse to a file, on a single line
# Note: The test sentences may include words not seen in training; this happens in real life. In a baseline system, these may fail to parse.


inStr = open(input_PCFG_filename, 'r').read()
inputPCFG = nltk.PCFG.fromstring(inStr)

if not inputPCFG.is_chomsky_normal_form():
	print("Input grammar is not in Chomsky normal form.")

start = str(inputPCFG.start())

term = {} # dictionary of terminal symbols
termInd = []
termIndToWord = [] # Map term indices to words
nonTerm = {} # dictionary of nonterminal symbols
nonTermInd = []

probability_d = {} # dictionary of rule probs K=rule V=probability

rulecount = 0
for inLine in inputPCFG.productions(): # use grammar from nltk to auto handle rules with '|'

############################################
# ADAPTATION FROM CKY
# SPLIT THE PROBABILITY FROM THE RULE AND ADD TO PROBABILITY DICTIONARY
############################################
	full_line = str(inLine) # GET A STRING OF THE RULE

	prob_parts = full_line.split(" [")
	rule = prob_parts[0] # String with the whole rule - used for cky algorithm
	prob = float(prob_parts[1][:-1]) # float with probability - sent to dictionary. Assumes that the last character of the line is the "]" and adjacent to the last digit.
	probability_d[rule] = prob

############################################
# BACK TO CKY ORIGINAL
############################################
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
		# if "\'d" in pieces[2]:
		# 	print(pieces[2])

	# Populate lists of terminals and nonterminals with all left hand sides from the rules for each terminal or nonterminal.
	if termCheck:
		if rhs in term:
			termInd[term[rhs]].append(lhs)
		else:
			term[rhs] = len(termInd) # Assign terminal the next index.
			termIndToWord.append(rhs)
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
# Make dictionary of lowercase terminals to default to.
lowerTerm = {}
for termName in term:
	lowerTerm[termName.lower()] = term[termName]


# Find the terminal that most closely matches the end of the given word/term.
def matchWordBySuffix(wordsDict, term):
	bestWord = None
	bestLen = -1
	for word in wordsDict:
		smallestLen = len(word)
		if smallestLen > len(term):
			smallestLen = len(term)
		for i in range(smallestLen,2,-1): # Could end at 1 to not include quotation marks
			# print("substrings: "+word[len(word)-i:]+" == "+term[len(term)-i:])
			if word[len(word)-i:] == term[len(term)-i:]:
				if i > bestLen: # Use the word with the greatest length of equal final characters.
					# print("Use similar word: "+str(word)+" of suffix length "+str(i)+" for "+str(term))
					bestWord = wordsDict[word]
					bestLen = i
	return bestWord


outStr = ""
sentenceI = 0
for sentence in sentences:
	sentenceI += 1
	changedWords = {}
	words = nltk.word_tokenize(sentence) # tokenize input sentence
	# print(sentence, words)
	if words[-1] == '':
		words = words[:-1]
	m = 0
	for word in words:
		if word[0] == "\'" and word[-1] != "\'":
			words[m] = "\"" + word + "\""
		else:
			words[m] = "\'" + word + "\'"
		m+=1
	for wordI in range(len(words)):
		if words[wordI] not in term: # If there is no terminal for this input word, try lowercasing it.
			lowerWord = words[wordI].lower()
			# print("sentenceI: "+str(sentenceI))
			if lowerWord in lowerTerm:
				chosenI = lowerTerm[lowerWord]
				changedWords[wordI] = chosenI # Save the index of the chosen alternative terminal
				# print("use lowercase: "+str(lowerWord))
			else:
				bestWord = matchWordBySuffix(lowerTerm, lowerWord)
				if bestWord:
					# print("Use similar word: "+str(bestWord)+" for "+str(words[wordI]))
					changedWords[wordI] = bestWord  # Save the index of the chosen alternative terminal
				else:
					# print("No alternative terminal found for "+str(words[wordI]))
					changedWords[wordI] = 0 # Choose the first word, since nothing else was found.
	# Embedded array for Row, Column, Tree, [symbol, tree text]
	# (n+1) x (n+1) matrix
	neo = [[[None] for x in range(len(words)+1)] for y in range(len(words)+1)] # neo because the Matrix

	numParses = 0
	c = 1 # column
	while c < len(neo):
		r = c - 1
		addFirst = False # Check that diagonal cells replace Null and add all
		# First row
		# For each terminal, populate triangular matrix with its path, represented by the nonterminal pointing to it and the terminal symbol.
		# r represents index of words in sentence (as well as the row)
		# if words[r] in term: # No longer need to check, since we've already handled OOV words.
		currWordI = -1
		currWord = ""
		if r in changedWords:
			currWordI = changedWords[r]
			# print("Use alternative "+str(termIndToWord[currWordI])+" for "+words[r])
		else:
			# print("Could not find "+str(r)+" in changedWords")
			currWordI = term[words[r]]
		currWord = termIndToWord[currWordI]
		for symbol in termInd[currWordI]:
			currWord = words[r] # For everything other than getting the symbols (for appending) use the input word instead of the alternative.
			new_word = currWord[1:-1]
			pathStr = "(" + symbol + " " + new_word + ")" # Since these are terminals, we know that these are the innermost parentheses/path.
			if not addFirst: # The first time, initialize with a list.
				neo[r][c] = [[symbol, pathStr, [symbol + " -> " + currWord]]]
				addFirst = True
			else:
				neo[r][c].append([symbol, pathStr, [symbol + " -> " + currWord]])
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

############################################
# ADAPTATION (NOT PCKY SPECIFIC)
# IF TEST WORD NOT IN GRAMMAR, DO NOT PROCESS
############################################
				if neo[r][move] != [None] and neo[move][c] != [None]: # Don't use the unfilled parts of the matrix (outside of the triangle).
############################################
# BACK TO CKY ORIGINAL
############################################
					for left_sub in neo[r][move]: # Each possible subtree for this cell.
						# left_symbs += left_sub[0] + "|"

						for right_sub in neo[move][c]: # Each possible subtree for this cell.
							# down_symbs += right_sub[0] + "|"

							sub = left_sub[0] + " " + right_sub[0] # Represent the combination of both subtrees/nonterminals (possible expansion)

							if sub in nonTerm: # Is there a rule for this expansion?
								symbols = nonTermInd[nonTerm[sub]]
								for symbol in symbols: # What are all the possible left hand sides of the right hand side found for the expansion?
									pathStr = "(" + symbol + " " + left_sub[1] + " " + right_sub[1] + ")"

############################################
# ADAPTATION FOR PCKY
# ADD THE ELEMENTS FROM THIRD ELEMENT (INDEX 2) IN BOTH SUBTREES TO NEW NODE
############################################
									current_list = []

									for l in left_sub[2]:
										current_list.append(l)
									for l in right_sub[2]:
										current_list.append(l)
									rule_name = symbol + " -> " + sub
									current_list.append(rule_name)
############################################
# BACK TO CKY ORIGINAL
############################################

									if neo[r][c] == [None]:
############################################
# ADAPTATION FOR PCKY
# ADD THIRD ELEMENT FOR ARRAY OF RULES FOR QUICK DICTIONARY LOOKUP
############################################
										neo[r][c] = [[symbol, pathStr, current_list]]
										addNew = True
									else:
										neo[r][c].append([symbol, pathStr, current_list])
							# else:
							# 	print("No rule found for : "+str(sub))

############################################
# BACK TO CKY ORIGINAL
############################################
				move += 1
			r-=1
		c+=1
# outStr = ""

# Test with NLTK
# from nltk.parse import viterbi
# nltkParser = viterbi.ViterbiParser(inputPCFG)
# for sent in sentences:
# 	tokens = sent.split()
# 	parses = nltkParser.parse(tokens)
# 	for parse in parses:
# 		outStr +=str(parse).replace("\n","")
# 		break # Print only the best parse
	# outStr+="\n" # Print a new line even if there isn't a parse

############################################
# ADAPTATION FOR PCKY
# FIND TREE IN TOP NODE WITH BEST PROBABILITY AND ADD THAT TREE TO WOUT STRING
############################################

	best_prob = 0 # placehold for best probability
	best_tree = "\n" # placeholder for best string to write - writes \n if no parse
	if neo[0][len(words)] != [None]: # make sure top node not empty
		for tree in neo[0][len(words)]:
			if tree[0] == start: # check that tree in top node is start symbol - based on nltk start()
				# print(tree[1])
				probab = 1 # the pobability of the whole tree
				for x in tree[2]:
					if x not in probability_d:
						probab *= probab / len(tree[2])
					else:
						probab *= probability_d[x]
					# print("NODE IN TREE", x)
					# print(probability_d[x])
				# print("THIS PROB:", probab, "BEST PROB:", best_prob)

				if probab > best_prob: # update best tree
					best_tree = tree[1]+"\n"
					best_prob = probab

	outStr+=best_tree
	# print(best_tree, best_prob)

############################################
# BACK TO CKY ORIGINAL
############################################

outFile = open(output_parse_filename,'w')
outFile.write(outStr)
