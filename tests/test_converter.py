from pathlib import Path

from app import allowed_file
from utils.converter import convert_to_markdown


def test_convert_to_markdown_html_fixture():
    fixture_path = Path(__file__).parent / "fixtures" / "public" / "sample.html"

    output = convert_to_markdown(str(fixture_path))

    assert output.strip()
    assert "Hello from file2md" in output


def test_allowed_file_accepts_supported_extensions():
    assert allowed_file("sample.pdf")
    assert allowed_file("sample.html")
    assert not allowed_file("sample.exe")
