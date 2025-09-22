import time
import pytest
from pathlib import Path
from src.services.filesystem_service import FileSystemService

@pytest.fixture
def fs_service():
    return FileSystemService(allowed_paths=["/tmp"])

def test_directory_listing_performance(fs_service):
    """Test that directory listing completes in under 100ms"""
    # Create a test directory with some files
    test_dir = Path("/tmp/mcp_test_dir")
    test_dir.mkdir(exist_ok=True)
    for i in range(10):
        (test_dir / f"file_{i}.txt").write_text(f"content {i}")

    try:
        start_time = time.time()
        result = fs_service.list_directory(str(test_dir))
        end_time = time.time()

        duration = (end_time - start_time) * 1000  # ms
        assert duration < 100, f"Directory listing took {duration}ms, expected <100ms"
        assert len(result["items"]) == 10
    finally:
        # Cleanup
        for f in test_dir.iterdir():
            f.unlink()
        test_dir.rmdir()

def test_file_reading_performance(fs_service):
    """Test that file reading completes in under 1s for reasonable size"""
    test_file = Path("/tmp/mcp_test_file.txt")
    content = "test content\n" * 1000  # ~13KB
    test_file.write_text(content)

    try:
        start_time = time.time()
        result = fs_service.read_file(str(test_file))
        end_time = time.time()

        duration = end_time - start_time
        assert duration < 1.0, f"File reading took {duration}s, expected <1s"
        assert result["content"] == content
    finally:
        test_file.unlink()