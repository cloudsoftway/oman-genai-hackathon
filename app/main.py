import argparse
import os
from app.crew import HRCrew
from app.tools.pdf_reader import PDFReaderTool



def run():
    """
    Run the crew with a given CV path.
    """

    inputs = {"file_path":"PDFCVs/3.pdf",
              "txt_output_path": "preprocessed-CVs",
              "jd_file_path": "Jobs/jd-01.json",}
    print(inputs)
    try:
        results = HRCrew().crew().kickoff(inputs=inputs)
        return results
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    results = run()
    print("Crew run completed. Results:")

    print("\n\n\n\n====================\n")
    # print(f"\nCrew Results Object:\n{results}\n")
    print("\n====================\n")
    print(type(results))
    print("\n====================\n")
    # print(f"\nCrew Output:\n{results.raw}\n")
    print("\n====================\n")
    print(f"\nToken Usage:\n{results.token_usage}\n")