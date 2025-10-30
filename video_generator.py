#!/usr/bin/env python3
"""
GRN Video Generator - A tkinter application to create videos from audio files and images.
"""

import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import threading
import shutil


class AudioImagePair:
    """Represents a pair of audio file and its associated image."""
    
    def __init__(self, audio_path):
        self.audio_path = audio_path
        self.image_path = None
        self.status = "Ready"


class VideoGeneratorApp:
    """Main application class for the Video Generator."""
    
    # Supported file extensions
    AUDIO_EXTENSIONS = {'.wav', '.mp3', '.m4a', '.aac', '.flac', '.ogg', '.wma'}
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp', '.gif'}
    
    def __init__(self, root):
        self.root = root
        self.root.title("GRN Video Generator")
        self.root.geometry("900x600")
        
        self.audio_folder = None
        self.audio_image_pairs = []
        
        self._create_ui()
        
    def _create_ui(self):
        """Create the user interface."""
        
        # Top frame for folder selection
        top_frame = tk.Frame(self.root, padx=10, pady=10)
        top_frame.pack(fill=tk.X)
        
        tk.Label(top_frame, text="Audio Folder:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        
        self.folder_label = tk.Label(top_frame, text="No folder selected", fg="gray")
        self.folder_label.pack(side=tk.LEFT, padx=10)
        
        tk.Button(top_frame, text="Select Folder", command=self.select_folder, 
                 bg="#4CAF50", fg="white", padx=20).pack(side=tk.RIGHT)
        
        # Middle frame for the file list
        middle_frame = tk.Frame(self.root, padx=10, pady=10)
        middle_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(middle_frame, text="Audio Files and Associated Images:", 
                font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        # Create Treeview for displaying files
        columns = ("Audio File", "Image File", "Status")
        self.tree = ttk.Treeview(middle_frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("Audio File", text="Audio File")
        self.tree.heading("Image File", text="Image File")
        self.tree.heading("Status", text="Status")
        
        self.tree.column("Audio File", width=300)
        self.tree.column("Image File", width=300)
        self.tree.column("Status", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(middle_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click to select image
        self.tree.bind("<Double-1>", self.on_double_click)
        
        # Bottom frame for action buttons
        bottom_frame = tk.Frame(self.root, padx=10, pady=10)
        bottom_frame.pack(fill=tk.X)
        
        tk.Button(bottom_frame, text="Select Image for Selected File", 
                 command=self.select_image_for_selected, 
                 bg="#2196F3", fg="white", padx=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(bottom_frame, text="Select Images for All", 
                 command=self.select_images_for_all, 
                 bg="#FF9800", fg="white", padx=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(bottom_frame, text="Create Videos", 
                 command=self.create_videos, 
                 bg="#f44336", fg="white", padx=30, 
                 font=("Arial", 10, "bold")).pack(side=tk.RIGHT, padx=5)
        
        # Progress label
        self.progress_label = tk.Label(self.root, text="", fg="blue")
        self.progress_label.pack(pady=5)
        
    def select_folder(self):
        """Open dialog to select folder containing audio files."""
        folder = filedialog.askdirectory(title="Select Folder with Audio Files")
        
        if not folder:
            return
        
        self.audio_folder = folder
        self.folder_label.config(text=folder, fg="black")
        
        # Scan folder for audio files
        self._scan_audio_files()
        
    def _scan_audio_files(self):
        """Scan the selected folder for audio files."""
        self.audio_image_pairs = []
        
        # Clear the tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not self.audio_folder:
            return
        
        # Find all audio files
        audio_files = []
        for file in os.listdir(self.audio_folder):
            ext = os.path.splitext(file)[1].lower()
            if ext in self.AUDIO_EXTENSIONS:
                audio_files.append(file)
        
        # Sort files for consistent ordering
        audio_files.sort()
        
        # Create audio-image pairs
        for audio_file in audio_files:
            audio_path = os.path.join(self.audio_folder, audio_file)
            pair = AudioImagePair(audio_path)
            self.audio_image_pairs.append(pair)
            
            # Add to tree
            self.tree.insert("", tk.END, values=(audio_file, "No image selected", "Ready"))
        
        self.progress_label.config(text=f"Found {len(audio_files)} audio file(s)")
        
    def on_double_click(self, event):
        """Handle double-click on tree item."""
        self.select_image_for_selected()
        
    def select_image_for_selected(self):
        """Select an image for the currently selected audio file."""
        selected = self.tree.selection()
        
        if not selected:
            messagebox.showwarning("No Selection", "Please select an audio file first.")
            return
        
        # Get the index of the selected item
        item = selected[0]
        index = self.tree.index(item)
        
        # Open file dialog for image selection
        image_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.tiff *.tif *.bmp *.gif"),
                ("All files", "*.*")
            ]
        )
        
        if not image_path:
            return
        
        # Update the pair
        self.audio_image_pairs[index].image_path = image_path
        
        # Update the tree
        audio_file = os.path.basename(self.audio_image_pairs[index].audio_path)
        image_file = os.path.basename(image_path)
        self.tree.item(item, values=(audio_file, image_file, "Ready"))
        
    def select_images_for_all(self):
        """Select images for all audio files in sequence."""
        if not self.audio_image_pairs:
            messagebox.showwarning("No Audio Files", "Please select a folder with audio files first.")
            return
        
        for i, pair in enumerate(self.audio_image_pairs):
            audio_file = os.path.basename(pair.audio_path)
            
            image_path = filedialog.askopenfilename(
                title=f"Select Image for: {audio_file}",
                filetypes=[
                    ("Image files", "*.jpg *.jpeg *.png *.tiff *.tif *.bmp *.gif"),
                    ("All files", "*.*")
                ]
            )
            
            if image_path:
                pair.image_path = image_path
                image_file = os.path.basename(image_path)
                
                # Update tree
                item = self.tree.get_children()[i]
                self.tree.item(item, values=(audio_file, image_file, "Ready"))
            else:
                # User cancelled, stop the process
                break
                
    def create_videos(self):
        """Create videos from audio-image pairs."""
        # Validate that all pairs have images
        pairs_without_images = [pair for pair in self.audio_image_pairs if not pair.image_path]
        
        if pairs_without_images:
            messagebox.showerror(
                "Missing Images", 
                f"{len(pairs_without_images)} audio file(s) don't have associated images.\n"
                "Please assign images to all audio files."
            )
            return
        
        if not self.audio_image_pairs:
            messagebox.showwarning("No Files", "Please select a folder with audio files first.")
            return
        
        # Ask for output folder
        output_folder = filedialog.askdirectory(title="Select Output Folder for Videos")
        
        if not output_folder:
            return
        
        # Start video creation in a separate thread to keep UI responsive
        thread = threading.Thread(target=self._create_videos_thread, args=(output_folder,))
        thread.daemon = True
        thread.start()
        
    def _create_videos_thread(self, output_folder):
        """Thread function to create videos."""
        total = len(self.audio_image_pairs)
        
        for i, pair in enumerate(self.audio_image_pairs):
            # Update status in tree
            item = self.tree.get_children()[i]
            audio_file = os.path.basename(pair.audio_path)
            image_file = os.path.basename(pair.image_path)
            
            self.tree.item(item, values=(audio_file, image_file, "Processing..."))
            self.progress_label.config(text=f"Processing {i+1}/{total}: {audio_file}")
            
            try:
                # Create video
                self._create_single_video(pair, output_folder)
                
                # Update status
                self.tree.item(item, values=(audio_file, image_file, "Done"))
            except Exception as e:
                self.tree.item(item, values=(audio_file, image_file, f"Error"))
                messagebox.showerror("Error", f"Failed to create video for {audio_file}:\n{str(e)}")
        
        self.progress_label.config(text=f"Completed! {total} video(s) created in {output_folder}")
        messagebox.showinfo("Success", f"Successfully created {total} video(s)!")
        
    def _create_single_video(self, pair, output_folder):
        """Create a single video from audio-image pair using ffmpeg."""
        # Generate output filename
        audio_basename = os.path.splitext(os.path.basename(pair.audio_path))[0]
        output_path = os.path.join(output_folder, f"{audio_basename}.mp4")
        
        # Build ffmpeg command for 720p video
        # -loop 1: loop the image
        # -i image: input image
        # -i audio: input audio
        # -c:v libx264: video codec
        # -tune stillimage: optimize for still image
        # -c:a aac: audio codec
        # -b:a 192k: audio bitrate
        # -pix_fmt yuv420p: pixel format for compatibility
        # -shortest: finish when audio ends
        # -vf scale=1280:720: scale to 720p
        
        cmd = [
            'ffmpeg',
            '-loop', '1',
            '-i', pair.image_path,
            '-i', pair.audio_path,
            '-c:v', 'libx264',
            '-tune', 'stillimage',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-pix_fmt', 'yuv420p',
            '-vf', 'scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2',
            '-shortest',
            '-y',  # Overwrite output file if exists
            output_path
        ]
        
        # Run ffmpeg
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"ffmpeg error: {result.stderr}")


def check_ffmpeg():
    """Check if ffmpeg is available in the system."""
    try:
        return shutil.which('ffmpeg') is not None
    except Exception:
        return False


def main():
    """Main entry point."""
    # Check if ffmpeg is available
    if not check_ffmpeg():
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror(
            "ffmpeg Not Found",
            "ffmpeg is not installed or not found in your system PATH.\n\n"
            "Please install ffmpeg:\n"
            "- Ubuntu/Debian: sudo apt-get install ffmpeg\n"
            "- macOS: brew install ffmpeg\n"
            "- Windows: Download from https://ffmpeg.org/download.html\n\n"
            "After installation, restart the application."
        )
        root.destroy()
        return
    
    root = tk.Tk()
    app = VideoGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
