import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_FILES

# Set appearance mode and color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PixelMorphConverter(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("PixelMorph Converter")
        self.minsize(500, 350)  # Minimum window size

        
        # Define path to icon
        if os.name == 'nt':  # Windows
            self.app_image_dir = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'PixelMorph', 'images')
        else:  # Linux
            self.app_image_dir = os.path.expanduser('~/.local/share/PixelMorph/images')
        
        os.makedirs(self.app_image_dir, exist_ok=True)
        
        self.formats = ["PNG", "JPEG", "WEBP", "BMP", "TIFF", "GIF", "ICO", "EPS", "PDF", "PSD"]
        self.current_files = []
        self.setup_ui()
        self.create_output_folder()
        
        # Set up drag and drop for the entire window
        self.drop_target_register(DND_FILES)
        self.dnd_bind('>', self.handle_drop)
        
        # Auto-adjust window size
        self.update()
        self.resize_to_content()

    def resize_to_content(self):
        """Adjust window size based on content"""
        self.update_idletasks()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        self.geometry(f"{width}x{height}")

    def create_app_folders(self):
        """Create application folders for storing resources"""
        if sys.platform == "win32":
            # Try both AppData locations
            roaming_path = os.path.join(os.environ.get('APPDATA', ''), 'PixelMorph', 'images')
            local_path = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'PixelMorph', 'images')
            
            self.app_image_dir = roaming_path if os.path.exists(os.path.join(roaming_path, 'upload.png')) else local_path
            os.makedirs(self.app_image_dir, exist_ok=True)
        else:
            # Linux path
            self.app_image_dir = os.path.expanduser('~/.local/share/PixelMorph/images')
            os.makedirs(self.app_image_dir, exist_ok=True)

    def setup_ui(self):
        # Main frame - fills the entire window

        self.main_frame = ctk.CTkFrame(self, fg_color="#2a2a2a", corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)

        # Upload section (1) - fills the entire main_frame
        self.upload_section = ctk.CTkFrame(self.main_frame, fg_color="#2a2a2a")
        self.upload_section.pack(fill="both", expand=True, padx=20, pady=20)

        # Platform-specific UI elements
        if sys.platform == "win32":
            # Windows - load custom icon
            try:
                icon_path = os.path.join(self.app_image_dir, 'upload.png')
                if os.path.exists(icon_path):
                    img = Image.open(icon_path)
                    self.icon_image = ctk.CTkImage(light_image=img, size=(90, 90))
                    
                    icon_label = ctk.CTkLabel(
                        master=self.upload_section,
                        image=self.icon_image,
                        text=""
                    )
                    icon_label.pack(pady=(30, 10))
                else:
                    # Fallback to text if icon not found
                    ctk.CTkLabel(
                        master=self.upload_section,
                        text="PixelMorph Converter",
                        font=("Segoe UI", 24, "bold"),
                        text_color="#00bfff"
                    ).pack(pady=(30, 10))
            except Exception as e:
                print(f"Error loading icon: {e}")
                # Fallback to text
                ctk.CTkLabel(
                    master=self.upload_section,
                    text="PixelMorph Converter",
                    font=("Segoe UI", 24, "bold"),
                    text_color="#00bfff"
                ).pack(pady=(30, 10))
        else:
            # Linux - just show title
            ctk.CTkLabel(
                master=self.upload_section,
                text="PixelMorph Converter",
                font=("Segoe UI", 24, "bold"),
                text_color="#00bfff"
            ).pack(pady=(30, 10))

        # Text instruction
        self.drag_label = ctk.CTkLabel(
            master=self.upload_section,
            text="DRAG AND DROP IMAGE FILES\nOR USE 'CHOOSE FILES' BUTTON",
            font=("Segoe UI", 20, "bold"),
            text_color="white"
        )
        self.drag_label.pack(pady=10)

        # Choose file button
        self.upload_btn = ctk.CTkButton(
            master=self.upload_section,
            text="CHOOSE FILES →",
            command=self.select_file_or_directory,
            width=300,
            height=50,
            fg_color="#2CC985",
            hover_color="#207A4F",
            font=("Segoe UI", 14, "bold"),
            corner_radius=25
        )
        self.upload_btn.pack(pady=20)

        self.footer_frame = ctk.CTkFrame(self, bg_color="#2a2a2a", fg_color="#2a2a2a")
        self.footer_frame.place(relx=0.5, rely=1.0, anchor="s", y=-5)

        # Copyright label
        self.copyright_label = ctk.CTkLabel(
            self.footer_frame,
            text="© 2026 | neikiri | Download my other programs:",
            font=("Arial", 15)
        )
        self.copyright_label.pack(side="left")

        # GitHub Link button
        self.github_link = ctk.CTkButton(
            self.footer_frame,
            text="GitHub",
            command=lambda: self.open_github(),
            font=("Arial Bold", 14),
            fg_color="#007bff",
            bg_color="transparent",
            text_color="white",
            width=50,
            height=15
        )
        self.github_link.pack(side="left", padx=5)

    def open_github(self):
        url = "https://github.com/jindrichstoklasa"
        if sys.platform == "win32":
            os.system(f"start {url}")
        elif sys.platform == "darwin":  # macOS
            os.system(f"open {url}")
        else:  # Linux and others
            os.system(f"xdg-open {url}")

    def create_output_folder(self):
        if os.name == 'nt':
            self.output_folder = os.path.join(os.environ['USERPROFILE'], 'Documents', 'PixelMorph', 'Converted Images')
        else:
            self.output_folder = os.path.expanduser('~/PixelMorph/Converted Images')
        
        os.makedirs(self.output_folder, exist_ok=True)

    def handle_drop(self, event):
        files = self.tk.splitlist(event.data)
        self.process_dropped_items(files)

    def process_dropped_items(self, items):
        self.current_files = []
        for item in items:
            if os.path.isfile(item):
                if item.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff', '.gif', '.ico')):
                    self.current_files.append(item)
        
        file_count = len(self.current_files)
        
        if file_count > 0:
            self.update_ui_after_upload(file_count)

    def select_file_or_directory(self):
        files = filedialog.askopenfilenames(
            title="Choose image files", 
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.webp *.bmp *.tiff *.gif *.ico")]
        )
        
        if files:
            self.current_files = list(files)
            file_count = len(self.current_files)
            
            if file_count > 0:
                self.update_ui_after_upload(file_count)

    def go_back_to_upload(self):
        # Remove all widgets from main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Reset current_files
        self.current_files = []
        
        # Create upload section again
        self.upload_section = ctk.CTkFrame(self.main_frame, fg_color="#2a2a2a")
        self.upload_section.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Platform-specific UI elements
        if sys.platform == "win32":
            # Windows - load custom icon
            try:
                icon_path = os.path.join(self.app_image_dir, 'upload.png')
                if os.path.exists(icon_path):
                    img = Image.open(icon_path)
                    self.icon_image = ctk.CTkImage(light_image=img, size=(90, 90))
                    icon_label = ctk.CTkLabel(
                        master=self.upload_section,
                        image=self.icon_image,
                        text=""
                    )
                    icon_label.pack(pady=(30, 10))
                else:
                    ctk.CTkLabel(
                        master=self.upload_section,
                        text="PixelMorph Converter",
                        font=("Segoe UI", 24, "bold"),
                        text_color="#00bfff"
                    ).pack(pady=(30, 10))
            except Exception as e:
                ctk.CTkLabel(
                    master=self.upload_section,
                    text="PixelMorph Converter",
                    font=("Segoe UI", 24, "bold"),
                    text_color="#00bfff"
                ).pack(pady=(30, 10))
        else:
            # Linux - just show title
            ctk.CTkLabel(
                master=self.upload_section,
                text="PixelMorph Converter",
                font=("Segoe UI", 24, "bold"),
                text_color="#00bfff"
            ).pack(pady=(30, 10))
        
        # Text instruction
        self.drag_label = ctk.CTkLabel(
            master=self.upload_section,
            text="DRAG AND DROP IMAGE FILES\nOR USE 'CHOOSE FILES' BUTTON",
            font=("Segoe UI", 16, "bold"),
            text_color="white"
        )
        self.drag_label.pack(pady=10)
        
        # Choose file button
        self.upload_btn = ctk.CTkButton(
            master=self.upload_section,
            text="CHOOSE FILES →",
            command=self.select_file_or_directory,
            width=300,
            height=50,
            fg_color="#2CC985",
            hover_color="#207A4F",
            font=("Segoe UI", 14, "bold"),
            corner_radius=25
        )
        self.upload_btn.pack(pady=20)
        
        # Restore drag and drop functionality
        self.drop_target_register(DND_FILES)
        self.dnd_bind('>', self.handle_drop)
        
        # Adjust window size
        self.update_idletasks()
        self.geometry('')

    def update_ui_after_upload(self, file_count):
        # Remove upload section (1)
        self.upload_section.destroy()

        # Create success section (2) - fills the entire main_frame
        success_section = ctk.CTkFrame(self.main_frame, fg_color="#2a2a2a")
        success_section.pack(fill="both", expand=True, padx=20, pady=20)

        # Success message - all in one sentence
        success_label = ctk.CTkLabel(
            master=success_section,
            text=f"{file_count} OF FILES HAS BEEN ADDED SUCCESSFULLY",
            font=("Segoe UI", 20, "bold"),  # Smaller font size for better display
            text_color="#00ffaa"
        )
        success_label.pack(pady=(20, 10))

        # Format selection
        ctk.CTkLabel(success_section, text="Choose format:", font=("Segoe UI", 14), text_color="white").pack(pady=(20, 5))
        
        self.format_var = ctk.StringVar(value="PNG")
        format_menu = ctk.CTkComboBox(
            master=success_section,
            values=self.formats,
            variable=self.format_var,
            width=200
        )
        format_menu.pack(pady=(0, 10))

        # Convert button
        convert_btn = ctk.CTkButton(
            master=success_section,
            text="Convert",
            command=self.start_conversion,
            width=300,  # Total width
            height=50,
            font=("Segoe UI", 16, "bold")
        )
        convert_btn.pack(pady=10)

        # Buttons frame for Open output folder and Back buttons
        buttons_frame = ctk.CTkFrame(success_section, fg_color="#2a2a2a")
        buttons_frame.pack(pady=10)

        # Calculate width for each button (half of Convert minus spacing)
        button_width = (300 - 10) / 2  # 300 is Convert width, 10 is spacing between buttons
        
        # Open output folder button
        self.open_btn = ctk.CTkButton(
            master=buttons_frame,
            text="Open output folder",
            command=self.open_output_folder,
            width=button_width,
            height=50  # Same height as Convert
        )
        self.open_btn.pack(side="left", padx=(0, 5))  # 5px spacing on right

        # Back button
        self.back_btn = ctk.CTkButton(
            master=buttons_frame,
            text="Back",
            command=self.go_back_to_upload,
            width=button_width,
            height=50  # Same height as Convert
        )
        self.back_btn.pack(side="left", padx=(5, 0))  # 5px spacing on left

    def start_conversion(self):
        if not self.current_files:
            messagebox.showwarning("Warning", "No images selected!")
            return
        
        threading.Thread(target=self.convert_images, daemon=True).start()

    def convert_images(self):
        try:
            total = len(self.current_files)
            
            for idx, file in enumerate(self.current_files):
                output_file = f"converted_{os.path.splitext(os.path.basename(file))[0]}.{self.format_var.get().lower()}"
                output_path = os.path.join(self.output_folder, output_file)

                with Image.open(file) as img:
                    if self.format_var.get() == "JPEG":
                        img = img.convert("RGB")
                    img.save(output_path, format=self.format_var.get())

                self.update_idletasks()

            messagebox.showinfo("Done", f"Successfully converted {total} images!")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    def open_output_folder(self):
        try:
            if os.name == 'nt':  # Windows
                os.startfile(self.output_folder)
            elif os.name == 'posix':  # macOS, Linux
                if os.system(f'xdg-open "{self.output_folder}"') != 0:
                    os.system(f'open "{self.output_folder}"')  # macOS fallback
        except Exception as e:
            messagebox.showerror("Error", f"Could not open output folder:\n{str(e)}")

if __name__ == "__main__":
    app = PixelMorphConverter()
    app.mainloop()