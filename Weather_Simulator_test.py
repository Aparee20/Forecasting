import unittest
from datetime import datetime 
from  Weather_Simulator import get_pressure , get_temperature ,get_humidity ,get_localtime,get_weather,get_elevation

import time

class TestWeatherMethods(unittest.TestCase):
    
    
    def setUp(self):
        self.startTime = time.time()

# Unit Test pressure 

    def test_get_pressure(self):
        for i in xrange(1,10):
            self.assertIsNotNone(get_pressure(1000+i))
            self.assertNotEqual(get_pressure(1000+i),0)
       
            
# Unit Test Temprature 
       
    def test_get_temperature(self):
        for i in xrange(1,10):
            self.assertIsNotNone(get_temperature(1000))
        self.assertTrue(-30<get_temperature(1000)<50)
            
        
# Unit Test Humidity 
       
    def test_get_humidity(self):
        for i in xrange(1,10):
            self.assertIsNotNone(get_humidity())
            self.assertTrue(69<get_humidity()<101)        

# Unit Test Local Time    
    
    def test_get_localtime(self):
        for i in xrange(1,10):
            self.assertIsNotNone(get_localtime(0,12))
            timeinp=get_localtime(0,12)
            hr=timeinp.hour
            self.assertTrue(0<=hr<=12)

 # Unit Test Weather conditions  
        
    def test_get_weather(self):
        self.assertIsNotNone(get_weather(90,25,1000,991))
        self.assertEqual(get_weather(90,25,1000,990),'Rain')
        self.assertEqual(get_weather(80,25,1000,1010),'Sunny')
        self.assertEqual(get_weather(90,-25,1000,980),'Snow')

 # Unit Test Elevation   

    def test_get_elevation(self):
        self.assertIsNotNone(get_elevation(90,25,False))
        self.assertEqual(get_elevation(-21.92,130.22,False),501)
    
        
    
if __name__ == '__main__':
    unittest.main()