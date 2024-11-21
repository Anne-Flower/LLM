import requests

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
        print(f"Fichier téléchargé localement sous : {local_file_path}")
    except Exception as e:
        print(f"Erreur lors du téléchargement depuis Google Drive : {e}")

if __name__ == "__main__":
    file_id = "16aYMvO1qfJ0qV94tnc97UYkUJ_hHwpNf"
    local_file_path = "les-etoiles-presentation.pdf"

    download_from_drive(file_id, local_file_path)
