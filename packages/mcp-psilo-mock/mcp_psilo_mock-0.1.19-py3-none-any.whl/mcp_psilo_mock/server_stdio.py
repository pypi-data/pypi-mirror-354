import json
from mcp.server.fastmcp import FastMCP
import pandas as pd
import asyncio
from importlib.resources import files

mcp = FastMCP("server_stdio MCP Demo")


def load_psilo_df() -> pd.DataFrame:
    csv_path = files("mcp_psilo_mock").joinpath("fake_psilo_data.csv")
    print(f"[DEBUG] Loading CSV from: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"[DEBUG] Loaded {len(df)} rows")
    return df


@mcp.tool()
def get_psilo_project_names() -> list[str]:
    """
    Retrieve a list of all unique project names present in the Psilo dataset.

    This function scans the 'Project' column of the Psilo CSV file and returns
    a deduplicated list of all distinct project names. These typically represent
    different experimental techniques or data sources (e.g., 'PDB', 'NMR', 'AlphaFold').

    Output:
        - List of strings: one for each unique project name.
    """
    try:
        df = load_psilo_df()
        projects = df["Project"].dropna().unique().tolist()
        print(f"[DEBUG] Found {len(projects)} unique projects")
        return projects
    except Exception as e:
        print(f"[ERROR] get_project_names failed: {e}")
        return [f"[ERROR] {e}"]


@mcp.tool()
def get_full_psilo_data() -> list[str]:
    """
    Retrieve the entire contents of the Psilo dataset.

    This function reads the full CSV and returns each row as a JSON-formatted string,
    containing the following fields:
        - pdb_id: The PDB identifier (e.g., 'Q7KT')
        - date: The date of entry or experiment (e.g., '12/16/97')
        - project: The associated project type (e.g., 'NMR', 'CryoEM')
        - title: A short description of the entry

    Output:
        - List of JSON strings, one per row in the dataset.
    """
    try:
        df = load_psilo_df()
        return [
            json.dumps(
                {
                    "pdb_id": row["PDB_ids"],
                    "date": row["Dates"],
                    "project": row["Project"],
                    "title": row["Title"],
                }
            )
            for _, row in df.iterrows()
        ]
    except Exception as e:
        print(f"[ERROR] get_full_psilo_data failed: {e}")
        return [json.dumps({"error": str(e)})]


@mcp.tool()
def get_psilo_data_filtered(project_name: str) -> list[str]:
    """
    Retrieve rows from the Psilo dataset that match a specific project name.

    Parameters:
        - project_name (str): The name of the project to filter by
                              (e.g., 'NMR', 'AlphaFold', 'CryoEM').

    This function filters the Psilo dataset by the 'Project' column and returns
    matching entries as JSON-formatted strings.

    Output:
        - List of JSON strings, each representing a matching row.
    """
    try:
        df = load_psilo_df()
        filtered = df[df["Project"] == project_name]
        print(f"[DEBUG] Filtered to {len(filtered)} rows for '{project_name}'")
        return [
            json.dumps(
                {
                    "pdb_id": row["PDB_ids"],
                    "date": row["Dates"],
                    "project": row["Project"],
                    "title": row["Title"],
                }
            )
            for _, row in filtered.iterrows()
        ]
    except Exception as e:
        print(f"[ERROR] get_psilo_data_filtered failed: {e}")
        return [json.dumps({"error": str(e)})]


@mcp.tool()
def psilo_data_description() -> str:
    """
    Provide a structural description of the Psilo dataset.

    This function introspects the CSV used for the Psilo data and returns:
        - Column names and their inferred data types
        - Number of rows in the dataset
        - A few sample entries

    Intended for LLMs and data agents to understand the dataset layout before querying.

    Output:
        - A JSON string describing the dataset structure, columns, types, and sample data.
    """
    try:
        df = load_psilo_df()
        column_info = df.dtypes.to_dict()
        sample_rows = df.head(3).to_dict(orient="records")
        description = {
            "columns": {col: str(dtype) for col, dtype in column_info.items()},
            "num_rows": len(df),
            "sample": sample_rows,
        }
        return json.dumps(description, indent=2)
    except Exception as e:
        print(f"[ERROR] psilo_data_description failed: {e}")
        return json.dumps({"error": str(e)})


def run_server():
    # print_registered_tools()
    # print("Starting MCP server...")
    mcp.run()


if __name__ == "__main__":
    mcp.run()

    # print(">>> Testing: get_project_names()")
    # projects = get_project_names()
    # print(json.dumps(projects, indent=2), "\n")

    # print(">>> Testing: get_full_psilo_data()")
    # full_data = get_full_psilo_data()
    # print(f"[INFO] Returned {len(full_data)} rows")

    # # Print every row as parsed JSON
    # for i, row in enumerate(full_data, 1):
    #     parsed = json.loads(row)
    #     print(f"\n--- Entry {i} ---")
    #     print(json.dumps(parsed, indent=2))
    # print()

    # print(">>> Testing: get_psilo_data_filtered('NMR')")
    # filtered = get_psilo_data_filtered("NMR")
    # print(f"[INFO] Returned {len(filtered)} rows for NMR")
    # for i, row in enumerate(filtered, 1):
    #     parsed = json.loads(row)
    #     print(f"\n--- Entry {i} ---")
    #     print(json.dumps(parsed, indent=2))
    # print()

    # print(">>> Testing: psilo_data_description()")
    # description = psilo_data_description()
    # print(description)
