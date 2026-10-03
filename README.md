# spotify-ad-mute

A Python script that automatically **mutes Spotify while an advertisement is playing** and
unmutes it again when your music resumes. Currently works on **Windows**.

## How it works

The script watches the Spotify window title through the Windows API. When the title indicates an
advert, it mutes Spotify / the system volume; when the advert ends, it restores the previous
volume.

## Setup

1. Install the dependencies used at the top of `ad3.py`.
2. Add your **own** Spotify API credentials in `ad3.py` (`CLIENT_ID` / `CLIENT_SECRET`).
   Do not commit real credentials.
3. Run it:
   ```
   python ad3.py
   ```

## Notes

- Windows only.
- Requires an active Spotify session.
- Bring your own API credentials.

## Stack

Python, Spotify Web API, Windows media controls
