# file2md
<div align="center">

![GitHub Tag](https://img.shields.io/github/v/tag/maheshrijal/file2md) 
![GitHub License](https://img.shields.io/github/license/maheshrijal/file2md) 
[![Docker CI](https://github.com/maheshrijal/file2md/actions/workflows/docker-image.yml/badge.svg?branch=main)](https://github.com/maheshrijal/file2md/actions/workflows/docker-image.yml)

</div>

A [web-based](https://file2md.maheshrijal.com) file converter that transforms various file formats into Markdown using the [Microsoft MarkItDown](https://github.com/microsoft/markitdown) library. This tool leverages the powerful MarkItDown library to provide accurate and reliable file conversions.

## Supported Formats

- PDF (.pdf)
- PowerPoint (.pptx)
- Word (.docx)
- Excel (.xlsx)
- HTML (special handling of Wikipedia, etc.)
- Various other text-based formats (csv, json, xml, etc.)


## Running the Application

```bash
docker run -p 5000:5000 maheshrijal/file2md
```

or

```bash
docker run -p 5000:5000 ghcr.io/maheshrijal/file2md
```

## Access the Application

Open your browser and go to:

```
http://localhost:5000
```
