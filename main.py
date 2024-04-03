import pandas as pd
import globalSort
import localSort
from sys import argv


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
    styled_matrix = matrix_copy.style.apply(highlight_moves, axis=None)
    styled_matrix.set_table_attributes('border=1 class="dataframe"')
    html = styled_matrix.to_html()

    # Change back the row and column labels with those of the original matrix
    for i in range(len(matrix.index)):
        html = html.replace(f'row{i}" >{i}</th>', f'row{i}" >{matrix.index[i]}</th>')
    for j in range(len(matrix.columns)):
        html = html.replace(f'col{j}" >{j}</th>', f'col{j}" >{matrix.columns[j]}</th>')
    return html  # This part took a while, I finally got it to work :)


if __name__ == "__main__":
    try:
        # Retrieve the inputs from argv
        seq1 = argv[1]
        seq2 = argv[2]
        method = argv[3].lower()  # Non-case sensitive argument
        if len(argv) == 4:  # Score settings ommited, resorts to default values
            match = 1
            mismatch = -1
            gap = -2
        elif len(argv) == 7:  # Score settings specified
            match = int(argv[4])
            mismatch = int(argv[5])
            gap = int(argv[6])
        else:  # Any other number of arguments is invalid, so this should print an error message
            raise IndexError

        if method == "global":
            M = globalSort.initializeMatrix(seq1, seq2, gap)
            score = globalSort.fillMatrix(M, match, mismatch, gap)
            alignment, moves = globalSort.traceback(M, match, mismatch, gap)
        elif method == "local":
            M = localSort.initializeMatrix(seq1, seq2)
            score = localSort.fillMatrix(M, match, mismatch, gap)
            alignment, moves = localSort.traceback(M, match, mismatch, gap)
        else:
            raise TypeError

        print(f"\nThe optimal alignment between the two sequences is:\n{alignment}")
        with open("alignment.txt", "w") as file:
            file.write(alignment)
        print("\nCreated text file containing the optimal alignment (saved as alignment.txt)")

        print(f"\nMethod used: {method}")
        print(f"Alignment score: {score}")
        print(f"\nScore matrix:\n{M}")

        html_content = matrix_to_html(M, moves)
        with open("score_matrix.html", "w") as file:
            file.write(html_content)

        print("\nCreated score matrix with highlighted moves (saved as score_matrix.html)\n")

    except IndexError:
        print("The number of arguments is incorrect (must be either 4 or 7).",
              "The correct structure for the command is:"
              "python main.py <seq1> <seq2> <method> <match> <mismatch> <gap>",
              "Refer to the README file for more information", sep="\n")

    except TypeError:
        print(f'Invalid alignment method "{method}", it must be either "global" or "local" (not case sensitive).')
