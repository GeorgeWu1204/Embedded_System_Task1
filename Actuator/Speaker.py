from ytmusicapi import YTMusic
import subprocess
from os import listdir,kill, environ
from os.path import isfile, join
import signal
import fnmatch
import re
import difflib


class speaker:
    def __init__(self, mac_address = "DD:AB:B0:E5:36:D8"):
        self.mac = mac_address
        self.start_connection()
        self.pid = None
    
    def start_connection(self):
        subprocess.call("systemctl --user start pulseaudio", shell=True)
        subprocess.call("bluetoothctl connect " + self.mac, shell=True)

    def generate_url(self,songname):
        try:
            ytmusic = YTMusic('headers_auth.json')
            # playlistId = ytmusic.create_playlist("test", "test description")
            search_results = ytmusic.search(songname)
            url = "https://music.youtube.com/watch?v=" + [search_results[0]['videoId']][0]
            print(url)
            return url
        except:
            print("Download fail")
            return None

    

    def regexMatching(self,songName, onlyfilesLst):
        firstWord = songName.split(" ")[0]
        pattern = r"^" + firstWord + ".*\.wav"
        regex = re.compile(pattern, re.IGNORECASE)
        for fileName in onlyfilesLst:
            if regex.match(fileName):
                return [True, fileName]
        return [False, None]

    def download_song_to_directory(self, songName, directory="/home/pi/Music/"):
        url = self.generate_url(songName)
        subprocess.call("pwd", shell=True, cwd="/home/pi/Music/")
        subprocess.call("youtube-dl -x --audio-format wav " + url, shell=True, cwd="/home/pi/Music/")
        try:
            onlyfiles = [f for f in listdir("/home/pi/Music/")]
            match = difflib.get_close_matches(songName, listdir("/home/pi/Music/"))
            condition, File = self.regexMatching(songName, onlyfiles)

            if match == [] and condition == False:
                print("Downloading: ", songName)
                self.download_song_to_directory(songName)

            _ , File = self.regexMatching(songName, onlyfiles)
            File = File.replace(" ", "\ ")
            songName = songName.replace(" ", "")
            print("mv " + File + " " + songName)
            subprocess.call("mv " + File + " " + songName + ".wav", shell=True, cwd="/home/pi/Music/")
        except:
            print("File renaming failed")

    def checkInLocal(self, songName="夜曲"):
        onlyfiles = [f for f in listdir("/home/pi/Music/")]
        songInData = songName.replace(" ", "")
        match = difflib.get_close_matches(songInData, listdir("/home/pi/Music/"))
        condition, File = self.regexMatching(songInData, onlyfiles)

        if match == [] and condition == False:
            print("Downloading: ", songName)
            self.download_song_to_directory(songName)

        _ , File = self.regexMatching(songInData, onlyfiles)
        print("Song", File, "is in the dataset")
        return True 


    def playSong(self, songName="夜的第七章"):
        try:
            for fileName in [f for f in listdir("/home/pi/Music/")]: 
                songInData = songName.replace(" ", "")
                print(songInData)
                pattern = r"^" + songInData + ".*\.wav"
                regex = re.compile(pattern, re.IGNORECASE)
                if regex.match(fileName):
                    songFile = fileName
                
            # songFile = songFile.replace(" ", "\ ")
            print("paplay /home/pi/Music/" + songFile)

            # environment = environ.copy()
            process = subprocess.Popen(['paplay', '/home/pi/Music/' + songFile], stdout=subprocess.PIPE) 
            # process.communicate()
            # print(environ)
            self.pid = process.pid

        except:
            print("The song", songName, " is not in database")

    def kill(self):
        try:
            subprocess.call("kill " + str(self.pid), shell=True)
        except:
            print("No song is playing")
    

if __name__ == "__main__":
    MySpeaker = speaker()
    MySpeaker.start_connection()
    # MySpeaker.download_song_to_directory("Something Just Like This")
    songName = "Legend Never Die"
    MySpeaker.checkInLocal(songName)
    MySpeaker.playSong(songName)
    MySpeaker.kill()
    
    # MySpeaker.playSong()
    




# ytmusic.add_playlist_items(playlistId, [search_results[0]['videoId']])