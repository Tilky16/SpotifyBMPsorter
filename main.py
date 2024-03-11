import tkinter as tk
from tkinter import font as tkFont, messagebox
import webbrowser
import json
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CREDENTIALS_FILE = 'spotify_credentials.json'
BACKGROUND_GIF = 'bg.gif'  # Ensure this GIF is in the same directory as your script

class SpotifySorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spotify Playlist Sorter")
        self.root.geometry("768x432")  # Size to match the GIF

        # Set up the GIF background
        self.bg_image = tk.PhotoImage(file=BACKGROUND_GIF)
        self.bg_label = tk.Label(root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Modern font style
        self.customFont = tkFont.Font(family="Helvetica", size=12, weight="bold")

        # Load saved credentials, if any
        self.credentials = self.load_credentials()

        # Entry field for the Spotify playlist URL
        self.input_field = tk.Entry(root, fg="black", font=self.customFont, highlightthickness=2, highlightbackground="white", highlightcolor="white")
        self.input_field.place(x=384-150, y=216-20, width=300, height=40)

        # Button to trigger the sorting of the playlist
        self.submit_button = self.create_rounded_button("Sort Playlist", self.sort_playlist, x=384-75, y=256, width=150, height=40)

        # Button to open the settings window for Spotify API credentials
        self.settings_button = self.create_rounded_button("Settings", self.open_settings, x=20, y=392, width=100, height=40)

    def sort_playlist(self):
        if not all([self.credentials.get(key) for key in ['client_id', 'client_secret', 'redirect_uri']]):
            messagebox.showerror("Error", "Spotify API credentials are not set. Please configure them in Settings.")
            return

        playlist_url = self.input_field.get()
        if not playlist_url:
            messagebox.showerror("Error", "Please enter a Spotify playlist URL.")
            return

        # Initialize the Spotify client with the stored credentials
        spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self.credentials['client_id'],
            client_secret=self.credentials['client_secret'],
            redirect_uri=self.credentials['redirect_uri'],
            scope='playlist-modify-public playlist-read-private'
        ))

        try:
            playlist_id = playlist_url.split('playlist/')[1].split('?')[0]
            results = spotify_client.playlist_tracks(playlist_id)
            tracks = [item['track']['id'] for item in results['items'] if item['track']]
            features = spotify_client.audio_features(tracks)
            tracks_with_bpm = {track: feature['tempo'] for track, feature in zip(tracks, features) if feature}

            # Sort the tracks by BPM
            sorted_tracks = sorted(tracks_with_bpm, key=tracks_with_bpm.get)

            # Create a new playlist with sorted tracks
            user_id = spotify_client.me()['id']
            new_playlist = spotify_client.user_playlist_create(user_id, 'Sorted Playlist', public=True)
            spotify_client.playlist_add_items(new_playlist['id'], sorted_tracks)

            # Open the new playlist in the web browser
            webbrowser.open(new_playlist['external_urls']['spotify'])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to sort the playlist: {e}")

    def load_credentials(self):
        if os.path.exists(CREDENTIALS_FILE):
            with open(CREDENTIALS_FILE, 'r') as file:
                return json.load(file)
        return {}

    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")

        # Function to save the entered credentials
        def save_credentials():
            self.credentials = {
                'client_id': client_id_field.get(),
                'client_secret': client_secret_field.get(),
                'redirect_uri': redirect_uri_field.get()
            }
            with open(CREDENTIALS_FILE, 'w') as file:
                json.dump(self.credentials, file)
            messagebox.showinfo("Info", "Credentials saved successfully.")
            settings_window.destroy()

        # Setting fields for Spotify API credentials
        tk.Label(settings_window, text="Client ID:", font=self.customFont).grid(row=0, column=0, padx=10, pady=10)
        client_id_field = tk.Entry(settings_window, font=self.customFont)
        client_id_field.insert(0, self.credentials.get('client_id', ''))
        client_id_field.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(settings_window, text="Client Secret:", font=self.customFont).grid(row=1, column=0, padx=10, pady=10)
        client_secret_field = tk.Entry(settings_window, font=self.customFont)
        client_secret_field.insert(0, self.credentials.get('client_secret', ''))
        client_secret_field.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(settings_window, text="Redirect URI:", font=self.customFont).grid(row=2, column=0, padx=10, pady=10)
        redirect_uri_field = tk.Entry(settings_window, font=self.customFont)
        redirect_uri_field.insert(0, self.credentials.get('redirect_uri', ''))
        redirect_uri_field.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(settings_window, text="Save", font=self.customFont, command=save_credentials).grid(row=3, column=1, pady=20)

    def create_rounded_button(self, text, command, x, y, width, height):
        canvas = tk.Canvas(self.root, width=width, height=height, bg="gray", bd=0, highlightthickness=0)
        canvas.place(x=x, y=y)
        canvas.create_oval(10, 10, 30, 30, fill="white", outline="white")
        canvas.create_oval(width-30, 10, width-10, 30, fill="white", outline="white")
        canvas.create_rectangle(20, 10, width-20, 30, fill="white", outline="white")
        button = tk.Label(canvas, text=text, font=self.customFont, fg="black", bg="white")
        button.bind("<Button-1>", lambda e: command())
        button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        return canvas

if __name__ == "__main__":
    root = tk.Tk()
    app = SpotifySorterApp(root)
    root.mainloop()
