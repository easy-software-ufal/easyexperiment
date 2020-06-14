# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import psycopg2


# GAZE_DATA_FILE = 'c:\\users\\nando\\desktop\\gaze_data.txt'
# utils
# def clear_gaze_data_file():
#     open(GAZE_DATA_FILE, 'w').close()

def read_gaze_data_file(gaze_data_file):
    with open(gaze_data_file, 'r') as filehandle:
        return filehandle.readlines()


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

        # participants = []
        # while row is not None:
        #    participants.append(row)
        #    row = cur.fetchone()
        cur.close()

        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def update_data_for_participant(participant_id, data):
    """ query data from the vendors table """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        print participant_id
        result = cur.execute("UPDATE experiments_participant SET task2_data = %s WHERE id = %s", (data, participant_id))
        print result
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print 'deu ruim'
        print(error)
    finally:
        if conn is not None:
            conn.close()


# datetime.fromtimestamp(task1_end).strftime('%Y-%m-%d %H:%M:%S')

## read_gaze_data_file(task1_start, task1_end)

gaze_data_file = 'c:\\users\\nando\\desktop\\Dennis2.txt'
data = read_gaze_data_file(gaze_data_file)
update_data_for_participant(26, data)
