#!/usr/bin/env python
'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
    Aaron Meier <aaron@bluespeed.org>
'''
import os, sys, time
import RPi.GPIO as GPIO
import getopt

class coffee():
    # Defaults
    typ, numbers = 'small', 1
    ports = {'long': {'port':3, 'typ': False},
             'small': {'port':14, 'typ': False},
             'medium': {'port':4, 'typ': False},
             'descale':{'port':15, 'typ': False}}

    def setup(self):
        GPIO.setup(2, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(3, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(4, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(14, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(15, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)

    def cook(self):
        GPIO.output(self.ports[self.typ]['port'], self.ports[self.typ]['typ'])
        time.sleep(1 * float(self.numbers))
        if self.ports[self.typ]['typ']:
            GPIO.output(self.ports[self.typ]['port'], False)
        else:
            GPIO.output(self.ports[self.typ]['port'], True)
        GPIO.cleanup()
    
    def __init__(self):   
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(True)
        self.setup()

def main(argv):
    typ, numbers = '', 0
    try:
        opts, args = getopt.getopt(argv,"hct:n:",["typ=","numbers="])
    except getopt.GetoptError:
        print 'coffeenator.py -t typ -n numbers'
        sys.exit(2)
    for opt, arg in opts:
        NewCoffee = coffee()
        if opt in ("-h", "--help"):
            print 'coffeenator.py -t typ -n numbers'
            sys.exit()
        elif opt in ("-c", "--clean"):
            GPIO.cleanup()
        elif opt in ("-t", "--typ"):
            typ = arg
        elif opt in ("-n", "--numbers"):
            numbers = int(arg)
    if typ != "" and numbers < 3 and numbers > 0:
        NewCoffee = coffee()
        NewCoffee.typ = typ
        NewCoffee.numbers = numbers
        print "Making ",NewCoffee.numbers, NewCoffee.typ, "coffee(s)"
        NewCoffee.cook()
    else:
        print 'Please enter a number between 1-2'
if __name__ == "__main__":
    main(sys.argv[1:])
