# 📦 Day 41: QR Code Generator

This is a simple and powerful Python script that allows you to generate QR codes from any text or URL — with an optional feature to overlay a custom logo at the center of the QR.

## 🚀 Features

- Generate a QR code from any text, URL, or string.
- Save it as a PNG image.
- Optional: Add your own logo image to the center of the QR code.
- High error correction level for logo overlay support.

## 🛠️ How It Works

1. The user inputs the text or URL they want to encode.
2. Optionally, they can specify a path to a logo (must be a `.png` file).
3. The script generates and saves the QR code image to disk.

## 🖼️ Example

- **Input:** `https://openai.com`
- **Output:** A `qr_code.png` file saved locally with or without a logo.

## 💻 Requirements

- `qrcode`
- `Pillow`

Install the dependencies using:

```bash
pip install qrcode[pil] pillow
````

## ▶️ Usage

Run the script:

```bash
python qr_code_generator.py
```

You’ll be prompted to:

* Enter the text or URL
* Choose an output filename
* Decide whether to include a logo (and specify its path)

## 📂 File Structure

```
qr_code_generator.py       # Main script
temp_qr_code.png           # Temporary file (auto-deleted if logo is used)
output.png                 # Final QR code output
```

## 📌 Notes

* For best results, use a square transparent PNG logo.
* Ensure the logo image file exists and is accessible.

---

> Part of my **100 Days of Python + AI** Challenge 🚀

```
