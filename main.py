import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import TkinterDnD
from clearvoice import ClearVoice
import threading

MODEL_MAP = {
    'speech_enhancement': ['MossFormer2_SE_48K'],
    'speech_separation': ['MossFormer2_SS_16K'],
    'target_speaker_extraction': ['AV_MossFormer2_TSE_16K']
}

class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("ClearVoice Audio Processor")
        self.geometry("700x600")
        self.minsize(600, 500)
        self.configure(bg='#f8f9fa')
        
        self.input_paths = []
        self.output_dir = None
        self.task = tk.StringVar(value='speech_enhancement')
        self.processing = False
        self.close_when_finished = tk.BooleanVar(value=False)
        
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Custom styles
        self.style.configure('Header.TLabel', 
                           font=('Segoe UI', 16, 'bold'),
                           background='#f8f9fa',
                           foreground='#212529')
        
        self.style.configure('Subheader.TLabel',
                           font=('Segoe UI', 10, 'bold'),
                           background='#f8f9fa',
                           foreground='#495057')
        
        self.style.configure('Success.TLabel',
                           font=('Segoe UI', 9),
                           background='#f8f9fa',
                           foreground='#28a745')
        
        self.style.configure('Warning.TLabel',
                           font=('Segoe UI', 9),
                           background='#f8f9fa',
                           foreground='#ffc107')
        
        self.style.configure('Primary.TButton',
                           font=('Segoe UI', 10, 'bold'),
                           padding=(20, 10))
        
        self.style.configure('Secondary.TButton',
                           font=('Segoe UI', 9),
                           padding=(15, 8))

    def create_widgets(self):
        # Main container with padding
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(header_frame, text="🎵 ClearVoice Audio Processor", 
                 style='Header.TLabel').pack()
        ttk.Label(header_frame, text="Enhance, separate, and extract speech from audio files",
                 font=('Segoe UI', 10)).pack(pady=(5, 0))
        
        # Input section
        input_section = ttk.LabelFrame(main_frame, text=" 📁 Input Files ", padding=15)
        input_section.pack(fill='both', expand=True, pady=(0, 15))
        
        # Drop area with better styling
        self.drop_area = tk.Frame(input_section, relief="solid", bd=2, bg="#e9ecef")
        self.drop_area.pack(fill='x', pady=(0, 10))
        
        drop_content = tk.Frame(self.drop_area, bg="#e9ecef")
        drop_content.pack(expand=True, fill='both', pady=30)
        
        tk.Label(drop_content, text="📤", font=('Segoe UI', 24), bg="#e9ecef", fg="#6c757d").pack()
        tk.Label(drop_content, text="Drag & drop audio files or folders here", 
                font=('Segoe UI', 11), bg="#e9ecef", fg="#6c757d").pack()
        tk.Label(drop_content, text="Supported: WAV, MP3, OGG, MP4", 
                font=('Segoe UI', 9), bg="#e9ecef", fg="#adb5bd").pack()
        tk.Label(drop_content, text="or click here to browse", 
                font=('Segoe UI', 9, 'underline'), bg="#e9ecef", fg="#007bff", cursor="hand2").pack(pady=(5, 0))
        
        self.drop_area.drop_target_register('*')
        self.drop_area.dnd_bind('<<Drop>>', self.on_drop)
        self.drop_area.bind("<Button-1>", self.on_drop_area_click)
        drop_content.bind("<Button-1>", self.on_drop_area_click)
        
        # Bind click event to all child widgets in drop_content
        for child in drop_content.winfo_children():
            child.bind("<Button-1>", self.on_drop_area_click)
        
        # File list with scrollbar
        files_frame = ttk.Frame(input_section)
        files_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        ttk.Label(files_frame, text="Selected Files:", style='Subheader.TLabel').pack(anchor='w')
        
        listbox_frame = ttk.Frame(files_frame)
        listbox_frame.pack(fill='both', expand=True, pady=(5, 0))
        
        self.file_listbox = tk.Listbox(listbox_frame, font=('Segoe UI', 9), 
                                      selectmode='extended', height=6)
        scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.file_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # File count label
        self.file_count_label = ttk.Label(files_frame, text="No files selected", 
                                         font=('Segoe UI', 9), foreground='#6c757d')
        self.file_count_label.pack(anchor='w', pady=(5, 0))
        
        # Buttons frame
        buttons_frame = ttk.Frame(input_section)
        buttons_frame.pack(anchor='e')
        
        ttk.Button(buttons_frame, text="🗑️ Remove Selected", command=self.remove_selected_files,
                  style='Secondary.TButton').pack(side='left', padx=(0, 5))
        
        ttk.Button(buttons_frame, text="🗑️ Clear All", command=self.clear_files,
                  style='Secondary.TButton').pack(side='left')
        
        # Settings section
        settings_section = ttk.LabelFrame(main_frame, text=" ⚙️ Configuration ", padding=15)
        settings_section.pack(fill='x', pady=(0, 15))
        
        # Two-column layout for settings
        settings_grid = ttk.Frame(settings_section)
        settings_grid.pack(fill='x')
        
        # Task selection
        task_frame = ttk.Frame(settings_grid)
        task_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        ttk.Label(task_frame, text="Processing Task:", style='Subheader.TLabel').pack(anchor='w')
        self.task_combo = ttk.Combobox(task_frame, textvariable=self.task, 
                                      values=list(MODEL_MAP.keys()), 
                                      state='readonly', font=('Segoe UI', 9))
        self.task_combo.pack(fill='x', pady=(5, 0))
        
        # Output folder
        output_frame = ttk.Frame(settings_grid)
        output_frame.pack(side='right', fill='x', expand=True)
        
        ttk.Label(output_frame, text="Output Folder:", style='Subheader.TLabel').pack(anchor='w')
        
        output_control = ttk.Frame(output_frame)
        output_control.pack(fill='x', pady=(5, 0))
        
        self.output_label = ttk.Label(output_control, text="📁 No folder selected", 
                                     font=('Segoe UI', 9), foreground='#6c757d')
        self.output_label.pack(side='left', fill='x', expand=True)
        
        ttk.Button(output_control, text="Browse...", command=self.choose_output,
                  style='Secondary.TButton').pack(side='right', padx=(10, 0))
        
        # Process section
        process_section = ttk.Frame(main_frame)
        process_section.pack(fill='x', pady=(0, 15))
        
        # Options frame
        options_frame = ttk.Frame(process_section)
        options_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Checkbutton(options_frame, text="Close application when finished", 
                       variable=self.close_when_finished).pack(anchor='w')
        
        # Status and process button
        status_frame = ttk.Frame(process_section)
        status_frame.pack(fill='x', pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="Ready to process", 
                                     font=('Segoe UI', 10), foreground='#28a745')
        self.status_label.pack(side='left')
        
        self.process_btn = ttk.Button(status_frame, text="🚀 Start Processing", 
                                     command=self.process_all, style='Primary.TButton')
        self.process_btn.pack(side='right')
        
        # Progress bar
        self.progress = ttk.Progressbar(process_section, mode='indeterminate')
        self.progress.pack(fill='x', pady=(0, 10))
        
        # Log section
        log_section = ttk.LabelFrame(main_frame, text=" 📋 Processing Log ", padding=10)
        log_section.pack(fill='both', expand=True)
        
        log_frame = ttk.Frame(log_section)
        log_frame.pack(fill='both', expand=True)
        
        self.log = tk.Text(log_frame, height=8, font=('Consolas', 9), 
                          state='disabled', wrap='word')
        log_scrollbar = ttk.Scrollbar(log_frame, orient='vertical', command=self.log.yview)
        self.log.configure(yscrollcommand=log_scrollbar.set)
        
        self.log.pack(side='left', fill='both', expand=True)
        log_scrollbar.pack(side='right', fill='y')

    def on_drop(self, event):
        if self.processing:
            return
            
        raw = self.drop_area.tk.splitlist(event.data)
        new_files = 0
        
        for path in raw:
            path = path.strip('{}')
            if path not in self.input_paths:
                self.input_paths.append(path)
                self.file_listbox.insert(tk.END, f"📄 {os.path.basename(path)}")
                new_files += 1
        
        self.update_file_count()
        self.update_status()
        
        if new_files > 0:
            self.log_message(f"✅ Added {new_files} file(s)")

    def clear_files(self):
        if self.processing:
            return
            
        self.input_paths.clear()
        self.file_listbox.delete(0, tk.END)
        self.update_file_count()
        self.update_status()
        self.log_message("🗑️ File list cleared")

    def choose_output(self):
        d = filedialog.askdirectory(title="Select Output Folder")
        if d:
            self.output_dir = d
            folder_name = os.path.basename(d) or d
            self.output_label.config(text=f"📁 {folder_name}", foreground='#28a745')
            self.update_status()

    def update_file_count(self):
        count = len(self.input_paths)
        if count == 0:
            self.file_count_label.config(text="No files selected", foreground='#6c757d')
        else:
            self.file_count_label.config(text=f"{count} file(s) selected", foreground='#28a745')

    def update_status(self):
        if self.processing:
            return
            
        if not self.input_paths:
            self.status_label.config(text="⚠️ No files selected", foreground='#ffc107')
            self.process_btn.config(state='disabled')
        elif not self.output_dir:
            self.status_label.config(text="⚠️ No output folder selected", foreground='#ffc107')
            self.process_btn.config(state='disabled')
        else:
            self.status_label.config(text="✅ Ready to process", foreground='#28a745')
            self.process_btn.config(state='normal')

    def log_message(self, msg):
        self.log.config(state='normal')
        self.log.insert('end', f"{msg}\n")
        self.log.see('end')
        self.log.config(state='disabled')
        self.update()

    def process_all(self):
        if not self.input_paths or not self.output_dir:
            messagebox.showwarning("Missing Information", 
                                 "Please select input files and output folder")
            return

        self.processing = True
        self.process_btn.config(state='disabled', text="⏳ Processing...")
        self.progress.start()
        self.status_label.config(text="🔄 Processing files...", foreground='#007bff')

        # Start processing in a separate thread
        processing_thread = threading.Thread(target=self._process_files_thread, daemon=True)
        processing_thread.start()

    def _process_files_thread(self):
        task = self.task.get()
        model_names = MODEL_MAP[task]
        self.safe_log_message(f"🚀 Starting {task} with model: {model_names[0]}")

        try:
            cv = ClearVoice(task=task, model_names=model_names)
            total_processed = 0

            for inp in self.input_paths:
                if os.path.isdir(inp):
                    files = [os.path.join(inp, f) for f in os.listdir(inp)
                             if f.lower().endswith(('.wav', '.mp3', '.ogg', '.mp4'))]
                else:
                    files = [inp]

                for fn in files:
                    self.safe_log_message(f"🔄 Processing: {os.path.basename(fn)}")
                    try:
                        result = cv(input_path=fn, online_write=False)
                        basename = os.path.splitext(os.path.basename(fn))[0]
                        outname = f"{basename}_{model_names[0]}.wav"
                        outpath = os.path.join(self.output_dir, outname)
                        cv.write(result, output_path=outpath)
                        self.safe_log_message(f"✅ Saved: {outname}")
                        total_processed += 1
                    except Exception as e:
                        self.safe_log_message(f"❌ Error with {os.path.basename(fn)}: {e}")

            self.safe_log_message(f"🎉 Processing complete! {total_processed} files processed.")
            
        except Exception as e:
            self.safe_log_message(f"❌ Fatal error: {e}")
            self.after(0, lambda: messagebox.showerror("Processing Error", f"An error occurred: {e}"))

        finally:
            # Schedule UI updates on the main thread
            self.after(0, self._finish_processing)

    def _finish_processing(self):
        """Called on main thread when processing is complete"""
        self.processing = False
        self.progress.stop()
        self.process_btn.config(state='normal', text="🚀 Start Processing")
        self.update_status()
        
        # Close application if checkbox is checked
        if self.close_when_finished.get():
            self.after(2000, self.quit)  # Wait 2 seconds before closing

    def safe_log_message(self, msg):
        """Thread-safe logging method"""
        self.after(0, lambda: self.log_message(msg))

    def remove_selected_files(self):
        if self.processing:
            return
            
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            messagebox.showinfo("No Selection", "Please select files to remove from the list.")
            return
        
        # Remove from back to front to maintain indices
        removed_count = 0
        for index in reversed(selected_indices):
            del self.input_paths[index]
            self.file_listbox.delete(index)
            removed_count += 1
        
        self.update_file_count()
        self.update_status()
        self.log_message(f"🗑️ Removed {removed_count} file(s)")

    def on_drop_area_click(self, event):
        if self.processing:
            return
            
        filetypes = [
            ("Audio files", "*.wav *.mp3 *.ogg *.mp4"),
            ("WAV files", "*.wav"),
            ("MP3 files", "*.mp3"),
            ("OGG files", "*.ogg"),
            ("MP4 files", "*.mp4"),
            ("All files", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Select Audio Files",
            filetypes=filetypes
        )
        
        if files:
            new_files = 0
            for file_path in files:
                if file_path not in self.input_paths:
                    self.input_paths.append(file_path)
                    self.file_listbox.insert(tk.END, f"📄 {os.path.basename(file_path)}")
                    new_files += 1
            
            self.update_file_count()
            self.update_status()
            
            if new_files > 0:
                self.log_message(f"✅ Added {new_files} file(s) via file browser")

if __name__ == "__main__":
    App().mainloop()
