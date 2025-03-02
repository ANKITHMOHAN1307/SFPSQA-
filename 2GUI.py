# Importing Libraries
import tkinter as tk
from Scanning import scanner  
from Upload import upload_image
from Decoding import decode_from_scan,decode_from_upload

# Main Window
root = tk.Tk()
root.title("SFPSQA")
root.geometry("300x550")  # Size

# Label 
label = tk.Label(root, text="PROVIDE THE QR/BARCODE :")
label.pack(pady=10, padx=50)
def open_result_window(product_info):
    """Opens a new window to display product details."""
    result_window = tk.Toplevel(root)
    result_window.title("Product Details")
    result_window.geometry("400x400")

    if "Error" in product_info:
        label = tk.Label(result_window, text=product_info["Error"], fg="red")
        label.pack(pady=10)
    else:
        label = tk.Label(result_window, text=f"Title: {product_info['Title']}", font=("Arial", 12, "bold"), wraplength=350, justify="center")
        label.pack(pady=10)

        brand_label = tk.Label(result_window, text=f"Brand: {product_info['Brand']}", wraplength=350, justify="center")
        brand_label.pack(pady=5)

        category_label = tk.Label(result_window, text=f"Category: {product_info['Category']}", wraplength=350, justify="center")
        category_label.pack(pady=5)

        serving_label = tk.Label(result_window, text=f"Serving Size: {product_info['Serving Size']}", wraplength=350, justify="center")
        serving_label.pack(pady=5)

        nutrient_button = tk.Button(result_window, text="Nutrient Profiling", command=lambda: show_profiling("Nutrient", product_info), wraplength=350, justify="center")
        nutrient_button.pack(pady=10)

        ingredient_button = tk.Button(result_window, text="Ingredient Profiling", command=lambda: show_profiling("Ingredient", product_info), wraplength=350, justify="center")
        ingredient_button.pack(pady=10)

    def go_back():
        result_window.destroy()

    back_button = tk.Button(result_window, text="Back", command=go_back)
    back_button.pack(pady=10)

def show_profiling(profiling_type, product_info):
    """Displays profiling details in a new window."""
    profiling_window = tk.Toplevel(root)
    profiling_window.title(f"{profiling_type} Profiling")
    profiling_window.geometry("400x300")

    profiling_label = tk.Label(profiling_window, text=f"{profiling_type} Profiling", font=("Arial", 12, "bold"))
    profiling_label.pack(pady=10)

    details = product_info.get(f"{profiling_type} Profiling", {})
    if not details:
        detail_label = tk.Label(profiling_window, text="No data available.", fg="red")
        detail_label.pack()
    else:
        for key, value in details.items():
            detail_label = tk.Label(profiling_window, text=f"{key}: {value}", wraplength=350, justify="center")
            detail_label.pack()

    close_button = tk.Button(profiling_window, text="Close", command=profiling_window.destroy)
    close_button.pack(pady=10)


# Upload Button
def on_Upload_button_click():
    print("Upload button clicked!")
    product_info = upload_image()
    # product_info = decode_from_upload(barcode)
    open_result_window(product_info)  # Open result window after successful upload

upload_button = tk.Button(root, text="UPLOAD", command=on_Upload_button_click)
upload_button.pack(pady=50)

# Scan Button
def on_Scan_button_click():
    print("Scan button clicked!")
    product_info=scanner()
    # product_info = decode_from_scan()
    open_result_window(product_info)  # Open result window after successful scan

scan_button = tk.Button(root, text="SCAN", command=on_Scan_button_click)
scan_button.pack(pady=50)

# Exit Button
def on_Exit_button_click():
    print("Exiting The Application")
    root.destroy()
    

exit_button = tk.Button(root, text='EXIT', command=on_Exit_button_click)
exit_button.pack(pady=50)

# Run the application
root.mainloop()
