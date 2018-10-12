
#!/usr/bin/env python
          
      
import time
import serial

ser = serial.Serial(

port='/dev/serial0',
baudrate = 9600,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS,
timeout=2
)

ser.write('10e')
returnData = ser.read()
time.sleep(0.1)
print(returnData)
ser.close()
