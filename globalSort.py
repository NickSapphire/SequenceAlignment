import numpy as np
import pandas as pd


def initializeMatrix(seq1: str, seq2: str, gap: int) -> pd.DataFrame:
    """
    Given two strings of length m and n respectively and the gap score penalty,
    returns a pandas DataFrame with m+1 rows and n+1 columns with the progressive gap
    penalty applied in the first row and column (both labeled '-'). The rest of the rows
    and columns represent each character of the first and second sequence respectively.
    """
    m = len(seq1)
    n = len(seq2)
    row_labels = ['-'] + [char for char in seq1]
    col_labels = ['-'] + [char for char in seq2]
    matrix = pd.DataFrame(data=np.zeros((m + 1, n + 1)), index=row_labels, columns=col_labels,
                          dtype="int64")

    # Add progressive gap penalties on row 0 and column 0
    for i in range(m + 1):
        matrix.iloc[i, 0] = i * gap
    for j in range(n + 1):
        matrix.iloc[0, j] = j * gap
    return matrix


def getNeighbours(matrix: pd.DataFrame, coords: tuple) -> tuple:
    """
    Returns a tuple containing all 3 neighbours obtained by moving left and/or up
    of a given set of coordinates of a matrix.
    nb1: vertical move, nb2: diagonal move (upper-left), nb3: horizontal move.
    """
    i, j = coords
    nb1 = matrix.iloc[i, j - 1]
    nb2 = matrix.iloc[i - 1, j - 1]
    nb3 = matrix.iloc[i - 1, j]
    return nb1, nb2, nb3


def cellScore(matrix: pd.DataFrame, coords: tuple, match: int, mismatch: int, gap: int) -> int:
    """
    Given two sequences, their score matrix and a coordinate tuple (row, col), computes
    the score of the specified cell.
    """
    i, j = coords
    nb1, nb2, nb3 = getNeighbours(matrix, coords)

    # Compare the row and column labels of a given coordinate
    if matrix.index[i] == matrix.columns[j]:
        score = nb2 + match  # Diagonal movement, adding the match score
    else:
        # No match, check the best move applying the mismatch or gap penalty accordingly
        score = max(nb1 + gap, nb2 + mismatch, nb3 + gap)
    return score


def fillMatrix(matrix, match, mismatch, gap):
    """
    Takes an initialized score matrix, fills it by in-place modification and
    returns the optimal alignment score (value on bottom right cell).
    """
    for i in range(1, matrix.shape[0]):
        for j in range(1, matrix.shape[1]):
            matrix.iloc[i, j] = cellScore(matrix, (i, j), match, mismatch, gap)
    return matrix.iloc[i, j]


def traceback(matrix, match, mismatch, gap):
    """
    Performs the traceback operation from the last cell to [1,1] and returns
    the optimal alignment as a string containing the two sequences separated
    by a newline. The characters are added from right to left.
    """
    seq1 = ""
    seq2 = ""
    match_string = ""  # Will connect matches with a "|" and mismatches with "." in the final output
    i = matrix.shape[0] - 1
    j = matrix.shape[1] - 1
    moves = []

    while i != 0 or j != 0:
        score = matrix.iloc[i, j]
        moves.append((i, j))  # The coordinates for the moves to be highlighted in the html file
        nb1, nb2, nb3 = getNeighbours(matrix, (i, j))
        if nb2 + match == score and matrix.index[i] == matrix.columns[j]:
            seq1 = matrix.index[i] + seq1
            seq2 = matrix.columns[j] + seq2
            i -= 1
            j -= 1
            match_string = "|" + match_string
        elif nb2 + mismatch == score:
            seq1 = matrix.index[i] + seq1
            seq2 = matrix.columns[j] + seq2
            i -= 1
            j -= 1
            match_string = "." + match_string
        elif nb3 + gap == score:
            seq1 = matrix.index[i] + seq1
            seq2 = "-" + seq2
            i -= 1
            match_string = " " + match_string
        elif nb1 + gap == score:
            seq1 = "-" + seq1
            seq2 = matrix.columns[j] + seq2
            j -= 1
            match_string = " " + match_string
        else:
            raise ValueError("Invalid score matrix")

    # If the index of a string doesn't reach 0, add gaps at the beggining of that string
    if i != 0:
        seq1 = i * '-' + seq1
    if j != 0:
        seq2 = j * '-' + seq2
    return f"{seq1}\n{match_string}\n{seq2}", moves
