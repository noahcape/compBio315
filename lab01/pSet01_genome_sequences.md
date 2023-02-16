Noah Cape pest/lab 01
compBio 315
Feb 13, 2023

Problem Set Questions

0) Unix commands. Identify the function of these Unix/Terminal/operators:
`ls` list the contents of your current dir

`cd` change directory

`cp` copy contents of a source file into a destination file

`mv` move files

`rm` removes non directory files

`mkdir` creates a directory in current dir

`pwd` prints current working directory

`scp` secure file copy between hosts on network

`lpr` print files, sent to default destination or named dest

`cat` concatenate and print files, read files and writing them to standard output

`more` forward movement reading through a file in cmdline

`grep` search given input files with specified pattern

`head` display the first n lines of a file (default to 10)

`tail` display the last n lines of a file (defualt to 10)

`man` read online manual pages

`chmod` change file modes and access control lists

`|` Pipe connecting stdout of command to stdin of next command

`&` Run command in the background, shell does not wait for command to finish

`>` Output redirection operator, overwriting files contents

`<` Input redirection

`>>` Output redirection, concatenate to files current contents

`*` Match zero or more characters

`?` Match one character

`;` Run multiple commands and execute the second no matter the status of the first

1) Get to know DNA

    (a) Directionality of the DNA backbone: The two DNA strands run opposite to eachother, 5'->3', major strand, then the minor strand which is upside down compared to major stand where the major stand is 5' at top minor is 3'.

    (b) The four bases of DNA are A, T, G, and C, RNA has A, U, G, and C. The two groups that bases fall into are purines (A, G) and prymidines (C, T, U). Purines consist of two carbon nitrogen ring bases and Pyrimidines consists of one.

    (c) Chromosome: Strucutre of DNA molecules and proteins, Gene: One contiguous stretch of DNA to corresponds to a different kind of protien., Operon: Unit made of linked genes, Codon: nucleotide triplet, Nucleotide: Basic DNA molecule consisting of sugar, phosphate and its base.

    (d) Typical nucleotides in chromosome: 50 mbp to 250 mbp, gene: 10-15 kpb, operon: 5 * avg gene length ~> 50-75 kbp, codon: 3.

    (e) What makes DNA an acid: the phosphate groups on in the DNA backbone have a net negative charge, since the basic component (nitrogen groups) form the inside of the double helix therefore with the phosphate groups having an negative charge and being exposed to the environment compared to the nitrogen bases makes DNA an acid.

2) Define the terms

- Oligo: polynucleotide which contains a relatively small number of nucleotides
- primer: short single stranded DNA fragment used for lab techniques, usually target certain places in genome to bind to (18-25 bp)
- dNTP: Deoxynucleotide triphosphates, bulding block of DNA, lose two phosphate groups when incorperated into DNA during replication.
- ddNTP: dideoxynucleotides lack the 3' hydroxyl group that inhibit further polymerization of DNA backbone, used in Sanger sequencing method.
- electrophoresis: Lab technique to seperate DNA, RNA, or protein molecules based on size and electrical charge. Smaller molecules move through gel faster than larger molecules.
- restriction enzyme fragment: Fragment of DNA from cutting of DNA by restriction enzyme. Matches to certain patterns in DNA and cuts DNA at those sites.
- pyrosequencing: Sequencing method of DNA that detects light emitted during the sequencial addition of nucleotides.
- primer walking: Sequencing technique that uses a series of Sanger sequencing reactions to clone a gene.
- ligation: Joining of two nucleic acid fragments through the action of an enzyme.
- mate-paired ends / paired-end sequencing: Methodologies that give information about two read belonging to a pair. The DNA is sheared into random fragments and then both ends of each fragment are sequenced. Mate pair tags that are sequenced belong to a larger molecule (btw 2 and 10 kbps) In Paired end sequences both reverse and forward templates, each end is seperately sequences and the two sequences are known as paired end reads. Distance between paired end reads is about 300bp.

3) Key innovations in DNa sequencing technologies:
- Paper suggests "the first implementation of this approach produces approximately 10 billion reads per run, with a turnaround time of under 20 hrs per run for 300 bp reads, and with base quality similar to existing platforms (Q30 >85%), at a price of $1/Gb."
- Longer reads (300bp) opening up analysis that cannot be achieved in short reads (100bp)

4) DNA with p_a = p_c = p_g = p_t = 0.25
- Liklihood of start codon (0.25 * 0.25 * 0.25) = 0.015625
- 64/3 bp (~21) If a stop codon happens occurs 3/64