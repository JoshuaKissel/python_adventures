import pandas as pd
import json
import requests
import chart_studio.tools as tls

TIMEOUT = 10

#calls realtime data API
def get_realtime_data(tv_host='', username='', password=''):
	url = 'https://' + str(tv_host) + '/realtime_data'

	try:
		r = requests.get(url, auth=(username,password), verify=False, timeout=TIMEOUT)
		if r.status_code == requests.codes.ok:
			return r.json()
	except Exception as e:
		return {'error': e}

	return {'error': r.status_code}

#api get call for incident list
def get_list_of_incidents(tv_host, camera_indices, pattern, username, password):
	url = 'https://' + str(tv_host) + '/json_post'
	
	data = {
		'request': 'cr_get_data_files_info',
		'request_id': 2016,
		'camera_indices': camera_indices,
		'folder': 'incidents',
		'pattern': pattern,
		'host': '127.0.0.1'
	}
	
	try:
		r = requests.post(url, data=json.dumps(data), auth=(username, password), verify=False, timeout=TIMEOUT)
		if r.status_code == requests.codes.ok:
			return r.json()
	except Exception as e:
		return {'error': e}
			
	return {'error': r.status_code}

#calls incident list API
pandas_dict = {'responses': []}    
r = get_list_of_incidents('tndemo.trafficvision.com:4443', list(range(1, 61)), '2020-10*incident_stopped*.json', 'HackHPC', 'TeamUser')
if 'responses' in r:
    for camera_obj in r['responses']:
        camera_index = camera_obj['camera_index']
        incident_entries = camera_obj['entries']
        for entry in incident_entries:
            pandas_dict['responses'].append({'camera_index': camera_index, 'filename': entry['filename'], 'timestamp': entry['time']})

#call incident list API and import to pandas DataFrame
traffic = pd.DataFrame(pandas_dict['responses'])
traffic.head(10)

#count how many times each camera index appears in the incident list
z = traffic['camera_index'].value_counts(dropna=True, sort=True)
df_value_counts = pd.DataFrame(z)
df_value_counts = df_value_counts.reset_index()
df_value_counts.columns = ['camera_index', 'counts'] # change column names
df_value_counts

r = get_realtime_data('tndemo.trafficvision.com:4443', 'HackHPC', 'TeamUser')

realtime = pd.DataFrame.from_dict(r['responses'])
realtime = realtime.drop(['sid', 'station_id', 'timezone', 'sync_flags', 'autolearn', 'incident_data', 'incidents', 'calib_data', 'inactive', 'inactive_reason', 'realtime_data', 'timestamp_video_input', 'response_id', 'host_id', 'host'], axis=1)

realtime['counts'] = realtime['camera_index'].map(df_value_counts.set_index('camera_index')['counts'])
realtime

realtime['values'] = df_value_counts['counts'].astype(int)
realtime = realtime.dropna()
realtime

import plotly.graph_objects as go
fig = go.Figure(go.Densitymapbox(lat=realtime.latitude, lon=realtime.longitude, z=realtime.counts,
                                 radius=10))
fig.update_layout(mapbox_style="open-street-map", mapbox_center_lon=-90)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

fig.write_html('map.htlm')