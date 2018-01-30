import re
import sys
import operator

# USAGE: hw4_topcfg.sh <treebank_filename> <output_PCFG_file>
# Example: export dataDir=~/dropbox/17-18/571/hw4/data
#   sh hw4_topcfg.sh $dataDir/parses.train hw4_trained_improved.pcfg

# <treebank_filename> is the name of the file holding the parsed sentences, one parse per line, in Chomsky Normal Form.
# <output_PCFG_file> is the name of the file where the induced grammar should be written.
if len(sys.argv) > 1:
    in_file = sys.argv[1]
    out_file = sys.argv[2]
else:
    print("USAGE: <treebank_filename> <output_PCFG_filename>")
    exit()

# Read in a set of parsed sentences (a mini-treebank) from a file
# Identify productions and estimate their probabilities
# Print out the induced PCFG with production of the form above.

# ----------------
# IMPORT SOURCE FILE
fileopen = open(in_file)
text = fileopen.read()
fileopen.close()
text = re.sub("\n", "", text)
text = re.sub("\s+", " ", text)

# ----------------
# EXTRACT RULES FROM SOURCE FILE

symbols = []      # List of dictionaries index=lhs K=rhs V=count
names = [] # List of symbols because I get confused in the calculation
symbols_d = {} # dictionary of all constituents K=name V=index in symbols

rules = [] # List of all rules extracted from tree
sym_q = [["BLANK", []]] # Stack of rules to extract. initialize w/ "BLANK" head node. I accidentally labeled it 'q' for queue
count = 0
for ch in text:
    if ch == "(":

        # Count forward from '(' from ' ' to get Symbol
        name = ""
        fc = count + 1
        forward = text[fc]
        while forward != " ":
            name += forward
            fc += 1
            forward = text[fc]
        sym_q.append([name, []])

        # Add symbol to dictionary of symbols
        if name not in symbols_d:
            symbols_d[name] = len(symbols)
            symbols.append({})
            names.append(name)

    elif ch == ")":

        # If current rule is terminal, add word to RHS
        if text[count-1] != ")":

            # Count backward from ')' until ' ' to get word
            name = ""
            bc = count - 1
            backward = text[bc]
            while backward != " ":
                name = backward + name
                bc -= 1
                backward = text[bc]
            sym_q[len(sym_q)-1][1].append(name)

        # Add current symbol to previous symbol RHS and pop current from queue
        sym_q[len(sym_q)-2][1].append(sym_q[len(sym_q)-1][0])
        rules.append(sym_q.pop())
    count += 1

# ----------------
# CALCULATE RULE PROBABILITIES

# Add all rules to dictionaries
for rule in sorted(rules): # Sorting for testing convenience (can be removed)

    name = rule[0]
    rhs = ""
    if len(rule[1]) == 1: # Terminal rule (only one on right hand side)
        rhs = "\"" + rule[1][0] + "\"" # Surround terminals with quotation marks (double quotations to avoid problems with terminals that contain apostrophes)
            # All terminals are lowercased.
    elif len(rule[1])== 2:
        rhs = rule[1][0] + " " + rule[1][1] # Binary expansion rule (two on RHS)

    index = symbols_d[rule[0]]

    # Count how many times each symbol (LHS) expands to the RHS of the current rule.
    if rhs not in symbols[index]:
        symbols[index][rhs] = 1
    else:
        symbols[index][rhs] += 1


grammar = "" # String to be written out
c = 0
for name in names:
	set_rules = sorted(symbols[c].items(), key=operator.itemgetter(0), reverse=False) # Sorting for testing convenience (can be removed)
	total = 0 # Total counts for RHS

    # Add counts for each RHS to a total for denominator
	for rule in set_rules:
		total += rule[1]

    # Calculate probability for each unique rule
	line = "" # Added to string to print
	for rule in set_rules:
		probability = str(rule[1]/total)
		line += name + " -> " + rule[0] + " [" + probability + "]\n"
	grammar += line

	c += 1

# Write grammar to file
wout = open(out_file, "w+")
wout.write(grammar)

