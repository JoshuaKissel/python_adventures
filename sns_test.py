import seaborn as sns
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
from incidents_report import create_incident_reports
from datetime import datetime
from matplotlib.offsetbox import AnchoredText


#per_camera= pd.read_excel('incident_report_per_camera.xlsx')
#weekly_inc = pd.read_excel('incident_report_per_dow.xlsx')
#timestamp = pd.read_excel('incidents_by_timestamp.xlsx')
per_camera = pd.read_csv('incident_report_per_camera.csv', delimiter=',')
weekly_inc = pd.read_csv('incident_report_per_dow_in_ALL.csv', delimiter=',')
timestamp = pd.read_csv('incidents_by_timestamp.csv', delimiter=',')
#pd = per_camera.sort_values(by=['Number times camera moved'], ascending=True,)
#dow = weekly_inc['DOW']
#pd = per_camera.sort_values(by=['Number times camera moved'], ascending=True,)
# print(per_camera.head(10))
# print(weekly_inc.head(10))
# print(timestamp.head(10))
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#analytics mode bargraph


# sns.set(style='darkgrid')
# fig = plt.figure()
# ax = sns.barplot(data=per_camera, x='Congestion',)
# plt.show()


# tmpfile = BytesIO()
# plt.savefig(tmpfile, format='png')
# encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

# message = """<html>
# <head></head>
# <body>
# <img src='data:image/png;base64,{{}}'>
# <img src='data:image/png;base64,{{}}'>
# </body>
# </html>"""

# with open('test.html','w') as f:
# 	f.write(message)


#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#

 #amount of incidents per type bargraph

# sns.set(style='darkgrid')
# mypal = {'stopped': 'r', 'congestion': 'y', 'wrong_way': 'r', 'slow': 'y', 'pedestrian': 'b'}
# a = sns.countplot(
# 	data=timestamp,
# 	x='Incident Type',
# 	palette=mypal)
# a.set_xlabel('Incident Type')
# a.set_ylabel('Amount of Incidents')
# a.set_title('Amount of Incidents per Type')
# plt.tight_layout()
# #plt.show()
# plt.savefig('incident_count_per_type.png')
# plt.clf()

#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#

#amount of incidents per hour bargraph

# sns.set(style='darkgrid')
# plt.figure(figsize=(10,6))
# b = sns.barplot(
# 	data=weekly_inc,
# 	color='b')
# b.set_ylabel('Amount of Incidents')
# b.set_xlabel('Hour')
# b.set_title('Amount of Incidents per Hour')
# plt.xticks(
# 	rotation=90,
# 	horizontalalignment='center',
# 	fontweight='light',
# 	fontsize=8)
# plt.tight_layout()
# #plt.show()
# plt.savefig('incidenets_per_hour.png')
# plt.clf()

# #------------------------------------------------------------------------------#
# #------------------------------------------------------------------------------#
# #------------------------------------------------------------------------------#

# # scatterplot of amount of stopped vehicles and congestion per camera
# per_camera_sorted = per_camera.sort_values(by='Stopped Vehicle', axis=0, ascending=False,)
# plt.figure(figsize=(10,6))
# sns.set(style='darkgrid')
# sns.set_style('ticks')
# c = sns.barplot(
# 	data=per_camera_sorted.head(30),
# 	y='Stopped Vehicle',
# 	x='Camera Name',
# 	color='r',
# 	)
# c.set_ylabel('Amount of Stopped Vehicles')
# c.set_xlabel('Camera')
# c.set_title('Top 30 Cameras for Stopped Vehicles')
# plt.xticks(
# 	rotation=90,
# 	horizontalalignment='center',
# 	fontweight='light',
# 	fontsize=8)
# plt.tight_layout()
# #plt.show()
# plt.savefig('top_thirty_cam_for_stopped.png')
# plt.clf()

# #plt.tight_layout()
# #plt.show()
# #figure.add_subplot(1, 2, 2)
# #sns.barplot(
# #	data=per_camera,
# #	y='Congestion',
# #	x='Camera Name',
# #	color='y'
# #	).set_title('Amount of Congestion Detected per Camera')

# #plt.xticks(
# #	rotation=90,
# #	horizontalalignment='right',
# #	fontweight='light',
# #	fontsize='6',
# #	)



# #------------------------------------------------------------------------------#
# #------------------------------------------------------------------------------#
# #------------------------------------------------------------------------------#

# per_camera_sorted_ww = per_camera.sort_values(by='Wrong Way', axis=0, ascending=False,)
# plt.figure(figsize=(10,6))
# sns.set(style='darkgrid')
# sns.set_style('ticks')
# d = sns.barplot(
# 	data=per_camera_sorted_ww.head(10),
# 	y='Wrong Way',
# 	x='Camera Name',
# 	color='r',
# 	)
# d.set_ylabel('Amount of Wrong Way')
# d.set_xlabel('Camera')
# d.set_title('Top 30 Cameras for Wrong Way')
# plt.xticks(
# 	rotation=90,
# 	horizontalalignment='center',
# 	fontweight='light',
# 	fontsize=8)
# plt.tight_layout()
# #plt.show()
# plt.savefig('top_ten_cam_for_ww.png')

