# importing modules
import configparser
import os.path
from datetime import date
from google.oauth2 import credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# defining scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 
            'https://www.googleapis.com/auth/drive']

# extracting data from config.ini file
configur = configparser.ConfigParser()
CONFIG_FILE = 'config.ini'
configur.read(CONFIG_FILE)
SUBJECT = configur.get('DEFAULT', 'Subject')
SPREADSHEET_ID = configur.get('DEFAULT', 'SpreadsheetID')
FOLDER_ID = configur.get('DEFAULT', 'FolderID')
FIRST_RUN = configur.get('DEFAULT', 'FirstRun')


def authenticator():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    spreadsheet = build('sheets', 'v4', credentials = creds)
    gdrive = build('drive', 'v3', credentials = creds)
    return spreadsheet, gdrive

def link_generator(folder_id, gdrive):
    # list(q = "'" + id + "' in parents", pageSize=10, fields="nextPageToken, files(id, name)").execute()
    QUERY = "'" + folder_id + "' in parents and mimeType = 'video/mp4' or mimeType = 'video/x-matroska'" 
    files = gdrive.files().list(q = QUERY, pageSize = 10,
                                fileds = "nextPageToken, files(id, name").execute()
    
    items = files.get('files', [])
    file_ids = []
    for item in items:
        file_ids.append(item['id'])

    share_links = []

    if FIRST_RUN:
        for id in file_ids:
            share = gdrive.new_batch_http_request()
            domain_permission = {
                'type' : 'domain',
                'role' : 'reader',
                'domain' : 'srmist.edu.in'
            }
            share.add(gdrive.permissions().create(
                fileId = id,
                body = domain_permission,
                fields = 'id',
            ))
            share.execute()
            link = 'https://drive.google.com/file/d/' + id + '/view?usp=sharing'
            share_links.append(link)
            # todo: turn the first run flag off

    else:
        cur_date = date.today()
        

    
    