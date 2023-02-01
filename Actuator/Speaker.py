from ytmusicapi import YTMusic
import subprocess
from os import listdir
from os.path import isfile, join



class speaker:
    def __init__(self, mac_address = "DD:AB:B0:E5:36:D8"):
        self.mac = mac_address
        self.MySpeaker.start_connection()
    
    def start_connection(self):
        subprocess.call("systemctl --user start pulseaudio", shell=True)
        subprocess.call("bluetoothctl connect " + self.mac, shell=True)

    def generate_url(self,songname):
        ytmusic = YTMusic('headers_auth.json')
        # playlistId = ytmusic.create_playlist("test", "test description")
        search_results = ytmusic.search(songname)
        print([search_results[0]['videoId']])
        url = "https://music.youtube.com/watch?v=" + [search_results[0]['videoId']][0]
        return url
    
    def download_song_to_directory(self, songName, directory="/home/pi/Music"):
        url = self.generate_url(songName)
        subprocess.call("cd " + directory, shell=True)
        subprocess.call("youtube-dl -x --audio-format wav " + url, shell=True)

    def playSong(self, songName="飘移"):
        onlyfiles = [f for f in listdir("/home/pi/Music")]
        print(onlyfiles)

        if not any(songName in fileName for fileName in onlyfiles):
           self.download_song_to_directory(songName)
             
        for fileName in onlyfiles: 
            if songName in fileName: songFile = fileName
        print("playing ", songFile)
        subprocess.call("paplay /home/pi/Music/" + songFile + ".wav", shell=True)


if __name__ == "__main__":
    MySpeaker = speaker()
    MySpeaker.start_connection()
    MySpeaker.playSong("飘移")




# ytmusic.add_playlist_items(playlistId, [search_results[0]['videoId']])