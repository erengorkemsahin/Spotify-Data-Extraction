#!/usr/bin/env python3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import tkinter as tk
from tkinter import ttk
import calendar
import pyperclip

# Spotify API anahtarlarınızı burada tanımlayın
client_id = '6e75ecc3753e4c8ea91dfccf8c44855f'
client_secret = 'dcc2a429452c4d359fd2db3da7e9b1cd'

# Spotify API oturumunuzu oluşturun
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

tracks = None  # Başlangıçta tracks listesini tanımlayın

# Albüm bilgisini alacak fonksiyon
def get_album_info():
    album_id = album_id_entry.get()
    global tracks  # Fonksiyonun içinde global olarak kullanılacak

    try:
        album = sp.album(album_id)
        if album:
            release_date = album['release_date']
            release_year = release_date.split('-')[0]
            release_month = int(release_date.split('-')[1])
            month_name = calendar.month_name[release_month]
            release_day = release_date.split('-')[2]
            album_release_label.config(text=f"{month_name} {release_day}, {release_year}")
            label_info_label.config(text=f"{album['label']}")
            track_listbox.delete(0, tk.END)

            if combobox.get() == "SAYILI":
                tracks = album['tracks']['items']
                for i in range(len(tracks)):
                    track_name = tracks[i]['name']
                    track_listbox.insert(i, f"{i + 1}. {track_name}")
            else:
                track_listbox.delete(0, tk.END)
                for track in album['tracks']['items']:
                    track_name = track['name']
                    track_listbox.insert(tk.END, track_name)

            total_duration = 0
            album_name_label.config(text=f"{album['name']}")

            for track in tracks:
                track_duration_ms = track['duration_ms']
                track_duration_seconds = track_duration_ms / 1000
                total_duration += track_duration_seconds

            hours, remainder = divmod(total_duration, 3600)
            minutes, seconds = divmod(remainder, 60)
            total_duration_text = f"{int(hours)} Hour {int(minutes)} Min {int(seconds)} Sec"
            total_duration_label.config(text=f"{total_duration_text}")

            artist_name = album['artists'][0]['name']
            artist_name_label.config(text=f"{artist_name}")

        else:
            album_name_label.config(text="Belirtilen albüm bulunamadı")
    except Exception as e:
        album_name_label.config(text=f"Albüm bilgilerini alırken bir hata oluştu: {str(e)}")

# Albüm adını panoya kopyala fonksiyonu
def copy_album_name():
    album_name_text = album_name_label.cget("text")
    pyperclip.copy(album_name_text)
    messagebox.showinfo("Kopyalandı", "Albüm adını panoya kopyalandı!")

# Bütün şarkıları kopyala fonksiyonu
def copy_all_tracks():
    all_tracks = track_listbox.get(0, tk.END)
    tracks_text = "\n".join(all_tracks)
    pyperclip.copy(tracks_text)
    messagebox.showinfo("Kopyalandı", "Bütün şarkılar panoya kopyalandı!")

# Çıkış tarihini panoya kopyala fonksiyonu
def copy_release_date():
    release_date_text = album_release_label.cget("text")
    pyperclip.copy(release_date_text)
    messagebox.showinfo("Kopyalandı", "Çıkış tarihi panoya kopyalandı!")

# Toplam süreyi panoya kopyala fonksiyonu
def copy_total_duration():
    total_duration_text = total_duration_label.cget("text")
    pyperclip.copy(total_duration_text)
    messagebox.showinfo("Kopyalandı", "Toplam süre panoya kopyalandı!")

# Yapımcı şirket bilgisini panoya kopyala fonksiyonu
def copy_label_info():
    label_info_text = label_info_label.cget("text")
    pyperclip.copy(label_info_text)
    messagebox.showinfo("Kopyalandı", "Yapımcı şirket bilgisi panoya kopyalandı!")

# Şarkıcı adını panoya kopyala fonksiyonu
def copy_artist_name():
    artist_name_text = artist_name_label.cget("text")
    pyperclip.copy(artist_name_text)
    messagebox.showinfo("Kopyalandı", "Şarkıcı adı panoya kopyalandı!")

# Tkinter penceresi oluşturun
root = tk.Tk()
root.title("Spotify Albüm Bilgisi")


# Albüm ID'si giriş kutusu
album_id_label = tk.Label(root, text="Spotify Albüm ID'si:")
album_id_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
album_id_entry = tk.Entry(root)
album_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky='e')

choices = ["SAYISIZ", "SAYILI"]
combobox = ttk.Combobox(root, values=choices)
combobox.grid(row=7, column=1, padx=10, pady=5, sticky='w')
combobox.set("SAYISIZ")  # Başlangıçta seçili olan seçenek

# Bilgi gösterme alanları
album_name_label = tk.Label(root, text="", font=("Helvetica", 12))
album_name_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='w')

album_release_label = tk.Label(root, text="", font=("Helvetica", 10))
album_release_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky='w')

label_info_label = tk.Label(root, text="", font=("Helvetica", 10))
label_info_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky='w')

total_duration_label = tk.Label(root, text="", font=("Helvetica", 10))
total_duration_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky='w')

artist_name_label = tk.Label(root, text="", font=("Helvetica", 10))
artist_name_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky='w')

# Şarkı listesi
track_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, font=("Helvetica", 10))
track_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky='w')

# Bilgi çekme düğmesi
get_info_button = tk.Button(root, text="Bilgi Çek", command=get_album_info, font=("Helvetica", 10))
get_info_button.grid(row=0, column=2, padx=10, pady=5, sticky='w')

# Çıkış tarihini panoya kopyala düğmesi
copy_release_date_button = tk.Button(root, text="Çıkış Tarihini Kopyala", command=copy_release_date)
copy_release_date_button.grid(row=5, column=2, padx=10, pady=5, sticky='w')

# Toplam süreyi panoya kopyala düğmesi
copy_total_duration_button = tk.Button(root, text="Toplam Süreyi Kopyala", command=copy_total_duration)
copy_total_duration_button.grid(row=4, column=2, padx=10, pady=5, sticky='w')

# Yapımcı şirket bilgisini panoya kopyala düğmesi
copy_label_info_button = tk.Button(root, text="Yapımcı Şirketi Kopyala", command=copy_label_info)
copy_label_info_button.grid(row=3, column=2, padx=10, pady=5, sticky='w')

# Şarkıcı adını panoya kopyala düğmesi
copy_artist_name_button = tk.Button(root, text="Şarkıcı Adını Kopyala", command=copy_artist_name)
copy_artist_name_button.grid(row=2, column=2, padx=10, pady=5, sticky='w')

# Bütün şarkıları kopyala düğmesi
copy_all_tracks_button = tk.Button(root, text="Bütün Şarkıları Kopyala", command=copy_all_tracks)
copy_all_tracks_button.grid(row=6, column=2, padx=10, pady=5, sticky='w')

# Albüm adnı panoya kopyala düğmesi
copy_album_name_button = tk.Button(root, text="Albüm Adını Kopyala", command=copy_album_name)
copy_album_name_button.grid(row=1, column=2, padx=10, pady=5, sticky='w')

root.mainloop()
