from typing import Any
from pydantic import BaseModel, Field

class ColumnSummary(BaseModel):
    """
    A summary of a column in a table.
    """
    name: str = Field(..., description="The column header (may have spaces)")
    owl_mapping: str | None = Field(None, description="The ROBOT template mapping for the column")
    description: str | None = Field(None, description="A description of the column")

class TableSummary(BaseModel):
    """
    A summary of a table.
    """
    name: str
    columns: list[ColumnSummary] = Field(..., description="The columns in the table")
    description: str | None = Field(None, description="A description of the table")
    size: int | None = Field(None, description="The number of rows in the table")
    examples: list[dict[str, Any]] | None = Field(None, description="Example rows")
