#!/usr/bin/env python

import argparse
import glob
import os
import re

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
            md_re = re.match("[^\s\t]*e_md\*/", line)
            if md_re:
                in_md = False
                if in_sv:
                    ofh.write("```sv\n")
            else:
                ofh.write(line)
        elif in_sv:
            md0_re = re.match("[^\s\t]*/\*s_md", line)
            md1_re = re.match("[^\s\t]*//md (.*)", line)
            sv_re = re.match("[^\s\t]*//e_sv", line)
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
            md0_re = re.match("[^\s\t]*/\*s_md", line)
            md1_re = re.match("[^\s\t]*//md (.*)", line)
            sv_re = re.match("[^\s\t]*//s_sv", line)
            if md0_re:
                in_md = True
            elif md1_re:
                ofh.write(md1_re.groups()[0])
            elif sv_re:
                in_sv = True
                ofh.write("```sv\n")
            else:
                md_re = re.match("^[\s\t]*//md (.*)", line)
                if md_re:
                    ofh.write(md_re.groups()[0])
    ifh.close()
    ofh.close()

args, parser = parse_arguments()
filelist = get_filelist(args)
for ifile in filelist:
    ofile = args.output_dir + "/" + os.path.basename(ifile)
    ofile = ofile.replace(".sv", ".md")
    markdown(ifile, ofile)
