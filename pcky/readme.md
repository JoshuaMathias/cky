# HW 4: PCFG Parser

Joshua Mathias & Kekoa Riggin - LING 570 - January 31, 2018

### Problems

**OOV** - 
Some words are not found in the training grammar.  
Sentence 41. 'either'  
Sentence 42. 'Traveling'  
Sentence 48. 'during'

**Match Case** - 
Sentence 23. 'Arriving'  
One word is unrecognized when it is capitalized, but is when lowercased.

**Absent Rules** - Rules that appear in the Gold parses file that are not merited in the training file.

| Test Sentence | Gold | Train |
| ------------- | ---- | ----- |
| 6 | (NP_NNP Westchester) | (NP (NNP Westchester) (NNP County)) |
| 41 | (NP_PRIME (CC either) (NNP Wednesday)) | NP_PRIME != CC NNP |
| 42 | (FRAG_VP (VBG Traveling) (NP ...)) | FRAG_VP != VBG NP
| 55 | (NNP Dulles) | (NP_NNP Dulles) |

### Solutions

## Basic PCKY

**OOV** - Ignore and don't include parse.

**Match Case** - Ignore and don't include parse.

**Absent Rules** - Because these rules are not present in the training data, they are not permitted in the parse.

## Improved PCKY

**OOV** - Go through each terminal in training and find the terminal that has the longest suffix (greatest length of final characters) equal to that of the OOV word.

**Match Case** - Lowercase for purposes of matching.

**Absent Rules** - Not permitted in the parse.

## Insights
Coverage may be further improved by allowing expansions that have no rule, if no rule is available for parts of a given sentence, and then assigning a probability that maximizes entropy to that expansion.


## Special features
speed_test_parser.sh and speed_test_parser.py - A script for comparing the process times and real times for running the base parser and the improved parser.  
USAGE: hw4_parser.sh <input_PCFG_file> <test_sentence_filename> <output_parse_filename>  
Output of speed_test_parser.sh:  
Average base parser process time (10 runs): 0.002238491400000002  
Average base parser real time (10 runs): 2.430286741256714  
Average improved parser process time (10 runs): 0.002238491400000002  
Average improved parser real time (10 runs): 2.430286741256714  
Process time difference: -0.0001393708000000009  
Real time difference: 0.08635613918304452  
Percentage improvement (process time): -6.226103884071246%  
Percentage improvement (real time): 3.55333128873465%

run_eval.sh - A script to run evalb (used by hw4_run.sh)  
USAGE: sh run_eval.sh <hypothesis_file> <eval_out_file>

## What Was Learned

Five of the test sentences, which parsed in the gold standard, did not parse with our original induction and parsing scripts. This was not a bug in the code but was a result of flaws in the training data because (mentioned above) a few words and rules that permitted parses in the gold standard were not found in the training data. The easiest fix to these problems is not additional features in the scripts, but additional training data that includes these words and rules.

One solution we considered for the unparsed sentences was including rules for OOV words in the PCFG. This would have required smoothing of rule probabilities and some "hacky" approaches to building the tree. This would have possibly allowed for parses of a sentences that did not make sense due to improper tagging. We settled on fewer incorrect parses rather than more, but incorrect parses.

## Incomplete Portions

We created a script to evaluate efficiency improvements, but no significant imporovement in efficiency was made. One improvement we tried was calculating the probabilities while building the tree instead of keeping track of the rules as the true is built and then multiplying all the tree's rule's probabilities at the end. This didn't make a significant difference.

## Improvements Implemented

**OOV** - Go through each terminal in training and find the terminal that has the longest suffix (greatest length of final characters) equal to that of the OOV word. this resulted in a partially successful parse (88.89%) for sentence 41 by mapping "either" to "other" (whereas it should be instead a "CC" such as "or" or "and"). It also matched "Traveling" and "during" to a gerund "connecting," which was correct for "Traveling" but not for "during" (which in parses.gold is labeled as IN). The sentence containing "Traveling" (42) was still not processed because of a rule missing from the training data (see Absent Rules).
 
**Match Case** - Lowercase for purposes of matching. This resulted in a successful (100%) parse for sentence 23 by matching "Arriving" with "arriving".

For both OOV and Match Case, the comparisons were made solely for the purpose of identifying rules (using the terminal matched) for a word that is otherwise not found in the training data. We then output the original input word.

## Improvements vs. Baseline Results

**Baseline**

| Recal | Prec. | Matched Bracket | Bracket gold | Bracket test | Cross Bracket | Words | Correct Tags | Tag Accracy |
| ----- | ----- | --------------- | ------------ | ------------ | ------------- | ----- | ------------ | ----------- |
| 87.96 | 87.96 | 285             | 324          | 324          | 26            | 424   | 420          | 99.06       |

| Summary | Value |
| ------- | ----- |
| Number of sentence | 55 |
| Number of Error sentence  |      0 |
| Number of Skip  sentence  |      5 |
| Number of Valid sentence  |     50 |
| Bracketing Recall         |  87.96 |
| Bracketing Precision      |  87.96 |
| Bracketing FMeasure       |  87.96 |
| Complete match            |  66.00 |
| Average crossing          |   0.52 |
| No crossing               |  80.00 |
| 2 or less crossing        |  92.00 |
| Tagging accuracy          |  99.06 |

**Improved**

| Recal | Prec. | Matched Bracket | Bracket gold | Bracket test | Cross Bracket | Words | Correct Tags | Tag Accracy |
| ----- | ----- | --------------- | ------------ | ------------ | ------------- | ----- | ------------ | ----------- |
| 87.72 | 87.72 | 293             | 334          | 334          | 26            | 438   | 433          | 98.86       |

| Summary | Value |
| ------- | ----- |
| Number of sentence        |     55 |
| Number of Error sentence  |      0 |
| Number of Skip  sentence  |      3 |
| Number of Valid sentence  |     52 |
| Bracketing Recall         |  87.72 |
| Bracketing Precision      |  87.72 |
| Bracketing FMeasure       |  87.72 |
| Complete match            |  65.38 |
| Average crossing          |   0.50 |
| No crossing               |  80.77 |
| 2 or less crossing        |  92.31 |
| Tagging accuracy          |  98.86 |

Our improved results has 2 fewer sentences skipped, and a greater number of matched brackets.

## Division of Work

**Scripts and file setup** - Joshua  
Determining what commands and parameters need to be used and taking in parameters. Includes script for running eval and hw4_run.sh.

**Coding induction** - Kekoa

**Induction code review and QA** - Joshua

**Coding PCKY Algorithm** - Kekoa

**PCKY code review and QA** - Joshua

**Evaluation** - Joshua & Kekoa

**Improving PCKY** - Joshua

**Discussion of all parts** - Kekoa & Joshua
