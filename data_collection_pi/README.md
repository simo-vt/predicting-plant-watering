# Component - Data Collection with Raspberry Pi

## Requirements

The following packages are required to run this project:

- IDE running Python
- pyserial
- gspread
- numpy
- A configured Google Sheets project in Google Console (and obtained `creds.json`)
- A Google Sheet configured to accept writes from te Google Sheets service account

## Running the project

1. Create a `creds.json` file with the credentials given by Google Console
2. Change the Spreadsheet ID in the variable `spreadsheet_id`
3. Run the resulting `collection.py` file