# print(per_camera_sorted_ww.head(10))

# #------------------------------------------------------------------------------#
# #------------------------------------------------------------------------------#
# #------------------------------------------------------------------------------#

# per_camera_sorted_con = per_camera.sort_values(by='Congestion', axis=0, ascending=False,)
# per_camera_sorted_con2 = per_camera_sorted_con[per_camera_sorted_con['Camera Name'].str.contains('I-85')]

# plt.figure(figsize=(10,6))
# sns.set(style='darkgrid')
# sns.set_style('ticks')
# d = sns.barplot(
# 	data=per_camera_sorted_con2.head(15),
# 	y='Congestion',
# 	x='Camera Name',
# 	color='y',
# 	)
# d.set_ylabel('Amount of Congestion Incidents')
# d.set_xlabel('Camera')
# d.set_title('Top 30 Cameras for Congestion Incidents')
# plt.xticks(
# 	rotation=90,
# 	horizontalalignment='center',
# 	fontweight='light',
# 	fontsize=8)
# plt.tight_layout()
# #plt.show()
# plt.savefig('top_fifteen_cam_for_con.png')


# #------------------------------------------------------------------------------#
# #------------------------------------------------------------------------------#
# #------------------------------------------------------------------------------#


# analytics mode bargraph

# sns.set(style='darkgrid')
# ax = sns.countplot(x='Analytics Mode', data=timestamp, order=['Preset Mode (Locked)', 'Preset Mode', 'AutoLearn Mode'], color='b')

# plt.show()

# #------------------------------------------------------------------------------#
# #------------------------------------------------------------------------------#
# #------------------------------------------------------------------------------#

# # cleared by operator bargraph

# sns.set(style='darkgrid')
# mypal = {'YES': 'b', 'NO': 'r'}
# ax = sns.countplot(x='Incident Cleared By User', 
# 	data=timestamp,
# 	order=['YES','NO'],
# 	palette=mypal,
# 	)
# ax.set_xlabel('Incident Cleared By Operator')
# for p in ax.patches:
# 	ax.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points')


# plt.show()

# #------------------------------------------------------------------------------#
# #------------------------------------------------------------------------------#
# #------------------------------------------------------------------------------#

# # Daily Incident Counts Bargraph

# sns.set(style='darkgrid')

# dfnew = weekly_inc.rename(columns={'DOW': 'dow'})
# dfnew['sum'] = weekly_inc.sum(axis=1)
# data = dfnew.groupby('sum').size()

# ax = sns.barplot(x='dow', y='sum', data=dfnew, color='r').set_title('Daily Incident Counts')

# plt.show()

# #------------------------------------------------------------------------------#
# #------------------------------------------------------------------------------#
# #------------------------------------------------------------------------------#

# sns.set(style='darkgrid')

# sns.countplot(
# 	data=timestamp,
# 	y='Incident Cleared Duration (seconds)',
# 	color='Blue')


# plt.show()

# sns.set(style='darkgrid')
# sns.set_style('ticks')
# e = sns.countplot(
# 	x='Incident Cleared Duration (seconds)',
# 	data=timestamp,
# 	color='r')
# e.set_xlabel(xlabel='Amount')
# e.set_ylabel(ylabel='Seconds Since Inicdient Occured')
# e.set_title('clear time')
# plt.xticks(
# 	rotation=90,
# 	horizontalalignment='center',
# 	fontweight='light',
# 	fontsize='8')
# plt.tight_layout()

# plt.show()

#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#

# fig = plt.figure()
# ax = fig.add_axes([0, 0, 1, 1])
# ax.bar(per_camera['Congestion'], per_camera['Camera Name'])


# plt.show()

#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
# weekly_inc['DOW'] = pd.to_numeric(weekly_inc['DOW'], errors='coerce')

# sns.color_palette='rocket'
# a = sns.heatmap(data=weekly_inc, square=True, linewidth=0.1, annot=True, fmt='.0f', yticklabels=['Sun', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat'])

# plt.tight_layout()
# plt.show()

dfheatmap = weekly_inc
dfheatmap['DOW'] = pd.to_numeric(weekly_inc['DOW'], errors='coerce')

plt.figure(figsize=(10, 6))
sns.set(style='darkgrid')
sns.set_style('ticks')
sns.color_palette('rocket')
h = sns.heatmap(
	data=dfheatmap,
	square=True,
	linewidth=.05,
	annot=True,
	fmt='.0f',
	yticklabels=['Sun', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat'])
h.set_xlabel(xlabel='Hour')
h.set_ylabel(ylabel='DOW')
h.set_title('Heatmap of Incidents by Hour, Week of ' + 'start_date_title' + ' - ' + 'end_date_title')
plt.xticks(
	rotation=90,
	horizontalalignment='center',
	fontweight='light',
	fontsize='8')
plt.tight_layout()
plt.show()
plt.clf()