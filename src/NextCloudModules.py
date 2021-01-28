import os
import requests
import xml.etree.ElementTree as ET
import urllib.request
import base64

class NextCloudModules:

    def __init__(self):
        self.url = os.getenv('NEXT_CLOUD_URL')
        self.user = os.getenv('NEXT_CLOUD_USER')
        self.password = os.getenv('NEXT_CLOUD_PASSWORD')
        self.down_load_dir = './static/Downloads/'
    
    def get_file_list(self, dir_name: str):
        url = self.url + '/remote.php/dav/files/fyui001/' + dir_name
        req = requests.Request('PROPFIND', url, headers={'Depth': '1'},auth=(self.user, self.password))
        prepped = req.prepare()
        
        s = requests.Session()
        resp = s.send(prepped)
        root = ET.fromstring(resp.text)
        
        files = [ f.text for f in root.findall('.//{DAV:}href') if f.text[-1] != '/' ]

        if (files):
            return files
        
        return False

    def get_file(self, file_path: str, file_name):
        basic_auth_info = base64.b64encode(f'{self.user}:{self.password}'.encode('utf8'))
        url = self.url + file_path
        request = urllib.request.Request(
            url,
            headers = {'Authorization': 'Basic ' + basic_auth_info.decode('utf-8')}
        )

        with urllib.request.urlopen(request) as res:
            data = res.read()

        with open (self.down_load_dir + file_name, mode='wb') as f:
            f.write(data)
        
        return self.down_load_dir + file_name