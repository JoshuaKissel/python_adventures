import pandas as pd
import json
import requests
import chart_studio.tools as tls
from datetime import timedelta
from datetime import datetime
import argparse

def densitymap():
	#call incident list API and import to pandas DataFrame
	traffic = pd.DataFrame(pandas_dict['responses'])
	traffic.head(10)
#count how many times each camera index appears in the incident list
	z = traffic['camera_index'].value_counts(dropna=True, sort=False)
	z
	df_value_counts = pd.DataFrame(z)
	df_value_counts = df_value_counts.reset_index()
	df_value_counts.columns = ['camera_index', 'counts'] # change column names
	df_value_counts
#get realtime datea
	r = get_realtime_data('tndemo.trafficvision.com:4443', 'HackHPC', 'TeamUser')

	realtime = pd.DataFrame.from_dict(r['responses'])
	realtime = realtime.drop(['sid', 'station_id', 'timezone', 'sync_flags', 'autolearn', 'incident_data', 'incidents', 'calib_data', 'inactive', 'inactive_reason', 'realtime_data', 'timestamp_video_input', 'response_id', 'host_id', 'host'], axis=1)

	realtime['counts'] = realtime['camera_index'].map(df_value_counts.set_index('camera_index')['counts'])
	realtime

# realtime['values'] = df_value_counts['counts'].astype(int)
	realtime = realtime.dropna()
	realtime
