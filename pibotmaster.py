import threading
import socket
import time
import string
import RPi.GPIO as GPIO
import os
from random import randint

## Disable warning as they get a bit annoying
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

## Set a random port so it can restart incase the script crashes
RPort = 7000

MOTA1 = 9
MOTA2 = 10
MOTAE = 11
MOTB1 = 24
MOTB2 = 23
MOTBE = 25
LASER = 22

GPIO.setup(MOTA1, GPIO.OUT)
GPIO.setup(MOTA2, GPIO.OUT)
GPIO.setup(MOTAE, GPIO.OUT)
GPIO.setup(MOTB1, GPIO.OUT)
GPIO.setup(MOTB2, GPIO.OUT)
GPIO.setup(MOTBE, GPIO.OUT)
GPIO.setup(LASER, GPIO.OUT)

class ReadRemote(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		

	def run(self):
		bot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		bot.bind(('', int(RPort)))
		bot.listen(5)
		print "Script ready"
		client, address = bot.accept()
		thread2.start() # Laser
		client2, address = bot.accept()
		thread3.start() # Servos
                client3, address = bot.accept()
                thread4.start() # Servos
                client4, address = bot.accept()
		thread5.start() # Motor
                client5, address = bot.accept()


		print "Ready.."
		while True:
			buffer = client.recv(1024)
			bufsplit = buffer.split(",")
			#print bufsplit
			client2.send(bufsplit[2])
			if bufsplit[3] == "1":
				servobuf = bufsplit[0]
				client3.send(servobuf)
				servobuf = bufsplit[1]
				client4.send(servobuf)

			else:
				split = ""
				split = bufsplit[0] + "," + bufsplit[1]
				client5.send(split)

class Laser(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)

        def run(self):
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(("127.0.0.1", RPort))
		print "Connected Laser"
		GPIO.output(LASER, GPIO.LOW)
                while True:
			data = client.recv(1)
			if data == "0":
				GPIO.output(LASER, GPIO.LOW)
	                else:
	                        GPIO.output(LASER, GPIO.HIGH)
	                       
				
class Motor(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)

        def run(self):

                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(("127.0.0.1", RPort))
                print "Connected Motor"
                GPIO.output(MOTAE, GPIO.LOW)
		GPIO.output(MOTA1, GPIO.LOW)
		GPIO.output(MOTA2, GPIO.LOW)
		GPIO.output(MOTBE, GPIO.LOW)
                GPIO.output(MOTB1, GPIO.LOW)
                GPIO.output(MOTB2, GPIO.LOW)
		count = 0
                while True:
                        buffer = client.recv(11)
                        data = buffer.split(",")
			data[0] = float(data[0])
			data[1] = float(data[1])
			
			if data[1] < 100:
				GPIO.output(MOTAE, GPIO.HIGH)
				GPIO.output(MOTA1, GPIO.LOW)
	        	        GPIO.output(MOTA2, GPIO.HIGH)
        	        	GPIO.output(MOTBE, GPIO.HIGH)
		                GPIO.output(MOTB1, GPIO.LOW)
		                GPIO.output(MOTB2, GPIO.HIGH)
			elif data[1] > 140:
				GPIO.output(MOTAE, GPIO.HIGH)
                                GPIO.output(MOTA1, GPIO.HIGH)
                                GPIO.output(MOTA2, GPIO.LOW)
                                GPIO.output(MOTBE, GPIO.HIGH)
                                GPIO.output(MOTB1, GPIO.HIGH)
                                GPIO.output(MOTB2, GPIO.LOW)
			elif data[0] < 100:
                                GPIO.output(MOTAE, GPIO.HIGH)
                                GPIO.output(MOTA1, GPIO.HIGH)
                                GPIO.output(MOTA2, GPIO.LOW)
                                GPIO.output(MOTBE, GPIO.HIGH)
                                GPIO.output(MOTB1, GPIO.LOW)
                                GPIO.output(MOTB2, GPIO.HIGH)
                        elif data[0] > 140:
                                GPIO.output(MOTAE, GPIO.HIGH)
                                GPIO.output(MOTA1, GPIO.LOW)
                                GPIO.output(MOTA2, GPIO.HIGH)
                                GPIO.output(MOTBE, GPIO.HIGH)
                                GPIO.output(MOTB1, GPIO.HIGH)
                                GPIO.output(MOTB2, GPIO.LOW)
                        

			else:
				GPIO.output(MOTAE, GPIO.LOW)
        		        GPIO.output(MOTBE, GPIO.LOW)


class Servo1(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)

        def run(self):
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(("127.0.0.1", RPort))
                print "Connected Servo"
                count = 0
                angle = ""
                anglestring = ""
                while True:
                        buffer = client.recv(11)
                        data = float(buffer)
                        angle = ((data / 255) * 180 )
			#print angle                        
			anglestring = "echo 0=%d > /dev/servoblaster" % angle
                        os.system(anglestring)

class Servo2(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)

        def run(self):
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(("127.0.0.1", RPort))
                print "Connected Servo"
                count = 0
                angle = ""
                anglestring = ""
                while True:
                        buffer = client.recv(11)
                        data = float(buffer)
                        angle = ((data / 255) * 245 )
#			print angle
                        anglestring = "echo 1=%d > /dev/servoblaster" % angle
                        os.system(anglestring)


thread1 = ReadRemote()
thread2 = Laser()
thread3 = Servo1()
thread4 = Servo2()
thread5 = Motor()

thread1.start()
