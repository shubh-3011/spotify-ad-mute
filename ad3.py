import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Setup Spotify auth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id='add your client id',
    client_secret='add your client secret',
    redirect_uri='http://127.0.0.1:8888/callback',
    scope='user-read-playback-state'))

# Volume control
def get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, 1, None)
    return interface.QueryInterface(IAudioEndpointVolume)

volume_interface = get_volume_interface()

def mute_audio(mute=True):
    volume_interface.SetMute(mute, None)

def gradually_restore_volume(target_volume, steps=20, delay=0.1):
    volume_interface.SetMute(False, None)
    for i in range(1, steps + 1):
        volume_interface.SetMasterVolumeLevelScalar(target_volume * (i / steps), None)
        time.sleep(delay)

previous_volume = volume_interface.GetMasterVolumeLevelScalar()
ad_muted = False

while True:
    playback = sp.current_playback()

    if playback:
        content_type = playback['currently_playing_type']
        item = playback.get('item')

        # If ad
        if content_type == 'ad':
            if not ad_muted:
                previous_volume = volume_interface.GetMasterVolumeLevelScalar()
                mute_audio(True)
                ad_muted = True
                print("🔇 Ad detected. Muting audio...")

            # Check every 5 seconds until ad ends
            while True:
                time.sleep(5)
                playback = sp.current_playback()
                if playback and playback['currently_playing_type'] != 'ad':
                    print("🎵 Ad finished.")
                    gradually_restore_volume(previous_volume)
                    ad_muted = False
                    break
            continue

        # If song
        if item:
            name = item['name']
            duration_ms = item['duration_ms']
            progress_ms = playback['progress_ms']
            time_left = (duration_ms - progress_ms) / 1000

            print(f"🎶 Now playing: {name}")
            print(f"⏳ Time left: {time_left:.2f} seconds")

            if ad_muted:
                gradually_restore_volume(previous_volume)
                ad_muted = False

            # Sleep until last 2 seconds of the song
            if time_left > 2:
                time.sleep(time_left - 2)

            # Final check in last 2 seconds
            time.sleep(2)
        else:
            print("🔁 No track item info.")
            time.sleep(2)
    else:
        print("🚫 No playback detected.")
        time.sleep(2)
