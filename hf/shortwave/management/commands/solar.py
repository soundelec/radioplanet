# weather.py - retrieve space weather info from N0NBH and display in database
import xml.etree.ElementTree as ET
import os, requests
from django.core.management.base import BaseCommand, CommandError
from shortwave.models import SolarData, Language

file = 'solar.xml'
solardata = "http://www.hamqsl.com/solarxml.php"

# We comment the next lines out during development to avoid repeated requests to hamqsl

# Request the solarxml.php file and write it as solar.xml
r = requests.get(solardata, allow_redirects=True)
open(file, 'wb').write(r.content)

# Initialise the XML tree with ElementTree
tree = ET.parse('solar.xml')
root = tree.getroot()

# We need to retrieve the following: solarflux, aindex, kindex, sunspots, geomagfield, signalnoise
for solarflux in root.iter('solarflux'):
    solarflux = int(solarflux.text)

for aindex in root.iter('aindex'):
    aindex = int(aindex.text)

for kindex in root.iter('kindex'):
    kindex = int(kindex.text)

for sunspots in root.iter('sunspots'):
    sunspots = int(sunspots.text)

for geomagfield in root.iter('geomagfield'):
    geomagfield = str(geomagfield.text)

for signalnoise in root.iter('signalnoise'):
    signalnoise = str(signalnoise.text)

print(solarflux, aindex, kindex, sunspots, geomagfield, signalnoise)

class Command(BaseCommand):
    help = 'Retrieves solar data from hamqsl.com and adds it to SolarData model'

    def handle(self, *args, **options):
        SolarData.objects.all().delete() # Delete old solar data - we only need most recent
        SolarData.objects.create(solarflux=solarflux,
        aindex=aindex,
        kindex=kindex,
        sunspots=sunspots,
        geomagfield=geomagfield,
        signalnoise=signalnoise)
        self.stdout.write('Written solar data to model')
        os.remove('solar.xml')
