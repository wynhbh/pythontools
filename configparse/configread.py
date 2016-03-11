import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('mal.conf')

path = config.get('basic','path')
mysql_server = config.get('basic','mysql')
server = config.get('server','server')
server_port = config.get('server','port')

print path,mysql_server,server,server_port

