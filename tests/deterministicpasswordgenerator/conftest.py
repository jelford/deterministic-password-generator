import pytest
import tempfile


@pytest.yield_fixture()
def tempdir():
    temp_dir = tempfile.TemporaryDirectory()
    yield temp_dir
    temp_dir.cleanup()
