import io

from app import app as flask_app


def test_convert_endpoint_with_html_file():
    flask_app.testing = True
    client = flask_app.test_client()

    data = {
        "file": (io.BytesIO(b"<!doctype html><html><body><h1>Hello</h1></body></html>"), "sample.html"),
    }

    response = client.post("/convert", data=data, content_type="multipart/form-data")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["success"] is True
    assert payload["markdown"].strip()


def test_convert_endpoint_rejects_unsupported_extension():
    flask_app.testing = True
    client = flask_app.test_client()

    data = {
        "file": (io.BytesIO(b"not really an exe"), "sample.exe"),
    }

    response = client.post("/convert", data=data, content_type="multipart/form-data")

    assert response.status_code == 400
