import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import pandas as pd

class MedicalCaseUI:
    def __init__(self, process):
        self.process = process
        self.root = tk.Tk()
        self.root.title("Medical Case Scenario Generator")
        self.root.geometry("800x700")
        self.root.config(bg="#e8f4f8")
        self.setup_ui()

    def setup_ui(self):
        # lable
        title_label = tk.Label(self.root, text="Medical Case Scenario Generator", font=("B Nazanin", 18, "bold"), bg="#e8f4f8", fg="#005f73")
        title_label.pack(pady=(10, 10))

        # api key
        self.api_key_label = tk.Label(self.root, text="API Key:", font=("B Nazanin", 14), bg="#e8f4f8", fg="#333")
        self.api_key_label.pack(anchor="w", padx=20)
        self.api_key_entry = tk.Entry(self.root, font=("B Nazanin", 14), width=50)
        self.api_key_entry.pack(padx=20, pady=(0, 10))

        # select api
        self.model_label = tk.Label(self.root, text="Model:", font=("B Nazanin", 14), bg="#e8f4f8", fg="#333")
        self.model_label.pack(anchor="w", padx=20)
        self.model_var = tk.StringVar(value="gemini-1.5-flash-latest")
        model_options = ["gemini-1.5-flash-latest", "openai-chat", "groq-model"]
        self.model_menu = tk.OptionMenu(self.root, self.model_var, *model_options)
        self.model_menu.config(font=("B Nazanin", 12), bg="#94d2bd", fg="black")
        self.model_menu.pack(padx=20, pady=(0, 10))

        # button for select CSV
        select_csv_button = tk.Button(self.root, text="انتخاب فایل CSV", command=self.select_csv, font=("B Nazanin", 14), bg="#0a9396", fg="white", padx=30, pady=10)
        select_csv_button.pack(pady=(0, 10))

        # button for select XLSX
        select_xlsx_button = tk.Button(self.root, text="انتخاب فایل XLSX", command=self.select_xlsx, font=("B Nazanin", 14), bg="#0a9396", fg="white", padx=30, pady=10)
        select_xlsx_button.pack(pady=(0, 10))

        # box for show result
        self.output_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("B Nazanin", 14), bg="#f7f7f7", fg="#333", padx=10, pady=10)
        self.output_text.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    def select_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.process_file(file_path)

    def select_xlsx(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            self.process_file(file_path)

    def process_file(self, file_path):
        api_key = self.api_key_entry.get()
        model = self.model_var.get()
        if not api_key:
            messagebox.showerror("Error", "Please enter your API Key.")
            return

        result = self.process(file_path, model, api_key)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, result)

    def run(self):
        self.root.mainloop()