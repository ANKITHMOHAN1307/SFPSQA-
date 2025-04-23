# Upload.py
import cv2
import tkinter as tk
from tkinter import filedialog
from pyzbar.pyzbar import decode
import json
# from Decoding import decode_from_upload, decode_from_scan

def upload_image():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select an image with a barcode/QR code",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )

    if not file_path:
        return {"Error": "No image selected"}

    image = cv2.imread(file_path)
    if image is None:
        return {"Error": "Could not read image"}

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)

    barcodes = decode(thresh) + decode(gray) + decode(blurred)

    if not barcodes:
        return {"Error": "No barcode found"}

    barcode_data = barcodes[0].data.decode("utf-8")
    return {"barcode": barcode_data}

if __name__ == "__main__":
    import json
    result = upload_image()
    print(json.dumps(result))
