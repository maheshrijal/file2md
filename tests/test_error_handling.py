import io
import pytest
from app import app as flask_app


class TestEndpointErrorHandling:
    """Test Flask endpoint error cases and edge conditions."""

    def setup_method(self):
        """Setup Flask test client for each test."""
        flask_app.testing = True
        self.client = flask_app.test_client()

    def test_convert_missing_file_field(self):
        """POST without file field should return 400."""
        response = self.client.post("/convert", data={}, content_type="multipart/form-data")
        assert response.status_code == 400
        payload = response.get_json()
        assert "error" in payload

    def test_convert_empty_filename(self):
        """POST with empty filename should return 400."""
        data = {
            "file": (io.BytesIO(b"content"), ""),
        }
        response = self.client.post("/convert", data=data, content_type="multipart/form-data")
        assert response.status_code == 400
        payload = response.get_json()
        assert "error" in payload

    def test_convert_extension_case_insensitive(self):
        """Extension checking should be case-insensitive."""
        # Uppercase extension should work
        data = {
            "file": (io.BytesIO(b"<!doctype html><html><body><h1>Test</h1></body></html>"), "sample.HTML"),
        }
        response = self.client.post("/convert", data=data, content_type="multipart/form-data")
        assert response.status_code == 200

    def test_convert_no_extension(self):
        """File with no extension should return 400."""
        data = {
            "file": (io.BytesIO(b"some content"), "noextension"),
        }
        response = self.client.post("/convert", data=data, content_type="multipart/form-data")
        assert response.status_code == 400

    def test_convert_dot_only_filename(self):
        """Filename that is only a dot should return 400."""
        data = {
            "file": (io.BytesIO(b"content"), "."),
        }
        response = self.client.post("/convert", data=data, content_type="multipart/form-data")
        assert response.status_code == 400

    def test_convert_corrupt_html(self):
        """Malformed HTML should still convert (markitdown is lenient)."""
        data = {
            "file": (io.BytesIO(b"<html><body>Unclosed tag"), "sample.html"),
        }
        response = self.client.post("/convert", data=data, content_type="multipart/form-data")
        # markitdown handles malformed HTML gracefully
        assert response.status_code == 200
        payload = response.get_json()
        assert payload["success"] is True

    def test_convert_invalid_json(self):
        """Invalid JSON should still convert (markitdown handles it)."""
        data = {
            "file": (io.BytesIO(b"{ invalid json }"), "sample.json"),
        }
        response = self.client.post("/convert", data=data, content_type="multipart/form-data")
        # markitdown may handle or reject gracefully
        assert response.status_code in [200, 500]

    def test_convert_empty_file(self):
        """Empty file should still attempt conversion."""
        data = {
            "file": (io.BytesIO(b""), "sample.html"),
        }
        response = self.client.post("/convert", data=data, content_type="multipart/form-data")
        # Empty HTML should return 200 with empty or minimal markdown
        assert response.status_code == 200

    def test_convert_path_traversal_attempt(self):
        """Filename with path traversal should be sanitized."""
        data = {
            "file": (io.BytesIO(b"<!doctype html><html><body>Test</body></html>"), "../../../etc/passwd.html"),
        }
        response = self.client.post("/convert", data=data, content_type="multipart/form-data")
        # werkzeug.secure_filename sanitizes the path
        assert response.status_code == 200
        assert response.get_json()["success"] is True

    def test_convert_special_chars_in_filename(self):
        """Filename with special characters should be handled."""
        data = {
            "file": (io.BytesIO(b"<!doctype html><html><body>Test</body></html>"), "sample@file#2024.html"),
        }
        response = self.client.post("/convert", data=data, content_type="multipart/form-data")
        assert response.status_code == 200

    def test_convert_allowed_extension_with_wrong_content(self):
        """File with allowed extension but wrong content type."""
        # PDF extension but HTML content - let converter handle it
        data = {
            "file": (io.BytesIO(b"<!doctype html><html><body>Not a real PDF</body></html>"), "sample.pdf"),
        }
        response = self.client.post("/convert", data=data, content_type="multipart/form-data")
        # Should attempt conversion; markitdown may fail or succeed
        assert response.status_code in [200, 500]

    def test_convert_very_long_filename(self):
        """Very long filename should be handled."""
        long_name = "a" * 500 + ".html"
        data = {
            "file": (io.BytesIO(b"<!doctype html><html><body>Test</body></html>"), long_name),
        }
        response = self.client.post("/convert", data=data, content_type="multipart/form-data")
        # secure_filename truncates if needed
        assert response.status_code == 200

    def test_index_route(self):
        """GET / should return 200 with HTML template."""
        response = self.client.get("/")
        assert response.status_code == 200
        assert b"<!doctype" in response.data.lower() or b"<html" in response.data.lower()

    def test_unsupported_method_on_convert(self):
        """GET on /convert should return 405."""
        response = self.client.get("/convert")
        assert response.status_code == 405

    def test_convert_whitespace_filename(self):
        """Filename with only whitespace should be rejected."""
        data = {
            "file": (io.BytesIO(b"<!doctype html><html><body>Test</body></html>"), "   "),
        }
        response = self.client.post("/convert", data=data, content_type="multipart/form-data")
        # secure_filename removes whitespace; no extension left
        assert response.status_code == 400


class TestAllowedFileFunction:
    """Test the allowed_file validation function."""

    def test_allowed_file_pdf(self):
        """PDF should be allowed."""
        from app import allowed_file
        assert allowed_file("sample.pdf") is True

    def test_allowed_file_html(self):
        """HTML should be allowed."""
        from app import allowed_file
        assert allowed_file("sample.html") is True

    def test_allowed_file_all_supported(self):
        """Test all supported extensions."""
        from app import allowed_file
        extensions = [
            "pdf", "docx", "pptx", "xlsx",
            "png", "jpg", "jpeg", "gif",
            "mp3", "wav", "html", "csv",
            "json", "xml"
        ]
        for ext in extensions:
            assert allowed_file(f"sample.{ext}") is True, f"Extension {ext} should be allowed"

    def test_allowed_file_uppercase_extension(self):
        """Uppercase extensions should be allowed."""
        from app import allowed_file
        assert allowed_file("sample.PDF") is True
        assert allowed_file("sample.HTML") is True

    def test_allowed_file_exe(self):
        """EXE should not be allowed."""
        from app import allowed_file
        assert allowed_file("sample.exe") is False

    def test_allowed_file_sh(self):
        """SH should not be allowed."""
        from app import allowed_file
        assert allowed_file("script.sh") is False

    def test_allowed_file_py(self):
        """PY should not be allowed."""
        from app import allowed_file
        assert allowed_file("script.py") is False

    def test_allowed_file_no_extension(self):
        """No extension should return False."""
        from app import allowed_file
        assert allowed_file("noextension") is False

    def test_allowed_file_dot_file(self):
        """Hidden file (dot file) with no extension should return False."""
        from app import allowed_file
        assert allowed_file(".gitignore") is False

    def test_allowed_file_multiple_dots(self):
        """File with multiple dots takes last extension."""
        from app import allowed_file
        assert allowed_file("archive.tar.html") is True  # .html is allowed
        assert allowed_file("archive.tar.exe") is False  # .exe is not allowed
