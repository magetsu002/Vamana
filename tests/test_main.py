import pytest
from pathlib import Path
from engine.security import resolve_safe_path
from engine.validation import validate_workflow, validate_step

# 1. Test Path Security (resolve_safe_path)
def test_resolve_safe_path():
    # Test valid filename
    assert resolve_safe_path("test.txt") == Path("workspace/test.txt").resolve()

    # Test that absolute paths raise a ValueError
    with pytest.raises(ValueError):
        resolve_safe_path("/etc/passwd")

    # Test that path traversal (..) raises a ValueError
    with pytest.raises(ValueError):
        resolve_safe_path("../secret.txt")

# 2. Test Workflow Structure (validate_workflow)
def test_validate_workflow():
    # Test valid workflow
    valid_data = {"name": "Test", "steps": []}
    assert validate_workflow(valid_data) is None # No exception means the workflow is valid

    # Test missing 'name'
    with pytest.raises(ValueError):
        validate_workflow({"steps": []})

    # Test invalid 'steps' type
    with pytest.raises(ValueError):
        validate_workflow({"name": "Test", "steps": "not a list"})

# 3. Test Individual Step Logic (validate_step)
def test_validate_step():
    # Test valid print step
    valid_step = {"type": "print", "message": "Hello"}
    assert validate_step(valid_step) is None

    # Test missing required field (filename for write_file)
    invalid_step = {"type": "write_file", "content": "test"}
    with pytest.raises(ValueError):
        validate_step(invalid_step)

    # Test unsupported step type
    with pytest.raises(ValueError):
        validate_step({"type": "hack_mainframe"})
