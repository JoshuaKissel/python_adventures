import pandas as pd


read_file = pd.read_csv (r'C:\Users\12157\Documents\GitHub\tv-zim-readonly\expirations.txt', header=None)
read_file.columns = ['first_column']
read_file = read_file['first_column'].str.split(expand=True)
read_file['Expires_on'] = read_file[0] + " " + read_file[1]
read_file['Licenses'] = read_file[3] + " " + read_file[4]
read_file['Deployment_ID'] = read_file[5] + " " + read_file[6]
read_file['Date'] = read_file[2]
read_file = read_file.drop(read_file.columns[[0, 1, 2, 3, 4, 5, 6, 7]], axis=1)

column_titles = ['Expires_on', 'Date' , 'Deployment_ID', 'Licenses']
read_file = read_file.reindex(columns=column_titles)
print(read_file.head(10))