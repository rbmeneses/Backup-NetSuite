import requests
import os
import logging
from requests_oauthlib import OAuth1
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

class NetSuiteBackup:
    def __init__(self, account_id, consumer_key, consumer_secret, token_key, token_secret, local_download_path):
        self.account_id = account_id.replace('_', '-').lower()
        self.local_download_path = local_download_path
        self.auth = OAuth1(consumer_key, consumer_secret, token_key, token_secret, signature_method='HMAC-SHA256')
        self.base_url = f"https://{self.account_id}.restlets.api.netsuite.com/app/site/hosting/restlet.nl"
        self._setup_logging()
        self.root_folder_id = self._get_root_folder_id()  # Get root folder ID

    def _setup_logging(self):
        log_dir = os.path.join(self.local_download_path, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler(log_file), logging.StreamHandler()])
        self.logger = logging.getLogger(__name__)

    def _get_root_folder_id(self):
        url = f"{self.base_url}?script=3500&deploy=1&recordtype=file"  # Correct URL for root folder
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        root_folder_id = response.json().get('id')
        self.logger.info(f"Root folder ID: {root_folder_id}")
        return root_folder_id

    def get_folder_contents(self, folder_id):
        url = f"{self.base_url}?script=3500&deploy=1&recordtype=file&folder={folder_id}"
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        return response.json().get('items', [])

    def download_file(self, file_id, file_name, local_path):
        url = f"{self.base_url}?script=3500&deploy=1&recordtype=file&id={file_id}"
        response = requests.get(url, auth=self.auth, stream=True)  # Stream for large files
        response.raise_for_status()

        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):  # Download in chunks
                f.write(chunk)
        self.logger.info(f"Downloaded: {file_name}")

    def backup_folder(self, folder_id, local_folder_path):
        try:
            os.makedirs(local_folder_path, exist_ok=True)  # Create local folder
            contents = self.get_folder_contents(folder_id)

            for item in contents:
                if item['recordType'] == 'folder':
                    new_local_path = os.path.join(local_folder_path, item['name'])
                    self.backup_folder(item['id'], new_local_path)  # Recursive call
                elif item['recordType'] == 'file':
                    file_path = os.path.join(local_folder_path, item['name'])
                    self.download_file(item['id'], item['name'], file_path)
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error backing up folder {folder_id}: {e}")
            messagebox.showerror("Erro", f"Falha no backup: {e}") # Show error in GUI
            raise # Re-raise the exception to stop the process

    def start_backup(self):
        if self.root_folder_id:
            self.backup_folder(self.root_folder_id, self.local_download_path)
            self.logger.info("Backup completed.")
        else:
            self.logger.error("Could not retrieve root folder ID. Backup failed.")
            messagebox.showerror("Erro", "Não foi possível obter o ID da pasta raiz. Backup falhou.")


def iniciar_interface():
    def iniciar_backup():
        try:
            account_id = entry_account.get()
            consumer_key = entry_consumer_key.get()
            consumer_secret = entry_consumer_secret.get()
            token_key = entry_token_key.get()
            token_secret = entry_token_secret.get()
            folder_path = entry_folder_path.get()

            if not all([account_id, consumer_key, consumer_secret, token_key, token_secret, folder_path]):
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
                return

            backup = NetSuiteBackup(
                account_id=account_id,
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                token_key=token_key,
                token_secret=token_secret,
                local_download_path=folder_path
            )
            backup.start_backup()
            messagebox.showinfo("Sucesso", "Backup concluído com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha no backup: {e}")

    def escolher_pasta():
        caminho = filedialog.askdirectory()
        entry_folder_path.delete(0, tk.END) # Clear previous entry
        entry_folder_path.insert(0, caminho) # Insert selected path

    root = tk.Tk()
    root.title("Backup NetSuite")
    root.geometry("400x450") # Increased height

    # Labels and Entries for credentials
    tk.Label(root, text="Account ID:").pack()
    entry_account = tk.Entry(root)
    entry_account.pack()

    tk.Label(root, text="Consumer Key:").pack()
    entry_consumer_key = tk.Entry(root)
    entry_consumer_key.pack()

    tk.Label(root, text="Consumer Secret:").pack()
    entry_consumer_secret = tk.Entry(root)
    entry_consumer_secret.pack()

    tk.Label(root, text="Token Key:").pack()
    entry_token_key = tk.Entry(root)
    entry_token_key.pack()

    tk.Label(root, text="Token Secret:").pack()
    entry_token_secret = tk.Entry(root)
    entry_token_secret.pack()

    tk.Label(root, text="Pasta de Destino:").pack()
    entry_folder_path = tk.Entry(root) # Entry to show selected path
    entry_folder_path.pack()
    tk.Button(root, text="Escolher Pasta", command=escolher_pasta).pack()

    tk.Button(root, text="Iniciar Backup", command=iniciar_backup).pack()

    root.mainloop()

if __name__ == '__main__':
    iniciar_interface()