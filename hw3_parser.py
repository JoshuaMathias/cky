import sys
import nltk

# USAGE: hw3_parser.sh <grammar_filename> <test_sentence_filename> <output_filename>
grammar_filename = ""
test_sentence_filename = ""
output_filename = ""
if len(sys.argv) > 1:
	grammar_filenamee = sys.argv[1]
	test_sentence_filename = sys.argv[2]
	output_filename = sys.argv[2]
else:
	print("USAGE: <grammar_filename> <test_sentence_filename> <output_filename>")
	exit()

inStr = open(input_grammar_file, 'r').read()
inputCFG = nltk.CFG.fromstring(inStr)