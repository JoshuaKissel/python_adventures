import os
import sys
import getopt
import argparse
import matplotlib.pyplot as plt 
import seaborn as sns 
import pandas as pd
# from incidents_report import create_incident_reports
# from datetime import datetime, timedelta
# import plotly.graph_objects as go
# import chart_studio
# import chart_studio.plotly as py
# import chart_studio.tools as tls

# timestamp=pd.read_csv(outputdir + month_start + '-' + month_end + '_incident_by_timestamp.csv', delimiter=',')
# weekly_inc=pd.read_csv(outputdir + month_start + '-' month_end + '_incident_report_per_dow_in_All.csv', delimiter=',')
# per_camera=pd.read_csv(outputdir + month_start + '-' + month_end + '_incident_report_per_camera.csv', delimiter=',')


#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#

def incident_by_type(data_output_dir, month_start, month_end):
	timestamp=pd.read_csv(data_output_dir + month_start + '-' + month_end + '_incidents_by_timestamp.csv', delimiter=',')
	mypal = {'stopped': 'r', 'congestion': 'y', 'wrong_way': 'r', 'slow': 'darksalmon', 'pedestrian': 'b', 'low_visibility': 'b'}
	plt.figure(figsize=(10,6))	
	sns.set(style='darkgrid') #sets style
	a = sns.countplot( #generates plot
	data=timestamp,
	x='Incident Type', 
	palette=mypal,)
	a.set_xlabel('Incident Type')
	a.set_ylabel('Incident Count')
	a.set_title('Amount of Inicidents by Type') #generates axis labels and title

	plt.tight_layout()
	plt.savefig(data_output_dir + month_start + '-' + month_end + 'Amount_Incidents_by_Type.png') #show plot
	plt.clf()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#

# def hourly_incidents(weekly_inc, outputdir, start_date_title, end_date_title):
# 	plt.figure(figsize=(10,6))	
# 	sns.set(style='darkgrid')
# 	sns.set_style('ticks')
# 	b = sns.barplot(
# 	data=weekly_inc,
# 	color='b')
# 	b.set_xlabel(xlabel='Hour')
# 	b.set_ylabel('Incident Count')
# 	b.set_title('Amount of Incidents per Hour for week of ' + start_date_title + ' - ' + end_date_title)
# 	plt.xticks(
# 		rotation=90,
# 		horizontalalignment='center',
# 		fontweight='light',
# 		fontsize='8')

# 	plt.tight_layout()
# 	plt.savefig(outputdir + 'hourly_incidents.png')
# 	plt.clf()

# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#

# def stopped_veh_per_camera(per_camera, outputdir, start_date_title, end_date_title):
# 	per_camera_sorted = per_camera.sort_values(by='Stopped Vehicle', axis=0, ascending=False)
# 	plt.figure(figsize=(10,6))
# 	sns.set(style='darkgrid')
# 	sns.set_style('ticks')
# 	c = sns.barplot(
# 	data=per_camera_sorted.head(10),
# 	y='Stopped Vehicle',
# 	x='Camera Name',
# 	color='r',
# 	)
# 	c.set_ylabel('Stopped Vehicle Incident Count')
# 	c.set_title('Top 10 Cameras for Stopped Vehicles, Week of ' + start_date_title + ' - ' + end_date_title)
# 	plt.xticks(
# 	rotation=45,
# 	horizontalalignment='right',
# 	fontweight='light',
# 	fontsize='8',
# 	)

# 	plt.tight_layout()
# 	plt.savefig(outputdir + 'stopped_veh_per_camera.png')
# 	plt.clf()

# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#

# def congestion_per_camera(per_camera, outputdir, start_date_title, end_date_title):
# 	per_camera_sorted = per_camera.sort_values(by='Congestion', axis=0, ascending=False)
# 	plt.figure(figsize=(10,6))
# 	sns.set(style='darkgrid')
# 	sns.set_style('ticks')
# 	d = sns.barplot(
# 	data=per_camera_sorted.head(10),
# 	y='Congestion',
# 	x='Camera Name',
# 	color='y',
# 	)
# 	d.set_ylabel('Congestion Incident Count')
# 	d.set_title('Top 10 Cameras for Congestion Incidents, Week of ' + start_date_title + ' - ' + end_date_title)
# 	plt.xticks(
# 	rotation=45,
# 	horizontalalignment='right',
# 	fontweight='light',
# 	fontsize='8',
# 	)

# 	plt.tight_layout()
# 	plt.savefig(outputdir + 'congestion_per_camera.png')
# 	plt.clf()

# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#

