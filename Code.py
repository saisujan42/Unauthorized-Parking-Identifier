import RPi.GPIO as GPIO
import time
from picamera import PiCamera
import cv2
import datetime
import os
import serial
from pytesser import *
import smtplib

camera = picamera.PiCamera() 
camera.resolution = (1024, 720)

gmail_user = "raspberry1786@yahoo.in" #Sender email address
gmail_pwd = "wtrbggvdvpu" #Sender email password


time.sleep(0.3)
to = open('/home/pi/email.txt').read()
print (to)

time.sleep(0.1)
to1 = open('/home/pi/email1.txt').read()
print (to1)

time.sleep(0.1)
to2 = open('/home/pi/email2.txt').read()
print (to2)

time.sleep(0.1)
to3 = open('/home/pi/email3.txt').read()
print (to3)

time.sleep(0.1)
to4 = open('/home/pi/email4.txt').read()
print (to4)

IMAGE_FILE = 'img.jpg'

# Define GPIO to LCD mapping
LCD_RS = 11
LCD_E  = 9
LCD_D4 = 10

LCD_D5 = 22
LCD_D6 = 27
LCD_D7 = 17

LEDR = 3
LEDG = 2

IR1 = 18


 
def main():
 
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  
  GPIO.setup(IR1, GPIO.IN) # IR
  
  
  GPIO.setup(LEDR, GPIO.OUT) # LED
  GPIO.setup(LEDG, GPIO.OUT) # LED
  
  GPIO.output(LEDR, True) # LED
  GPIO.output(LEDG, True) # LED
  time.sleep(0.7) # 700 milli second delay
  GPIO.output(LEDR, False) # LED
  GPIO.output(LEDG, False) # LED
  time.sleep(0.7) # 700 milli second delay
  GPIO.output(LEDR, True) # LED
  GPIO.output(LEDG, True) # LED
  time.sleep(0.7) # 700 milli second delay
  GPIO.output(LEDR, False) # LED
  GPIO.output(LEDG, False) # LED

  time.sleep(1) # 3 second delay
  i = 0
  tcount = 0
  valid = 0
  id = 0

  VN = ''
  count =0
  speed = 0
            
  while True:

        lcd_byte(0x01, LCD_CMD)
        lcd_string("Monitoring",LCD_LINE_1)
        
        GPIO.output(LEDR, True) # LED
        time.sleep(0.3) # 700 milli second delay
        GPIO.output(LEDR, False) # LED
  
        if not GPIO.input(IR1):
            print('Hello')
            i = 1
        
        
        if i == 1:
              i = 0
              
              
              print('Vehicle Detected')
              time.sleep(0.1) # 1 second delay
              
              
              camera.capture('hvs.jpg')
                  
              time.sleep(0.3) # 1 second delay
              
              img=cv2.imread('hvs.jpg')
              time.sleep(0.2)
              output = subprocess.check_output("tesseract hvs.jpg stdout", shell=True)

              open("data.txt","w").close()
              text_file = open("data.txt","w")
              time.sleep(0.3)
              text_file.write(output)
              text_file.flush()
              time.sleep(0.1)

              lines = open("data.txt",'r').readlines()
              data = open("/home/pi/numbers.txt",'r').readlines()
              
              for j in range(len(lines)):
                                   
                  for i in range(len(data)):
                      
                    if lines[j] == data[i] > -1:    
                        
                        print ('---------------------')
                        VN = data[i]
                        id = i
                        valid = 1
                        print ('---------------------')
                        
              tcount = tcount+1
              if valid == 1:
                  
                  GPIO.output(LEDG, True) # LED
              if tcount > 7:
                  if valid == 1:
                      valid = 0
                      tcount = 0
                      print (VN)
                      print (id)
                      
                      GPIO.output(LEDR, True) # LED
                      print("Sending mail")
              
                      dt_stamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")
                      
                      subject = "No Parking Challan :"+dt_stamp
                        
                      text = "No Parking Challan : - Photo Attached"
                                            
                      
                      attach = 'hvs.jpg'
                      msg = MIMEMultipart()

                      msg['From'] = gmail_user
                      msg['To'] = to
                      msg['Subject'] = subject

                      msg.attach(MIMEText(text))

                      mailServer.login(gmail_user, gmail_pwd)
                      mailServer.sendmail(gmail_user, to, msg.as_string())
                      
                      mailServer.close()
                      print ("Email Sent")
                      
                      time.sleep(6)
                      
                      
                      attach = 'hvs.jpg'
                      msg = MIMEMultipart()

                      msg['From'] = gmail_user
                      
                      if id == 0:
                          msg['To'] = to1
                          
                      if id == 1:
                          msg['To'] = to2
                          
                      if id == 2:
                          msg['To'] = to3
                          
                      if id == 3:
                          msg['To'] = to4
                          
                      msg['Subject'] = subject

                      msg.attach(MIMEText(text))

                      mailServer.login(gmail_user, gmail_pwd)
                      
                      if id == 0:
                          mailServer.sendmail(gmail_user, to1, msg.as_string())
                          
                      if id == 1:
                          
                          mailServer.sendmail(gmail_user, to2, msg.as_string())
                          
                      if id == 2:
                          
                          mailServer.sendmail(gmail_user, to3, msg.as_string())
                          
                      if id == 3:
                          
                          mailServer.sendmail(gmail_user, to4, msg.as_string())
                          
                      mailServer.close()
                      print ("Email Sent")
                      time.sleep(3)
                      GPIO.output(LEDG, False) # LED
                      
        else:
              tcount = 0
              valid = 0              
                  
