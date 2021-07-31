import uos
from machine import UART, I2C, Pin
import utime
import DS3231
"""
ESPRESSIF AT Command Set
https://docs.espressif.com/projects/esp-at/en/latest/AT_Command_Set/
"""

print()
print("Machine: \t" + uos.uname()[4])
print("MicroPython: \t" + uos.uname()[3])

#indicate program started visually
led_onboard = machine.Pin(25, machine.Pin.OUT)
led_onboard.value(0)     # onboard LED OFF/ON for 0.5/1.0 sec
utime.sleep(0.5)
led_onboard.value(1)
utime.sleep(1.0)
led_onboard.value(0)

i2c = I2C(0,sda = Pin(8), scl=Pin(9))
ds = DS3231.DS3231(i2c)
uart0 = UART(0, rx=Pin(17), tx=Pin(16), baudrate=115200)

# NOTE that we explicitly set the Tx and Rx pins for use with the UART
# If we do not do this, they WILL default to Pin 0 and Pin 1
# Also note that Rx and Tx are swapped, meaning Pico Tx goes to ESP01 Rx 
# and vice versa.
print(uart0)

def sendCMD_waitResp(cmd, uart=uart0, timeout=2000):
    #print("CMD: " + cmd)
    uart.write(cmd)
    test = waitResp(uart, timeout)
    print()
    return test
    
def waitResp(uart=uart0, timeout=2000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    #print("resp:")
    try:
        print(resp.decode())
        #test = resp.decode()
        return resp.decode()
    except UnicodeError:
        print(resp)
    
#sendCMD_waitResp('AT\r\n')          #Test AT startup
#sendCMD_waitResp('AT+GMR\r\n')      #Check version information
#sendCMD_waitResp('AT+RESTORE\r\n')  #Restore Factory Default Settings
#sendCMD_waitResp('AT+CWMODE?\r\n')  #Query the Wi-Fi mode
#sendCMD_waitResp('AT+CWMODE=1\r\n') #Set the Wi-Fi mode = Station mode
#sendCMD_waitResp('AT+CWMODE?\r\n')  #Query the Wi-Fi mode again
#sendCMD_waitResp('AT+CWLAP\r\n', timeout=11000) #List available APs
#sendCMD_waitResp('AT+CWJAP="ATS-2G",""\r\n', timeout=6000) #Connect to AP
#sendCMD_waitResp('AT+CWJAP="Hive-Mind",""\r\n', timeout=6000)
utime.sleep(1)
sendCMD_waitResp('AT+CIFSR\r\n')    #Obtain the Local IP Address
#sendCMD_waitResp('AT+CIPSNTPCFG?\r\n') #check NTP config
#print("<=>"+test+"<=>")
sendCMD_waitResp('AT+CIPSNTPCFG=1,-4,"cn.ntp.org.cn","ntp.sjtu.edu.cn","us.pool.ntp.org"\r\n')
test = sendCMD_waitResp('AT+CIPSNTPTIME?\r\n')
#print(test)
dayList = ['Sun','Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
monthList = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

colpos = test.index(':')
datetime= test[colpos+1:]
datetimesp = datetime.split()

timesp = datetimesp[3].split(':')
print(timesp)
print('\n')
print(datetimesp)

year = int(datetimesp[4])
day = int(datetimesp[2])
hour = int(timesp[0])
minutes = int(timesp[1])
seconds = int(timesp[2])

for i,j in enumerate(dayList):
    if j == datetimesp[0]:
        dayNum = i + 1
        
for i,j in enumerate(monthList):
    if j == datetimesp[1]:
        monthNum = i + 1
        
ds.DateTime([year, monthNum, day, dayNum, hour, minutes, seconds])
#ds.DateTime([Year,7,DayofMonth,1,Hours,Minutes,Seconds])
print (ds.DateTime())


