from speedtest import Speedtest

speed = speedtest.speedtest()
download_speed = speed.download()
upload_speed = speed.upload()
print(f'The download speed is {download_speed}')
print(f'The upload speed is {upload_speed}')


