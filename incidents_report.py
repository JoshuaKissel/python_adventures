import os
import sys
import getopt
import argparse
import json
import csv
import pytz
from datetime import datetime
import tmcdata_utility




#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
def count_incidents(incidents_list, timezone, start_timestamp, end_timestamp):
    count_dict = {}
    count_dict['stopped'] = 0
    count_dict['stopped_dow'] = []
    count_dict['congestion'] = 0
    count_dict['congestion_dow'] = []
    count_dict['slow'] = 0
    count_dict['slow_dow'] = []
    count_dict['pedestrian'] = 0
    count_dict['pedestrian_dow'] = []
    count_dict['wrong_way'] = 0
    count_dict['wrong_way_dow'] = []
    count_dict['unknown'] = 0
    count_dict['unknown_dow'] = []
    count_dict['low_visibility'] = 0
    count_dict['low_visibility_dow'] = []

    for i in range(0,7):
        count_dict['stopped_dow'].append([])
        count_dict['congestion_dow'].append([])
        count_dict['slow_dow'].append([])
        count_dict['pedestrian_dow'].append([])
        count_dict['wrong_way_dow'].append([])
        count_dict['unknown_dow'].append([])
        count_dict['low_visibility_dow'].append([])
        for j in range(0, 24):
            count_dict['stopped_dow'][i].append(0)
            count_dict['congestion_dow'][i].append(0)
            count_dict['slow_dow'][i].append(0)
            count_dict['pedestrian_dow'][i].append(0)
            count_dict['wrong_way_dow'][i].append(0)
            count_dict['unknown_dow'][i].append(0)
            count_dict['low_visibility_dow'][i].append(0)

    for incident_dict in incidents_list:       
        timestamp = incident_dict['timestamp']
        if timestamp >= start_timestamp and timestamp <= end_timestamp:
            dt = datetime.fromtimestamp(timestamp, timezone)
            dt_dow = dt.weekday()
            i_type = tmcdata_utility.get_incident_type(incident_dict['incident_type'])
            count_dict[i_type] = count_dict[i_type] + 1
            count_dict[i_type + "_dow"][dt_dow][dt.hour] = count_dict[i_type + "_dow"][dt_dow][dt.hour] + 1

    return count_dict

#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
def find_speed_boundaries(archived_data_path, min_speed_threshold, max_speed_threshold, start_int, end_int):
    min_speeds_list = []
    max_speeds_list = []
    num_times_camera_moved = 0
    start_date = 0
    end_date = 0
    data_list = []
    for csv_file in os.listdir(archived_data_path):
        if csv_file.startswith('current') or csv_file.startswith('vlog') or csv_file.endswith('.loj'):
            continue
        date = int(csv_file.split('.')[0])
        if csv_file.endswith(".csv") and date >= start_int and date <= end_int:            
            if date < start_date or start_date == 0:
                start_date = date
            if date > end_date:
                end_date = date
            data_list =  data_list + tmcdata_utility.parse_archived_data_file(archived_data_path+csv_file)

    for obj in data_list:
        if (obj['speed_ns'] <= min_speed_threshold and obj['speed_ns'] != 0) or (obj['speed_fs'] <= min_speed_threshold and obj['speed_fs'] != 0):
            min_speeds_list.append(obj['date'] + ' ' + obj['time'])

        if obj['speed_ns'] >= max_speed_threshold or obj['speed_fs'] >= max_speed_threshold:
            max_speeds_list.append(obj['date'] + ' ' + obj['time'])

        if obj['camera_moved'] == "moved":
            num_times_camera_moved = num_times_camera_moved + 1

    return {'min_speeds_list': min_speeds_list, 'max_speeds_list': max_speeds_list, 'num_times_camera_moved': num_times_camera_moved, 'start_date': start_date, 'end_date': end_date}

