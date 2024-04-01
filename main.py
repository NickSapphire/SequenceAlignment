import globalSort
import localSort
from sys import argv

if __name__ == "__main__":
    try:
        # Retrieve the inputs from argv
        seq1 = argv[1]
        seq2 = argv[2]
        method = argv[3].lower()
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
            html_content = globalSort.matrix_to_html(M, moves)
        elif method == "local":
            M = localSort.initializeMatrix(seq1, seq2)
            score = localSort.fillMatrix(M, match, mismatch, gap)
            alignment, moves = localSort.traceback(M, match, mismatch, gap)
            html_content = localSort.matrix_to_html(M, moves)
        else:
            raise TypeError

        print(f"\nThe optimal alignment between the two sequences is:\n{alignment}")
        print(f"\nMethod used: {method}")
        print(f"Alignment score: {score}")
        print(f"\nScore matrix:\n{M}")

        with open("alignment.txt", "w") as file:
            file.write(alignment)
        print("\nCreated text file containing the optimal alignment (saved as alignment.txt)")

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
