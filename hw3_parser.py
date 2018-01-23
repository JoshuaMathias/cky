import sys
import nltk

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

inStr = open(grammar_filename, 'r').read()
inputCFG = nltk.CFG.fromstring(inStr)

if not inputCFG.is_chomsky_normal_form():
	print("Input grammar is not in Chomsky normal form.")

sentences = open(test_sentence_filename,'r').readlines()

outStr = ""
# Test parsing with NLTK
parser = nltk.ChartParser(inputCFG)
for sentence in sentences:
	outStr+=sentence+"\n"
	parses = parser.parse(sentence)
	numParses = len(parses)
	for tree in parser.parse(sentence):
		outStr+=str(tree)+"\n"
	outStr+="Number of parses: "+str(numParses)+"\n\n"

outFile = open(output_filename,'w')
outFile.write(outStr)