#!/usr/bin/env python

import argparse
import glob
import os
import re

## Markdown rules
## 1. At any time the state is "sv" or "non-sv"
## 2. Initial state is non-sv
## 3. At any time the substate is "md" or "non-md"
## 4. Initial substate is "non-md"
## 5. State changes from non-sv to sv with //sv+ block
## 6. State chages from sv to non-sv with //sv- block
## 7. Final state must be non-sv
## 8. Substate can be changed to md with /*md block
## 9. Substate can be changed to non-md with */ block
## 10. No text is allowed in the /*md and */ lines
## 11. Text in md substate is printed as Markdown
## 12. Text in non-sv state and non-markdown state is ignored
##     This can be used for removing file headers
## 13. Text in sv state and non-markdown state is
##     printed as SystemVerilog code
## 14. //md <Text> is a single line markdown and the <Text>
##     is printed as markdown

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-if', '--file', help='Input file')
    parser.add_argument('-id', '--input_dir', help='Input directory')
    parser.add_argument('-od', '--output_dir', help='Output directory')
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()
    if args.file is None and args.input_dir is None:
        print("Error: no input file or directory specified")
        parser.print_help()
        exit(1)

    if args.output_dir is None:
        args.output_dir = os.getcwd()

    return args, parser

def get_filelist(args):
    if args.input_dir is not None:
        filelist = glob.glob(args.input_dir + "/*.sv")
    else:
        filelist = []
    if args.file is not None:
        filelist.append(args.file)
    return filelist

def markdown(ifile, ofile):
    print("Generating markdown for " + ifile + " -> " + ofile)
    try:
        ifh = open(ifile, "r")
    except IOError:
        print("Error: Could not open input file " + ifile)
    try:
        ofh = open(ofile, "w")
    except IOError:
        print("Error: Could not open output file " + ofile)
    in_md = False
    in_sv = False
    for line in ifh:
        if in_md:
            md_re = re.match("^[\s\t]*\*/", line)
            if md_re:
                in_md = False
                if in_sv:
                    ofh.write("```sv\n")
            else:
                ofh.write(line)
        elif in_sv:
            md0_re = re.match("^[\s\t]*/\*md", line)
            md1_re = re.match("^[\s\t]*//md (.*)", line)
            sv_re = re.match("^[\s\t]*//sv-", line)
            if md0_re:
                in_md = True
                ofh.write("```\n")
            elif md1_re:
                ofh.write("```\n")
                ofh.write(md1_re.groups()[0] + "\n")
                ofh.write("```sv\n")
            elif sv_re:
                in_sv = False
                ofh.write("```\n")
            else:
                ofh.write(line)
        else:
            md0_re = re.match("^[\s\t]*/\*md", line)
            md1_re = re.match("^[\s\t]*//md (.*)", line)
            not_empty = line.strip();
            sv_re = re.match("^[\s\t]*//sv+", line)
            if md0_re:
                in_md = True
            elif md1_re:
                ofh.write(md1_re.groups()[0] + "\n")
            elif sv_re:
                in_sv = True
                ofh.write("```sv\n")
    ifh.close()
    ofh.close()

args, parser = parse_arguments()
filelist = get_filelist(args)
for ifile in filelist:
    ofile = args.output_dir + "/" + os.path.basename(ifile)
    ofile = ofile.replace(".sv", ".md")
    markdown(ifile, ofile)
