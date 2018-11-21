# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import psycopg2
from datetime import datetime, timedelta
import numpy as np

GAZE_DATA_FILE = 'c:\\users\\nando\\desktop\\gaze_data.txt'
# utils
def clear_gaze_data_file():
    open(GAZE_DATA_FILE, 'w').close()

def read_gaze_data_file(start_date, end_date):
    with open(GAZE_DATA_FILE, 'r') as filehandle:
        for line in filehandle:
            row = line.split('\t')
            print datetime.fromtimestamp(float(row[2].replace(',', '.')))

def get_connection():
    return psycopg2.connect("dbname=easy user=postgres password=postgres")

def get_participant(participant_id):
    """ query data from the vendors table """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM experiments_participant WHERE id = %s ORDER BY id desc" % participant_id)
        row = cur.fetchone()
        
        #participants = []
        #while row is not None:
        #    participants.append(row)
        #    row = cur.fetchone()
        cur.close()

        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

task1_start = get_participant(27)[7]
task1_end = get_participant(27)[6]

print task1_start
print task1_end

print datetime.fromtimestamp(41546414.8935177).strftime('%Y-%m-%d %H:%M:%S')
print datetime.fromtimestamp(41546425.9464115).strftime('%Y-%m-%d %H:%M:%S')

excel_date = 41546414
dt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + excel_date - 2)
tt = dt.timetuple()
print dt
print tt

# datetime.fromtimestamp(task1_end).strftime('%Y-%m-%d %H:%M:%S')

## read_gaze_data_file(task1_start, task1_end)