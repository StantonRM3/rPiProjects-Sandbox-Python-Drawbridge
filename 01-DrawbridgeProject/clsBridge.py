import threading
import RPi.GPIO as gpio
import time
import clsTraficLight 
   
class clsBridge(threading.Thread):
    
    # Initialise the class object with:
    # -- threadId - This class is designed to run in a thread.  
    #               This enables it to run forever until the main program
    #               exits.  ThreadId is a unique thread number assigned by 
    #               the main program
    # -- upPin - The GPIO motor drive up pin number
    # -- downPin - The GPIO motor drive down pin number
    # -- enablePin - The GPIO motor on/off pin number
    # -- openSensor - The GPIO bridge open sensor pin number
    # -- closedSensor - The GPIO bridge closed sensor pin number
    # -- redPin - The GPIO trafic lights redPin number
    # -- amberPin - The GPIO trafic lights amberPin number
    # -- greenPin - The GPIO trafic lights greenPin number
    # -- safeRedTime - The time after the light Red before the object returns
    # ---- This is to accomodate time required to clear the danger zone 
    #      i.e. once the light goes red, we may wait 10 seconds before
    # ---- returning to allow the roadway to clear

    def __init__(self, threadId, upPin, downPin, enablePin, upButtonPin, 
                 downButtonPin, openSensor, closedSensor, 
                 redPin, amberPin, greenPin, safeRedTime):   

        threading.Thread.__init__(self)

        self.THREAD_ID = threadId
        
        # Motor, control and sensor pins... 
        self.UP_MOTOR = upPin
        self.DOWN_MOTOR = downPin
        self.ENABLE_MOTOR = enablePin
        self.UP_BUTTON = upButtonPin
        self.DOWN_BUTTON = downButtonPin
        self.SENSOR_OPEN = openSensor
        self.SENSOR_CLOSED = closedSensor

        # Trafic light pins...
        self.RED_LED = redPin
        self.AMBER_LED = amberPin
        self.GREEN_LED = greenPin
        self.SAFE_TIME = safeRedTime
        
        # Some prgram constants to tell us where/what the bridge is doing...
        self.BRIDGE_CLOSED = 'Closed'
        self.BRIDGE_MOVING = 'Moving'
        self.BRIDGE_POSITION_MIDWAY = 'Midway'
        self.BRIDGE_OPEN = 'Open'
        self.BRIDGE_POSITION = self.BRIDGE_CLOSED
        
        # Set the pins as inputs (rx info) or outputs (tx info)...
        gpio.setup(self.UP_MOTOR, gpio.OUT)
        gpio.setup(self.DOWN_MOTOR, gpio.OUT)
        gpio.setup(self.ENABLE_MOTOR, gpio.OUT)
        
        # Special setups to handle control buttons.
        # -- pull_up_down - remove 'random' states when buttons not pressed
        # -- add_event_detect - used to set an interupt to notify program when
        #    an input is rxed and what to do i.e. the up/down buttons pressed.
        gpio.setup(self.UP_BUTTON, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.add_event_detect(self.UP_BUTTON, gpio.RISING, 
                              callback=self.cb_open_button_pressed, 
                              bouncetime=1000)
        gpio.setup(self.DOWN_BUTTON, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.add_event_detect(self.DOWN_BUTTON, gpio.FALLING, 
                              callback=self.cb_close_button_pressed, 
                              bouncetime=1000)
        
        # Set the sensors on the bridge to detect when the bridge is fully 
        # open or closed...
        gpio.setup(self.SENSOR_OPEN, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.add_event_detect(self.SENSOR_OPEN, gpio.RISING, 
                              callback=self.cb_bridge_open_sensor, 
                              bouncetime=300)
        gpio.setup(self.SENSOR_CLOSED, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.add_event_detect(self.SENSOR_CLOSED, gpio.RISING, 
                              callback=self.cb_bridge_closed_sensor, 
                              bouncetime=300)
        
        # Create a trafic light object (see clsTraficLight...
        self.traficLight = clsTraficLight.clsTraficLight(self.RED_LED,
                                                         self.AMBER_LED,
                                                         self.GREEN_LED,
                                                         self.SAFE_TIME)
        
        # Run a self_test on the bridge to ensure it is working and set it to 
        # a known state before running proper...
        self.test()
       
    def test(self):

        print('-----------------------------------------')
        print('| Testing the bridge motors and sensors |')
        print('-----------------------------------------')
        print('Bridge is left closed/down')
        self.BRIDGE_POSITION = self.BRIDGE_CLOSED

    def cb_open_button_pressed(self, channel):

        print('')
        print('INTERUPT: Open button pressed...')
        
        if ((self.BRIDGE_POSITION == self.BRIDGE_CLOSED) or 
           (self.BRIDGE_POSITION == self.BRIDGE_POSITION_MIDWAY)):
            
            if self.BRIDGE_POSITION == self.BRIDGE_CLOSED:
                
                print('Open the bridge...')
                self.traficLight.stop()
                
            else: 
            
                print('Continue to open the bridge...')
                
            gpio.output(self.UP_MOTOR, gpio.HIGH)
            gpio.output(self.DOWN_MOTOR, gpio.LOW)
            gpio.output(self.ENABLE_MOTOR, gpio.HIGH)
            
            self.BRIDGE_POSITION = self.BRIDGE_MOVING
            
        elif self.BRIDGE_POSITION == self.BRIDGE_MOVING:
            
            print('Stop the bridge...')
            
            gpio.output(self.ENABLE_MOTOR, gpio.LOW)
            
            self.BRIDGE_POSITION = self.BRIDGE_POSITION_MIDWAY
       
        else:
            
            print('Bridge already open, ignoring open request')
            
        print('BRIDGE_POSITION: ', self.BRIDGE_POSITION)
        
    def cb_close_button_pressed(self, channel):

        print('')
        print('INTERUPT: Close button pressed...')
        
        if ((self.BRIDGE_POSITION == self.BRIDGE_OPEN) or 
           (self.BRIDGE_POSITION == self.BRIDGE_POSITION_MIDWAY)):
 
            print('Close the bridge...')
                
            gpio.output(self.UP_MOTOR, gpio.LOW)
            gpio.output(self.DOWN_MOTOR, gpio.HIGH)
            gpio.output(self.ENABLE_MOTOR, gpio.HIGH)
            
            self.BRIDGE_POSITION = self.BRIDGE_MOVING
            
        elif self.BRIDGE_POSITION == self.BRIDGE_MOVING:
            
            print('Stop the bridge...')
            
            gpio.output(self.ENABLE_MOTOR, gpio.LOW)
            
            self.BRIDGE_POSITION = self.BRIDGE_POSITION_MIDWAY
       
        else:
            
            print('Bridge already open, ignoring open request')

        print('BRIDGE_POSITION: ', self.BRIDGE_POSITION)
        
    def cb_bridge_open_sensor(self, channel):

        print('')
        print('INTERUPT: Bridge open sensor detected...')
        
        gpio.output(self.ENABLE_MOTOR, gpio.LOW)
        
        self.BRIDGE_POSITION = self.BRIDGE_OPEN
                        
        print('BRIDGE_POSITION: ', self.BRIDGE_POSITION)

    def cb_bridge_closed_sensor(self, channel):
        
        print('')
        print('INTERUPT: Bridge closed sensor detected...')
        
        gpio.output(self.ENABLE_MOTOR, gpio.LOW)
        
        # Only change the lights to green once, if the bridge was moving and 
        # has now stopped.  If this triggers again then ignore it...
        if self.BRIDGE_POSITION == self.BRIDGE_MOVING:
            
            self.traficLight.go()
        
        self.BRIDGE_POSITION = self.BRIDGE_CLOSED
                        
        print('BRIDGE_POSITION: ', self.BRIDGE_POSITION)
        
    def run(self):
        
        while True:
            
            try:

                print('BRIDGE WAITING FOR SOMETHING TO DO....')

                time.sleep(60)
                
            except:
            
                print('clsBridge.run: Died of something?!?!?!')
                    
    def cleanup(self):
        
        self.traficLight.cleanup()
        
        print('clsBridge.cleanup: Closing the thread...')

        gpio.output(self.UP_MOTOR, gpio.LOW)
        gpio.output(self.DOWN_MOTOR, gpio.LOW)