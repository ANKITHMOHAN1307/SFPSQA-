# SFPSQA - Smart Food Product Scanner and Quality Analyzer

## Overview

SFPSQA is a Python-based desktop application designed to scan or upload barcodes/QR codes of food products and provide detailed nutritional and ingredient profiling. It fetches product data from the Open Food Facts API, evaluates the nutritional content, categorizes ingredients, and visually presents the information through an interactive dashboard with charts.

---

## Features

- **Barcode Scanning:** Use your webcam to scan barcodes or QR codes directly.
- **Image Upload:** Upload images containing barcodes/QR codes for decoding.
- **Product Information Retrieval:** Fetches product details including brand, category, serving size, and product images from Open Food Facts.
- **Nutrient Profiling:** Analyzes key nutrients per 10g serving (energy, sugars, fat, proteins, sodium) and provides a health evaluation.
- **Ingredient Profiling:** Categorizes ingredients into organic, chemical, overlapping, and others based on keyword matching.
- **Interactive Dashboard:** Displays product info, nutrient and ingredient profiling with color-coded health evaluation.
- **Nutrient Composition Chart:** Generates and displays a pie chart of major nutrients (sugars, fat, proteins).
- **User-Friendly GUI:** Built with Tkinter, featuring easy navigation between nutrient and ingredient views.

---

## Application Structure

| File Name       | Description                                                  |
|-----------------|--------------------------------------------------------------|
| `2GUI.py`       | Main GUI application entry point handling user interactions. |
| `Decoding.py`   | Handles API requests, fetches product data, and basic processing. |
| `Evaluation.py` | Contains logic for nutrient and ingredient profiling.        |
| `Dashboard.py`  | GUI dashboard displaying product details, profiling, and charts. |
| `Scanning.py`   | Handles barcode scanning via webcam using OpenCV and pyzbar. |
| `Upload.py`     | Handles image upload and barcode decoding from images.       |
| `chart.py`      | Generates nutrient composition pie charts (used internally). |

---

## Installation

### Prerequisites

- Python 3.8 or higher (64-bit recommended for chart generation)
- pip package manager

### Required Python Packages

Install dependencies using:

```bash
pip install -r requirements.txt
```

**`requirements.txt` example:**

```
requests
Pillow
matplotlib
opencv-python
pyzbar
```

---

## Usage

1. **Launch the Application:**

```bash
python 2GUI.exe
```

2. **Choose an Option:**

- **Upload:** Select an image file containing a barcode/QR code.
- **Scan:** Use your webcam to scan a barcode/QR code live.

3. **View Results:**

- After decoding, the dashboard will display:
  - Product information (title, brand, category, serving size).
  - Nutrient profiling with health evaluation.
  - Ingredient profiling categorized by type.
  - Nutrient composition pie chart.

4. **Toggle Views:**

- Use the toggle button to switch between nutrient and ingredient views.

5. **Exit:**

- Use the exit button to close the dashboard or application.

---

## How It Works

- **Barcode Decoding:** Using `pyzbar` and OpenCV, barcodes are decoded from webcam feed or uploaded images.
- **API Integration:** The barcode is sent to Open Food Facts API to retrieve product data.
- **Profiling:**
  - Nutrient data is extracted from the API response and evaluated per 10g serving.
  - Ingredients are parsed and categorized based on keyword lists.
- **Dashboard Display:** Tkinter GUI presents all information with interactive elements and charts generated dynamically using Matplotlib.

---

## Troubleshooting

- **Chart Not Displaying:** Ensure you have 64-bit Python installed for Matplotlib chart generation. The app calls the 64-bit Python interpreter explicitly for chart rendering.
- **No Barcode Detected:** Make sure the barcode is clear and well-lit in images or webcam.
- **API Errors:** Check your internet connection; Open Food Facts API must be reachable.
- **Missing Images or Icons:** Verify that the `Images/` directory contains required assets.

---

## Project Structure

```
SFPSQA/
│
├── 2GUI.py
├── Decoding.py
├── Evaluation.py
├── Dashboard.py
├── Scanning.py
├── Upload.py
├── chart.py
├── Images/
│   ├── Background.jpg
│   ├── upload.png
│   ├── Barcode_Scan.png
│   └── chart_output.png (generated)
├── requirements.txt
└── README.md
```

---

## License

This project is released under the MIT License.

---

## Acknowledgements

- [Open Food Facts](https://world.openfoodfacts.org/) for their comprehensive food product database and API.
- Libraries: OpenCV, pyzbar, Pillow, Matplotlib, Tkinter.

---

## Contact

For questions, issues, or contributions, please contact:

**Your Name**  
Email: ankith1092@gmail.com 
GitHub: https://github.com/ANKITHMOHAN1307/SQFA

---

Thank you for using SFPSQA — your smart assistant for food product quality analysis!

---

