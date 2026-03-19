import os
import pandas as pd


def convert_to_csv(file_path: str, output_folder=None):
    """
    Converts Excel (.xlsx, .xls), CSV, TSV, TXT, and JSON files to CSV.
    Saves the converted CSV inside output_folder.

    Returns:
        csv_path: path of saved CSV file
        df: pandas DataFrame loaded from file
    """

    # Get the directory where this script is located
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # If no output folder specified, use 'processed' in the backend directory
    if output_folder is None:
        output_folder = os.path.join(BASE_DIR, "processed")
    elif output_folder == "processed":
        # If using the default "processed", make it absolute
        output_folder = os.path.join(BASE_DIR, "processed")

    base_name = os.path.basename(file_path)
    file_name, ext = os.path.splitext(base_name)
    ext = ext.lower()

    if ext in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path)
    elif ext == ".csv":
        df = pd.read_csv(file_path)
    elif ext in [".tsv", ".txt"]:
        try:
            df = pd.read_csv(file_path, delimiter="\t")
        except Exception:
            df = pd.read_csv(file_path)
    elif ext == ".json":
        df = pd.read_json(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

    os.makedirs(output_folder, exist_ok=True)

    csv_name = f"{file_name}_converted.csv"
    csv_path = os.path.join(output_folder, csv_name)

    df.to_csv(csv_path, index=False)

    print(f"✓ CSV saved to: {csv_path}")  # Debug print
    return csv_path, df
