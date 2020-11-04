import os
import sys
import getopt
import argparse
import matplotlib.pyplot as plt 
import seaborn as sns 
import pandas as pd
from incidents_report import create_incident_reports
from datetime import datetime, timedelta

#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#

def incident_by_type(timestamp, outputdir, start_date_title, end_date_title):
	mypal = {'stopped': 'r', 'congestion': 'y', 'wrong_way': 'r', 'slow': 'y', 'pedestrian': 'b', 'low_visibility': 'b'}
	plt.figure(figsize=(10,6))	
	sns.set(style='darkgrid') #sets style
	a = sns.countplot( #generates plot
	data=timestamp,
	x='Incident Type', 
	palette=mypal,)
	a.set_xlabel('Incident Type')
	a.set_ylabel('Incident Count')
	a.set_title('Amount of Inicidents by Type for week of ' + start_date_title + ' - ' + end_date_title) #generates axis labels and title

	plt.tight_layout()
	plt.savefig(outputdir + 'Amount_Incidents_by_Type.png') #show plot
	plt.clf()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#

def hourly_incidents(weekly_inc, outputdir, start_date_title, end_date_title):
	plt.figure(figsize=(10,6))	
	sns.set(style='darkgrid')
	sns.set_style('ticks')
	b = sns.barplot(
	data=weekly_inc,
	color='b')
	b.set_xlabel(xlabel='Hour')
	b.set_ylabel('Incident Count')
	b.set_title('Amount of Incidents per Hour for week of ' + start_date_title + ' - ' + end_date_title)
	plt.xticks(
		rotation=90,
		horizontalalignment='center',
		fontweight='light',
		fontsize='8')

	plt.tight_layout()
	plt.savefig(outputdir + 'hourly_incidents.png')
	plt.clf()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#

def stopped_veh_per_camera(per_camera, outputdir, start_date_title, end_date_title):
	per_camera_sorted = per_camera.sort_values(by='Stopped Vehicle', axis=0, ascending=False)
	plt.figure(figsize=(10,6))
	sns.set(style='darkgrid')
	sns.set_style('ticks')
	c = sns.barplot(
	data=per_camera_sorted.head(10),
	y='Stopped Vehicle',
	x='Camera Name',
	color='r',
	)
	c.set_ylabel('Stopped Vehicle Incident Count')
	c.set_title('Top 10 Cameras for Stopped Vehicles, Week of ' + start_date_title + ' - ' + end_date_title)
	plt.xticks(
	rotation=45,
	horizontalalignment='right',
	fontweight='light',
	fontsize='8',
	)

	plt.tight_layout()
	plt.savefig(outputdir + 'stopped_veh_per_camera.png')
	plt.clf()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#

def congestion_per_camera(per_camera, outputdir, start_date_title, end_date_title):
	per_camera_sorted = per_camera.sort_values(by='Congestion', axis=0, ascending=False)
	plt.figure(figsize=(10,6))
	sns.set(style='darkgrid')
	sns.set_style('ticks')
	d = sns.barplot(
	data=per_camera_sorted.head(10),
	y='Congestion',
	x='Camera Name',
	color='y',
	)
	d.set_ylabel('Congestion Incident Count')
	d.set_title('Top 10 Cameras for Congestion Incidents, Week of ' + start_date_title + ' - ' + end_date_title)
	plt.xticks(
	rotation=45,
	horizontalalignment='right',
	fontweight='light',
	fontsize='8',
	)

	plt.tight_layout()
	plt.savefig(outputdir + 'congestion_per_camera.png')
	plt.clf()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#

def dow_sum(weekly_inc, outputdir, start_date_title, end_date_title):
	dfnew = weekly_inc.rename(columns={'DOW': 'dow'})
	dfnew['sum'] = weekly_inc.sum(axis=1)
	data = dfnew.groupby('sum').size()

	plt.figure(figsize=(10,6))
	sns.set(style='darkgrid')
	sns.set_style('ticks')
	e = sns.barplot(
		x='dow',
		y='sum',
		data=dfnew,
		color='r',)
	e.set_xlabel(xlabel='DOW')
	e.set_ylabel(ylabel='Incident Count')
	e.set_title('Daily Incident Counts, Week of ' + start_date_title + ' - ' + end_date_title)
	plt.xticks(
		rotation=90,
		horizontalalignment='center',
		fontweight='light',
		fontsize='8')
	plt.tight_layout()
	plt.savefig(outputdir + 'dow_incidents.png')
	plt.clf()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
def heatmap(weekly_inc, outputdir, start_date_title, end_date_title):
	dfheatmap = weekly_inc
	dfheatmap['DOW'] = pd.to_numeric(weekly_inc['DOW'], errors='coerce')

	plt.figure(figsize=(10, 6))
	# sns.set(style='darkgrid')
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
	h.set_title('Heatmap of Incidents by Hour, Week of ' + start_date_title + ' - ' + end_date_title)
	plt.xticks(
		rotation=90,
		horizontalalignment='center',
		fontweight='light',
		fontsize='8')
	plt.tight_layout()
	plt.savefig(outputdir + 'heatmap.png')
	plt.clf()



#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-timezone', help='Timezone of Camera', default='America/New_York')
	parser.add_argument('-days', help='How many days ago', default=6)
	parser.add_argument('-outputdir', help='Output directory path with ending /', default='/home/tvdev/')

	args=parser.parse_args()

	end_date = datetime.now().date() - timedelta(days=1)
	start_date = end_date - timedelta(days=int(args.days))
	end_date_run = end_date.strftime('%Y%m%d')
	start_date_run = start_date.strftime('%Y%m%d')
	start_date_title = start_date.strftime('%m/%d/%Y')
	end_date_title = end_date.strftime('%m/%d/%Y')

	create_incident_reports('/home/tvdev/trafficvision/webroot/tmcdata/', args.outputdir, args.timezone , start_date_run, end_date_run, 25, 90)

	outputdir = args.outputdir

	#uses pandas to import 3 csvs 
	timestamp=pd.read_csv(outputdir + 'incidents_by_timestamp.csv', delimiter=',')
	weekly_inc=pd.read_csv(outputdir + 'incident_report_per_dow_in_All.csv', delimiter=',')
	per_camera=pd.read_csv(outputdir + 'incident_report_per_camera.csv', delimiter=',')

	incident_by_type(timestamp, outputdir, start_date_title, end_date_title)
	hourly_incidents(weekly_inc, outputdir, start_date_title, end_date_title)
	stopped_veh_per_camera(per_camera, outputdir, start_date_title, end_date_title)
	congestion_per_camera(per_camera, outputdir, start_date_title, end_date_title)
	dow_sum(weekly_inc, outputdir, start_date_title, end_date_title)
	heatmap(weekly_inc, outputdir, start_date_title, end_date_title)