# def dow_sum(weekly_inc, outputdir, start_date_title, end_date_title):
# 	dfnew = weekly_inc.rename(columns={'DOW': 'dow'})
# 	dfnew['sum'] = weekly_inc.sum(axis=1)
# 	data = dfnew.groupby('sum').size()

# 	plt.figure(figsize=(10,6))
# 	sns.set(style='darkgrid')
# 	sns.set_style('ticks')
# 	e = sns.barplot(
# 		x='dow',
# 		y='sum',
# 		data=dfnew,
# 		color='r',)
# 	e.set_xlabel(xlabel='DOW')
# 	e.set_ylabel(ylabel='Incident Count')
# 	e.set_title('Daily Incident Counts, Week of ' + start_date_title + ' - ' + end_date_title)
# 	plt.xticks(
# 		rotation=90,
# 		horizontalalignment='center',
# 		fontweight='light',
# 		fontsize='8')
# 	plt.tight_layout()
# 	plt.savefig(outputdir + 'dow_incidents.png')
# 	plt.clf()

# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# def heatmap(weekly_inc, outputdir, start_date_title, end_date_title):
# 	dfheatmap = weekly_inc
# 	dfheatmap['DOW'] = pd.to_numeric(weekly_inc['DOW'], errors='coerce')

# 	plt.figure(figsize=(10, 6))
# 	# sns.set(style='darkgrid')
# 	sns.set_style('ticks')
# 	sns.color_palette('rocket')
# 	h = sns.heatmap(
# 		data=dfheatmap,
# 		square=True,
# 		linewidth=.05,
# 		annot=True,
# 		fmt='.0f',
# 		yticklabels=['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat','Sun'])
# 	h.set_xlabel(xlabel='Hour')
# 	h.set_ylabel(ylabel='DOW')
# 	h.set_title('Heatmap of Incidents by Hour, Week of ' + start_date_title + ' - ' + end_date_title)
# 	plt.xticks(
# 		rotation=90,
# 		horizontalalignment='center',
# 		fontweight='light',
# 		fontsize='8')
# 	plt.tight_layout()
# 	plt.savefig(outputdir + 'heatmap.png')
# 	plt.clf()


# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #EDIT- Inc Per Date by Type Daily

# def inc_per_date_by_type(timestamp, outputdir, start_date_title, end_date_title, datem):
# 	timestamp['just_date'] = timestamp['Timestamp'].str[:10]
# 	date_sorted = timestamp.sort_values(by='just_date', axis=0, ascending=True)

# 	mypal = {'stopped': 'r', 'congestion': 'y', 'wrong_way': 'r', 'slow': 'darksalmon', 'pedestrian': 'b'}
# 	sns.set(style='darkgrid')

# 	a = sns.countplot(
# 		x=date_sorted['just_date'],
# 		hue=date_sorted['Incident Type'],
# 		data=date_sorted,
# 		palette=mypal,
# 		hue_order=date_sorted['Incident Type'].value_counts(ascending=False).index)
# 	a.set_xlabel('Date')
# 	a.set_ylabel('Amount of Incdients Detected Since')
# 	a.set_title('Amount of Incidents per Day by Type Since' + datem)
# 	plt.xticks(
# 		rotation=90,
# 		horizontalalignment='center',
# 		fontweight='light',
# 		fontsize=8)
# 	plt.tight_layout()
# 	plt.savefig(outputdir + 'incidents_per_date_by_type_since_' + datem + '.png')
# 	plt.clf()

# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #EDIT- Veh Count Map

# preset = preset.rename({'Camera Name': 'camera_name', 'Total Vehicles': 'veh_count'}, axis='columns')


# fig = go.Figure(go.Densitymapbox(lat=preset.Latitude, lon=preset.Longitude, z=preset.veh_count, customdata=preset.camera_name, hovertemplate='Amount of Vehicles Detected: %{z} <br> Camera Name: %{customdata} <extra></extra>',
#                                  radius=20,))
# config = dict({'scrollZoom': True})
# fig.update_layout(mapbox_style="open-street-map", mapbox_center_lon=-117.3, mapbox_center_lat=33.66355, mapbox_zoom=9)
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# # fig.show(config=config)
# fig.write_html("veh_map.html")
# link = py.plot(fig, filename = 'caltrans_vechile_map', auto_open=False)

# iframe = tls.get_embed(link) #change to your url

# index = iframe.find('" height')
# iframe = iframe[:index] + '?showlink=false' + iframe[index:]



# print(iframe)

# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #EDIT - All Incident Map

