import os
import tkinter as tk 
from tkinter import filedialog
from PIL import Image
from tkinter import messagebox

class ImageTransformerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title = "Image Transformer"

        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.quality_var = tk.IntVar()
        self.target_size_var = tk.IntVar()
        self.create_widgets()
    
    def create_widgets(self):

        tk.Label(self.root, text="Input Folder:").pack()
        tk.Entry(self.root, textvariable= self.input_folder, state = 'readonly'). pack(side=tk.LEFT)
        tk.Button(self.root, text="Browse", command=self.browse_output_folder).pack(side=tk.LEFT)

        tk.Label(self.root, text="JPEG Quality (0-100):").pack()
        tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.quality_var).pack()

        tk.Label(self.root, text="Target Size:").pack()
        tk.Entry(self.root, textvariable=self.target_size_var).pack()

        tk.Button(self.root, text="Convert Images", command=self.convert_images).pack()
    
    def browse_input_folder(self):
        folder_path = filedialog.askdirectory()
        self.input_folder.set(folder_path)
    
    def browse_output_folder(self):
        folder_path = filedialog.askdirectory()
        self.output_folder.set(folder_path)

    def convert_images(self):

        input_folder = self.input_folder.get()
        output_folder = self.output_folder.get()
        quality = self.quality_var.get()
        target_size_str = self.target_size_var.get()
        
        try:
            target_width, target_height = map(int, target_size_str.split('x'))
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid target size format (width x height).")
        return
        
        transformer = ImageTransformer(input_folder, output_folder, quality, (target_width, target_height))
        transformer.transform_images()
        tk.messagebox.showinfo("Conversion Complete", "Images have been converted successfully.")





class ImageTransformer:

    def __init__(self, input_folder, output_folder, quality, target_size):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.quality = quality
        self.target_size = target_size

    def transform_images(self):
        os.makedirs(self.output_folder, exist_ok=True)

        image_files = [f for f in os.listdir(self.input_folder) if f.lower().endswith(('.png', '.jpeg', '.jpg'))]

        try:
            target_width, target_height = map(int, self.target_size.split('x'))
        except ValueError:
            messagebox.showerror("Error", "Invalid target size format (width x height).")
            return

        for image_file in image_files:
            input_path = os.path.join(self.input_folder, image_file)
            output_path = os.path.join(self.output_folder, os.path.splitext(image_file)[0] + ".jpeg")

            with Image.open(input_path) as img:
                img = img.convert('RGB')
                img = img.resize((target_width, target_height), Image.ANTIALIAS)
                img.save(output_path, 'JPEG', quality=self.quality)
        


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    input_folder = filedialog.askdirectory(title="Select Input Folder")
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    quality = 90  # Set your desired quality
    target_size = "300x300"  # Set your desired target size

    transformer = ImageTransformer(input_folder, output_folder, quality, target_size)
    transformer.transform_images()
    messagebox.showinfo("Conversion Complete", "Images have been converted successfully.")



