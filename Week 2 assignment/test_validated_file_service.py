
import pytest

from validated_file_service import WorkspaceService


def test_valid_write_read_and_list(tmp_path):
    service = WorkspaceService(tmp_path)

    assert service.dispatch(
        "write_file",
        {"filepath": "note.txt", "content": "workspace content"},
    ).startswith("OK:")
    assert service.dispatch("read_file", {"filepath": "note.txt"}) == "workspace content"
    assert service.dispatch("list_files", {}) == "note.txt"


@pytest.mark.parametrize(
    "filename",
    ["", " ", ".", "..", "../secret.txt", "nested/file.txt", r"nested\file.txt", r"C:\x"],
)
def test_path_policy_rejects_non_filenames(tmp_path, filename):
    service = WorkspaceService(tmp_path)
    result = service.dispatch("read_file", {"filepath": filename})

    assert result.startswith("ERROR: invalid arguments")


def test_dispatch_returns_safe_unknown_and_filesystem_errors(tmp_path):
    service = WorkspaceService(tmp_path)

    assert service.dispatch("erase_file", {}).startswith("ERROR: unknown tool")
    assert service.dispatch("read_file", {"filepath": "missing.txt"}) == (
        "ERROR: filesystem failure: file not found in workspace."
    )
    assert service.dispatch("write_file", "not-an-object").startswith(
        "ERROR: invalid arguments"
    )
