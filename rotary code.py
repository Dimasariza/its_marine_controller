import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

right_interrupter = 16
left_interrupter = 18

out1 = 13
out2 = 11
out3 = 15
out4 = 12

counter = 0
i = 0
positive = 0
negative = 0
y = 0

GPIO.setup(out1,GPIO.OUT)
GPIO.setup(out2,GPIO.OUT)
GPIO.setup(out3,GPIO.OUT)
GPIO.setup(out4,GPIO.OUT)

GPIO.setup(right_interrupter, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(left_interrupter, GPIO.IN)

def interrupter_callback():
    print("interrupt stepper")

#GPIO.add_event_detect(right_interrupter, GPIO.BOTH, interrupter_callback, bouncetime=50)

print ("First calibrate by giving some +ve and -ve values.....")

delay = 0.01 # best delay 0.03

#for i in range(5):
#    GPIO.output(led_photoelectric, GPIO.HIGH)
#    time.sleep(0.5)
#    GPIO.output(led_photoelectric, GPIO.LOW)
#    time.sleep(0.5)
    
#while True:
#    print("Time", time.strftime("%H:%M:%S", time.gmtime()), "Right interrupter", GPIO.input(right_interrupter), "Left interrupter", GPIO.input(left_interrupter))
#    time.sleep(0.5)


    
def setGPIOoutput(conds1, conds2, conds3, conds4, use_delay = True):
    GPIO.output(out1, (GPIO.LOW, GPIO.HIGH)[conds1])
    GPIO.output(out2, (GPIO.LOW, GPIO.HIGH)[conds2])
    GPIO.output(out3, (GPIO.LOW, GPIO.HIGH)[conds3])
    GPIO.output(out4, (GPIO.LOW, GPIO.HIGH)[conds4])
    
    if GPIO.input(left_interrupter) == 0:
        global counter
        counter += 1
        print("Thick", counter)
    
    #print("Left Interrupter", GPIO.input(left_interrupter), "Right Interrupter", GPIO.input(right_interrupter))
    
    if use_delay:
        time.sleep(delay)

def stepperPosition(i):
    if i == 0:
        setGPIOoutput(True, False, False, False)
    elif i == 1:
        setGPIOoutput(True, True, False, False)
    elif i == 2:
        setGPIOoutput(False, True, False, False)
    elif i == 3:
        setGPIOoutput(False, True, True, False)
    elif i == 4:
        setGPIOoutput(False, False, True, False)
    elif i == 5:
        setGPIOoutput(False, False, True, True)
    elif i == 6:
        setGPIOoutput(False, False, False, True)
    elif i == 7:
        setGPIOoutput(True, False, False, True)
        

try:
    while(True):
        setGPIOoutput(False, False, False, False, False)
        x = int(input("please input a number"))
      
        if x > 0 and x <= 400:
            for y in range(x, 0, -1):          
                if negative == 1:
                    if i == 7:
                        i = 0
                    else:
                        i = i+1
                    y = y+2
                    negative = 0
                positive = 1
              
                stepperPosition(i)
              
                if i == 7:
                    i = 0
                    continue
                i = i+1

        elif x < 0 and x >= -400:
            x = x*-1
            for y in range(x,0,-1):
                if positive == 1:
                    if i == 0:
                        i = 7
                    else:
                        i = i-1
                    y = y+3
                    positive = 0
                negative = 1
               
                stepperPosition(i)
                
                if i == 0:
                    i = 7
                    continue
                i = i-1 


except KeyboardInterrupt:
    GPIO.cleanup()