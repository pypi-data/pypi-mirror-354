from pathlib import Path
import re
from typing import Any
import duckdb

from robot_mcp.models import ColumnSummary, TableSummary

def safe_table_name(name: str) -> str:
    """
    Make a table name safe for DuckDB.
    """
    # replace all non-alphanumeric characters with an underscore
    return re.sub(r'[^a-zA-Z0-9]', '_', name)

def map_files_to_tables(directory: str | Path, table_mappings: dict[str, str]) -> duckdb.DuckDBPyConnection:
    """
    Map files to tables in a DuckDB connection.

    Args:
        directory: The directory containing the CSV files.
        table_mappings: A dictionary of table names and file paths.

    Returns:
        A DuckDB connection with the tables mapped to the files.

    Example:

        >>> conn = map_files_to_tables("tests/input/obi-templates", {"assays": "assays.tsv"})
        >>> conn.sql("SELECT * FROM assays LIMIT 1").fetchall()[0][:2]
        ('CHMO:0000087', 'fluorescence microscopy assay')
        >>> conn.sql("SELECT * FROM assays__meta LIMIT 1").fetchall()[0][:2]
        ('ID', 'A rdfs:label')

    """
    conn = duckdb.connect(":memory:")
    for table, file in table_mappings.items():
        table = safe_table_name(table)
        full_path = Path(directory) / file
        rel = duckdb.read_csv(full_path)
        # insert the rel into the conn
        id_col = rel.columns[0]
        id_col_name = f'"{id_col}"'
        conn.sql(f"CREATE TABLE {table} AS SELECT * FROM '{full_path}' WHERE {id_col_name} != 'ID'")
        conn.sql(f"CREATE TABLE {table}__meta AS SELECT * FROM '{full_path}' WHERE {id_col_name} = 'ID'")
    return conn

def run_template_sql(sql: str, directory: str | Path, table_mappings: dict[str, str]) -> list[Any] | None:
    """
    Execute a SQL query on a directory of CSV files.

    Args:
        sql: The SQL query to execute.
        directory: The directory containing the CSV files.
        table_mappings: A dictionary of table names and file paths.

    Returns:
        The result of the SQL query.

    Example:

        >>> import shutil
        >>> import os
        >>> os.makedirs("tests/output/obi-templates", exist_ok=True)
        >>> shutil.copy("tests/input/obi-templates/assays.tsv", "tests/output/obi-templates/assays.tsv")
        'tests/output/obi-templates/assays.tsv'

        >>> directory = "tests/output/obi-templates"
        
        >>> run_template_sql("SELECT count(*) FROM assays", directory, {"assays": "assays.tsv"})
        [(1097,)]

        >>> def dquote(*s):
        ...     return ", ".join(f'"{v}"' for v in s)

        >>> sql = f"INSERT INTO assays ({dquote('ontology ID', 'label')}) VALUES('a', 'b')"
        >>> print(sql)
        INSERT INTO assays ("ontology ID", "label") VALUES('a', 'b')
        >>> run_template_sql(sql, directory, {"assays": "assays.tsv"})
        >>> run_template_sql("SELECT count(*) FROM assays", directory, {"assays": "assays.tsv"})
        [(1098,)]
        >>> # compare the files at ascii level
        >>> with open(f"{directory}/assays.tsv", "r") as f1, open("tests/input/obi-templates/assays.tsv", "r") as f2:
        ...     assert f1.read() != f2.read()
        >>> run_template_sql("UPDATE assays SET label = 'c' WHERE label = 'b'", directory, {"assays": "assays.tsv"})
        >>> run_template_sql("SELECT count(*) FROM assays WHERE label='c'", directory, {"assays": "assays.tsv"})
        [(1,)]
        >>> run_template_sql("DELETE FROM assays WHERE label = 'c'", directory, {"assays": "assays.tsv"})
        >>> # no effect
        >>> run_template_sql("DELETE FROM assays WHERE label = 'b'", directory, {"assays": "assays.tsv"})
        >>> # compare the files at ascii level
        >>> with open(f"{directory}/assays.tsv", "r") as f1, open("tests/input/obi-templates/assays.tsv", "r") as f2:
        ...     assert f1.read() == f2.read()
        
        
    """
    conn = map_files_to_tables(directory, table_mappings)
    result = conn.sql(sql)
    # check if it a select query
    if sql.strip().lower().startswith("select"):
        return result.fetchall()
    # save the result back to the file
    for table, file in table_mappings.items():
        format = "csv"
        sep = ","
        if file.endswith(".tsv"):
            sep = "\t"
        full_path = Path(directory) / file
        # sort the table by the id column, and insert the meta data at the top;
        # needs to be done as a single query (UNION)
        conn.sql(f"COPY (SELECT * FROM {table}__meta UNION ALL SELECT * FROM {table}) TO '{full_path}' WITH (FORMAT '{format}', HEADER true, SEPARATOR '{sep}', QUOTE '')")
    return result

