import os
import subprocess

# Set the Bluetooth MAC address of the speaker
speaker_mac = "00:11:22:33:44:55"

# Connect to the speaker
subprocess.call("sudo bluetoothctl", shell=True)
subprocess.call("connect " + speaker_mac, shell=True)

# Send the song to the speaker
os.system("sudo sendto -t a2dp " + speaker_mac + " /path/to/song.mp3")