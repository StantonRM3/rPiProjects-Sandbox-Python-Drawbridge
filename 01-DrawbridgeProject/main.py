# Update to check GitHub sees it...
import RPi.GPIO as gpio     # Need to run on rPi...  Now do it directly again...
import time
import clsBridge
import clsLCD

# LCD Control Parameters
LCD_RST_PIN = 12            # pin number (Output)
LCD_RS_PIN = 25             # pin number (Output)
LCD_CS_PIN = 8              # pin number (Output)
LCD_SCLK_PIN = 11           # pin number (Output)
LCD_MOSI_PIN = 10           # pin number (Output)
LCD_RED_PIN = 6             # pin number (Output) - shared with trafic lights
LCD_GREEN_PIN = 26          # pin number (Output) - shared with trafic lights
LCD_BLUE_PIN = 18           # pin number (Output) - thrown away

# Bridge Control Parameters
BRIDGE_UP_PIN = 27           # pin number (Output)
BRIDGE_DOWN_PIN = 24         # pin number (Output)
BRIDGE_ENABLE_PIN = 5        # pin number (Output)`
BRIDGE_BUTTON_UP_PIN = 17    # pin number (Output)
BRIDGE_BUTTON_DOWN_PIN = 22  # pin number (Output)
BRIDGE_OPEN_SENSOR = 23      # pin number (Input)
BRIDGE_CLOSED_SENSOR = 7     # pin number (Input) XXXXXXX
BRIDGE_LIGHT_SENSOR = 16     # pin number (Input)
BRIDGE_LIGHTS = 12           # pin number (Output)
BRIDGE_THREAD_ID = 1         # Unique number for bridge thread

# Trafic Light Control Parameters
TL_RED_LED = 6              # pin number
TL_AMBER_LED = 13           # pin number
TL_GREEN_LED = 26           # pin number
TL_RED_SAFE_TIME = 5        # seconds

try:
    
    gpio.setmode(gpio.BCM)
    
    lcdDisplay = clsLCD.clsLCD(LCD_RST_PIN, LCD_RS_PIN, LCD_CS_PIN, 
                               LCD_SCLK_PIN, LCD_MOSI_PIN, LCD_RED_PIN, 
                               LCD_GREEN_PIN, LCD_BLUE_PIN)
    # gpio.setup(LCD_BLUE_PIN,gpio.OUT)
    # gpio.output(LCD_BLUE_PIN,gpio.LOW)
    # lcd.set_contrast(20)
    # lcd.clear()
    # lcd.set_cursor_position(0,0)
    # lcd.write('Rory Sweeney')
    # lcd.set_cursor_position(0,1)
    # lcd.write('- Initialising')
    # lcd.set_cursor_position(0,2)
    # lcd.write('- Closed')
    
    bridge = clsBridge.clsBridge(BRIDGE_THREAD_ID, 
                                 BRIDGE_UP_PIN, BRIDGE_DOWN_PIN, 
                                 BRIDGE_ENABLE_PIN,
                                 BRIDGE_BUTTON_UP_PIN, BRIDGE_BUTTON_DOWN_PIN,
                                 BRIDGE_OPEN_SENSOR, BRIDGE_CLOSED_SENSOR,
                                 TL_RED_LED, TL_AMBER_LED, TL_GREEN_LED, 
                                 TL_RED_SAFE_TIME)
    bridge.start()
    
    while True:
        
        try:
            
            # print("main: Loop forever, now sleep..")
            time.sleep(5)
        
        except(KeyboardInterrupt):

            print("main: Executing KeyboardInterupt code")
            raise
        
        except:

            print('main: Unknown exception thrown within infinate loop')
    
except(KeyboardInterrupt):
    
    print('main: Closing the bridge thread...')
    bridge.cleanup()

except:
    
    print('main: Unhandled exception thrown')
    
finally:
            
    gpio.cleanup()
    print('main: FINISHED AND GOING HOME')
    
    quit()
    
#    os.system('sudo shutdown -h now')