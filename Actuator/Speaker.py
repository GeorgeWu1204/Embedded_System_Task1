from ytmusicapi import YTMusic
import subprocess
from os import listdir,kill
from os.path import isfile, join
import signal



class speaker:
    def __init__(self, mac_address = "DD:AB:B0:E5:36:D8"):
        self.mac = mac_address
        self.start_connection()
        self.pid = None
    
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
    
    def download_song_to_directory(self, songName, directory="/home/pi/Music/"):
        url = self.generate_url(songName)
        subprocess.call("pwd", shell=True, cwd="/home/pi/Music/")
        subprocess.call("youtube-dl -x --audio-format wav " + url, shell=True, cwd="/home/pi/Music/")

    def checkInLocal(self, songName="夜曲"):
        onlyfiles = [f for f in listdir("/home/pi/Music/")]
        print(onlyfiles)
        if not any(songName in fileName for fileName in onlyfiles):
            print("Downloading")
            self.download_song_to_directory(songName)
            print("Download Complete")
            return True
        return True

    def playSong(self, songName="夜曲"):
        try:
            for fileName in [f for f in listdir("/home/pi/Music/")]: 
                if songName in fileName: songFile = fileName

            songFile = songFile.replace(" ", "\ ")
            print("paplay /home/pi/Music/" + songFile)
            process = subprocess.Popen(['paplay', '/home/pi/Music/'+songFile], stdout=subprocess.PIPE) 
            self.pid = process.pid
        except:
            print("The song is not in database")

    def kill(self):
        try:
            subprocess.call("kill " + str(self.pid), shell=True)
        except:
            print("No song is playing")
    

if __name__ == "__main__":
    MySpeaker = speaker()
    MySpeaker.start_connection()
    MySpeaker.playSong(songName="夜的第七章")




# ytmusic.add_playlist_items(playlistId, [search_results[0]['videoId']])