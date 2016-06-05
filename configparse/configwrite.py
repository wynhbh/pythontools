import os
import sys
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('sample.info')
    
with open('ek_angler') as samples:
    for line in samples:
        samplename = line.strip()
        config.set("sample", "name", samplename)
        config.write(open('sample.info', 'w'))
        os.system('cat sample.info')