# serial is pyserial
import serial
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import time
import numpy as np

# Serial port configuration
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust the baud rate if necessary
i = 0

# Function to authenticate with Google Sheets
def open_sheet(credential_file_path, spredsheet_id, worksheet):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_file_path, scope)
    gc = gspread.authorize(credentials)
    worksheet = gc.open_by_key(spredsheet_id).worksheet(worksheet)
    return worksheet

credentials_file_path = 'creds.json'
spreadsheet_id = 'XXXXXXXXXXXXXXXXXXXXXXXX'
worksheet_name = 'readings'

worksheet = open_sheet(credentials_file_path, spreadsheet_id, worksheet_name)

# Get the current time
start_time = time.time()
upload_interval = 600
interval_readings = []

while True:
    current_time = time.time()

    # Read data from serial port
    data = ser.readline().strip().decode('utf-8')
    data_split = data.split(",")
    
    if len(data_split) != 3:
        print("Data is incorrect, skipping")
        continue
    
    readings = [ float(data_split[0]), float(data_split[1]), int(data_split[2]) ]
    
    interval_readings.append(readings)
    
    print(readings)
    
    # Check if it's time to upload to Google Sheets
    if current_time - start_time >= upload_interval:        
        avg_air_humidity = np.average([ r[0] for r in interval_readings ])
        avg_air_temperature = np.average([ r[1] for r in interval_readings ])
        avg_soil_moisture = np.average([ r[2] for r in interval_readings ])
    
        # Update Google Sheets
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_to_upload = [timestamp, avg_air_humidity, avg_air_temperature, avg_soil_moisture]
        
        try:
            worksheet.append_row(data_to_upload)
        except Exception as e:
            print(f"Error: {e}")

        # Reset the start time
        start_time = current_time
        interval_readings = []

