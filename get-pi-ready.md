# Set up Pi to connect to Endpoint

[ screen 0 ]
In this module we're going to set up a Raspberry Pi to send some weather data to our endpoint. We are going to use a couple of sensors that are already familiar to you from other modules in the course. 

[ screen 1 ]
We are going to:

- Install a AM2302
- Install a BMP180
- Create a script that gathers data from both devices
- Send that data to our Endpoint.

Let's get started!!

## Our Wiring Setup

[ screen 2 ]

If you completed other modules in this course you know we've already set up these devices individually. But now that we are running them together the wiring is a little different. Here is our diagram:

As you can see { fill this in }

This is what the Physical set up looks like:

{ camera shot of Pi}

Now that we have that wired up, let's install our devices. 

## Setting up the AM2302

Now I'm here on my Raspberry Pi and we'll be setting this up locally. You can also SSH into your Pi if you choose to. 

First we'll set up our AM2302. We'll do that in a similar fashion as before. 

We will clone the DHT library from Adafruit:

```
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
```

Next we'll install some prerequisites:

```
sudo apt-get upgrade
sudo apt-get install build-essential python-dev
```

Now, we'll run the installer:

```
sudo python setup.py install
```

After the installer completes, let's do a quick test:

```
cd examples
sudo python AdafruitDHT.py 2302 4

```

You should see output here. This will verify that our sensor is functioning properly. Now we'll install the BMP180.

## Setting up the BMP180

[ screen 4 ]

Now we're going to set up the BMP180. As we had to do in a previous module, we'll need to set up I2C for the Raspberry Pi. 

Run the following commands: 

```
sudo apt-get install python-smbus
sudo apt-get install i2c-tools
```

Now, run sudo raspi-config and follow the prompts to install i2c support for the ARM core and linux kernel

Next, run the following:

```
sudo nano /etc/modules
```

and add these two lines:

```
i2c-bcm2708 
i2c-dev
```

Save and exit. 

Then you'll need to edit your boot config:

```
sudo nano /boot/config.txt 
```

Add the following two lines:

```
dtparam=i2c1=on
dtparam=i2c_arm=on
```

Save and exit. Now reboot the pi

```
sudo reboot
```

To verify your device is connected properly and your drivers are installed, type in

```
sudo i2cdetect -y 0
```

### Hooking up the Adafruit BMP Library

Now were going to install the Adafruit BMP library. This is a handy library for interacting with our BMP180 that is provided by the fine folks at adafruit.

To install the Adafruit BMP library, run the following commands:

```
sudo apt-get update
sudo apt-get install git build-essential python-dev python-smbus
git clone https://github.com/adafruit/Adafruit_Python_BMP.git
cd Adafruit_Python_BMP
sudo python setup.py install
```

Once those are all installed, run

```
cd examples
sudo python simpletest.py
```

You should output like this

### Reading both sensors

Next we're going to write a script to read both of the sensors and send it to our endpoint. While that might seem complex, the code is pretty straightforward. 

First we want to import the libraries we're going to be using:

```
import Adafruit_BMP.BMP085 as BMP085
import Adafruit_DHT
import urllib
import urllib2
```

Next, we'll set a few values. These are values we may need to change later so it's a good idea to keep them at the top. 

```
url = "http://localhost:5000"
sensor = BMP085.BMP085()
sensor2 = Adafruit_DHT.DHT22
pin = 4
```

In this example, url is the url of the endpoint we set up. If you set up the endpoint on your pi, it can be localhost. 

Sensor is the BMP180, and the library we use is for the BMP085. 
Sensor 2 is the AM2302, and we'll use the DHT22 library for that. 
Pin is the pin number where we pur our orange data wire from the AM2302, which in our case is 4. 

Next we'll set some actions:

```
temp1 = sensor.read_temperature()
pressure = sensor.read_pressure()
sealevelpressure = sensor.read_sealevel_pressure()
```

As you can see here we're reading these values from the 2302 into variables we'll use later. 

For the AM2302, we'll read in those values with this line:

```
humidity, temp2 = Adafruit_DHT.read_retry(sensor2, pin)
```

Then we'll get an average of the two temperatures:

```
tempavg = (temp1 + temp2) / 2
```

Next, we're going to assemble all that data into a packet in JSON. 

```
data = {
	'temp1': str(temp1),
	'temp2': str(temp2),
	'tempavg' : str(tempavg),
	'pressure': str(pressure),
	'sealevelpressure': str(sealevelpressure),
	'humidity': str(humidity)
}
```



Next we'll add some headers to the post: 

```
headers = {
	'Connection': 'keep-alive',
	'Content-type': 'application/json; charset=UTF-8',
}
```

We then convert our data packet to JSON:

```
urldata = json.dumps(data)
```



Finally, we'll open the request and capture the response:

```
req = urllib2.Request(url, urldata, headers)
response = urllib2.urlopen(req)
the_page = response.read()
```

Now our script is ready to send data to the end point! 


##Conclusion

In this module we:

- Installed a AM2302
- Installed a BMP180
- Created a script to gather data from both devices
- Sent that data to our Endpoint.

Most of the code for this excersize was already written, so this is a pretty easy set up for beginners, and I hope this module has shown you how easy it is to get started. Next we're going to tie it all together. 