#!/usr/bin/env python

###############################################
# Based on the code from Sunfounder SuperKit  #
###############################################

from time import sleep

class LCD_DISPLAY:
    LCD_CLEAR_DISPLAY = 0x01

    def __init__(self, pin_rs=14, pin_e=15, pins_db=[17, 18, 27, 22], GPIO = None):
        import RPi.GPIO as GPIO
	self.GPIO = GPIO
	self.pin_rs = pin_rs
	self.pin_e = pin_e
	self.pins_db = pins_db
        self.used_gpio = self.pins_db

        self.GPIO.setwarnings(False)
	self.GPIO.setmode(GPIO.BCM)
        self.GPIO.setup(self.pin_e, GPIO.OUT)
	self.GPIO.setup(self.pin_rs, GPIO.OUT)
        
	for pin in self.pins_db:
	    self.GPIO.setup(pin, GPIO.OUT)

	self.write4bits(0x33) # initialization
	self.write4bits(0x32) # initialization
	self.write4bits(0x28) # 2 line 5x7 matrix
	self.write4bits(0x0C) # turn cursor off 0x0E to enable cursor
	self.write4bits(0x06) # shift cursor right
        self.clear()

    def clear(self):
	self.write4bits(self.LCD_CLEAR_DISPLAY) # command to clear display
	self.delayMicroseconds(3000)	# 3000 microsecond sleep, clearing the display takes a long time

    def write4bits(self, bits, char_mode=False):
        """ Send command to LCD """
	self.delayMicroseconds(1000) # 1000 microsecond sleep

        bits=bin(bits)[2:].zfill(8)

        self.GPIO.output(self.pin_rs, char_mode)

        for pin in self.pins_db:
            self.GPIO.output(pin, False)

        for i in range(4):
            if bits[i] == "1":
                self.GPIO.output(self.pins_db[::-1][i], True)

	self.pulseEnable()

        for pin in self.pins_db:
            self.GPIO.output(pin, False)

        for i in range(4,8):
            if bits[i] == "1":
                self.GPIO.output(self.pins_db[::-1][i-4], True)

	self.pulseEnable()


    def delayMicroseconds(self, microseconds):
	seconds = microseconds / float(1000000)	# divide microseconds by 1 million for seconds
	sleep(seconds)

    def pulseEnable(self):
	self.GPIO.output(self.pin_e, False)
	self.delayMicroseconds(1)		# 1 microsecond pause - enable pulse must be > 450ns 
	self.GPIO.output(self.pin_e, True)
	self.delayMicroseconds(1)		# 1 microsecond pause - enable pulse must be > 450ns 
	self.GPIO.output(self.pin_e, False)
	self.delayMicroseconds(1)		# commands need > 37us to settle

    def message(self, text):
        """ Send string to LCD. Newline wraps to second line"""
        for char in text:
            if char == '\n':
                self.write4bits(0xC0) # next line
            else:
                self.write4bits(ord(char),True)
        
    def destroy(self):
        self.GPIO.cleanup(self.used_gpio)

if __name__ == '__main__':
    myLCD = LCD_DISPLAY()
    
    while True:
        myMessage = raw_input("\nPlease enter a text to display (or \'Quit\' to exit):\n")
        myLCD.clear()
        if myMessage.lower()=="quit":
            myLCD.message("Quitting!!")
            sleep(1)
            myLCD.clear()
            exit(1)
        myLCD.message(myMessage)
        sleep(1)
