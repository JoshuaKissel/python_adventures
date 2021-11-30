import csv
import urllib.request
from pathvalidate import sanitize_filename

#imports csv, ffmpeg-python, sanatize_filename
with open ('CalTrans D10 Camera Evaluation - TrafficVision Suggestions.csv') as cameras: #opens the csv file
    reader = csv.reader(cameras) #reads csv file
    for row in reader: #for each row in the csv...
        rtsp = row[1] #the second column of the row is now keyed as rtsp
        name = row[0] #the firest column of the row is now keyed as name
        camera = sanitize_filename(name) #name is now sanitized for use as a filename and called camera
        try:
            urllib.request.urlretrieve(rtsp, camera +'.png')
        except Exception as e:
            print(e)
