#!/bin/sh

# USAGE: sh run_eval.sh <hypothesis_file> <eval_out_file>
# Examples: 
	# sh run_eval.sh parses_base.out parses_base.eval
	# sh run_eval.sh parses_improved.out parses_improved.eval

export datadir=/dropbox/17-18/571/hw4/data
export toolsDir=/dropbox/17-18/571/hw4/tools

hypothesis_file=$1
eval_out_file=$2
$toolsDir/evalb -p $toolsDir/COLLINS.prm $dataDir/parses.gold $hypothesis_file > $eval_out_file