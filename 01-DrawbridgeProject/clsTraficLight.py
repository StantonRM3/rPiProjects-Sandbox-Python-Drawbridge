# Trafic Light Class
import RPi.GPIO as gpio
import time

class clsTraficLight:

    # Initialise the class object with:
    # -- redPin - The GPIO RedPin number
    # -- amberPin - The GPIO AmberPin number
    # -- greenPin - The GPIO GreenPin number
    # -- safeRedTime - The time after the light goes Red before the object 
    #                  will return
    # ---- This is to accomodate time required to clear the danger zone 
    #      i.e. once the light goes red, we may wait 10 seconds before
    # ---- returning to allow the roadway to clear
    def __init__(self, redPin, amberPin, greenPin, safeRedTime):
    
        self.RED_LED = redPin
        self.AMBER_LED = amberPin
        self.GREEN_LED = greenPin
        
        gpio.setup(self.RED_LED, gpio.OUT)     
        gpio.setup(self.AMBER_LED, gpio.OUT)
        gpio.setup(self.GREEN_LED, gpio.OUT)
        
        self.SAFE_TIME = safeRedTime
        
        self.INIT_SPEED = 0.5     # Cycle speed during light init stage 
        self.LIGHT_SEQ_SPEED = 5  # Speed trafic lights cycle colours (5s)

        self.test()               # Initialise/test the lights...
        
        # Start lights in stop state ...
        gpio.output(self.RED_LED, gpio.LOW)     
        gpio.output(self.AMBER_LED, gpio.LOW)
        gpio.output(self.GREEN_LED, gpio.HIGH)

    def test(self):

        print('+---------------------------+')
        print('| Testing the trafic lights |')
        print('+---------------------------+')
        
        for i in range(8):
            
            binStr = '{0:03b}'.format(i)
#            print(binStr)

            tst_green = binStr[2]
            tst_amber = binStr[1]
            tst_red = binStr[0]
            
            if tst_red == '0':
                gpio.output(self.RED_LED, gpio.LOW)
            else:
                gpio.output(self.RED_LED, gpio.HIGH)
            
            if tst_amber == '0':
                gpio.output(self.AMBER_LED, gpio.LOW)
            else:
                gpio.output(self.AMBER_LED, gpio.HIGH)

            if tst_green == '0':
                gpio.output(self.GREEN_LED, gpio.LOW)
            else:
                gpio.output(self.GREEN_LED, gpio.HIGH)
                
            time.sleep(self.INIT_SPEED)

        print('+---------------------+')
        print('| Lights tested... ok |')
        print('+---------------------+')
        
    def stop(self):
        
        print('+--------------------+')
        print('| Stopping Trafic... |')
        print('+--------------------+')
#        print('|   RED:Off          |')
#        print('|   AMBER:On         |')
#        print('|   GREEN:On         |')
        gpio.output(self.RED_LED, gpio.LOW)
        gpio.output(self.AMBER_LED, gpio.HIGH)
        gpio.output(self.GREEN_LED, gpio.HIGH)
    
        time.sleep(self.LIGHT_SEQ_SPEED)

        # print('+--------------------+')
        # print('|   RED:Off          |')
        # print('|   AMBER:On         |')
        # print('|   GREEN:Off        |')
        gpio.output(self.RED_LED, gpio.LOW)
        gpio.output(self.AMBER_LED, gpio.HIGH)
        gpio.output(self.GREEN_LED, gpio.LOW)
        
        time.sleep(self.LIGHT_SEQ_SPEED)
 
#        print('+--------------------+')
#        print('|   RED:On           |')
#        print('|   AMBER:Off        |')
#        print('|   GREEN:Off        |')
        gpio.output(self.RED_LED, gpio.HIGH)
        gpio.output(self.AMBER_LED, gpio.LOW)
        gpio.output(self.GREEN_LED, gpio.LOW)

        print('+--------------------+')
        print('| TRAFIC... Stopped  |')
        print('+--------------------+')
        print('| WAITING SAFE TIME  |')
        print('| B4 RAISING BRIDGE  |')
        print('+--------------------+')       
        time.sleep(self.SAFE_TIME)

        print('+--------------------+')       
        print('|SAFE 2 RAISE BRIDGE |')
        print('+--------------------+')

    def go(self):

        print('+--------------------+')
        print('| Starting Trafic... |')
        print('+--------------------+')
        # print('|   RED:On           |')
        # print('|   AMBER:Off        |')
        # print('|   GREEN:Off        |')
        gpio.output(self.RED_LED, gpio.HIGH)
        gpio.output(self.AMBER_LED, gpio.LOW)
        gpio.output(self.GREEN_LED, gpio.LOW)
    
        time.sleep(self.LIGHT_SEQ_SPEED)
        
        # print('+--------------------+')
        # print('|   RED:Off          |')
        # print('|   AMBER:Off        |')
        # print('|   GREEN:On         |')
        gpio.output(self.RED_LED, gpio.LOW)
        gpio.output(self.AMBER_LED, gpio.LOW)
        gpio.output(self.GREEN_LED, gpio.HIGH)

        # print('+--------------------+')
        # print('| TRAFIC... Moving   |')
        # print('+--------------------+')  

    def cleanup(self):
        
        print('clsTraficLight.cleanup: Closing the thread...')
        gpio.output(self.RED_LED, gpio.LOW)
        gpio.output(self.AMBER_LED, gpio.LOW)
        gpio.output(self.GREEN_LED, gpio.LOW)
    