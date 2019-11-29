# LCD Display Class
import RPi.GPIO as gpio
import dot3k.lcd as lcd

class clsLCD:
    
    def __init__(self, rstPin, rsPin, csPin, sclkPin, mosiPin, 
                 redPin, greenPin, bluePin):
        
        self.RED_PIN = redPin
        self.GREEN_PIN = greenPin
        self.BLUE_PIN = bluePin
        
        gpio.setup(self.RED_PIN, gpio.OUT)
        gpio.setup(self.GREEN_PIN, gpio.OUT)
        gpio.setup(self.BLUE_PIN, gpio.OUT)
        
        # Force blue pin low, we wont use it as the LCD background colour 
        # will be triggered by the trafic lights
        gpio.output(self.BLUE_PIN, gpio.LOW)
        
        lcd.set_contrast(20)
        lcd.clear()

        self.write_line_1('Rory Sweeney')
        self.write_line_2('- Initialising')
        self.write_line_3('- Setup LCD')
        
    def write_line_1(self, message):
    
        lcd.set_cursor_position(0, 0)
        lcd.write(message)

    def write_line_2(self, message):
    
        lcd.set_cursor_position(0, 1)
        lcd.write(message)
        
    def write_line_3(self, message):
    
        lcd.set_cursor_position(0, 2)
        lcd.write(message)