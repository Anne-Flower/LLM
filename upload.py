import os
import tkinter as tk
from tkinter import filedialog
import PyPDF2
import re
import json

def convert_specific_pdf_to_text(file_path="les-etoiles-presentation.pdf"):

  
    try:
        if not os.path.exists(file_path):
            print(f"Erreur : le fichier {file_path} est introuvable.")
            return
        
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ''
            for page in pdf_reader.pages:
                if page.extract_text():
                    text += page.extract_text() + " "
            
            text = re.sub(r'\s+', ' ', text).strip()
            
            sentences = re.split(r'(?<=[.!?]) +', text)
            chunks = []
            current_chunk = ""
            for sentence in sentences:
                if len(current_chunk) + len(sentence) + 1 < 500:
                    current_chunk += (sentence + " ").strip()
                else:
                    chunks.append(current_chunk)
                    current_chunk = sentence + " "
            if current_chunk:
                chunks.append(current_chunk)
            
            with open("vault.txt", "a", encoding="utf-8") as vault_file:
                for chunk in chunks:
                    vault_file.write(chunk.strip() + "\n")
            
            print(f"PDF '{file_path}' ajouté à vault.txt avec des chunks séparés.")
    except Exception as e:
        print(f"Erreur lors de la conversion du fichier PDF : {e}")

def upload_txtfile():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r', encoding="utf-8") as txt_file:
                text = txt_file.read()
            
            text = re.sub(r'\s+', ' ', text).strip()
            
            sentences = re.split(r'(?<=[.!?]) +', text)
            chunks = []
            current_chunk = ""
            for sentence in sentences:
                if len(current_chunk) + len(sentence) + 1 < 500:
                    current_chunk += (sentence + " ").strip()
                else:
                    chunks.append(current_chunk)
                    current_chunk = sentence + " "
            if current_chunk:
                chunks.append(current_chunk)
            
            with open("vault.txt", "a", encoding="utf-8") as vault_file:
                for chunk in chunks:
                    vault_file.write(chunk.strip() + "\n")
            
            print(f"Contenu du fichier texte ajouté à vault.txt.")
        except Exception as e:
            print(f"Erreur lors du traitement du fichier texte : {e}")

def upload_jsonfile():
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        try:
            with open(file_path, 'r', encoding="utf-8") as json_file:
                data = json.load(json_file)
            
            text = json.dumps(data, ensure_ascii=False)
            
            text = re.sub(r'\s+', ' ', text).strip()
            
            sentences = re.split(r'(?<=[.!?]) +', text)
            chunks = []
            current_chunk = ""
            for sentence in sentences:
                if len(current_chunk) + len(sentence) + 1 < 500:
                    current_chunk += (sentence + " ").strip()
                else:
                    chunks.append(current_chunk)
                    current_chunk = sentence + " "
            if current_chunk:
                chunks.append(current_chunk)
            
            with open("vault.txt", "a", encoding="utf-8") as vault_file:
                for chunk in chunks:
                    vault_file.write(chunk.strip() + "\n")
            
            print(f"Contenu du fichier JSON ajouté à vault.txt.")
        except Exception as e:
            print(f"Erreur lors du traitement du fichier JSON : {e}")

root = tk.Tk()
root.title("Upload .pdf, .txt, or .json")

specific_pdf_button = tk.Button(root, text="Convert Specific PDF", command=lambda: convert_specific_pdf_to_text("les-etoiles-presentation.pdf"))
specific_pdf_button.pack(pady=10)

txt_button = tk.Button(root, text="Upload Text File", command=upload_txtfile)
txt_button.pack(pady=10)

json_button = tk.Button(root, text="Upload JSON File", command=upload_jsonfile)
json_button.pack(pady=10)

root.mainloop()
