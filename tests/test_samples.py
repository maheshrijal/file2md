import os
import markitdown.converters._audio_converter as audio_converter
import pytest

from tests.remote_samples import download_remote_samples
from tests.sample_files import create_sample_files
from utils.converter import convert_to_markdown


def test_convert_all_sample_files(tmp_path, monkeypatch):
    monkeypatch.setattr(
        audio_converter,
        "transcribe_audio",
        lambda *args, **kwargs: "Test transcript",
    )

    sample_files = create_sample_files(tmp_path)

    expectations = {
        ".html": "Hello HTML",
        ".csv": "Hello CSV",
        ".json": "Hello JSON",
        ".xml": "Hello XML",
        ".pdf": "Hello PDF",
        ".docx": "Hello DOCX",
        ".pptx": "Hello PPTX",
        ".xlsx": "Hello XLSX",
    }

    for extension, path in sample_files.items():
        output = convert_to_markdown(str(path))
        assert isinstance(output, str)

        expected_text = expectations.get(extension)
        if expected_text:
            assert expected_text in output

        if extension in {".wav", ".mp3"}:
            assert "Audio Transcript" in output


def test_convert_remote_samples(tmp_path, monkeypatch):
    if os.getenv("FILE2MD_REMOTE_SAMPLES") != "1":
        pytest.skip("Remote samples not enabled")

    monkeypatch.setattr(
        audio_converter,
        "transcribe_audio",
        lambda *args, **kwargs: "Test transcript",
    )

    remote_dir = tmp_path / "remote"
    remote_samples = download_remote_samples(remote_dir)

    for name, path in remote_samples.items():
        if path.suffix == ".doc":
            try:
                output = convert_to_markdown(str(path))
            except Exception:
                pytest.xfail("MarkItDown docs list docx support; .doc is best-effort.")
            assert isinstance(output, str)
            continue

        output = convert_to_markdown(str(path))
        assert isinstance(output, str)
