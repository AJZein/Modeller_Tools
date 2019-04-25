This document provides help/instructions on how to use the mutator_functions program (version 1.1.2).
The program uses python version 3.7.0.

Introduction:
The mutator_functions.py file contains a set of functions which quick methods to mutate a target sequence in an alignment file.
The program provides two methods of mutation, replace and insertion mutations, which will be described below.

Input:
In the same folder as your script you should have the alignment file you seek to mutate, the pdbs of your knowns and the 
mutator_functions.py script.

Outputs:
Your script should generate new alignment files for modeller to use (the original alignment file is unchanged) as well as
all the files modeller will generate when running.

Creating a script:
An example script is provided to illustrate this process. 
Begin by importing all the functions from mutator_functions.py.
Next specify the names of your alignment file, knowns and the target sequence.
Create a structure by passing the above names to 'get_structure(ali_filename, sources)'
Next decide on what kind of mutation you would like to perform.
Performing a mutation will require using either 'insert_mutation()' or 'replace_mutation()', both of which generate a mutated structure.
Save the mutated structure into an alignment file using 'structure_to_file()'
Run Modeller as usual using the newly created alignment file.

Notes on the example script:
The example script illustrates how to perform multiple mutations and create multiple pdbs.
In this script the sequence 'SAGG' is replaced with 'GGAS' once on line 3 of the target and 2 pdbs are created.
The pdbs are then renamed so they are not overwritten 
'SAGG' is then replaced with 'SAGGSAGG' on line 3 and more pdbs are created.

Function details:
Below are details of the various functions in mutator_functions.py that the user will need to use 


get_structure(ali_filename, sources)
ali_filename is a string which contains the name of your alignment file (without extensions).
sources is a list which contains the names of your knowns and the name of the target
Returns a structure, which is a specially organised list

Before any work can be done a structure must be generated. This is a specially formatted list
which contains the alignments files data, it is utilised by the rest of the functions




insert_mutation(structure, linenum, mutation, pos=-1)
structure is a list outputted by get_structure()
linenum is a non negative integer which specifies the line on which to perform the mutation
mutation is a string which contains the sequence you wish to insert
pos is an integer which specifies where on the line the mutation will be inserted

This function takes a previously generated structure, and modifies the target by inserting inserting the
sequence given by 'mutation' on the line given by 'linenum' at a position given by 'pos'. For example if 
mutation = 'Hi', linenum = 2 and pos = 3 it will insert 'Hi' on the 3rd line, after the 3rd character 
(both pos and linenum start counting from 0). If pos isn't specified it will be inserted at the end 
of the line.


replace_mutation(structure, linenum, original='-', mutation='-', maximum=-1, origin=0)
structure is a list outputted by get_structure()
linenum is a non negative integer which specifies the line on which to perform the mutation
original is a string which contains the sequence to be replaced
mutation is a string which contains the sequence that will replace 'original'
maximum is an integer which indicates the number of replacements that will be performed
origin is an integer which specifies what character to begin replacing from.

This function replaces a particular sequence in the target with another sequence. 'original' is the sequence
to be replaced and 'mutation' replaces it. 'structure' and 'linenum' are as before. If 'original' occurs multiple
times in the same line, 'maximum' allows you to specify how many of these to replace (default all).
If 'original' is unspecified the entire line in the target will be replaced. If 'mutation' is not specified
the sequence will be deleted from the target.

Furthermore by specifying 'origin' the function will begin searching for occurences of 'original' from the position 
specified by origin. The first occurence of 'original' that will be replaced is the one closest to 'origin', the second
occurence of 'original' that will be replaced is the one second closest to 'origin' and so on until 'maximum' is reached.
This can be used for example to replace only the first 4 occurences of a string in the middle of a line, or from the end of a line
or even to perform just a single mutation at a specific point in the line. 




structure_to_file(structure, filename='untitled', extension='.txt')
structure is a list outputted by get_structure()
filename is a string which contains the name under which to save the file
extension is a string, self explanatory.

This function is used to save the structure into a file which modeller can then use to generate pdbs. 
Make sure to set extension to '.ali' in this case.



** 
Note: 'linenum' counts the number of lines from the first line (linenum=0) in the target, where the first line is
the first line of actual sequence data. It doesn't count the lines with the targets name and information.
For example
>P1;egfr-hinge-sensor-mutate2
 #IGNORED
sequence:egfr-hinge-sensor-mutate2::::::composed from Nguyen et al : 1.90: 0.19 #IGNORED
MVSKGEELFGGIVPILVELDGDVNGHK # FIRST LINE, linenum = 0
FKDDGNYKTRAEVKFEGDTLVNRIELKGIDFKEDG # SECOND LINE, linenum = 1
NFKIRHNITDGGVQLAD
**
