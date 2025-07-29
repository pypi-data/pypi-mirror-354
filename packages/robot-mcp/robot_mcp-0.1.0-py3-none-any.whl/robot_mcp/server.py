
import os
from pathlib import Path
from typing import Any, Optional
import duckdb

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

from robot_mcp.models import TableSummary
import robot_mcp.robot_sql as robot_sql

# Initialize FastMCP server
mcp = FastMCP(
    "owl-server",
    instructions="""
The robot mcp server provides tools for working with robot templates.

These templates are managed as csv or tsv files on local disk. They
are ultimately compiled to OWL, but the job of this mcp server is
simply to help manage the contents of the templates.

The universal interface used here is SQL; any SQL query can be used to
either read or write to the templates.

For example, assume the user has a directory of robot templates:

   src/ontology/templates/
     processes.csv
     entities.csv


Where column headers follow normal ROBOT template idioms (e.g. "ontology ID", "label", followed by more
customized columns.

You can use the `find_template_files` tool to get a dictionary of table names to file paths:

    `find_template_files(".")`
    {'processes': 'src/ontology/templates/processes.csv', 'entities': 'src/ontology/templates/entities.csv'}

(Only call this if you have not already been provided this or have independently viewed the folder structure)

You will likely need to EITHER use absolute directory paths (you should concatenate the directory path with 
the file path) OR use the `set_working_directory` tool to set the working directory to the directory containing
the templates.

You can get metadata about the tables using the `get_table_summary` tool:

    `get_table_summary("src/ontology/templates/", {'processes': 'processes.csv', 'entities': 'entities.csv'})`

Note how we provide the folder path for convienence, and we always pass a mapping of safe table names to file paths.

You can always pass the full path in the dictionary, but if you do this, DO NOT include the folder path as the first
argument, just use `.`. Otherwise it will make a path `src/ontology/templates/src/ontology/templates/processes.csv`!

You can use the `execute_sql` tool to execute SQL queries on the tables:

    `execute_sql("SELECT * FROM processes LIMIT 10", "src/ontology/templates/", {'processes': 'processes.csv'})

Note how we only provide mappings for the tables we want to query.

You can also use the `execute_sql` tool to do standard SQL CRUD operations in response to user requests, for example:

    `execute_sql("UPDATE processes SET label = 'new label' WHERE ontology_id = 'MYONT:123'", "src/ontology/templates/", {'processes': 'processes.csv'})`

I assume you are familiar with robot templates, you can always check the online documentation for more information:

    https://robot.obolibrary.org/template/

However, a few key things bear repeating. Some columns are interpreted as OWL manchester syntax expressions; these
will have OWL mappings that start with a `C`. Always check this. You can look at the file directly (the OWL
mapping in a ROBOT template is always the 2nd row, i.e. the first after the header row). Or you can use the `get_table_summary` tool to get the summary of the table.

Note that single quotes are significant in manchester syntax expressions, as they are used to reference
the label of an existing term. You must include the single quotes in the expression, which may require some escaping
in your SQL query.

Some example:

 * `'part of' some 'brain'`
 * `'hippocampal neuron'`

Also note that the referenced ontology term must exist in the import closure of the ontology. For now,
importing new terms is out of scope. In general you should reuse the expressions that are already present
in the template, and ask the user if you need to reference new terms.

""",
)


@mcp.prompt()
def find_terms_with_matching_label_prompt(table: str, label_substring: str) -> str:
    """Generates a user message asking for rows with a matching label."""
    return (
        f"Find rows in the {table} table with a label containing the string '{label_substring}'"
    )

@mcp.tool()
async def set_working_directory(directory: str | Path) -> str:
    """
    Set the working directory.

    Args:
        directory: The directory to set as the working directory.

    This is preserved across tool calls, so you can use it to set the working directory for subsequent tool calls.
    If you set this, then you can use relative paths for the directory argument in other tools.

    If you set this to the directory containing the templates, then you can generally subsequently
    provide `.` as the directory argument and mappings like `{'processes': 'processes.csv'}`
    """
    if isinstance(directory, str):
        directory = Path(directory)
    if not directory.exists():
        raise ValueError(f"Directory {directory} does not exist")
    os.chdir(directory)
    return f"Working directory set to {directory}"

@mcp.tool()
async def execute_sql(sql: str, directory: str, table_mappings: dict[str, str]) -> list[Any] | None:
    """
    Execute a SQL query on a directory of CSV files.

    Args:
        sql: The SQL query to execute.
        directory: The directory containing the robot templates CSV/TSV files.
        table_mappings: A dictionary of safe table names to file paths (relative to the directory).
    """
    result = robot_sql.run_template_sql(sql, directory, table_mappings)
    def _normalize_row(row: Any) -> Any:
        if isinstance(row, tuple):
            if len(row) == 1:
                return str(row[0])
        return str(row)
    if isinstance(result, list):
        return [_normalize_row(row) for row in result]
    return result
    
@mcp.tool()
async def get_table_summary(directory: str, table_mappings: dict[str, str]) -> dict[str, TableSummary]:
    """
    Get a summary of the template files in a directory.

    Args:
        directory: The directory containing the robot templates CSV/TSV files.
        table_mappings: A dictionary of safe table names to file paths (relative to the directory).
    """
    try:
        summary = robot_sql.template_summary(directory, table_mappings)
        if not summary:
            raise ValueError(f"No tables found in directory {directory}; current working directory is {os.getcwd()}")
        return summary
    except Exception as e:
        raise ValueError(f"Error getting table summary: {e}; current working directory is {os.getcwd()}")

@mcp.tool()
async def find_template_files(directory: str) -> dict[str, str]:
    """
    Find the template files in a directory.

    Args:
        directory: The directory containing the robot templates CSV/TSV files.

    Returns:
    """
    try:
        tfiles = robot_sql.find_template_files(directory)
        if not tfiles:
            raise ValueError(f"No tables found in directory {directory}; current working directory is {os.getcwd()}")
        return tfiles
    except Exception as e:
        raise ValueError(f"Error finding template files: {e}; current working directory is {os.getcwd()}")

def main():
    """
    Run the MCP server.
    """
    mcp.run(transport="stdio")


if __name__ == "__main__":
    # Initialize and run the server
    main()
