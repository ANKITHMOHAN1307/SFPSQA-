#imporoting libarires 
from Scanning import scanner
from Upload import upload_image
from Decoding import get_product_details
from Evaluation import nutrient_profiling,ingredient_profiling
import os
console_width = os.get_terminal_size().columns
def main():
    print('*' * 50)
    print("Smart Food Packet Scanner for Quality Assessment")
    print('*' * 50)
    print("Choose form the Following Choices,\n", 
              "1. --Scan \n",
              "2. --Upload \n",
              "3. --Exit")
    print('*' * console_width)
    ch=int(input(' '))

    # Corresponding function
    match ch:
        case 1:
            print('*'* console_width,"\nStarting scanner...")
            scanner()
        case 2:
            print('*'* console_width,"\nStarting uploader...")
            upload_image()
        case 3:
            return "I hope I helped you find the desired results"
        case _ :
            print("Please specify an action: --Scan or --Upload or --Exit")

if __name__ == "__main__":
    while True:
        c=main()
        if c == "I hope I helped you find the desired results":
            # Exit Condition
            print(c)
            break
        else:
            # Repeat menu
            continue