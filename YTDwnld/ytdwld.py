import threading
import tkinter as tk
from tkinter import messagebox, filedialog
from pytube import YouTube

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Téléchargeur de Vidéos YouTube")
        self.root.geometry("500x300")
        self.root.config(bg="lightblue")

        self.url_label = tk.Label(root, text="URL de la vidéo YouTube :")
        self.url_label.pack(pady=10)

        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack(pady=5)

        self.path_label = tk.Label(root, text="Spécifiez le Chemin de sauvegarde :")
        self.path_label.pack(pady=10)

        self.path_entry = tk.Entry(root, width=50)
        self.path_entry.pack(pady=5)

        self.browse_button = tk.Button(root, text="Parcourir", command=self.browse)
        self.browse_button.pack(pady=5)

        self.download_button = tk.Button(root, text="Télécharger", command=self.start_download)
        self.download_button.pack(pady=20)

    def browse(self):
        download_directory = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, download_directory)

    def start_download(self):
        url = self.url_entry.get()
        save_path = self.path_entry.get()
        
        if url == "" or save_path == "":
            messagebox.showwarning("Avertissement", "Veuillez remplir tous les champs")
            return

        threading.Thread(target=self.download_youtube_video, args=(url, save_path)).start()

    def download_youtube_video(self, url, save_path):
        try:
            yt = YouTube(url, on_progress_callback=self.show_progress)
            stream = yt.streams.get_highest_resolution()
            
            self.download_button.config(state=tk.DISABLED)
            stream.download(save_path)
            messagebox.showinfo("Succès", f"Téléchargement réussi ! : {yt.title}")
            self.download_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")
            self.download_button.config(state=tk.NORMAL)

    def show_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        self.root.title(f"Téléchargeur de Vidéos YouTube - {int(percentage)}% téléchargé")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()
