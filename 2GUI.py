import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from runner import run_32bit_script
from Dashboard import Dashboard
from Decoding import decode_from_scan, decode_from_upload
import json

class SFPSQAApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SFPSQA")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        self._show_splash()

    def _show_splash(self):
        splash = tk.Frame(self.root)
        splash.pack(fill="both", expand=True)

        splash_bg_path = os.path.join(self._get_script_dir(), "Images", "Bac.jpg")
        self._setup_background(splash_bg_path, splash)

        label = tk.Label(splash, text="SFPSQA APP", font=("Times New Roman", 30, "bold"), bg="white", fg="green")
        label.place(relx=0.5, rely=0.5, anchor="center")

        self.root.after(5000, lambda: self._launch_main(splash))

    def _launch_main(self, splash):
        splash.destroy()
        main_bg_path = os.path.join(self._get_script_dir(), "Images", "Bac.jpg")
        self._setup_background(main_bg_path, self.root)
        self._setup_main_window()

    def _setup_background(self, image_path, parent):
        original_img = Image.open(image_path)
        width = parent.winfo_width() or 600
        height = parent.winfo_height() or 500
        resized = original_img.resize((width, height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized)

        if hasattr(self, 'bg_label') and self.bg_label.winfo_exists():
            self.bg_label.destroy()

        self.bg_label = tk.Label(parent, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.lower()

        def resize_bg(event):
            resized = original_img.resize((event.width, event.height), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized)
            self.bg_label.config(image=self.bg_photo)
            self.bg_label.image = self.bg_photo

        parent.bind("<Configure>", resize_bg)

    def _setup_main_window(self):
        tk.Label(self.root, text="PROVIDE THE QR/BARCODE:", font=("Times New Roman", 14, "bold"), bg="white").pack(pady=10)

        self.upload_icon = self._load_icon(os.path.join("Images", "upload.png"), (130, 70))
        self.scan_icon = self._load_icon(os.path.join("Images", "Barcode_Scan.png"), (130, 60))

        tk.Button(self.root, text="UPLOAD", image=self.upload_icon, compound="top", font=("Arial", 10), command=self._on_upload_button_click).pack(pady=20)
        tk.Button(self.root, text="SCAN", image=self.scan_icon, compound="top", font=("Arial", 10), command=self._on_scan_button_click).pack(pady=20)
        
       
        
        tk.Button(self.root, text='ABOUT', font=("Arial", 18), command=self._show_about).pack(side="left", padx=20)
        tk.Button(self.root, text='EXIT',   font=("Arial", 18), command=self.root.destroy).pack(side="right", padx=20)

    def _show_about(self):
        about_text = """SFPSQA - Smart Food Product Scanner and Quality Analyzer

Features:
• Scan/upload barcodes
• Nutritional analysis
• Ingredient categorization
• Interactive dashboard

Requirements:
> Good Network
> Good Image quality 

Contact:
ankith1092@gmail.com
github.com/ANKITHMOHAN1307/SQFA

License: MIT"""
        messagebox.showinfo("About SFPSQA", about_text)

    def _load_icon(self, relative_path, size):
        try:
            abs_icon_path = os.path.join(self._get_script_dir(), relative_path)
            img = Image.open(abs_icon_path).resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading icon '{relative_path}': {e}")
            return None

    def _on_upload_button_click(self):
        result = run_32bit_script("Upload.py")
        print(f"Result from run_32bit_script: {result}, type: {type(result)}")
        try:
            result_dict = json.loads(result)
            product_info = decode_from_upload(result_dict["barcode"]) if "barcode" in result_dict else result_dict
        except json.JSONDecodeError:
            product_info = {"Error": "Invalid JSON format"}
        self._handle_product_info(product_info)

    def _on_scan_button_click(self):
        result = run_32bit_script("Scanning.py")
        print(f"Result from run_32bit_script: {result}, type: {type(result)}")
        try:
            result_dict = json.loads(result)
            product_info = decode_from_upload(result_dict["barcode"]) if "barcode" in result_dict else result_dict
        except json.JSONDecodeError:
            product_info = {"Error": "Invalid JSON format"}
        self._handle_product_info(product_info)

    def _handle_product_info(self, product_info):
        if not product_info or "Error" in product_info:
            messagebox.showerror("Error", product_info.get("Error", "NO BARCODE FOUND"))
        else:
            self._open_dashboard(product_info)

    def _open_dashboard(self, product_info):
        self.root.withdraw()
        Dashboard(product_info, master=self.root)

    def _get_script_dir(self):
        return os.path.dirname(os.path.abspath(__file__))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SFPSQAApp()
    app.run()