# fig_incidents = go.Figure(go.Densitymapbox(lat=no_preset.Latitude, lon=no_preset.Longitude, z=no_preset.all_inc, customdata=no_preset.camera_name, hovertemplate='Amount of Incidents: %{z} <br> Camera Name: %{customdata} <extra></extra>',
#                                  radius=20,))
# config = dict({'scrollZoom': True})
# fig_incidents.update_layout(mapbox_style="open-street-map", mapbox_center_lon=-117.3, mapbox_center_lat=33.66355, mapbox_zoom=9)
# fig_incidents.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show(config=config)
# fig.write_html("map.html")

# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #EDIT - create slow speed incidents map
# fig_slow = go.Figure(go.Densitymapbox(lat=no_preset.Latitude, lon=no_preset.Longitude, z=no_preset.slow_veh, customdata=no_preset.camera_name, hovertemplate='Amount of Slow Speed Incidents: %{z} <br> Camera Name: %{customdata} <extra></extra>',
#                                  radius=20,))
# config = dict({'scrollZoom': True})
# fig_slow.update_layout(mapbox_style="open-street-map", mapbox_center_lon=-117.3, mapbox_center_lat=33.66355, mapbox_zoom=9)
# fig_slow.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show(config=config)
# fig.write_html("map.html")

# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #EDIT- stopped obj incident map
# fig_stopped_obj = go.Figure(go.Densitymapbox(lat=no_preset.Latitude, lon=no_preset.Longitude, z=no_preset.stopped_obj, customdata=no_preset.camera_name, hovertemplate='Amount of Stopped Object Incidents: %{z} <br> Camera Name: %{customdata} <extra></extra>',
#                                  radius=20,))
# config = dict({'scrollZoom': True})
# fig_stopped_obj.update_layout(mapbox_style="open-street-map", mapbox_center_lon=-117.3, mapbox_center_lat=33.66355, mapbox_zoom=9)
# fig_stopped_obj.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show(config=config)
# fig.write_html("map.html")
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #EDIT Top 30 cameras - movement - This Month
# def top_camera_movements(per_camera, outputdir, start_date_title, end_date_title, datem):
# 	per_camera_sorted_moved=per_camera.sort_values(by='Number times camera moved', axis=0, ascending=False)

# 	plt.figsize(figsize=(10,6))
# 	sns.set(style='darkgrid')
# 	sns.set_style('ticks')
# 	c = sns.barplot(
# 		data=per_camera_sorted_moved.head(30),
# 		y='Number times camera moved',
# 		x='Camera Name',
# 		color='b'
# 		)
# 	c.set_xlabel('Camera Name')
# 	c.set_ylabel('Amount of Camera Movement')
# 	c.set_title('Top 30 Cameras for Camera Movement Since ' + datem)
# 	plt.xticks(
# 		rotation=90,
# 		horizontalalignment='center',
# 		fontweight='light',
# 		fontsize=8)
# 	plt.tight_layout()
# 	plt.savefig(outputdir + 'top_thirty_cam_for_movement_since_' + datem + '.png')
# 	plt.clf()

# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #EDIT Top 5 cameras for under 25 - This Month
# def top__camera_slowspeeds():
# 	pass

# per_camera_sorted_under25 = preset.sort_values(by='Number of times speeds less than 25 mph', axis=0, ascending=False,)
# plt.figure(figsize=(10,6))
# sns.set(style='darkgrid')
# sns.set_style('ticks')
# c = sns.barplot(
# 	data=per_camera_sorted_under25.head(5),
# 	y='Number of times speeds less than 25 mph',
# 	x='Camera Name',
# 	color='y',
# 	)
# c.set_ylabel('Amount of Average Speeds Under 25 MPH Detections')
# c.set_xlabel('Camera')
# c.set_title('Top 5 Cameras for Average Speeds Under 25 MPH Detections - Nov 17-30')
# plt.xticks(
# 	rotation=90,
# 	horizontalalignment='center',
# 	fontweight='light',
# 	fontsize=8)
# plt.tight_layout()
# #plt.show()
# plt.savefig('top_five_cam_for_under25_nov17_30.png')
# plt.clf()


# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #EDIT Top 5 cameras for above 90
# per_camera_sorted_over90 = preset.sort_values(by='Number of times speeds greater than 90 mph', axis=0, ascending=False,)
# plt.figure(figsize=(10,6))
# sns.set(style='darkgrid')
# sns.set_style('ticks')
# c = sns.barplot(
# 	data=per_camera_sorted_over90.head(5),
# 	y='Number of times speeds greater than 90 mph',
# 	x='Camera Name',
# 	color='r',
# 	)
# c.set_ylabel('Amount of Average Speeds Over 90 MPH Detections')
# c.set_xlabel('Camera')
# c.set_title('Top 5 Cameras for Average Speeds Over 90 MPH Detections - Nov 17-30')
# plt.xticks(
# 	rotation=90,
# 	horizontalalignment='center',
# 	fontweight='light',
# 	fontsize=8)
# plt.tight_layout()
# #plt.show()
# plt.savefig('top_five_cam_for_over90_nov17_30.png')
# plt.clf()

# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #EDIT Top 20 cameras for slow speeds
# per_camera_sorted_slow = preset.sort_values(by='Slow Speeds', axis=0, ascending=False,)
# plt.figure(figsize=(10,6))
# sns.set(style='darkgrid')
# sns.set_style('ticks')
# c = sns.barplot(
# 	data=per_camera_sorted_slow.head(20),
# 	y='Slow Speeds',
# 	x='Camera Name',
# 	color='y',
# 	)
# c.set_ylabel('Amount of Slow Speed Detections')
# c.set_xlabel('Camera')
# c.set_title('Top 20 Cameras for Slow Speed Detections - Nov 17-30')
# plt.xticks(
# 	rotation=90,
# 	horizontalalignment='center',
# 	fontweight='light',
# 	fontsize=8)
# plt.tight_layout()
# #plt.show()
# plt.savefig('top_twenty_cam_for_slow_nov17_30.png')
# plt.clf()
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #EDIT Top 10 cameras for pedestrian
# per_camera_sorted_ped = preset.sort_values(by='Pedestrian', axis=0, ascending=False,)
# plt.figure(figsize=(10,6))
# sns.set(style='darkgrid')
# sns.set_style('ticks')
# c = sns.barplot(
# 	data=per_camera_sorted_ped.head(5),
# 	y='Pedestrian',
# 	x='Camera Name',
# 	color='b',
# 	)
# c.set_ylabel('Amount of Pedestrian Detections')
# c.set_xlabel('Camera')
# c.set_title('Top 5 Cameras for Pedestrian Detections - Nov 17-30')
# plt.xticks(
# 	rotation=90,
# 	horizontalalignment='center',
# 	fontweight='light',
# 	fontsize=8)
# plt.tight_layout()
# #plt.show()
# plt.savefig('top_five_cam_for_pedest_nov17_30.png')
# plt.clf()

# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#

# #EDIT Top 30 cameras - Vehicle Counts

# per_camera_sorted_counts = preset.sort_values(by='Total Vehicles', axis=0, ascending=False)
# plt.figure(figsize=(10,6))
# sns.set(style='darkgrid')
# sns.set_style('ticks')
# c = sns.barplot(
# 	data=per_camera_sorted_counts.head(30),
# 	y='Total Vehicles',
# 	x='Camera Name',
# 	color='g',
# 	)
# c.set_ylabel('Amount of Vehicles Counted')
# c.set_xlabel('Camera')
# c.set_title('Top 30 Cameras for Vehicle Counts - Nov 17-30')
# plt.xticks(
# 	rotation=90,
# 	horizontalalignment='center',
# 	fontweight='light',
# 	fontsize=8)
# c.ticklabel_format(style='plain', axis='y')
# plt.tight_layout()
# #plt.show()
# plt.savefig('top_thirty_cam_for_total_veh_nov17_30.png')
# plt.clf()

# # plt.tight_layout()
# # plt.show()


# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# #-----------------------------------------------------------------------------------------------------------------------------------------------------------#


# # if __name__ == '__main__':
# # 	parser = argparse.ArgumentParser()
# # 	parser.add_argument('-timezone', help='Timezone of Camera', default='America/New_York')
# # 	# parser.add_argument('-days', help='How many days ago', default=6)
# # 	parser.add_argument('-outputdir', help='Output directory path with ending /', default='/home/tvdev/')
# # 	parser.add_argument('-slowspeed', help='Slow Speed in MPH', default=25)
# # 	parser.add_argument('-highspeed', help='High Speed in MPH', default=90)

# # 	args=parser.parse_args()

# # 	# find current month
# # 	today = datetime.today()
# # 	datem = datetime(today.year, today.month, 1)

# # 	# find start and end date
# # 	end_date = datetime.now().date()
# # 	start_date = datem
# # 	end_date_run = end_date.strftime('%Y%m%d')
# # 	start_date_run = start_date.strftime('%Y%m%d')
# # 	start_date_title = start_date.strftime('%m/%d/%Y')
# # 	end_date_title = end_date.strftime('%m/%d/%Y')
# # 	end_date_sort = end_date.strftime('%Y-%m-%d')


# 	#uses pandas to import 3 csvs 
# 	timestamp=pd.read_csv(outputdir + 'incidents_by_timestamp.csv', delimiter=',')
# 	weekly_inc=pd.read_csv(outputdir + 'incident_report_per_dow_in_All.csv', delimiter=',')
# 	per_camera=pd.read_csv(outputdir + 'incident_report_per_camera.csv', delimiter=',')






