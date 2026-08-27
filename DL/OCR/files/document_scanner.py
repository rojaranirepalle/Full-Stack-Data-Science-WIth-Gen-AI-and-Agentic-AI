"""
Document / Receipt Scanner & Text Extractor
--------------------------------------------
Pipeline:
  1. Load image
  2. Detect the document/receipt boundary (edge detection + contour finding)
  3. Apply a perspective transform to get a flat, top-down "scanned" view
  4. Preprocess for OCR (grayscale, adaptive threshold, denoise)
  5. Run OCR (pytesseract) to extract raw text
  6. Parse common receipt fields (date, total, vendor) with regex
  7. Save the scanned image + extracted text + structured JSON

Usage:
    python document_scanner.py path/to/image.jpg
    python document_scanner.py path/to/image.jpg --output-dir results/
    python document_scanner.py path/to/image.jpg --no-crop   # skip document-edge detection
"""

import argparse
import json
import re
import sys
from pathlib import Path

import cv2
import numpy as np
import pytesseract


# --------------------------------------------------------------------------
# 1. Document boundary detection + perspective transform
# --------------------------------------------------------------------------

def order_points(pts: np.ndarray) -> np.ndarray:
    """Order 4 points as: top-left, top-right, bottom-right, bottom-left."""
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]      # top-left has smallest sum
    rect[2] = pts[np.argmax(s)]      # bottom-right has largest sum
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]   # top-right has smallest difference
    rect[3] = pts[np.argmax(diff)]   # bottom-left has largest difference
    return rect


def four_point_transform(image: np.ndarray, pts: np.ndarray) -> np.ndarray:
    """Warp the quadrilateral region defined by pts into a flat rectangle."""
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    width_a = np.linalg.norm(br - bl)
    width_b = np.linalg.norm(tr - tl)
    max_width = max(int(width_a), int(width_b))

    height_a = np.linalg.norm(tr - br)
    height_b = np.linalg.norm(tl - bl)
    max_height = max(int(height_a), int(height_b))

    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]
    ], dtype="float32")

    matrix = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, matrix, (max_width, max_height))
    return warped


def find_document_contour(image: np.ndarray):
    """
    Find the largest 4-point contour in the image, assumed to be the
    document/receipt edge. Returns None if no good quadrilateral is found.
    """
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    resized = cv2.resize(image, (int(image.shape[1] / ratio), 500))

    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)

    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            return approx.reshape(4, 2) * ratio

    return None


def scan_to_flat_image(image: np.ndarray, allow_crop: bool = True) -> np.ndarray:
    """Return a flattened top-down view of the document if found, else the original."""
    if allow_crop:
        contour = find_document_contour(image)
        if contour is not None:
            return four_point_transform(image, contour)
    return image


# --------------------------------------------------------------------------
# 2. Preprocessing for OCR
# --------------------------------------------------------------------------

def preprocess_for_ocr(image: np.ndarray) -> np.ndarray:
    """Grayscale + denoise + adaptive threshold to make text crisp for OCR."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)  # denoise while keeping edges sharp
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=31,
        C=15
    )
    return thresh


# --------------------------------------------------------------------------
# 3. OCR + field extraction
# --------------------------------------------------------------------------

def extract_text(preprocessed_image: np.ndarray) -> str:
    config = "--oem 3 --psm 6"  # assume a uniform block of text
    return pytesseract.image_to_string(preprocessed_image, config=config)


DATE_PATTERN = re.compile(
    r"\b(\d{1,2}[/\-.]\d{1,2}[/\-.]\d{2,4}|\d{4}[/\-.]\d{1,2}[/\-.]\d{1,2})\b"
)
TOTAL_PATTERN = re.compile(
    r"(?<!sub)(?:total|amount due|grand total|balance due)\s*[:\-]?\s*\$?\s*([\d,]+\.\d{2})",
    re.IGNORECASE
)
GENERIC_MONEY_PATTERN = re.compile(r"\$?\s?(\d+[.,]\d{2})\b")


def extract_fields(text: str) -> dict:
    """Pull out common receipt fields using regex heuristics."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    date_match = DATE_PATTERN.search(text)
    total_match = TOTAL_PATTERN.search(text)

    total_value = None
    if total_match:
        total_value = total_match.group(1)
    else:
        # fallback: take the largest money-looking value found anywhere
        amounts = GENERIC_MONEY_PATTERN.findall(text)
        if amounts:
            try:
                total_value = max(amounts, key=lambda a: float(a.replace(",", "")))
            except ValueError:
                total_value = None

    vendor_guess = lines[0] if lines else None  # top line is usually the store name

    return {
        "vendor_guess": vendor_guess,
        "date": date_match.group(0) if date_match else None,
        "total": total_value,
        "line_count": len(lines),
    }


# --------------------------------------------------------------------------
# 4. Orchestration
# --------------------------------------------------------------------------

def scan_document(image_path: str, output_dir: str = "output", allow_crop: bool = True) -> dict:
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"No such file: {image_path}")

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Could not read image: {image_path}")

    flat = scan_to_flat_image(image, allow_crop=allow_crop)
    processed = preprocess_for_ocr(flat)

    raw_text = extract_text(processed)
    fields = extract_fields(raw_text)

    scanned_path = out_dir / f"{image_path.stem}_scanned.png"
    processed_path = out_dir / f"{image_path.stem}_processed.png"
    text_path = out_dir / f"{image_path.stem}_text.txt"
    json_path = out_dir / f"{image_path.stem}_fields.json"

    cv2.imwrite(str(scanned_path), flat)
    cv2.imwrite(str(processed_path), processed)
    text_path.write_text(raw_text, encoding="utf-8")
    json_path.write_text(json.dumps(fields, indent=2), encoding="utf-8")

    result = {
        "source_image": str(image_path),
        "scanned_image": str(scanned_path),
        "processed_image": str(processed_path),
        "text_file": str(text_path),
        "fields_file": str(json_path),
        "raw_text": raw_text,
        "fields": fields,
    }
    return result


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Document/Receipt Scanner & Text Extractor")
    parser.add_argument("image", help="Path to the input image (photo of a receipt/document)")
    parser.add_argument("--output-dir", default="output", help="Directory to save results")
    parser.add_argument("--no-crop", action="store_true", help="Skip document edge detection/cropping")
    args = parser.parse_args()

    result = scan_document(args.image, output_dir=args.output_dir, allow_crop=not args.no_crop)

    print("\n--- Extracted Text ---")
    print(result["raw_text"])
    print("--- Structured Fields ---")
    print(json.dumps(result["fields"], indent=2))
    print(f"\nSaved scanned image:   {result['scanned_image']}")
    print(f"Saved processed image: {result['processed_image']}")
    print(f"Saved raw text:        {result['text_file']}")
    print(f"Saved fields JSON:     {result['fields_file']}")


if __name__ == "__main__":
    main()
