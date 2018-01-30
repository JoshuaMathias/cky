# HW 4: PCFG Parser

Joshua Mathias & Kekoa Riggin - LING 570 - January 31, 2018

## Basic PCKY

### Problems

**OOV** - 'either'

**Match Case** - 'Arriving'

### Solutions

**OOV** - Ignore and don't include parse

**Match Case** - Ignore and don't include parse

## Improved PCKY

### Problems


### Solutions



## Insights



## Special features



## What Was Learned



## Incomplete Portions

*discuss what you tried and/or what did not work*

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
