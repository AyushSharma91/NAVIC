from src.parser import parse_all_logs
from src.analysis import run_analysis
from src.model import train_model


# run the full pipeline: parsing -> route/satellite analysis -> ml training
def main():
    print("\n==============================================")
    print(" AI Powered Smart Route Analyzer")
    print("==============================================")

    # step 1: parse raw logs into csv files
    print("\n[1/3] Parsing GNSS Logs...\n")
    parse_all_logs()

    # step 2: compute trip metrics and satellite stats
    print("\n[2/3] Running Route Analysis...\n")
    run_analysis()

    # step 3: train random forest model on route coordinates
    print("\n[3/3] Training Machine Learning Model...\n")
    train_model()

    print("\n==============================================")
    print(" Project Completed Successfully ")
    print("==============================================")


if __name__ == "__main__":
    main()