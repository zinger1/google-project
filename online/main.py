from online.search_results import get_best_k_completions
from utils.ignore_casing import ignore_casing


def main():
    print("The system is ready. Enter your text:")

    prefix = input()

    while True:
        if "#" == prefix[-1]:
            prefix = input()
        if ignore_casing(prefix):
            i = 0
            suggestions = get_best_k_completions(prefix)
            num = len(suggestions)
            if suggestions:
                print("\n ********************************************************* \n")
                print(f"Here are {num} suggestion to \'{ignore_casing(prefix)}\': \n")
                for suggest in suggestions:
                    i += 1
                    print(
                        f"{i}. {suggest.get_completed_sentence()} ({suggest.get_offset()} {suggest.get_source_text()} {suggest.get_score()})")

                print("\n ********************************************************* \n ")
                print(prefix, end="")

            else:
                print("\n ********************************************************* \n ")
                print("\tThere are no suggestions")
                print("\n ********************************************************* \n ")
                prefix = ""

        prefix += input()


if __name__ == "__main__":
    main()
