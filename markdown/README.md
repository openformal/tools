# Introduction
This script generates markdown files from SystemVerilog code.
The comments in the SystemVerilog code get converted to markdown
and SystemVerilog code is put in (```sv, ```) block and is treated
as SystemVerilog code.

Comments need to be written in Markdown language of Github. The
syntax fits the pattern of regular comments so the comments can
be effective viewed in the source or the markdown.

# Rule for writing markdown in SystemVerilog code
When parsing a SystemVerilog file there is a concept of a main
state and substate. 

* At any time the state is "sv" or "non-sv"
* Initial state is non-sv
* At any time the substate is "md" or "non-md"
* Initial substate is "non-md"
* State changes from non-sv to sv with //sv+ block
* State chages from sv to non-sv with //sv- block
* Final state must be non-sv
* Substate can be changed to md with /*md block
* Substate can be changed to non-md with */ block
*  No text is allowed in the /*md and */ lines
*  Text in md substate is printed as Markdown
*  Text in non-sv state and non-markdown state is ignored
   This can be used for removing file headers
*  Text in sv state and non-markdown state is
   printed as SystemVerilog code
*  //md <Text> is a single line markdown and the <Text>
   is printed as markdown
