from __future__ import annotations

from pathlib import Path
from urllib.request import urlopen

POI_COMMIT = "6d42ff955ad13a79ebafdaaeffa5617880c00d3b"
POI_BASE = f"https://raw.githubusercontent.com/apache/poi/{POI_COMMIT}"

REMOTE_SAMPLES = {
    "hello-world-unsigned.docx": f"{POI_BASE}/test-data/xmldsign/hello-world-unsigned.docx",
    "hello-world-unsigned.pptx": f"{POI_BASE}/test-data/xmldsign/hello-world-unsigned.pptx",
    "hello-world-unsigned.xlsx": f"{POI_BASE}/test-data/xmldsign/hello-world-unsigned.xlsx",
    "quick.pdf": f"{POI_BASE}/test-data/hmef/quick-contents/quick.pdf",
    "ms-sample.docx": "https://media.githubusercontent.com/media/microsoft/SLG-Business-Applications/66a88ecd53f0e77a56c43705d0ab9ebc54be88bb/demos/administration/RecruIT%20Employee%20Hiring/RecruIT%20installation.docx",
}


def download_remote_samples(base_dir: Path) -> dict[str, Path]:
    base_dir.mkdir(parents=True, exist_ok=True)
    downloaded: dict[str, Path] = {}

    for filename, url in REMOTE_SAMPLES.items():
        destination = base_dir / filename
        if not destination.exists():
            with urlopen(url, timeout=30) as response:
                destination.write_bytes(response.read())
        downloaded[filename] = destination

    return downloaded
