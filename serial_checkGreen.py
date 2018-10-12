
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
time.sleep(0.2)
ser.write('14e')
time.sleep(0.1)
returnData = ser.read()
print(returnData)
ser.close()
