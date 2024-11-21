import os
import tkinter as tk
import PyPDF2
import re
import requests

# Télécharger un fichier depuis un lien public Google Drive
def download_from_drive(file_id, local_file_path):
    try:
        drive_url = f"https://drive.google.com/uc?id={file_id}&export=download"
        session = requests.Session()
        response = session.get(drive_url, stream=True)
        
        # Gérer les éventuels avertissements de téléchargement
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                drive_url = f"https://drive.google.com/uc?export=download&id={file_id}&confirm={value}"
                response = session.get(drive_url, stream=True)
                break

        # Écrire le contenu téléchargé dans un fichier local
        with open(local_file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=32768):
                if chunk:
                    f.write(chunk)
        print(f"Fichier téléchargé localement sous : {local_file_path}")
    except Exception as e:
        print(f"Erreur lors du téléchargement depuis Google Drive : {e}")

# Convertir un PDF local en texte et l'ajouter à vault.txt
def convert_specific_pdf_to_text(file_path="les-etoiles-presentation.pdf"):
    try:
        if not os.path.exists(file_path):
            print(f"Erreur : le fichier {file_path} est introuvable.")
            return
        
        # Lire le fichier PDF
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ''
            for page in pdf_reader.pages:
                if page.extract_text():
                    text += page.extract_text() + " "
            
            # Nettoyer et découper le texte en chunks
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
            
            # Ajouter les chunks dans vault.txt
            with open("vault.txt", "a", encoding="utf-8") as vault_file:
                for chunk in chunks:
                    vault_file.write(chunk.strip() + "\n")
            
            print(f"PDF '{file_path}' ajouté à vault.txt avec des chunks séparés.")
    except Exception as e:
        print(f"Erreur lors de la conversion du fichier PDF : {e}")

# Télécharger et traiter un PDF depuis Google Drive
def convert_pdf_from_drive(file_id, local_file_path="les-etoiles-presentation.pdf"):
    download_from_drive(file_id, local_file_path)
    convert_specific_pdf_to_text(local_file_path)

# Interface graphique avec Tkinter
root = tk.Tk()
root.title("Traitement des fichiers Google Drive")

# Bouton pour convertir un PDF spécifique
specific_pdf_button = tk.Button(
    root, 
    text="Convert Specific PDF", 
    command=lambda: convert_specific_pdf_to_text("les-etoiles-presentation.pdf")
)
specific_pdf_button.pack(pady=10)

# Bouton pour télécharger et convertir un fichier Google Drive
read_from_drive_button = tk.Button(
    root, 
    text="Read PDF from Drive", 
    command=lambda: convert_pdf_from_drive("16aYMvO1qfJ0qV94tnc97UYkUJ_hHwpNf")
)
read_from_drive_button.pack(pady=10)

root.mainloop()
