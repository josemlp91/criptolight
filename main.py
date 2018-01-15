
# Tiempo de refresco del valor de la moneda.
FRECUENCY = 60 
DEBUG = False

# Configuración de la API cryptocompare
CRYPTOCURRENCY = 'ETH' 
CURRENCY = 'EUR'
API_BASE_URL = 'https://min-api.cryptocompare.com/data/price'

# Configuración red Wifi.
WIFI_SSID = "XXXXXX"
WIFI_PASSWOED = "XXXXX"

# Configuración pines I/O
PIN_RED = 22
PIN_GREEN = 19

###############################################################################

def connect():
	"""
	Conectar placa micropython a la red WIFI.
	"""
    import network
 
    station = network.WLAN(network.STA_IF)
    if station.isconnected() == True:
        return
 
    station.active(True)
    station.connect(WIFI_SSID, WIFI_PASSWOED)
 
    while station.isconnected() == False:
        pass
 

###############################################################################

def setup():
	connect()

def light_green(pin_red, pin_green):
	pin_red.value(0)
	pin_green.value(1)

def light_red(pin_red, pin_green):
	pin_red.value(1)
	pin_green.value(0)

def print_trend(trend, pin_red, pin_green):
	if trend:
		#print ("GREEN")
		light_green(pin_red, pin_green)
	else:
		#print ("RED")
		light_red(pin_red, pin_green)


def main():

	import urequests, json, time, machine
	from machine import Pin
	
	result = None
	last_price = -1	
	trend = 0

	# Inicializar pines 
	pin_red = Pin(PIN_RED, Pin.OUT, Pin.PULL_UP)                                                                                                          
	pin_green = Pin(PIN_GREEN, Pin.OUT, Pin.PULL_UP) 

	while True:
		response = urequests.get("{0}?fsym={1}&tsyms={2}".format(API_BASE_URL, CRYPTOCURRENCY, CURRENCY))
		result = response.json()
		response.close()

		if result:
			current_price = result[CURRENCY]
			if last_price > -1:
				
				# If debug
				if DEBUG:
					print ("LAST: " + str(last_price))
					print ("CURRENT: " + str(current_price))
					
				if last_price <= current_price:
					trend = 1
				else:
					trend = 0

			last_price = current_price
		
		print_trend(trend, pin_red, pin_green)
		time.sleep(FRECUENCY)	 

if __name__ == "__main__":
	setup()
	main()
