import os
import glob
import time
import subprocess
import urllib
import urllib2

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#################### Begin Adafruit.IO stuff ######
# My adafruit IO key
aiokey = '[ YOUR AIO KEY ]'

outsideUrl = 'https://io.adafruit.com/api/feeds/outside/data'
weticetopUrl = 'https://io.adafruit.com/api/feeds/weticetop/data'
weticebottomUrl = 'https://io.adafruit.com/api/feeds/weticebottom/data'
dryicetopUrl = 'https://io.adafruit.com/api/feeds/dryicetop/data'
dryicebottomUrl = 'https://io.adafruit.com/api/feeds/dryicebottom/data'
dryiceavgUrl = 'https://io.adafruit.com/api/feeds/dryiceaverage/data'
weticeavgUrl = 'https://io.adafruit.com/api/feeds/weticeaverage/data'

################### Begin Sparkfun stuff #######

sparkfunpublickey = '[]'
sparkfunprivatekey = '[]'
sparkfunprojecturl = '[]'

base_dir = '/sys/bus/w1/devices/'

#your serial numbers will be different!
sensor = ('28-01156492b9ff','28-011564966aff','28-011564c7a9ff','28-0115649279ff','28-011564d991ff')

def read_temp_raw(sensor):
    
    device_folder = glob.glob(base_dir + sensor)[0]
    device_file = device_folder + '/w1_slave'
    catdata = subprocess.Popen(['cat',device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = catdata.communicate()
    out_decode = out.decode('utf-8')
    lines = out_decode.split('\n')
    return lines

def read_temp(sensorid):
    lines = read_temp_raw(sensor[sensorid])
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

def send_to_adafruit(url,values):

    ourvalue = {'value' : values }
    data = urllib.urlencode(ourvalue)
    req = urllib2.Request(url, data)
    req.add_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
    req.add_header('x-aio-key',aiokey)

    response = urllib2.urlopen(req)

    return response


# Get readings
outside = read_temp(0)
weticetop = read_temp(1)
weticebot = read_temp(2)
dryicetop = read_temp(3)
dryicebot = read_temp(2)

## get averages

weticeavg = (weticebot + weticetop) / 2
dryiceavg = (dryicebot + dryicetop) / 2


## Sending data to Adafruit.IO 
send_to_adafruit(outsideUrl,outside)
send_to_adafruit(weticetopUrl,weticetop)
send_to_adafruit(weticebottomUrl,weticebot)
send_to_adafruit(dryicetopUrl,dryicetop)
send_to_adafruit(dryicebottomUrl,dryicebot)
send_to_adafruit(dryiceavgUrl,dryiceavg)
send_to_adafruit(weticeavgUrl,weticeavg)

## Sending data to sparkfun 

oururl = sparkfunprojecturl + '?private_key=' + sparkfunprivatekey + '&dryiceavg=' + str(dryiceavg) +  '&dryicebottom=' + str(dryicebot) + '&dryicetop=' + str(dryicetop) + '&outside=' + str(outside) + '&weticeavg=' + str(weticeavg) + '&weticebottom=' + str(weticebot) + '&weticetop=' + str(weticetop)

content = urllib2.urlopen(oururl).read()

print oururl
#print "outside is " + outside
#print "weticetop is " +  weticetop
#print "weticebot is " +  weticebot
#print "dryicetop is " +  dryicetop
#print "dryicebot is " +  dryicebot
