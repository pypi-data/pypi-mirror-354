import Utilies
from Utilies import Chrome
from Utilies.SFTP import  RemoteConnection
ch = Chrome()
ch.Open_Chrome()
rm = RemoteConnection(  # Connect to the server
            ipaddress='', username='', password='', port = '')
rm.connect_server()