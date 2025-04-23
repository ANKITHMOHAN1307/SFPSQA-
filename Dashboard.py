import tkinter as tk
from PIL import Image, ImageTk
import os
import json
import textwrap
import matplotlib.pyplot as plt
from io import BytesIO
from Evaluation import nutrient_profiling, ingredient_profiling
from Decoding import get_product_details

class Dashboard(tk.Toplevel):
    def __init__(self, product_info, master=None):
        super().__init__(master=master)
        self.product_info = product_info
        self.master = master
        self.geometry("600x500")
        self.title("Product Dashboard")
        self._set_background("Images/Bac.jpg")
        self._create_widgets()
        self.current_view = None
        self.chart_image = None  # To maintain reference to chart image

    def _set_background(self, image_name):
        try:
            img = Image.open(os.path.join(self._get_script_dir(), image_name))
            self.bg_image = ImageTk.PhotoImage(img.resize((600, 500), Image.LANCZOS))
            tk.Label(self, image=self.bg_image).place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print(f"Background image '{image_name}' not found.")
            self.config(bg="lightgreen")
        except Exception as e:
            print(f"Error loading background: {e}")
            self.config(bg="lightgreen")

    def _create_widgets(self):
        tk.Label(self, text="Product Info", font=("Times New Roman", 18, "bold"), bg="white").place(relx=0.5, rely=0.05, anchor="center")
        
        self.content_frame = tk.Frame(self, bg="lightgreen")
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.7)
        
        footer = tk.Frame(self)
        footer.pack(side="bottom", fill="x", pady=10)
        tk.Button(footer, text="🚪 Home ", font=("Times New Roman", 12), bg="white", command=self._exit_dashboard).pack(side="left", padx=20)
        
        self.toggle_btn_text = tk.StringVar(value="🧪 Show Ingredients")
        self.toggle_btn = tk.Button(footer, textvariable=self.toggle_btn_text, font=("Times New Roman", 12), 
                                  bg="white", command=self._toggle_view)
        self.toggle_btn.pack(side="right", padx=20)
        
        self._show_nutrient_view()

    def _clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.chart_image = None  # Clear previous chart reference

    def _create_scrollable_frame(self, parent):
        container = tk.Frame(parent, bg="lightgreen")
        container.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(container, bg="lightgreen", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="lightgreen")
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return scrollable_frame

    def _create_nutrient_chart(self, data):
        """Create and return a PhotoImage of the nutrient chart"""
        keys = ["sugars", "fat", "proteins"]
        values = [data.get(k, 0) for k in keys if isinstance(data.get(k), (int, float)) and data.get(k) > 0]
        labels = [k.capitalize() for k in keys if isinstance(data.get(k), (int, float)) and data.get(k) > 0]
        
        if not values:
            print("No valid data to plot")
            return None
            
        plt.figure(figsize=(4, 3.5))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.tight_layout()
        
        # Save to a buffer instead of file
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        plt.close()
        buf.seek(0)
        
        return ImageTk.PhotoImage(Image.open(buf))

    def _show_nutrient_view(self):
        self._clear_content_frame()
        scrollable_frame = self._create_scrollable_frame(self.content_frame)
        
        # Product info
        info = [
            f"Title: {self.product_info.get('Title', '-')}",
            f"Brand: {self.product_info.get('Brand', '-')}",
            f"Category: {self.product_info.get('Category', '-')}",
            f"Serving Size: {self.product_info.get('Serving Size', '-')}",
        ]
        
        for line in info:
            wrap = 500 if line.startswith("Category:") else 0
            tk.Label(scrollable_frame, text=line, font=("Times New Roman", 12), 
                    bg="lightgreen", wraplength=wrap).pack(pady=2, anchor="w")
        
        # Nutrient info
        tk.Label(scrollable_frame, text="🌀 Nutrient Profiling", 
                font=("Times New Roman", 14, "bold"), bg="lightgreen").pack(pady=(10, 5), anchor="w")
        
        # Get raw product data from product_info
        # product_data = self.product_info.get("product", {})
        product_data = self.product_info.get("product", {})
        nutriments = product_data.get("nutriments", {})
        nutrient_info = nutrient_profiling(nutriments)


        # Call nutrient_profiling to get nutrient info dictionary
        # nutrient_info = nutrient_profiling(product_data)
        print("Nutrient profiling output:", nutrient_info)
        

        lines = ["Nutrient Profiling:"]
        for key, value in nutrient_info.items():
            health_status = "🟢" if "highly" in str(value).lower() else "⚪"
            display_value = f"  - Health Evaluation: {health_status} {value}" if key.lower() == "health evaluation" else f"  - {key}: {value}"
            lines.append(display_value)

        formatted_info = "\n".join(lines)
        tk.Label(scrollable_frame, text=formatted_info, bg="lightgreen", fg="black",
                wraplength=550, justify="left", font=("Times New Roman", 11)).pack(padx=10, anchor="w")

        # Create chart using nutrient_info["Nutrients per 10g"]
        # nutrients_10g = nutrient_info.get("Nutrients per 10g", {})?
        nutrients_10g = nutrient_info.get("Nutrients per 10g", {})
        self.chart_image = self._create_nutrient_chart(nutrients_10g)

        print("Nutrients data to show chart",nutrients_10g)
       

        if self.chart_image:
            chart_frame = tk.Frame(scrollable_frame, bg="lightgreen")
            chart_frame.pack(pady=20)
            
            tk.Label(chart_frame, text="Nutrient Composition", 
                    font=("Times New Roman", 12, "bold"), bg="lightgreen").pack()
            
            chart_label = tk.Label(chart_frame, image=self.chart_image, bg="lightgreen")
            chart_label.image = self.chart_image  # Keep reference
            chart_label.pack()
        else:
            tk.Label(scrollable_frame, text="No nutrient data available for chart", 
                    bg="lightgreen", font=("Times New Roman", 12)).pack()
        
        self.current_view = "nutrient"
        self.toggle_btn_text.set("🧪 Show Ingredients")

    def _show_ingredient_view(self):
        self._clear_content_frame()
        scrollable_frame = self._create_scrollable_frame(self.content_frame)
        
        tk.Label(scrollable_frame, text="Ingredient Profiling", 
                font=("Times New Roman", 14, "bold"), bg="lightgreen").pack(pady=(10, 5), anchor="w")
        
        ingredients = self.product_info.get("Ingredient Profiling", {})
        if not ingredients:
            tk.Label(scrollable_frame, text="No ingredient information available", 
                    bg="lightgreen", font=("Times New Roman", 12)).pack()
            return
        
        for category, items in ingredients.items():
            color = "#9ACD32" if "organic" in category.lower() else "#CD5C5C" if any(x in category.lower() for x in ["chemical", "additive"]) else "#FFD700"
            
            category_frame = tk.Frame(scrollable_frame, bg=color, padx=10, pady=5)
            category_frame.pack(fill="x", padx=10, pady=5)
            
            tk.Label(category_frame, text=f"❖ {category}:", bg=color, 
                    font=("Times New Roman", 12, "bold")).pack(anchor="w")
            
            if items:
                for item in items:
                    tk.Label(category_frame, text=f"• {item}", bg=color, 
                            font=("Times New Roman", 11), anchor="w").pack(anchor="w")
            else:
                tk.Label(category_frame, text="None", bg=color, 
                        font=("Times New Roman", 11)).pack()
        
        self.current_view = "ingredient"
        self.toggle_btn_text.set("🧬 Show Nutrients")

    def _toggle_view(self):
        if self.current_view == "nutrient":
            self._show_ingredient_view()
        else:
            self._show_nutrient_view()

    def _exit_dashboard(self):
        self.destroy()
        if self.master:
            self.master.deiconify()

    def _get_script_dir(self):
        return os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_nutrient.json"), "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {
            "Title": "Sample Product",
            "Brand": "Sample Brand",
            "Category": "Sample Category",
            "Serving Size": "100g",
            "Nutrients per 10g": {"fat": 15, "sugars": 5, "proteins": 8},
            "Nutrient Profiling": {"Health Evaluation": "Highly Nutritious"},
            "Ingredient Profiling": {"Organic": ["Water", "Sugar"], "Additives": ["Preservative"]},
        }
    Dashboard(data, master=root).mainloop()