def template_summary(directory: str | Path, table_mappings: dict[str, str]) -> dict[str, TableSummary]:
    """
    Get a summary of the template files in a directory.

    Args:
        directory: The directory containing the template files.
        table_mappings: A dictionary of table names and file paths.

    Returns:
        A dictionary of table summaries, with the key being the table name and the value being the table summary.

    Example:    

        >>> dir = "tests/input/obi-templates"
        >>> tmap = find_template_files(dir)
        >>> summary = template_summary(dir, tmap)
        >>> assays = summary["assays"]
        >>> assert isinstance(assays, TableSummary)
        >>> assays.name
        'assays'
        >>> assays.size
        1097
        >>> col0 = assays.columns[0]
        >>> col0
        ColumnSummary(name='ontology ID', owl_mapping='ID', description=None)

    """
    conn = map_files_to_tables(directory, table_mappings)

    def _select_as_dict(sql: str) -> list[dict[str, Any]]:
        """
        Select a query as a dictionary.
        """
        result = conn.sql(sql)
        columns = result.columns
        rows = result.fetchall()
        return [dict(zip(columns, row)) for row in rows]

    result = {}
    for table, _file in table_mappings.items():
        # get the column names
        column_names = conn.sql(f"SELECT * FROM {table} LIMIT 1").columns
        # get the column descriptions
        column_owl_mappings = _select_as_dict(f"SELECT * FROM {table}__meta")[0]
        # get the column examples
        table_examples = _select_as_dict(f"SELECT * FROM {table} LIMIT 5")
        # get the table description
        result[table] = TableSummary(
            name=table,
            columns=[ColumnSummary(name=name, owl_mapping=owl_mapping, description=None) for name, owl_mapping in column_owl_mappings.items()],
            description=None,
            size=conn.sql(f"SELECT COUNT(*) FROM {table}").fetchone()[0],
            examples=table_examples
        )
    return result
        
def find_template_files(directory: str | Path | None = None) -> dict[str, str]:
    """
    Find all the template files in a directory.

    Args:
        directory: The directory to search for template files.

    Returns:
        A dictionary of template files, with the key being the table name and the value being the file path.

    Example:

        >>> tmap = find_template_files("tests/input/obi-templates")
        >>> tmap["assays"]
        'assays.tsv'
        >>> tmap = find_template_files("tests/input")
        >>> tmap["assays"]
        'obi-templates/assays.tsv'
    """
    if directory is None:
        # use current directory
        directory = Path.cwd()
    # tsv or csv files - TODO make this recursive:
    tsvs = Path(directory).glob("**/*.tsv")
    csvs = Path(directory).glob("**/*.csv")
    result = {}
    for file in set(tsvs) | set(csvs):
        # if it is a template file, 2nd row should start with 'ID'
        try:
            with open(file, "r") as f:
                lines = f.readlines()
                if len(lines) > 1 and lines[1].startswith("ID"):
                    relative_path = file.relative_to(directory)
                    result[safe_table_name(file.stem)] = str(relative_path)
        except Exception as e:
            # normally it's bad to pass over exceptions, but things like file permissions
            # or sym links could cause issues
            print(f"Error reading file {file}: {e}")
            continue
    return result