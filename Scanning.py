# Importing Libraries
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from Decoding import decode_from_scan  

def scanner():
    cam = cv2.VideoCapture(0)  
    print(" Scanner started!")

    # Set camera resolution and autofocus
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  
    cam.set(cv2.CAP_PROP_AUTOFOCUS, 1)  # Disable auto-focus (improves stability)

    scan_obj = False  # Flag to track barcode detection

    while True:
        success, frame = cam.read()
        if not success:
            print(" Failed to capture frame")
            break
        
        # Flip the frame horizontally for correct orientation
        frame = cv2.flip(frame, 1)

        # Convert to Grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply adaptive thresholding to enhance barcode visibility
        gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        # Decode from both color and enhanced grayscale images
        barcodes = decode(frame) + decode(gray)

        if barcodes:
            for barcode in barcodes:
                barcode_data = barcode.data.decode("utf-8")
                barcode_type = barcode.type
                x, y, w, h = barcode.rect

                # Draw rectangle around barcode
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f"{barcode_type}: {barcode_data}", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                print(f" Scanned: {barcode_data}")
                print("Press 'q' or 'Q' to decode, or scanning will close automatically.")

                # Set flag and break loop
                scan_obj = True
                break

        cv2.imshow("Barcode Scanner", frame)
        cv2.waitKey(1)

        key = cv2.waitKey(1) & 0xFF
        if scan_obj or key == ord('q') or key == ord('Q'):
            print(" Decoding process started...")
            cv2.destroyAllWindows()
            break

    # Release Resources
    cam.release()
    cv2.destroyAllWindows()

    if scan_obj:
        decode_from_scan(barcode_data)
        return decode_from_scan(barcode_data)  # Send barcode data for decoding
    else:
        print(" No barcode detected. Try again.")

# Run Scanner
# scanner()
