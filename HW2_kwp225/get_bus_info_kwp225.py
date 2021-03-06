# Kent Pan
# PUI HW2 Part 1

# import packages
from __future__ import print_function
import sys
import os
import json
try:
    import urllib2 as urllib
except ImportError:
    import urllib.request as urllib

# check for number of arguments
if not len(sys.argv) == 4:
    print ("Invalid number of arguments. Run as: python get_bus_info_kwp225.py <MTA_KEY> <BUS_LINE> <BUS_LINE>.csv")
    sys.exit()

# assigns arguments to variables
key = sys.argv[1]
line = sys.argv[2]
output = sys.argv[3]

# pulls bus data from MTA API
url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=" + key + "&VehicleMonitoringDetailLevel=calls&LineRef=" + line
response = urllib.urlopen(url)
data = response.read().decode("utf-8")
data = json.loads(data)

# navigates through JSON to specific bus activity
buses = data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']

# loop through each active bus, go to next stop information, and write information to output csv file
try:
    with open(output, 'w') as fhandler:
        fhandler.write('Latitude,Longitude,Stop Name,Stop Status,\n')
        for i in range(len(buses)):
            try: 
                fhandler.write(str(buses[i]['MonitoredVehicleJourney']['VehicleLocation']['Latitude']) + "," +
                               str(buses[i]['MonitoredVehicleJourney']['VehicleLocation']['Longitude']) + "," +
                               buses[i]['MonitoredVehicleJourney']['OnwardCalls']['OnwardCall'][0]['StopPointName'] + "," +
                               buses[i]['MonitoredVehicleJourney']['OnwardCalls']['OnwardCall'][0]['Extensions']['Distances']['PresentableDistance'] + '\n')
            except:
                fhandler.write(str(buses[i]['MonitoredVehicleJourney']['VehicleLocation']['Latitude']) + "," +
                               str(buses[i]['MonitoredVehicleJourney']['VehicleLocation']['Longitude']) + "," +
                               'N/A,N/A' + '\n')
except IOError as ex:
    print("Error performing I/O operations on the file: ",ex)