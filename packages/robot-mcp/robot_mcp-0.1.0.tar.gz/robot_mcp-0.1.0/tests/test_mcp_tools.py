import contextlib
import os
import tempfile

import pytest
import pytest_asyncio

from robot_mcp.server import (
    execute_sql,
    get_table_summary,
    find_template_files,
)
from tests import OUTPUT_DIR, copy_templates

ONTOLOGY_ID_COLUMN = '"ontology ID"'



@pytest_asyncio.fixture
async def templates(autouse=True, scope="function"):
    """Copy the template files to output directory."""
    output_template_dir = copy_templates()
    table_mappings = await find_template_files(OUTPUT_DIR)
    yield table_mappings

@pytest.mark.asyncio
async def test_find_templates(templates):
    table_mappings = await find_template_files(OUTPUT_DIR)
    assert table_mappings["assays"] == "obi-templates/assays.tsv"

@pytest.mark.asyncio
async def test_find_templates_integration(templates):
    summary = await get_table_summary(OUTPUT_DIR, templates)
    path = "/Users/cjm/repos/obi"
    table_mappings = await find_template_files(path)
    assert table_mappings["assays"] == "src/ontology/templates/assays.tsv"

    table_mappings = await find_template_files(path + "/src/ontology/templates")
    assert table_mappings["assays"] == "assays.tsv"
    

@pytest.mark.asyncio
async def test_table_summary(templates):
    summary = await get_table_summary(OUTPUT_DIR, templates)
    assert summary["assays"].columns[0].name == "ontology ID"
    assert summary["assays"].columns[0].owl_mapping == "ID"
    assert summary["assays"].columns[1].name == "label"
    assert summary["assays"].columns[1].owl_mapping == "A rdfs:label"
    assert summary["assays"].size == 1097
    assert summary["assays"].examples[0]["ontology ID"] == "CHMO:0000087"
    summary = await get_table_summary(str(OUTPUT_DIR), templates)
    assert summary["assays"].columns[0].name == "ontology ID"
    summary = await get_table_summary(str(OUTPUT_DIR / "obi-templates"), {"assays": "assays.tsv"})
    assert summary["assays"].columns[0].name == "ontology ID"
    summary = await get_table_summary(str(OUTPUT_DIR / "obi-templates"), {"foo": "assays.tsv"})
    assert summary["foo"].columns[0].name == "ontology ID"

@pytest.mark.asyncio
async def test_query(templates):
    """Test adding and removing axioms."""
    assay_loc = templates["assays"]
    print(f"assay_loc: {assay_loc}")
    assert assay_loc.endswith("assays.tsv")
    assert not assay_loc.startswith(str(OUTPUT_DIR))
    result = await execute_sql(f"SELECT label FROM assays WHERE {ONTOLOGY_ID_COLUMN} = 'CHMO:0000087' LIMIT 1", OUTPUT_DIR, templates)
    assert result == ['fluorescence microscopy assay']
    summary = await get_table_summary(OUTPUT_DIR, templates)
    assert summary["assays"].size == 1097


@pytest.mark.asyncio
async def test_query_rel_path(templates):
    """Test adding and removing axioms."""
    rel_dir = OUTPUT_DIR / "obi-templates"
    result = await execute_sql(f"SELECT label FROM assays WHERE {ONTOLOGY_ID_COLUMN} = 'CHMO:0000087' LIMIT 1", rel_dir, {'assays': 'assays.tsv'})
    # assert result == [('fluorescence microscopy assay', )]
    assert result == ['fluorescence microscopy assay']
    summary = await get_table_summary(rel_dir, {'assays': 'assays.tsv'})
    assert summary["assays"].size == 1097

@pytest.mark.asyncio
async def test_update(templates):
    """Test adding and removing axioms."""
    result = await execute_sql(f"UPDATE assays SET label = 'TEST VALUE' WHERE {ONTOLOGY_ID_COLUMN} = 'CHMO:0000087'", OUTPUT_DIR, templates)
    result = await execute_sql(f"SELECT label FROM assays WHERE {ONTOLOGY_ID_COLUMN} = 'CHMO:0000087' LIMIT 1", OUTPUT_DIR, templates)
    # assert result == [('TEST VALUE', )]
    assert result == ['TEST VALUE']

@pytest.mark.asyncio
async def test_delete_all(templates):
    """Test adding and removing axioms."""
    assay_loc = templates["assays"]
    summary = await get_table_summary(OUTPUT_DIR, templates)
    assert summary["assays"].size == 1097
    result = await execute_sql("DELETE FROM assays", OUTPUT_DIR, templates)
    summary = await get_table_summary(OUTPUT_DIR, templates)
    assert summary["assays"].size == 0

# test summary with no tables
@pytest.mark.asyncio
async def test_summary_no_tables(templates):
    """Test summary with no tables."""
    # we expect this to raise an error
    with pytest.raises(ValueError):
        await get_table_summary(OUTPUT_DIR / "non-existent-dir", {})

