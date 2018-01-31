# HW 4: PCFG Parser

Joshua Mathias & Kekoa Riggin - LING 570 - January 31, 2018

## Basic PCKY

### Problems

**OOV** - 41. 'either' 48. 'during'

**Match Case** - 'Arriving'

**Absent Rules** - Rules that appear in the Gold parses file that are not merited in the training file.

| Test Sentence | Gold | Train |
| ------------- | ---- | ----- |
| 6 | (NP_NNP Westchester) | (NP (NNP Westchester) (NNP County)) |
| 41 | (NP_PRIME (CC either) (NNP Wednesday)) | NP_PRIME != CC NNP |
| 42 | (FRAG_VP (VBG Traveling) (NP ...)) | FRAG_VP != VBG NP
| 55 | (NNP Dulles) | (NP_NNP Dulles) |

### Solutions

**OOV** - Ignore and don't include parse

**Match Case** - Ignore and don't include parse

**Absent Rules** - Because these rules are not present in the training data, they are not permitted in the parse.

## Improved PCKY

### Problems


### Solutions



## Insights



## Special features

<!--- I Think this is covered by improvements. --->

## What Was Learned

Five of the test sentences, which parsed in the gold standard, did not parse with our original induction and parsing scripts. This was not a bug in the code but was a result of flaws in the training data because (mentioned above) a few words and rules that permitted parses in the gold standard were not found in the training data. The easiest fix to these problems is not additional features in the scripts, but additional training data that includes these words and rules.

One solution we considered for the unparsed sentences was including rules for OOV words in the PCFG. This would have required smoothing of rule probabilities and some "hacky" approaches to building the tree. This would have possibly allowed for parses of a sentences that did not make sense due to improper tagging. We settled on fewer incorrect parses rather than more, but incorrect parses.


## Incomplete Portions

<!--- Possibly move the paragraph on OOV here --->

## Improvements Implemented



## Improvements vs. Baseline Results

**Baseline**

| Recal | Prec. | Matched Bracket | Bracket gold | Bracket test | Cross Bracket | Words | Correct Tags | Tag Accracy |
| ----- | ----- | --------------- | ----------------- | --------------- | ----- | ------------ | ----------- |
| 87.96 | 87.96 | 285 | 324 | 324 | 26 | 424 | 420 | 99.06 |

| Summary | Value |
| ---- | ----- |
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

## Division of Work

**Scripts and file setup** - Joshua
Determining what commands and parameters need to be used and taking in parameters. Includes script for running eval and hw4_run.sh.

**Coding induction** - Kekoa

**Induction code review and QA** - Joshua

**Coding PCKY Algorithm** - Kekoa

**PCKY code review and QA** - Joshua

**Evaluation** - Joshua & Kekoa

**Improving PCKY** - Joshua
