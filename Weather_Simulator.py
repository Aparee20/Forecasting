import sys
import urllib2
import json
import random
import math
from random import randint,uniform
from datetime import datetime
from urllib2 import urlopen
import json

'''
Pressure drop with increase in altitude is not uniform. Pressure drop takes place @
about 90 mb(mili bar) per km rise in altitude up to a distance of 6 km.That is
about 50% drop in air pressure takes place at an altitude of 5.5 km up in the troposphere.
Beyond 6 Km rate of pressure drop slows down and it is about @ 20 mb/km upto a height of 30 km.
There after rate of pressure drop further slows downAssuming at sea level pressure is 1013.25 .

'''
def get_pressure(elevation):
    '''This function returns pressure at a certain elevation. '''
    if (elevation <= 6000):
        pressure=random.uniform(980.25,1013.25)-(elevation/1000)*90
        
        return round(pressure,1)
    else:
        pressure=random.uniform(980.25,1013.25)-(6000/1000)*90+(elevation-6000/1000)*20
        return round(pressure,1)


''' 
The temperature in the troposphere usually decreases with
height at the average lapse rate of 6.5 C per kilometer.
The air in the troposphere is more unstable and with strong convection .

'''      
def get_temperature(elevation):
    '''This function returns temprature at a certain elevation '''
    temp = 30-int((elevation/1000)*6.5)
    temperature=float(random.uniform(0.0,1.0))* 2*temp-temp +20
    return round(temperature,1)


'''
High Humidity causes rain .

'''
def get_humidity():
    '''This function returns humidity at a certain elevation '''
    humidity=randint(70,100)
    return humidity
    

'''
Random localtime.

'''
def get_localtime(hrmin,hrmax):
    '''This function returns  random Local time  '''
    year = randint(2015, 2016)
    month = randint(1, 12)
    day = randint(1, 28)
    hr = randint(hrmin,hrmax)
    mi = randint(0, 59)
    ss = randint(0, 59)
    local_time = datetime(year, month, day, hr, mi, ss)
    return local_time


'''
High Humidity causes rain.

'''
def get_weather(humidity,temperature,elevation,pressure):
    '''This function returns climatic conditions '''
    
    if temperature>0  and humidity <90 :
        return 'Sunny'
    elif temperature<=0: 
        return 'Snow'   
    elif  humidity>=90  and temperature>0 and pressure<1000:
        return 'Rain'
    else: return 'Sunny'  

'''
Elevation derieved from google map api.

'''
def get_elevation(xLat, yLong, sensor=False):
    '''This function returns elevation of a location based on longitude and latitude'''
    ELEVATION_BASE_URL = 'http://maps.google.com/maps/api/elevation/json'
    URL_PARAMS = "locations=%.7f,%.7f&sensor=%s" % (xLat,yLong, "false")
    url = ELEVATION_BASE_URL + "?" + URL_PARAMS
    response = urllib2.urlopen(url)
    jsondata = response.read().decode()
    data = json.loads(jsondata)
    status = data['status']
    if status == 'OK':
        result = data['results'][0]
        elevation = int(result['elevation'])
    else:
        elevation=100  
    return elevation


'''
Result generated in the required format.

'''
def generate_data(lat,lon,num_rows,radius):
    '''This function calculates random latitude and longitude based on a point on earth with 
    certian radius defined and publishes the weather conditions at various location '''
    radiusInDegrees=radius/111300
    r = radiusInDegrees
    x0 = lat
    y0 = lon

    f = open('Weather_data.txt', 'w+')
    sys.stdout = f
    
    placelst =['Sydney','Melbourne','Albury','Armidale','Darwin'   ,'Mackay','Hamilton','Perth','Geelong','Karratha','Cairns','Newcastle','Tamworth','Wollongong','Grafton']
    len_pl_lst=len(placelst);
    place=random.sample(placelst,len(placelst)-1)
    lst_iter=0
    
    for i in range(0,num_rows):
        u = float(random.uniform(0.0,1.0))
        v = float(random.uniform(0.0,1.0))
        w = r * math.sqrt(u)
        t = 2 * math.pi * v
        x = w * math.cos(t)
        y = w * math.sin(t)
   
        xLat  = round(float(x) + float(x0),2)
        yLong = round(float(y) + float(y0),2)
        
        elevation = get_elevation(xLat,yLong)
        pressure = get_pressure(elevation)
        temperature = get_temperature(elevation)
        

        if temperature>-1 and temperature<1:
           output_temperature=0
        else:output_temperature = "{0:+.1f}".format(temperature)

   
        humidity =get_humidity()
        weather = get_weather(humidity,temperature,elevation,pressure)
        
        if weather=='Sunny':
            local_time = get_localtime(07,19)
        else:
            local_time = get_localtime(0,23)
        
        Output_time_format = local_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        if lst_iter==len_pl_lst-2:
            lst_iter=1
        else:
            lst_iter=lst_iter+1
            
        
        print(place[lst_iter]+str('|')+str(xLat)+str(',')+str(yLong)+str(',')+str(elevation)+str('|')+str(Output_time_format)+str('|')+weather+str('|')+str(output_temperature)+str('|')+str(pressure)+str('|')+str(humidity))
        
        
    f.close()

if __name__ == "__main__":
    
    if len(sys.argv)<2:
        print "Execution details :Weather_forecast.py <num_rows>"
        sys.exit
    else:
        records_gen = int(sys.argv[1])
        radius=1000000
        generate_data(-24.61, 134.64,records_gen,radius)