#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
'''
def get_district(abbr):
    if abbr.upper() == 'N':
        return "Nashville"
    elif abbr.upper() == 'C':
        return "Chattanooga"
    elif abbr.upper() == 'M':
        return "Memphis"
    elif abbr.upper() == 'K':
        return "Knoxville"

    return ""
'''
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
def create_incident_reports(dir, outputdir, timezone, start, end, min_speed, max_speed):
    tz = pytz.timezone(timezone)
    start_year = start[0:4]
    start_month = start[4:6]
    start_day = start[6:8]
    end_year = end[0:4]
    end_month = end[4:6]
    end_day = end[6:8]
    start_dt = datetime(int(start_year), int(start_month), int(start_day), 0, 0, 0, tzinfo=tz)
    end_dt = datetime(int(end_year), int(end_month), int(end_day), 23, 59, 59, tzinfo=tz)
    start_ts = start_dt.timestamp()
    end_ts = end_dt.timestamp()
    report_dict = {}
    all_incidents_list = []

    for camera_directory in os.listdir(dir):
        full_camera_path = dir + camera_directory + "/"
        if os.path.isdir(full_camera_path):
            # Get camera_info.json
            try:
                with open(full_camera_path + "camera_info.json", "r") as fp:
                    camera_info = json.load(fp)
                    camera_name = camera_info['camera_name']

                    incidents_list = tmcdata_utility.get_all_incidents_from_directory(full_camera_path+"incidents/")
                    for incident_dict in incidents_list:
                        incident_dict['camera_info'] = camera_info
                    all_incidents_list = all_incidents_list + incidents_list

                    report_dict[camera_name] = count_incidents(incidents_list, tz, start_ts, end_ts)
                    report_dict[camera_name]['camera_name'] = camera_name
                    report_dict[camera_name]['camera_index'] = camera_directory
                    report_dict[camera_name]['latitude'] = camera_info['latitude'] if 'latitude' in camera_info else 0
                    report_dict[camera_name]['longitude'] = camera_info['longitude'] if 'longitude' in camera_info else 0
                    report_dict[camera_name]['district'] = '' #get_district(camera_name[0])
                    
                    speed_threshold_dict = find_speed_boundaries(full_camera_path+"data/", min_speed, max_speed, int(start), int(end))
                    report_dict[camera_name]['speeds_greater_than_max_threshold'] = speed_threshold_dict['max_speeds_list']
                    report_dict[camera_name]['speeds_lower_than_min_threshold'] = speed_threshold_dict['min_speeds_list']
                    report_dict[camera_name]['num_times_camera_moved'] = speed_threshold_dict['num_times_camera_moved']
                    report_dict[camera_name]['start_date'] = speed_threshold_dict['start_date']
                    report_dict[camera_name]['end_date'] = speed_threshold_dict['end_date']
                    
                    fp.close()
            except Exception as e:
                print(e)

    
    # Print out csv files
    with open(outputdir + 'incident_report_per_camera.csv', 'w', newline='') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(["Camera Name", "Latitude", "Longitude", "District", "Stopped Vehicle", "Congestion", "Low Visibility", "Slow Speeds", "Pedestrian", "Wrong Way", "Number of times speeds less than "+str(min_speed)+" mph", "Number of times speeds greater than "+str(max_speed)+" mph", "Number times camera moved", "Start Date", "End Date"])
        for camera in report_dict:
            csv_writer.writerow([report_dict[camera]['camera_name'], report_dict[camera]['latitude'], report_dict[camera]['longitude'], report_dict[camera]['district'], report_dict[camera]['stopped'], report_dict[camera]['congestion'], report_dict[camera]['low_visibility'], report_dict[camera]['slow'], report_dict[camera]['pedestrian'], report_dict[camera]['wrong_way'], len(report_dict[camera]['speeds_lower_than_min_threshold']), len(report_dict[camera]['speeds_greater_than_max_threshold']), report_dict[camera]['num_times_camera_moved'], report_dict[camera]['start_date'], report_dict[camera]['end_date']])
        fp.close()



    with open(outputdir + 'incidents_by_timestamp.csv', 'w', newline='') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(['Camera Name', 'Latitude', 'Longitude', 'Timestamp', 'Incident Type', 'Incident Cleared By User', 'Incident Cleared On', 'Incident Cleared Duration (seconds)', 'Preset Index', "Analytics Mode"])
        for incident_dict in all_incidents_list:
            timestamp = incident_dict['timestamp']
            if timestamp >= start_ts and timestamp <= end_ts:
                dt = datetime.fromtimestamp(timestamp, tz)
                date_string = dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')
                cleared_by_user = 'YES' if incident_dict['clear_trigger'] == 'CLEARED_EXTERNAL' else 'NO'
                calib_mode = tmcdata_utility.getCalibrationMode(incident_dict['dbg']['calib_mode'])
                preset_index = incident_dict['dbg']['closest_preset'] + 1
                preset_status = f'On Preset {preset_index}' if preset_index > 0 else "Off Preset"
                latitude = incident_dict['camera_info']['latitude'] if 'latitude' in incident_dict['camera_info'] else 0
                longitude = incident_dict['camera_info']['longitude'] if 'longitude' in incident_dict['camera_info'] else 0
                incident_cleared = datetime.fromtimestamp(incident_dict['t_clear'], tz).strftime('%Y-%m-%d %H:%M:%S %Z%z')
                duration = incident_dict['t_clear'] - timestamp
                csv_writer.writerow([incident_dict['camera_info']['camera_name'], latitude, longitude, date_string, tmcdata_utility.get_incident_type(incident_dict['incident_type']), cleared_by_user, incident_cleared, duration, preset_status, calib_mode])
        fp.close()

    
    #districts = ["All", "Chattanooga", "Knoxville", "Memphis", "Nashville"]
    districts = ["All"]
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    headers = ["DOW"]
    for i in range(0, 24):
        a = "AM"
        if i >= 12:
            a = "PM"
        h = i % 12
        if h == 0:
            h = 12
        headers.append(str(h) + ' ' + a)

    for district in districts:
        with open(outputdir + 'incident_report_per_dow_in_' + district + '.csv', 'w', newline='') as fp:
            csv_writer = csv.writer(fp, delimiter=',')
            csv_writer.writerow(headers)
            for i in range(0, 7):
                row = [weekdays[i]]
                for j in range(0, 24):
                    row.append(0)
                for camera in report_dict:
                    if report_dict[camera]['district'] == district or district == "All":
                        for j in range(0, 24):
                            row[j+1] = row[j+1] + report_dict[camera]['stopped_dow'][i][j] + report_dict[camera]['congestion_dow'][i][j] + report_dict[camera]['slow_dow'][i][j] + report_dict[camera]['pedestrian_dow'][i][j] + report_dict[camera]['wrong_way_dow'][i][j]
                csv_writer.writerow(row)
            fp.close()
    
    print("----------FINISHED----------")

