
import webbrowser
import argparse

def weather_function(city):
	webbrowser.open('https://wttr.in/' + city.replace(" ", "+"))
	print('https://wttr.in/' + city)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-city', help='Enter City', default="Salt Lake City")

	args=parser.parse_args()
	weather_function(args.city)
# 	parser = argparse.ArgumentParser()
# 	parser.add_argument('-city', help='Enter city', default='SaltLakeCity')
# 	args=parser.parse_args()


# resp = requests.get(f'https://wttr.in/{sys.argv[1].replace(" ", "+")}')


# # html_file = open('weather.html','w')
# # html_file.write(resp.text)
# # html_file.close()
# print(resp)