import sys
import os
import pandas as pd
import numpy as np
from tabulate import tabulate
import time

# Now you can import db_compare
import Database_comparator.db_compare as db_compare



FULL_PASSED = True
def clean_up_blast_files():
        # Cleanup temporary filesP
    if os.path.exists("Fasta_files"):
        for file in os.listdir("Fasta_files"):
            os.remove(os.path.join("Fasta_files", file))
        os.rmdir("Fasta_files")

    if os.path.exists("Query_files"):
        for file in os.listdir("Query_files"):
            os.remove(os.path.join("Query_files", file))
        os.rmdir("Query_files")

    if os.path.exists("BLAST_database"):
        for file in os.listdir("BLAST_database"):
            os.remove(os.path.join("BLAST_database", file))
        os.rmdir("BLAST_database")

    if os.path.exists("blastp_output.txt"):os.remove("blastp_output.txt")

def test_initialization():
    """Tests if the DB_comparator class initializes correctly and measures initialization time."""
    config_file = r"TMP_testing_folder/test_config_file.txt"
    global FULL_PASSED

    try:
        start_time = time.time()
        db_comparator = db_compare.DB_comparator(config_file, log_tag="initialization_test", log_project="Testing")
        end_time = time.time()
        elapsed_time = end_time - start_time

        passed = True
        if db_comparator is None: passed = False
        if db_comparator.config != db_comparator.aligner.config: passed = False
        if db_comparator.config != db_comparator.exact_match.config: passed = False
        if db_comparator.config != db_comparator.hamming_distances.config: passed = False
        if db_comparator.config != db_comparator.fast_hamming_distances.config: passed = False
        if db_comparator.config != db_comparator.blast.config: passed = False

        FULL_PASSED = FULL_PASSED and passed

        return "✅ Success" if passed else "❌ Failed", "N/A", round(elapsed_time, 2)

    except Exception as e:
        print(f"Initialization test failed with error: {e}")
        return "❌ Failed", "N/A", "N/A"

def test_exporting():
    """Tests if the DB_comparator class exports data frames correctly."""
    config_file = r"TMP_testing_folder/test_config_file.txt"
    possible_formats = ['xlsx', 'csv', 'tsv', 'md']
    global FULL_PASSED
    try:
        db_comparator = db_compare.DB_comparator(config_file, show_log_in_console=False, log_tag="exporting_test", log_project="Testing")

        start_time = time.time()
        for data_format in possible_formats:
            db_comparator.export_data_frame("TEST_exporting." + data_format, data_format)
            os.remove("TEST_exporting." + data_format)
        end_time = time.time()

        final_time = (end_time - start_time)

        
        return "✅ Success", "N/A", round(final_time, 2)

    except Exception as e:
        for data_format in possible_formats:
            if os.path.exists("TEST_exporting." + data_format):
                os.remove("TEST_exporting." + data_format)
        
        FULL_PASSED = False
        return "❌ Failed", "N/A", "N/A"

def run_test(test_function, true_file_path, output_file_name):
    """Runs a test function, checks search success, file comparison, and measures execution time."""
    config_file = r"TMP_testing_folder/test_config_file.txt"
    global FULL_PASSED
    try:
        db_comparator = db_compare.DB_comparator(config_file, show_log_in_console=False, log_tag=test_function.__name__, log_project="Testing")

        # Measure search execution time
        start_time = time.time()
        test_function(db_comparator)
        end_time = time.time()
        elapsed_time = end_time - start_time

        search_status = "✅ Success"

        # Compare generated test file with true file
        true_file = pd.read_excel(true_file_path)
        test_file = pd.read_excel(output_file_name)

        # rename all colum to "test"
        true_file.columns = ["test"] * len(true_file.columns)
        test_file.columns = ["test"] * len(test_file.columns)
        comparison_status = "✅ Match" if true_file.equals(test_file) else "❌ Mismatch"

        if comparison_status == "❌ Mismatch":
            # If mismatch, print the rows that differ
            FULL_PASSED = False
            diff = pd.concat([true_file, test_file]).drop_duplicates(keep=False)
            print("Differences found:")
            print(diff)

        os.remove(output_file_name)
        clean_up_blast_files()

        return search_status, comparison_status, round(elapsed_time, 2)

    except Exception as e:
        if os.path.exists(output_file_name): os.remove(output_file_name)
        clean_up_blast_files()
        FULL_PASSED = False
        return "❌ Failed", "❌ Not compared", "N/A"

def exact_match_TEST(db_comparator: db_compare.DB_comparator):
    """Performs an exact match test."""
    db_comparator.exact_match.exact_match_search_in_all_databases(parallel=False)
    db_comparator.export_data_frame("TMP_testing_folder/exact_match_TEST_testing.xlsx", data_format="xlsx", control_cell_size=False)

def hamming_distances_TEST(db_comparator: db_compare.DB_comparator):
    """Performs a hamming distances test."""
    db_comparator.fast_hamming_distances.find_hamming_distances_for_all_databases(parallel=False)
    db_comparator.export_data_frame("TMP_testing_folder/hamming_distances_TEST_testing.xlsx", data_format="xlsx", control_cell_size=False)

def aligner_TEST(db_comparator: db_compare.DB_comparator):
    """Performs an aligner test."""
    db_comparator.aligner.aligner_search_in_all_databases(parallel=False)
    db_comparator.export_data_frame("TMP_testing_folder/aligner_TEST_testing.xlsx", data_format="xlsx", control_cell_size=False)

def blast_TEST(db_comparator: db_compare.DB_comparator):
    """Performs a BLAST test."""
    db_comparator.blast.blast_make_database()
    db_comparator.blast.blast_search_and_analyze_matches_in_database()
    db_comparator.export_data_frame("TMP_testing_folder/blast_TEST_testing.xlsx", data_format="xlsx", control_cell_size=False)

    clean_up_blast_files()

def generate_table_of_results():
    """Generates a table of test results, including search success, file comparison, and execution time."""
    results = [
        ["Test Name", "Status", "File Comparison", "Execution Time (s)"],
        ["Initialization Test", *test_initialization()],
        ["Exporting Test", *test_exporting()],
        ["Exact Match Test", *run_test(exact_match_TEST, "TMP_testing_folder/True_files/exact_match_TEST_true.xlsx", "TMP_testing_folder/exact_match_TEST_testing.xlsx")],
        ["Hamming Distances Test", *run_test(hamming_distances_TEST, "TMP_testing_folder/True_files/hamming_distances_TEST_true.xlsx", "TMP_testing_folder/hamming_distances_TEST_testing.xlsx")],
        ["Aligner Test", *run_test(aligner_TEST, "TMP_testing_folder/True_files/aligner_TEST_true.xlsx", "TMP_testing_folder/aligner_TEST_testing.xlsx")],
        ["BLAST Test", *run_test(blast_TEST, "TMP_testing_folder/True_files/blast_TEST_true.xlsx", "TMP_testing_folder/blast_TEST_testing.xlsx")]
    ]

    table = tabulate(results, headers="firstrow", tablefmt="fancy_grid", floatfmt=".2f")

    global FULL_PASSED
    return FULL_PASSED, table

def main():
    exit_code, table =  generate_table_of_results()
    if exit_code: return 0, table
    else: return 1, table

if __name__ == "__main__":
    exit_status, table = main()
    print(table)
    sys.exit(exit_status)