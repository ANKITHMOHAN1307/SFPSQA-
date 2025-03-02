# Import Libraries
import cv2
import tkinter as tk
from tkinter import filedialog
from Decoding import decode_from_upload
from pyzbar.pyzbar import decode
import numpy as np

# Function to Upload and Process an Image
def upload_image():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Select the Image File
    file_path = filedialog.askopenfilename(
        title="Select an image with a barcode/QR code",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    scan_obj = False
    if not file_path:
        print("No image selected.")
        return

    print(f"Selected file: {file_path}")

    # Load Image with OpenCV
    image = cv2.imread(file_path)

    if image is None:
        print("Error: Could not read the image. Please check the file format.")
        return

    # Preprocessing for Better Detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Reduce noise
    _, thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)  # Enhance contrast

    # Decode barcode/QR code
    barcodes = decode(thresh)  + decode(gray) + decode(blurred)

    if not barcodes:
        print("No barcode found in the image.")
        return

    # Process detected barcodes
    for barcode in barcodes:
        barcode_data = barcode.data.decode("utf-8")  # Decode barcode data
        barcodeType = barcode.type  # Get barcode type
        x, y, w, h = barcode.rect  # Get bounding box

        # Draw rectangle and text on image
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, f"{barcodeType}: {barcode_data}", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        #print(f"Decoded Data: {barcodeData}, Type: {barcodeType}")
        scan_obj = True
    # Show the uploaded image with barcode details
    # cv2.imshow("Scanned Image", image)
    # cv2.waitKey(0)  # Wait indefinitely until a key is pressed
    cv2.destroyAllWindows()  # Close all windows
     
    if scan_obj:
        decode_from_upload(barcode_data)
        return decode_from_upload(barcode_data)  # Send barcode data for decoding
    else:
        print(" No barcode detected. Try again.")



# Run the function
# upload_image()