#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-dir", help="tmcdata directory path with ending /", default="/home/tvdev/trafficvision/webroot/tmcdata/")
    parser.add_argument("-outputdir", help="output directory path with ending /", default="/home/tvdev/")
    parser.add_argument("-timezone", help="Timezone of cameras", default="America/New_York")
    parser.add_argument("-start", help="Start date for report YYYYMMDD", default="20200101")
    parser.add_argument("-end", help="End date for report YYYYMMDD", default="20201231")
    parser.add_argument("-min_speed", help="Minimum speed threshold", default=25)
    parser.add_argument("-max_speed", help="Maximum speed threshold", default=90)

    args=parser.parse_args()

    create_incident_reports(args.dir, args.outputdir, args.timezone, args.start, args.end, args.min_speed, args.max_speed)
    '''
    tz = pytz.timezone(args.timezone)
    start_year = args.start[0:4]
    start_month = args.start[4:6]
    start_day = args.start[6:8]
    end_year = args.end[0:4]
    end_month = args.end[4:6]
    end_day = args.end[6:8]
    start_dt = datetime(int(start_year), int(start_month), int(start_day), 0, 0, 0, tzinfo=tz)
    end_dt = datetime(int(end_year), int(end_month), int(end_day), 23, 59, 59, tzinfo=tz)
    start_ts = start_dt.timestamp()
    end_ts = end_dt.timestamp()
    report_dict = {}
    all_incidents_list = []

    for camera_directory in os.listdir(args.dir):
        full_camera_path = args.dir + camera_directory + "/"
        if os.path.isdir(full_camera_path):
            # Get camera_info.json
            try:
                with open(full_camera_path + "camera_info.json", "r") as fp:
                    camera_info = json.load(fp)
                    camera_name = camera_info['camera_name']

                    incidents_list = tmcdata_utility.get_all_incidents_from_directory(full_camera_path+"incidents/")
                    for incident_dict in incidents_list:
                        incident_dict['camera_info'] = camera_info
                    all_incidents_list = all_incidents_list + incidents_list

                    report_dict[camera_name] = count_incidents(incidents_list, tz, start_ts, end_ts)
                    report_dict[camera_name]['camera_name'] = camera_name
                    report_dict[camera_name]['camera_index'] = camera_directory
                    report_dict[camera_name]['latitude'] = camera_info['latitude'] if 'latitude' in camera_info else 0
                    report_dict[camera_name]['longitude'] = camera_info['longitude'] if 'longitude' in camera_info else 0
                    report_dict[camera_name]['district'] = '' #get_district(camera_name[0])
                    
                    speed_threshold_dict = find_speed_boundaries(full_camera_path+"data/", args.min_speed, args.max_speed, int(args.start), int(args.end))
                    report_dict[camera_name]['speeds_greater_than_max_threshold'] = speed_threshold_dict['max_speeds_list']
                    report_dict[camera_name]['speeds_lower_than_min_threshold'] = speed_threshold_dict['min_speeds_list']
                    report_dict[camera_name]['num_times_camera_moved'] = speed_threshold_dict['num_times_camera_moved']
                    report_dict[camera_name]['start_date'] = speed_threshold_dict['start_date']
                    report_dict[camera_name]['end_date'] = speed_threshold_dict['end_date']
                    
                    fp.close()
            except Exception as e:
                print(e)

    
    # Print out csv files
    with open('incident_report_per_camera.csv', 'w', newline='') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(["Camera Name", "Latitude", "Longitude", "District", "Stopped Vehicle", "Congestion", "Low Visibility", "Slow Speeds", "Pedestrian", "Wrong Way", "Number of times speeds less than "+str(args.min_speed)+" mph", "Number of times speeds greater than "+str(args.max_speed)+" mph", "Number times camera moved", "Start Date", "End Date"])
        for camera in report_dict:
            csv_writer.writerow([report_dict[camera]['camera_name'], report_dict[camera]['latitude'], report_dict[camera]['longitude'], report_dict[camera]['district'], report_dict[camera]['stopped'], report_dict[camera]['congestion'], report_dict[camera]['low_visibility'], report_dict[camera]['slow'], report_dict[camera]['pedestrian'], report_dict[camera]['wrong_way'], len(report_dict[camera]['speeds_lower_than_min_threshold']), len(report_dict[camera]['speeds_greater_than_max_threshold']), report_dict[camera]['num_times_camera_moved'], report_dict[camera]['start_date'], report_dict[camera]['end_date']])
        fp.close()



    with open('incidents_by_timestamp.csv', 'w', newline='') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(['Camera Name', 'Latitude', 'Longitude', 'Timestamp', 'Incident Type', 'Incident Cleared By User', 'Incident Cleared On', 'Incident Cleared Duration (seconds)', 'Preset Index', "Analytics Mode"])
        for incident_dict in all_incidents_list:
            timestamp = incident_dict['timestamp']
            if timestamp >= start_ts and timestamp <= end_ts:
                dt = datetime.fromtimestamp(timestamp, tz)
                date_string = dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')
                cleared_by_user = 'YES' if incident_dict['clear_trigger'] == 'CLEARED_EXTERNAL' else 'NO'
                calib_mode = tmcdata_utility.getCalibrationMode(incident_dict['dbg']['calib_mode'])
                preset_index = incident_dict['dbg']['closest_preset'] + 1
                preset_status = f'On Preset {preset_index}' if preset_index > 0 else "Off Preset"
                latitude = incident_dict['camera_info']['latitude'] if 'latitude' in incident_dict['camera_info'] else 0
                longitude = incident_dict['camera_info']['longitude'] if 'longitude' in incident_dict['camera_info'] else 0
                incident_cleared = datetime.fromtimestamp(incident_dict['t_clear'], tz).strftime('%Y-%m-%d %H:%M:%S %Z%z')
                duration = incident_dict['t_clear'] - timestamp
                csv_writer.writerow([incident_dict['camera_info']['camera_name'], latitude, longitude, date_string, tmcdata_utility.get_incident_type(incident_dict['incident_type']), cleared_by_user, incident_cleared, duration, preset_status, calib_mode])
        fp.close()

    
    #districts = ["All", "Chattanooga", "Knoxville", "Memphis", "Nashville"]
    districts = ["All"]
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    headers = ["DOW"]
    for i in range(0, 24):
        a = "AM"
        if i >= 12:
            a = "PM"
        h = i % 12
        if h == 0:
            h = 12
        headers.append(str(h) + ' ' + a)

    for district in districts:
        with open('incident_report_per_dow_in_' + district + '.csv', 'w', newline='') as fp:
            csv_writer = csv.writer(fp, delimiter=',')
            csv_writer.writerow(headers)
            for i in range(0, 7):
                row = [weekdays[i]]
                for j in range(0, 24):
                    row.append(0)
                for camera in report_dict:
                    if report_dict[camera]['district'] == district or district == "All":
                        for j in range(0, 24):
                            row[j+1] = row[j+1] + report_dict[camera]['stopped_dow'][i][j] + report_dict[camera]['congestion_dow'][i][j] + report_dict[camera]['slow_dow'][i][j] + report_dict[camera]['pedestrian_dow'][i][j] + report_dict[camera]['wrong_way_dow'][i][j]
                csv_writer.writerow(row)
            fp.close()
    
    print("----------FINISHED----------")
    '''





