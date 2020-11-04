
import json
import os
import sys
import csv
import json

#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
def filter_streams(stream_list=[], number_to_add=0):
    if len(stream_list) < 1 or number_to_add < 1:
        print("ERROR: Must specify stream_list and number_to_add.")
        sys.exit(1)

    filtered_list = []
    for entry in stream_list:
        if not 'tv_host' in entry or entry['tv_host'] == '' or entry['tv_host'] == 'undefined':
            filtered_list.append(entry)
            number_to_add -= 1

        if number_to_add < 1:
            break

    return filtered_list


#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
def read_uuid_list_file(uuid_list_file):
    # Returns array of uuids
    try:
        with open(uuid_list_file, 'r') as fp:
            lines = fp.readlines()
            t_lines = []
            for line in lines:
                t_lines.append(line.strip())
            return t_lines
    except Exception as e:
        print("ERROR: Could not read: " + uuid_list_file)
        print(e)
        sys.exit(1)

#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
def create_tmcdata_folders(directory='tmcdata_output/', stream_list=[], starting_camera_index=1):
    index = starting_camera_index
    for entry in stream_list:
        camera_directory = directory + str(index) + '/'
        if not os.path.exists(camera_directory):
            os.makedirs(camera_directory)
        make_video_input(camera_directory, entry['video_uri'])
        make_camera_info(camera_directory, entry['name'], entry['lat'], entry['long'], entry['timezone'])
        make_config_zc(camera_directory, entry['direction'].upper(), entry['camera_placement'].upper())
        #make_sid_file(camera_directory, entry['UUID'])
        make_camera_notes(camera_directory)
        index = index + 1


#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
def make_video_input(directory, source_url):
    vi_dict = {
	   "source_type":	"NETWORK",
	   "source":	source_url,
	   "extra_args":	[""],
	   "rec_loop":	0
    }

    with open(directory + 'video_input.json', 'w') as fp:
        json.dump(vi_dict, fp)

#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
def make_camera_info(directory, camera_name, lat, lng, timezone):
    try:
        latitude = float(lat)
        longitude = float(lng)
    except:
        latitude = 0
        longitude = 0

    info_dict = {
	   "camera_name":	camera_name,
	   "station_id":	"",
       "has_marker":	0,
	   "latitude":	latitude,
	   "longitude":	longitude,
       "timezone": timezone
    }

    if (type(latitude) == float or type(latitude) == int) and (latitude != 0 and longitude != 0):
        info_dict['has_marker'] = 1

    with open(directory + 'camera_info.json', 'w') as fp:
        json.dump(info_dict, fp)

#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
def make_config_zc(directory, near_direction='NS', camera_placement='S'):
    far_direction_dict = {
        "NB": "SB",
        "SB": "NB",
        "EB": "WB",
        "WB": "EB",
        "NS": "FS"
    }
    far_direction = far_direction_dict[near_direction]

    near_quadrants = [3, 0]
    far_quadrants = [2, 1]
    if camera_placement == "M":
        near_quadrants = [1]
        far_quadrants = [2]

    config_dict = {
        "flows": [
            {"quadrants": near_quadrants, "label": near_direction},
            {"quadrants": far_quadrants, "label": far_direction}
        ]
    }

    with open(directory + 'config_zc.json', 'w') as fp:
        json.dump(config_dict, fp)

#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
def make_sid_file(directory, sid=None):
    if not sid is None:
        with open(directory + 'sid', 'w') as fp:
            fp.write(sid)

#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
def make_camera_notes(directory):
    note_dict = {
	   "content": ""
    }

    with open(directory + 'camera_notes.json', 'w') as fp:
        json.dump(note_dict, fp)

#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
def get_all_incidents_from_directory(incidents_path):
    incidents_list = []

    for i_file in os.listdir(incidents_path):
        if i_file.endswith(".json"):
            with open(incidents_path+i_file, 'r') as fp:
                incident_json = json.load(fp)
                incidents_list.append(incident_json)
                fp.close()

    return incidents_list

#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
def get_incident_type(i_type):
    if i_type == 0:
        return "unknown"
    elif i_type == 1:
        return "wrong_way"
    elif i_type == 2:
        return "pedestrian"
    elif i_type == 3:
        return "stopped"
    elif i_type == 4:
        return "congestion"
    elif i_type == 5:
        return "slow"
    elif i_type == 6:
        return "low_visibility"


#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
def parse_archived_data_file(filepath):
    data_list = []
    
    with open(filepath, 'r') as fp:
        lines = fp.readlines()
        for line in lines:
            row = line.split(',')
            if len(row) > 2 and row[0].find('#') == -1:
                obj = {}
                obj['date'] = row[0].strip()
                obj['time'] = row[1].strip()
                obj['volume_ns'] = int(row[2].strip())
                obj['volume_fs'] = int(row[3].strip())
                obj['speed_ns'] = int(row[4].strip())
                obj['speed_fs'] = int(row[5].strip())
                obj['counts_cars_ns'] = int(row[6].strip())
                obj['counts_trucks_ns'] = int(row[7].strip())
                obj['counts_tractor_trailers_ns'] = int(row[8].strip())
                obj['counts_motorcycles_ns'] = int(row[9].strip())
                obj['counts_unknowns_ns'] = int(row[10].strip())
                obj['counts_cars_fs'] = int(row[11].strip())
                obj['counts_trucks_fs'] = int(row[12].strip())
                obj['counts_tractor_trailers_fs'] = int(row[13].strip())
                obj['counts_motorcycles_fs'] = int(row[14].strip())
                obj['counts_unknowns_fs'] = int(row[15].strip())
                obj['camera_moved'] = row[16].strip()
                obj['calib_preset'] = row[17].strip()
                obj['num_lanes_ns'] = int(row[18].strip())
                obj['num_lanes_fs'] = int(row[19].strip())

                data_list.append(obj)

        fp.close()        
    

    return data_list

#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
'''enum PtzMode
{
  PTZ_UNKNOWN = 0,
  PTZ_AUTOLEARN = 1,
  PTZ_DPA = 2,          // use preset after adjusting pan-tilt
  PTZ_APS = 3,          // use preset as-is
  PTZ_MPS = 4           // manual preset override
};'''
def getCalibrationMode(calib_mode_int):
    if calib_mode_int == 1:
        return "AutoLearn Mode"

    if calib_mode_int == 2 or calib_mode_int == 3:
        return "Preset Mode"

    if calib_mode_int == 4:
        return "Preset Mode (Locked)"

    return "Unknown"