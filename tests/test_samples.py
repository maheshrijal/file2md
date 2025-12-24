import markitdown.converters._audio_converter as audio_converter

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
