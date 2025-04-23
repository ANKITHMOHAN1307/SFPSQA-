# Scanning.py
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import json
from Decoding import decode_from_upload, decode_from_scan


def scanner():
    cam = cv2.VideoCapture(0)
    scanned_barcode = None

    try:
        while True:
            success, frame = cam.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY, 11, 2)

            barcodes = decode(frame) + decode(gray)

            if barcodes:
                barcode = barcodes[0]
                barcode_data = barcode.data.decode("utf-8")
                scanned_barcode = barcode_data
                break

            cv2.imshow("Barcode Scanner", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cam.release()
        cv2.destroyAllWindows()

    if scanned_barcode:
        return {"barcode": scanned_barcode}
    else:
        return {"Error": "No barcode detected"}

if __name__ == "__main__":
    result = scanner()
    print(json.dumps(result))
