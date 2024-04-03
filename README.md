# SequenceAlignment

This is a Python implementation of the Needleman-Wunsch and Smith-Waterman algorithms
for sequence alignment.

## Library dependencies

This program relies on the numpy and pandas libraries.

Pandas provides a nice visual representation for the score matrix, it allows the use
of string indices for rows and columns and has built-in functions to create html representations
of matrices as tables. NumPy facilitated some tasks such as generating a matrix with all zeros and
finding the largest value in the matrix.

## How to use

Run the main.py script in the terminal while in the SequenceAlignment directory,
passing the specified arguments in the following order:

```
python main.py <seq1> <seq2> <method> <match> <mismatch> <gap>
```

Mandatory parameters:
- seq1 and seq2: The two sequences to be aligned.
- method: Either "global" or "local", determines the algorithm used for alignment.

Optional parameters: Must be either all included or all ommited. They all expect integer values.
- match: Score increase for a match, 1 by default
- mismatch: Score penalty for a mismatch, -1 by default
- gap: Score penalty for a gap in either string, -2 by default

Example: 
```
python main.py ATCGATCGATCG ATGCTAGCTAG global 2 -1 -2
```

Note: In Mac python3 should be used instead of python for the command.

The output will contain:
- The optimal alignment between both strings, with a string in between describing the alignment:
  - line (|) match
  - dot (.): mismatch
  - space ( ): gap
- The method used to align the strings.
- The overall alignment score (last value for global, largest value for local).
- The score matrix.

The above command provides the following output:
```
The optimal alignment between the two sequences is:
ATCGATCGATCG
|| |.|.|.|.|
AT-GCTAGCTAG

Created text file containing the optimal alignment (saved as alignment.txt)

Method used: global
Alignment score: 8

Score matrix:
    -   A   T   G  C   T   A   G   C   T   A   G
-   0  -2  -4  -6 -8 -10 -12 -14 -16 -18 -20 -22
A  -2   2   0  -2 -4  -6  -8 -10 -12 -14 -16 -18
T  -4   0   4   2  0  -2  -4  -6  -8 -10 -12 -14
C  -6  -2   2   3  4   2   0  -2  -4  -6  -8 -10
G  -8  -4   0   4  2   3   1   2   0  -2  -4  -6
A -10  -6  -2   2  3   1   5   3   1  -1   0  -2
T -12  -8  -4   0  1   5   3   4   2   3   1  -1
C -14 -10  -6  -2  2   3   4   2   6   4   2   0
G -16 -12  -8  -4  0   1   2   6   4   5   3   4
A -18 -14 -10  -6 -2  -1   3   4   5   3   7   5
T -20 -16 -12  -8 -4   0   1   2   3   7   5   6
C -22 -18 -14 -10 -6  -2  -1   0   4   5   6   4
G -24 -20 -16 -12 -8  -4  -3   1   2   3   4   8

Created score matrix with highlighted moves (saved as score_matrix.html) in the SequenceAlignment directory.
```

When doing local alignment, only the aligned substrings from both sequences will be uppercase,
the rest will be lowercase, as seen below:

```
python main.py TFDERILGQTYWAECLA QTFWECIKGDNATY local 3 -3 -5
```

```
The optimal alignment between the two sequences is:
tfderilgQTYWAECla
        ||.| ||         
        QTFW-ECikgdnaty

Created text file containing the optimal alignment (saved as alignment.txt)

Method used: local
Alignment score: 7

Score matrix:
   -  Q  T  F  W  E  C  I  K  G  D  N  A  T  Y
-  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
T  0  0  3  0  0  0  0  0  0  0  0  0  0  3  0
F  0  0  0  6  1  0  0  0  0  0  0  0  0  0  0
D  0  0  0  1  3  0  0  0  0  0  3  0  0  0  0
E  0  0  0  0  0  6  1  0  0  0  0  0  0  0  0
R  0  0  0  0  0  1  3  0  0  0  0  0  0  0  0
I  0  0  0  0  0  0  0  6  1  0  0  0  0  0  0
L  0  0  0  0  0  0  0  1  3  0  0  0  0  0  0
G  0  0  0  0  0  0  0  0  0  6  1  0  0  0  0
Q  0  3  0  0  0  0  0  0  0  1  3  0  0  0  0
T  0  0  6  1  0  0  0  0  0  0  0  0  0  3  0
Y  0  0  1  3  0  0  0  0  0  0  0  0  0  0  6
W  0  0  0  0  6  1  0  0  0  0  0  0  0  0  1
A  0  0  0  0  1  3  0  0  0  0  0  0  3  0  0
E  0  0  0  0  0  4  0  0  0  0  0  0  0  0  0
C  0  0  0  0  0  0  7  2  0  0  0  0  0  0  0
L  0  0  0  0  0  0  2  4  0  0  0  0  0  0  0
A  0  0  0  0  0  0  0  0  1  0  0  0  3  0  0

Created score matrix with highlighted moves (saved as score_matrix.html) in the SequenceAlignment directory.
```

Note: Use python3 instead of python when running the command on MacOS.

## File outputs

- `alignment.txt`: Aligned strings with the match string in between as seen in the terminal output.
Best to visualize long sequences.
- `score_matrix.html`: Table representation of the score matrix, with the moves taken during traceback
highlighted in green. Once again it allows the visualization of large alignments, since the matrix
will not be shown entirely in the terminal if it's too large.

## Different optimal alignments

It's possible that more than one traceback path will yield the score written in the final cell.
This program will only compute one of the multiple optimal alignments. If a match was not found, it will
check if it can move diagonally (mismatch), left or up respectively. This is a somewhat arbitrary decision,
mostly based around the fact that mismatches usually cause a lighter penalty than gaps. 

## Contact

Nicolas Schiappa

nicolas.schiappa@studio.unibo.it