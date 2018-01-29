import sys
import nltk
import re

# USAGE: hw4_topcfg.sh <treebank_filename> <output_PCFG_file>
# Example: export dataDir=~/dropbox/17-18/571/hw4/data
#	sh hw4_topcfg.sh $dataDir/parses.train hw4_trained.pcfg

# <treebank_filename> is the name of the file holding the parsed sentences, one parse per line, in Chomsky Normal Form.
# <output_PCFG_file> is the name of the file where the induced grammar should be written.
treebank_filename = ""
output_PCFG_filename = ""
if len(sys.argv) > 1:
	treebank_filename = sys.argv[1]
	output_PCFG_filename = sys.argv[2]
else:
	print("USAGE: <treebank_filename> <output_PCFG_filename>")
	exit()

# Read in a set of parsed sentences (a mini-treebank) from a file
# Identify productions and estimate their probabilities
# Print out the induced PCFG with production of the form above.
# # --------------------
# CREATE GRAMMAR
# --------------------
inStr = open(treebank_filename, 'r').read()

outStr = ""
outFile = open(output_PCFG_filename,'w')
outFile.write(outStr)
