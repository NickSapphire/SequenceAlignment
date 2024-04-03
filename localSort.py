import numpy as np
import pandas as pd


def initializeMatrix(seq1: str, seq2: str) -> pd.DataFrame:
    """
    Given two strings of length m and n respectively, returns a pandas DataFrame
    with m+1 rows and n+1 columns with only zeros.
    """
    m = len(seq1)
    n = len(seq2)
    row_labels = ['-'] + [char for char in seq1]
    col_labels = ['-'] + [char for char in seq2]
    matrix = pd.DataFrame(data=np.zeros((m + 1, n + 1)), index=row_labels, columns=col_labels,
                          dtype="int64")
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
        # If the three possible moves have a negative score, the score is set to 0
        score = max(nb1 + gap, nb2 + mismatch, nb3 + gap, 0)
    return score


def fillMatrix(matrix: pd.DataFrame, match: int, mismatch: int, gap: int) -> int:
    """
    Takes an initialized score matrix, fills it by in-place modification and
    returns the optimal alignment score (highest score value in the matrix).
    """
    for i in range(1, matrix.shape[0]):
        for j in range(1, matrix.shape[1]):
            matrix.iloc[i, j] = cellScore(matrix, (i, j), match, mismatch, gap)
    return matrix.max(axis=None)  # axis set to None to scan the whole matrix


def traceback(matrix: pd.DataFrame, match, mismatch, gap) -> tuple:
    """
    Performs the traceback operation from the cell with the highest value up to the first
    cell found whose neighbours are all zero and returns the optimal alignment as a string
    containing the two sequences separated by a newline character. The aligned substrings
    will be uppercase and the rest of the strings will be in lowercase. The characters are
    added from right to left.
    """
    max_pos = matrix.to_numpy().argmax()  # Position of max value in the flattened array
    i, j = np.unravel_index(max_pos, matrix.shape)  # Coordinates of max value
    seq1 = "".join(matrix.index[i + 1:]).lower()
    seq2 = "".join(matrix.columns[j + 1:]).lower()
    match_string = " " * abs(i - j)  # Will connect matches with a "|" character in the final output
    moves = []
    nb1, nb2, nb3 = getNeighbours(matrix, (i, j))
    score = matrix.iloc[i, j]

    while score != 0:
        moves.append((i, j))
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
        nb1, nb2, nb3 = getNeighbours(matrix, (i, j))
        score = matrix.iloc[i, j]

    # Add the unaligned prefixes to both strings, if they exist
    if i != 0:
        seq1 = "".join(matrix.index[1:i+1]).lower() + seq1
    if j != 0:
        seq2 = "".join(matrix.columns[1:j+1]).lower() + seq2

    # If misaligned, add spaces at the start of the string with the most lowercase characters on the left.
    spaces = abs(i - j) * " "
    if i < j:
        seq1 = spaces + seq1
        match_string = j * " " + match_string   # Realign match_string to the start of uppercase letters
    elif j < i:
        seq2 = spaces + seq2
        match_string = i * " " + match_string

    return f"{seq1}\n{match_string}\n{seq2}", moves


def matrix_to_html(matrix, moves):
    """
    Creates an html representation of the score matrix and highlights coordinates in moves
    green. The resulting string will be converted by an html file by the main script.
    """
    def highlight_moves(df):
        color = "background-color: lightgreen"
        df1 = pd.DataFrame('', index=df.index, columns=df.columns)
        for coords in moves:
            df1.iloc[coords] = color
        return df1

    # style doesn't admit non-unique indices, converting to numpy gets rid of the labels
    matrix_copy = pd.DataFrame(matrix.to_numpy(), index=range(matrix.shape[0]),
                               columns=range(matrix.shape[1]))
    styled_matrix = matrix_copy.style.apply(highlight_moves, axis=None)  # colors the coordinates in moves
    styled_matrix.set_table_attributes('border=1 class="dataframe"')
    html = styled_matrix.to_html()

    # Change back the row and column labels with those of the original matrix
    for i in range(len(matrix.index)):
        html = html.replace(f'row{i}" >{i}</th>', f'row{i}" >{matrix.index[i]}</th>')
    for j in range(len(matrix.columns)):
        html = html.replace(f'col{j}" >{j}</th>', f'col{j}" >{matrix.columns[j]}</th>')
    return html  # This part took a while, I finally got it to work :)
