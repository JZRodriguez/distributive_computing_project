#!/usr/bin/env python3

import psycopg2
from config import config
import xml.etree.ElementTree as ET
from datetime import date
from datetime import datetime
import matplotlib.pyplot as plt
import subprocess


def connect() :
    conn = None
    try :
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        print('PostgreSQL database version: ')
        sql = "SELECT * from gpus"
        cur.execute(sql)
        records = cur.fetchall()
        cur.close()

        X = []
        Y = []
        fig = plt.figure()
        ax = fig.add_subplot(111)

        for row in records :
            Y.append(float(row[1].replace('$', '').replace(',', '')))
            date = datetime.date()
            time = datetime.time()
            datiteme = date + time
            X.append(datiteme)

        ax.plot(X, Y)
        plt.savefig("/data/team3/gpus.png")
        
        process = subprocess.Popen(['scp','/data/team3/gpus.png','team3@10.99.1.138:/home/jzuniga/public_html/static/'],stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(stdout, stderr)

    except (Exception, psycopg2.DatabaseError) as error :
        print(error)
    finally :
        if conn is not None :
            conn.close()
            print('Database connection closed.')

if __name__ == '__main__' :
    connect()
