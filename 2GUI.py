import tkinter as tk
from Scanning import scanner  
from Upload import upload_image
from Decoding import decode_from_scan, decode_from_upload
from PIL import Image, ImageTk
import os


# Main Window
root = tk.Tk()
root.title("SFPSQA")
root.geometry("359x550")  # Size
root.configure(bg="lightblue", bd=2, relief="solid")  # Add border to the main window

label = tk.Label(root, text="PROVIDE THE QR/BARCODE :", bg="lightblue", font=("Arial", 14, "bold"))
label.pack(pady=10, padx=30)

def open_result_window(product_info):
    """Opens a new window to display product details."""
    if product_info:
        root.withdraw()  # Hide the root window

        result_window = tk.Toplevel()
        result_window.title("Product Details")
        result_window.geometry("359x550")
        result_window.configure(bg="lightblue", bd=2, relief="solid")  # Add border to the result window

        if "Error" in product_info:
            label = tk.Label(result_window, text=product_info["Error"], fg="red", bg="lightblue", font=("Arial", 12))
            label.pack(pady=10)
        else:
            label = tk.Label(result_window, text=f"Title: {product_info['Title']}", font=("Arial", 12, "bold"), wraplength=350, justify="center", bg="lightblue")
            label.pack(pady=10)

            brand_label = tk.Label(result_window, text=f"Brand: {product_info['Brand']}", wraplength=350, justify="center", bg="lightblue", font=("Arial", 12))
            brand_label.pack(pady=5)

            category_label = tk.Label(result_window, text=f"Category: {product_info['Category']}", wraplength=350, justify="center", bg="lightblue", font=("Arial", 12))
            category_label.pack(pady=5)

            serving_label = tk.Label(result_window, text=f"Serving Size: {product_info['Serving Size']}", wraplength=350, justify="center", bg="lightblue", font=("Arial", 12))
            serving_label.pack(pady=5)

            nutrient_button = tk.Button(result_window, text="Nutrient Profiling", command=lambda: show_profiling("Nutrient", product_info, result_window), wraplength=350, justify="center", bg="lightgreen", font=("Arial", 12))
            nutrient_button.pack(pady=10)

            ingredient_button = tk.Button(result_window, text="Ingredient Profiling", command=lambda: show_profiling("Ingredient", product_info, result_window), wraplength=350, justify="center", bg="lightgreen", font=("Arial", 12))
            ingredient_button.pack(pady=10)

        def go_back():
            result_window.destroy()
            root.deiconify()  # Reopen the main window

        back_button = tk.Button(result_window, text="Back", command=go_back, bg="lightgreen", font=("Arial", 12))
        back_button.pack(pady=10)

def show_profiling(profiling_type, product_info, parent_window):
    """Displays profiling details in a new window."""
    parent_window.withdraw()  # Hide the result window

    profiling_window = tk.Toplevel()
    profiling_window.title(f"{profiling_type} Profiling")
    profiling_window.geometry("359x550")
    profiling_window.configure(bg="lightblue", bd=2, relief="solid")  # Add border to the profiling window

    profiling_label = tk.Label(profiling_window, text=f"{profiling_type} Profiling", font=("Arial", 12, "bold"), bg="lightblue")
    profiling_label.pack(pady=10)

    details = product_info.get(f"{profiling_type} Profiling", {})
    if not details:
        detail_label = tk.Label(profiling_window, text="No data available.", fg="red", bg="lightblue", font=("Arial", 12))
        detail_label.pack()
    else:
        # Display the description separately
        description_label = tk.Label(profiling_window, text="Description:", font=("Arial", 12, "bold"), bg="lightblue")
        description_label.pack(pady=5)

        for key, value in details.items():
            detail_label = tk.Label(profiling_window, text=f"{key}: {value}", wraplength=350, justify="left", bg="lightblue", font=("Arial", 12))
            detail_label.pack(pady=2)

        

    def go_back():
        profiling_window.destroy()
        parent_window.deiconify()  # Reopen the result window

    back_button = tk.Button(profiling_window, text="Back", command=go_back, bg="lightgreen", font=("Arial", 12))
    back_button.pack(pady=10)

# Upload Button
def on_Upload_button_click():
    print("Upload button clicked!")
    product_info = upload_image()
    open_result_window(product_info)  # Open result window after successful upload

upload_button = tk.Button(root, text="UPLOAD", command=on_Upload_button_click, bg="lightgreen", font=("Arial", 12))
upload_button.pack(pady=50)

# Scan Button
def on_Scan_button_click():
    print("Scan button clicked!")
    product_info = scanner()
    open_result_window(product_info)  # Open result window after successful scan

scan_button = tk.Button(root, text="SCAN", command=on_Scan_button_click, bg="lightgreen", font=("Arial", 12))
scan_button.pack(pady=50)

# Exit Button
def on_Exit_button_click():
    print("Exiting The Application")
    root.destroy()

exit_button = tk.Button(root, text='EXIT', command=on_Exit_button_click, bg="lightgreen", font=("Arial", 12))
exit_button.pack(pady=50)

# Run the application
root.mainloop()
exit()
