# file2md

A web-based file converter that transforms various file formats into Markdown using the [Microsoft MarkItDown](https://github.com/microsoft/markitdown) library. This tool leverages the powerful MarkItDown library to provide accurate and reliable file conversions.

## Supported Formats

- PDF (.pdf)
- PowerPoint (.pptx)
- Word (.docx)
- Excel (.xlsx)
- Images (EXIF metadata, and OCR)
- Audio (EXIF metadata, and speech transcription)
- HTML (special handling of Wikipedia, etc.)
- Various other text-based formats (csv, json, xml, etc.)


## Running the Application

### Running with Docker

1. Run the container:
   ```bash
   docker run -p 5000:5000 maheshrijal/file2md
   ```

2. Open your browser and navigate to `http://localhost:5000`
