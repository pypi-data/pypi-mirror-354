# urllink

`urllink` is a simple Python library that allows you to shorten URLs and generate QR codes using online APIs.

## Installation

```bash
pip install urllink

## Example Usage

--------------------------------------------------------------
from urllink import shorten_url, generate_qrcode

# Shorten a URL
short_url = shorten_url("https://example.com")
print("Shortened URL:", short_url)

# Generate a QR code
qr_path = generate_qrcode("https://example.com", save_path="output/qrcode.png", size=300)
print("QR Code saved to:", qr_path)
--------------------------------------------------------------

Generates a QR code from the provided text or URL.
Function Reference
Parameters:

data (str, required): The content to encode into the QR code.

save_path (str, optional): Full path (including filename) to save the image.
Default: "qrcode.png" saved in the current directory.

size (int, optional): The size of the QR code image in pixels.
Default: 500

Returns:

The file path where the QR code image was saved.

An error message string if generation fails.

