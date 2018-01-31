import subprocess
import sys
import time

# Example command:
 # sh speed_test_parser.sh ../hw4_trained.pcfg $dataDir/sentences.txt ../parses_base.out
numRuns = 1

# Base parser
baseArguments = ["sh","hw4_parser.sh"]

averageBase = 0
averageBaseReal = 0
for i in range(numRuns):
	realStart = time.time()
	start = time.process_time()
	subprocess.call(baseArguments+sys.argv[1:]) # Add arguments from command line
	averageBase += time.process_time() - start
	averageBaseReal += time.time() - realStart
averageBase /= numRuns
averageBaseReal /= numRuns

print("Average base parser process time ("+str(numRuns)+" runs): "+str(averageBase))
print("Average base parser real time ("+str(numRuns)+" runs): "+str(averageBaseReal))

# Improved parser
improvedArguments = ["sh","hw4_improved_parser.sh"]

averageImproved = 0
averageImprovedReal = 0
for i in range(numRuns):
	realStart = time.time()
	start = time.process_time()
	subprocess.call(improvedArguments+sys.argv[1:])
	averageImproved += time.process_time() - start
	averageImprovedReal += time.time() - realStart
averageImproved /= numRuns
averageImprovedReal /= numRuns

print("Average base parser process time ("+str(numRuns)+" runs): "+str(averageBase))
print("Average base parser real time ("+str(numRuns)+" runs): "+str(averageBaseReal))

avgTimeDiff = averageBase - averageImproved
avgTimeDiffReal = averageBaseReal - averageImprovedReal
print("Process time difference: "+str(avgTimeDiff))
print("Process time difference: "+str(avgTimeDiffReal))
percentProcessDiff = avgTimeDiff / averageBase * 100
percentRealDiff = avgTimeDiffReal / averageBaseReal * 100
print("Percentage improvement (process time): "+str(percentProcessDiff)+"%")
print("Percentage improvement (real time): "+str(percentRealDiff)+"%")