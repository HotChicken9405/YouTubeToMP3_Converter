import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import yt_dlp
import threading

def download_mp3():
    url = link_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please paste a YouTube link")
        return

    status_label.config(text="Downloading...")
    progress_bar['value'] = 0
    download_button.config(state='disabled')

    def progress_hook(d):
        if d['status'] == 'downloading':
            # Extract percentage
            percent_str = d.get('_percent_str', '0%').replace('%', '').strip()
            try:
                percent = float(percent_str)
                progress_bar['value'] = percent
                status_label.config(text=f"Downloading... {percent:.1f}%")
            except:
                pass
        elif d['status'] == 'finished':
            status_label.config(text="Converting to MP3...")
            progress_bar['value'] = 100

    def task():
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': '%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'progress_hooks': [progress_hook],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            status_label.config(text="Download completed ✅")
            progress_bar['value'] = 100
            messagebox.showinfo("Success", "MP3 downloaded successfully!")

        except Exception as e:
            status_label.config(text="Error ❌")
            messagebox.showerror("Error", str(e))
        
        finally:
            download_button.config(state='normal')

    threading.Thread(target=task).start()


app = tk.Tk()
app.title("YouTube → MP3")
app.geometry("420x230")
app.resizable(False, False)

tk.Label(app, text="Paste YouTube link:").pack(pady=10)
link_entry = tk.Entry(app, width=55)
link_entry.pack()

download_button = tk.Button(app, text="Download MP3", command=download_mp3)
download_button.pack(pady=15)

progress_bar = ttk.Progressbar(app, length=380, mode='determinate')
progress_bar.pack(pady=5)

status_label = tk.Label(app, text="Waiting...")
status_label.pack()

app.mainloop()

