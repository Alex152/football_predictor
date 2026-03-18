from src.core.analyzer_engine import run_analysis


def main():

    print("\n============================")
    print(" FOOTBALL ANALYSIS ENGINE ")
    print("============================\n")

    run_analysis(limit=40)

    print("\nAnalysis completed\n")


if __name__ == "__main__":
    main()

# se ejecuta con:
# python scripts/run_analyzer.py