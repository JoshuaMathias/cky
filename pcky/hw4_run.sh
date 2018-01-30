#!/bin/sh

# USAGE: hw4_run.sh <treebank_filename> <output_PCFG_file> \
      #      <test_sentence_filename> <baseline_parse_output_filename> \
      #      <input_PCFG_file> \
      #      <improved_parse_output_filename> \
		    # <baseline_eval> <improved_eval>
# Example:
# 	export dataDir=~/dropbox/17-18/571/hw4/data
# 	sh hw4_run.sh $dataDir/parses.train hw4_trained.pcfg $dataDir/sentences.txt parses_base.out hw4_trained.pcfg parses_improved.out parses_base.eval parses_improved.eval
#		This example assumes that the induction process isn't improved, but that the parser is improved.

# treebank_filename: Input parsed sentences.
# output_PCFG_file: Output PCFG for your grammar induction
# test_sentence_filename: input test sentences
# baseline_parse_output_filename: output parses from your baseline PCFG parser
# input_PCFG_file:
# If you have not modified the induction process:
# You should take this argument in your script, but may ignore it and re-use the original induced PCFG output.
# If you have modified the induction process:
# This argument should specify the output PCFG of the modified induction process.
# improved_parse_output_filename: output parses from your improved PCFG parser
# baseline_eval: evalb output for your baseline parses
# improved_eval: evalb output for your improved parses.

treebank_filename=$1
output_PCFG_file=$2
test_sentence_filename=$3
baseline_parse_output_filename=$4
input_PCFG_file=$5
improved_parse_output_filename=$6
baseline_eval=$7
improved_eval=$8

sh hw4_topcfg.sh $treebank_filename $output_PCFG_file
sh hw4_parser.sh $output_PCFG_file $test_sentence_filename $baseline_parse_output_filename
sh hw4_improved_parser.sh $input_PCFG_file $test_sentence_filename $improved_parse_output_filename
sh run_eval.sh $baseline_parse_output_filename $baseline_eval
sh run_eval.sh $improved_parse_output_filename $improved_eval