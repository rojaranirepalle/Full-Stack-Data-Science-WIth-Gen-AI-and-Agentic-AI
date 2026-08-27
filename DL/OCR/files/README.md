# Document / Receipt Scanner & Text Extractor

A Python OCR pipeline that takes a photo of a receipt/document and:
1. Detects the document edges (even if tilted or on a cluttered background)
2. Warps it into a flat, top-down "scanned" view (perspective transform)
3. Cleans it up for OCR (denoise + adaptive threshold)
4. Extracts raw text with pytesseract
5. Parses out vendor, date, and total using regex heuristics
6. Saves the scanned image, processed image, raw text, and a fields JSON

## Requirements
```
pip install opencv-python pytesseract numpy
```
You also need the Tesseract OCR engine installed separately (not just the pip package):
- Ubuntu/Debian: `sudo apt install tesseract-ocr`
- Mac: `brew install tesseract`
- Windows: install from https://github.com/UB-Mannheim/tesseract/wiki

## Usage
```bash
python document_scanner.py test_receipt.jpg
python document_scanner.py your_photo.jpg --output-dir results/
python document_scanner.py your_photo.jpg --no-crop   # skip edge detection if the image is already flat
```

## Included test image
`test_receipt.jpg` is a synthetic receipt (tilted, on a table background, with
camera-like noise/blur) included so you can test the pipeline immediately
without needing your own photo. Try it first:
```bash
python document_scanner.py test_receipt.jpg
```

## Notes / things to extend
- `find_document_contour()` looks for the largest 4-sided contour — works well
  on receipts/documents with a clear edge against the background, but can fail
  on very low-contrast photos. Use `--no-crop` as a fallback.
- `extract_fields()` uses simple regex — good starting point, but real-world
  receipts vary a lot. Worth tuning patterns for the specific receipt formats
  you're testing against.
- Swap `pytesseract` for `easyocr` in `extract_text()` if you want to compare
  accuracy on messier/handwritten receipts (same idea as your earlier
  pytesseract vs. PyTorch OCR comparison).
