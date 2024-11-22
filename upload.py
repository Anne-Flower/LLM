import os
import tkinter as tk
from tkinter import simpledialog
import PyPDF2
import re
import requests
import json


def download_from_drive(file_id, local_file_path):
    try:
        drive_url = f"https://drive.google.com/uc?id={file_id}&export=download"
        session = requests.Session()
        response = session.get(drive_url, stream=True)

        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                drive_url = f"https://drive.google.com/uc?export=download&id={file_id}&confirm={value}"
                response = session.get(drive_url, stream=True)
                break

        with open(local_file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=32768):
                if chunk:
                    f.write(chunk)
        print(f"File downloaded locally as: {local_file_path}")
    except Exception as e:
        print(f"Error downloading from Google Drive: {e}")


def convert_specific_pdf_to_text(file_path="sample.pdf"):
    try:
        if not os.path.exists(file_path):
            print(f"Error: file {file_path} not found.")
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

            print(f"PDF '{file_path}' added to vault.txt in chunks.")
    except Exception as e:
        print(f"Error converting PDF: {e}")


def convert_pdf_from_drive(file_id, local_file_path="sample.pdf"):
    download_from_drive(file_id, local_file_path)
    convert_specific_pdf_to_text(local_file_path)


def query_llm(question, context="", temperature=0.7):
    if context:
        print("**Mode: With RAG**")
        prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    else:
        print("**Mode: Without RAG**")
        prompt = f"Question: {question}\nAnswer:"

    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama2",
        "prompt": prompt,
        "options": {"temperature": temperature}
    }

    try:
        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()

        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    json_line = json.loads(line.decode("utf-8"))
                    if "response" in json_line:
                        full_response += json_line["response"]
                        print(json_line["response"], end="")
                except json.JSONDecodeError as e:
                    print(f"Erreur de parsing JSON : {e}")
                    print(f"Ligne problématique : {line.decode('utf-8')}")
        
        return full_response.strip()
    except requests.exceptions.RequestException as e:
        print(f"Error during API call: {e}")
        return "An error occurred while generating the response."



def get_context_from_vault(question, vault_file="vault.txt"):
    try:
        if not os.path.exists(vault_file):
            print(f"Error: {vault_file} not found.")
            return ""

        with open(vault_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

        relevant_lines = [line for line in lines if any(word.lower() in line.lower() for word in question.split())]
        context = " ".join(relevant_lines[:5])
        if not context:
            print("No relevant context found.")
        return context

    except Exception as e:
        print(f"Error searching context in vault.txt: {e}")
        return ""


def demonstrate_rag_vs_no_rag():
    print("Choose mode:")
    print("1: Without RAG (no documents)")
    print("2: With RAG (retrieve from vault.txt)")
    mode = input("Enter your choice (1 or 2): ").strip()

    question = input("Enter your question: ").strip()
    try:
        temperature = float(input("Enter temperature (e.g., 0.7): ").strip())
    except ValueError:
        print("Invalid temperature. Using default value of 0.7.")
        temperature = 0.7

    if mode == "1":
        answer = query_llm(question, context="", temperature=temperature)
    elif mode == "2":
        context = get_context_from_vault(question)
        answer = query_llm(question, context=context, temperature=temperature)
    else:
        print("Invalid choice. Exiting.")
        return

    print("\n--- Answer ---")
    print(answer)


# Gestion de la température (ajoutée)
def set_temperature():
    global user_temperature
    try:
        temp = simpledialog.askfloat("Temperature", "Enter a temperature value (e.g., 0.7):")
        if temp is not None:
            user_temperature = temp
            print(f"Temperature set to {user_temperature}")
        else:
            print("Temperature unchanged.")
    except ValueError:
        print("Invalid temperature input. Please try again.")

root = tk.Tk()
root.title("Google Drive File Processing")

specific_pdf_button = tk.Button(
    root, 
    text="Convert Specific PDF", 
    command=lambda: convert_specific_pdf_to_text("sample.pdf")
)
specific_pdf_button.pack(pady=10)

read_from_drive_button = tk.Button(
    root, 
    text="Read PDF from Drive", 
    command=lambda: convert_pdf_from_drive("16aYMvO1qfJ0qV94tnc97UYkUJ_hHwpNf")
)
read_from_drive_button.pack(pady=10)

demonstrate_button_rag = tk.Button(
    root, 
    text="Demonstrate RAG vs No RAG", 
    command=demonstrate_rag_vs_no_rag
)
demonstrate_button_rag.pack(pady=10)

demonstrate_button_temperature = tk.Button(
    root, 
    text="Demonstrate RAG vs No RAG with temperature", 
    command=demonstrate_rag_vs_no_rag
)
demonstrate_button_temperature.pack(pady=10)

root.mainloop()
