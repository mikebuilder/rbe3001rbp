# See http://stackoverflow.com/questions/29345325/raspberry-pyusb-gets-resource-busy#29347455
# Run python2 as root (sudo /usr/bin/python2.7 /home/pi/pythondev/HelloSpaceNavigator.py)
# requires pyUSB to be installed and libusb, see pysub readme
import usb.core
import usb.util
import sys
from time import gmtime, strftime
import time
import serial as cereal



# Look for SpaceNavigator
dev = usb.core.find(idVendor=0x46d, idProduct=0xc628)
if dev is None:
    raise ValueError('SpaceNavigator not found');
else:
    print ('SpaceNavigator found')
    print dev



cfg = dev.get_active_configuration()
print 'cfg is ', cfg
intf = cfg[(0,0)]
print 'intf is ', intf
ep = usb.util.find_descriptor(intf, custom_match = lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)
print 'ep is ', ep

reattach = False
if dev.is_kernel_driver_active(0):
    reattach = True
    dev.detach_kernel_driver(0)

ep_in = dev[0][(0,0)][0]
ep_out = dev[0][(0,0)][1]

print ''
print 'Exit by pressing any button on the SpaceNavigator'
print ''

run = True
globalStart = time.time()
x = 0
y = 0
z = 0
count = 0
while run:
    try:
        start = time.time()
        data = dev.read(ep_in.bEndpointAddress, ep_in.bLength, 0)
        # raw data
        # print data

        # print it correctly T: x,y,z R: x,y,z
        if data[0] == 1:
            # translation packet
            now = time.time()-globalStart
            
            
            tx = data[1] + (data[2]*256)
            ty = data[3] + (data[4]*256)
            tz = data[5] + (data[6]*256)
            

            if data[2] > 127:
                tx -= 65536
            if data[4] > 127:
                ty -= 65536
            if data[6] > 127:
                tz -= 65536

            end = time.time()
            elapsed = end - start
            x += int(tx*elapsed)*2
            y += int(ty*elapsed)*2
            z += int(tz*elapsed)*2
            if(x > 280):
                x=280
            if(x < 100):
                x=100
            if(z > -5):
                z=-5                
            if(z < -120):
                z=-200
            if(y > 150):
                y=150
            if(y < -150):
                y=150
            
            #print "T: ", tx, ty, tz, now, "elapsed: ", elapsed,
            print "cursor: ", x, y, -z
            
            if(now-count > 0.1):
                count = now
                # serial init
                ser = cereal.Serial(

                port='/dev/serial0',
                baudrate = 9600,
                parity = cereal.PARITY_NONE,
                stopbits=cereal.STOPBITS_ONE,
                bytesize=cereal.EIGHTBITS,
                timeout=.1
                )
                print("send to serial")
                ser.write('m'+ str(x) + ',' + str(y) + ',' + str(-1*z) + 'e')
                returnData = ser.read()
                    
                ser.close()
            #endif
            
            
        if data[0] == 3 and data[1] == 0:
            # button packet - exit on the release
            run = False
        #endif

    except usb.core.USBError:
        print("USB error")
    except Exception as e:
        print "read failed", e
# end while
usb.util.dispose_resources(dev)

if reattach:
    dev.attach_kernel_driver(0)
   

def sendPosition(xP, yP, zP):
    # serial init
    ser = serial.Serial(

    port='dev/serial0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=2
    )
    print("send to serial")
    ser.write('m'+ str(xP) + ',' + str(yP) + ',' + str(zP))
    returnData = ser.read()
    
    ser.close()
 
