import csv
import ffmpeg
from pathvalidate import sanitize_filename

#imports csv, ffmpeg-python, sanatize_filename
with open ('cameras.csv') as cameras: #opens the csv file
    reader = csv.reader(cameras) #reads csv file
    for row in reader: #for each row in the csv...
        rtsp = row[1] #the second column of the row is now keyed as rtsp
        name = row[0] #the firest column of the row is now keyed as name
        camera = sanitize_filename(name) #name is now sanitized for use as a filename and called camera

        (
            ffmpeg #call ffmpeg
            .input(rtsp, ss=.05) #input the second column of the row, and the amount of time into the video at which to grab a screenshot
            .output(camera + '.png', vframes=1) #output a sanitizedfile name.png, and the amount of frames desired
            .run() #run ffmpeg 
        )