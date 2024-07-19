""" Different effects for ws281x led strips 
"""
import time
from rpi_ws281x import PixelStrip, RGBW
from enum import Enum

""" rpi_ws281x library for controlling led strip
time library for time delaying
"""


class Color(Enum):
	""" Color definitions with RGB tuples.
	"""
	RED = (255, 0, 0)
	GREEN = (0, 255, 0)
	BLUE = (0, 0, 255)
	YELLOW = (255, 255, 0)
	PURPLE = (160, 32, 240)
	TURQUOISE = (48, 213, 200)
	ORANGE = (255, 120, 0)
	WHITE = (255, 255, 255)
	


	
class LED:
	""" Class to represent a SK6812/WS281x LED display. 

	Methods:
		turnOn (color, shineSpeed):
			Turns on the led strip with what speed and color do you want
		
		transition (startColor, endColor, effectSpeed):
			Color transitions to endColor from startColor with effectSpeed
		
		transitionEffect (colors, effectSpeed):
			Color transitions of colors array with effectSpeed
		
		getRgbFromColor (color): 
			Returns seperately RGB values from 24-bit color parameter which using bit-wise process
		
		setLedColor (n,red, green, blue, white): 
			Checks and sets RGB values
		
		turnOff (fadeSpeed): 
			Turns off the led strip with fadeSpeed
		
		colorLoop (shineSpeed, fadeSpeed, effectSpeed, colorOrder):
			Turns on the led strip with first color and shineSpeed. Provides transition
			for each color in colors array until pressing CTRL + C. When pressed turns
			off the led with fadeSpeed.
		
		breathe(shineSpeed, fadeSpeed, color):
			Turns on with shineSpeed and which color selected and turns off with fadeSpeed.
		
		flow(colorOrder, effectSpeed):
			Turns on pixels with effectSpeed from first to last for every 
			colorOrder element until pressing CTRL + C

		chase(colorOrder, repeat, effectSpeed):
			Repeats each colorOrder element at effectSpeed until CTRL + C pressed.
		

	"""
	def __init__(self,ledCount: int, ledPin: int, ledFreqHz: int = 800000, ledDma: int = 10, ledInvert: bool = False,
			  	 ledBrightness: int = 255, ledChannel: int = 0, brightness: int = 120, delayMs: int = 4):
		self.brightness = brightness
		self.delayMs = delayMs
		
		# Assignment values for strip 
		self.strip = PixelStrip(ledCount, ledPin, ledFreqHz, ledDma, ledInvert, ledBrightness, ledChannel)
		
		# Initializing strip
		self.strip.begin()

	"""  ledCount: should be the number of pixels in the display (default 29)
	
	ledPin: should be the GPIO pin connected to the display signal line (must 
		be a PWM pin like 18!)
	
	brightness: should be between 0-255 but recommanded range is 100-200(default 120)
	
	delayMs: duration is delaying milliseconds for after every loop at program
	
	Optional parameters are freq, the frequency of the display 
	signal in hertz (default 800khz), dma, the DMA channel to use (default 10), invert, a boolean
    specifying if the signal line should be inverted (default False), and channel, the PWM 
	channel to use (defaults to 0).

	"""
	
	def turnOn(self, color: Color, shineSpeed: int) -> None:
		""" Turns on the led strip with what speed and color do you want

		Parameters:
			color ((int, int, int)): RGB tuple value of the color.
				Each int value must be range in 0-255
			shineSpeed (int): Shine speed while light on the led
				(recommanded range is [1 - 6])
		"""
		# Splitting tuple to 3 values
		r, g, b = color.value

		# Setting and showing led pixels to which color needed
		for i in range(0, self.brightness, shineSpeed):
			for j in range(self.strip.numPixels()):
				self.setLedColor(j, int(r * (i / self.brightness)), 
									int(g * (i / self.brightness)), 
									int(b * (i / self.brightness)))
			self.strip.show()
			time.sleep(1 / (self.delayMs*10))
			
	def transition(self, startColor: tuple, endColor: tuple, effectSpeed: int) -> None:
		""" Color transitions to endColor from startColor with effectSpeed

		Parameters: 
			startColor ((int, int, int)): RGB tuple value of color which is wanted to start
				Each int value must be range in 0-255
			endColor ((int, int, int)): RGB tuple value of color which is wanted to end
				Each int value must be range in 0-255
			effectSpeed (int): Color changing speed while color transition
				(recommanded range is [1 - 6])
		"""

		# Splitting tuple to 3 values
		red, green, blue = startColor

		# Splitting tuple to 3 values
		targetRed, targetGreen, targetBlue = endColor

		# Setting and showing led pixels to which color needed
		for i in range(0, self.brightness, effectSpeed):
			for j in range(self.strip.numPixels()):
				self.setLedColor(j, int(red + (i * (targetRed - red) / self.brightness)), 
									int(green + (i * (targetGreen - green) / self.brightness)),  
									int(blue + (i * (targetBlue - blue) / self.brightness)))
			self.strip.show()
			time.sleep(1 / (self.delayMs*10))
	
	def transitionEffect(self, colors: list[tuple], effectSpeed: int) -> None:
		""" Color transitions of colors array with effectSpeed 

		Parameters:
			colors (list of colors): Colors of wanted to light on(it shoul be tuple array)
				Ex: [(int, int, int), (int, int, int),...] (Each int value must be range in 0-255)
			effectSpeed (int): Color changing speed while color transition
				(recommanded range is [1 - 6])

		"""
		while True:
			# Providing transition effect with transition function from first to last in colors array 
			for i in range(len(colors)):
				if i + 1 >= len(colors):
					self.transition(colors[i], colors[0],effectSpeed)
				else:
					self.transition(colors[i], colors[i + 1], effectSpeed)
	
	def getRgbFromColor(self,color: int) -> tuple:
		""" Returns seperately RGB values from 24-bit color parameter which using bit-wise process

		Parameters: 
			color (int): 24-bit RGB value

		Returns:
			r, g, b (int): Seperately color of RGB value (each value have a 0-255 value range)
		"""
		# Bit-wise processings
		r = (color >> 16) & 0xFF
		g = (color >> 8) & 0xFF
		b = color & 0xFF

		return r, g, b
		
	def setLedColor(self,n: int,red: int, green: int, blue: int, white: int = 0) -> None:
		""" Checks and sets RGB values

		Parameters: 
			n (int): Which pixel want to light on 
			red (int): Red value of RGB color (must be range in 0-255 )
			green (int): Green value of RGB color (must be range in 0-255 )
			blue (int): Blue value of RGB color (must be range in 0-255 )
			white (int): White value of RGB color (must be range in 0-255, default 0)
		"""
		
		# Checking
		if(red < 0):
			red = 0
		elif(red > 255):
			red = 255
		if(green < 0 ):
			green = 0
		elif(green > 255):
			green = 255
		if(blue < 0):
			blue = 0
		elif(blue > 255):
			blue = 255

		# Setting
		self.strip.setPixelColor(n,RGBW(red, green, blue, white))
			
	def turnOff(self,fadeSpeed: int) -> None:
		""" Turn off the led strip with fadeSpeed  

		Parameters: 
			fadeSpeed (int): Light off speed while brightness getting 0
				(recommanded range is [3-8])
		"""

		# Getting color from first pixel
		color = self.strip.getPixelColor(0)
		if not isinstance(color, int):
			raise ValueError("Color should be a 24-bit integer value")
		# Spiltting RGB values from color parameter
		r, g, b = self.getRgbFromColor(color)

		# Decreasing brightness each pixel untill 0  
		while (r > 0 or g > 0 or b > 0):
			r -= fadeSpeed
			g -= fadeSpeed
			b -= fadeSpeed
			for i in range(self.strip.numPixels()):
				self.setLedColor(i, r, g, b)
			self.strip.show()
			time.sleep(1 / (self.delayMs*10))

	def colorLoop(self, shineSpeed: int = 5, fadeSpeed: int = 7, effectSpeed: int = 3, colorOrder: list[Color] = [Color.GREEN, Color.BLUE, Color.RED]) -> None:
		""" Turns on the led strip with first color and shineSpeed. Provides transition
		  for each color in colors array until pressing CTRL + C. When pressed turns
		  off the led with fadeSpeed.

		Parameters:
			shineSpeed (int): Shine speed while light on the led
				(recommanded range is [1 - 6])
			fadeSpeed (int): Light off speed while brightness getting 0
				(recommanded range is [3-8])
			effectSpeed (int): Color changing speed while color transition
				(recommanded range is [1 - 6])
			colors (list of colors): Colors of wanted to light on(it shoul be tuple array)
				Ex: [(int, int, int), (int, int, int),...] (Each int value must be range in 0-255)
		"""
		try:

			self.turnOn(colorOrder[0],shineSpeed)
			liste = []
			for i in range(len(colorOrder)):
				liste.append(colorOrder[i].value)
			self.transitionEffect(liste,effectSpeed)
		except KeyboardInterrupt:
			self.turnOff(fadeSpeed)


	def breathe(self, shineSpeed: int = 5, fadeSpeed: int = 7, color: Color = Color.RED) -> None:
		""" Turns on with shineSpeed and which color selected and turns off with fadeSpeed.
		
		Parameters:
			shineSpeed (int): Shine speed while light on the led
				(recommanded range is [1 - 6])
			fadeSpeed (int): Light off speed while brightness getting 0
				(recommanded range is [3-8])
		"""
		try:
			while True:
				self.turnOn(color, shineSpeed)
				self.turnOff(fadeSpeed)
		except KeyboardInterrupt:
			self.turnOff(fadeSpeed)
		
		
	
	def flow(self, colorOrder: list[Color]=[Color.GREEN, Color.BLUE, Color.RED], effectSpeed: int=4) -> None:
		""" Turns on pixels with effectSpeed from first to last for every 
		colorOrder element until pressing CTRL + C

		Parameters:
			colorOrder (list of colors): Colors of wanted to light on(it shoul be tuple array)
				Ex: [(int, int, int), (int, int, int),...] (Each int value must be range in 0-255)
			effectSpeed (int): Color changing speed while color transition
				(recommanded range is [1 - 6])
		"""
		try:
			while True:
				
				# Choosing color
				for color in colorOrder:
					
					# Setting led pixels to selected color
					for j in range(self.strip.numPixels()):
						
						# Spiltting RGB values from color parameter
						r, g, b = color.value
						self.setLedColor(j, r, g, b)
						self.strip.show()
						time.sleep(1 / (self.delayMs*10))
		except KeyboardInterrupt:
			for i in range(self.strip.numPixels()):
				self.setLedColor(i,0,0,0)
				self.strip.show()
				time.sleep(1 / (self.delayMs*10))

	
	def chase(self, colorOrder: list[Color]=[Color.GREEN, Color.BLUE, Color.RED], repeat: int=3, effectSpeed: int=4) -> None:
		""" Repeats each colorOrder element at effectSpeed until CTRL + C pressed.

		Parameters:
			colorOrder (list of colors): Colors of wanted to light on(it shoul be tuple array)
				Ex: [(int, int, int), (int, int, int),...] (Each int value must be range in 0-255)
			repeat (int): Led pixel repeat of each color 
			effectSpeed (int): Color changing speed while color transition
				(recommanded range is [1 - 6])
		"""
		try:
			# Backs up the color array
			order = []
			for color in colorOrder:
				for i in range(repeat):
					order.append(color.value)
			while True:
				# Sets and shows led pixels for each color with repeat
				for i in range(self.strip.numPixels()):
					for j in range(len(order)):
						r, g, b = order[i % (j+1)]
						self.setLedColor(i, r, g, b)
						self.strip.show()
				time.sleep(1 / (self.delayMs*10))
					
				if len(order) > 1:
					last_color = order[-1]
					for k in range(len(order) - 1, 0, -1):
						order[k] = order[k - 1]
					order[0] = last_color
				
				
		except KeyboardInterrupt:
			for i in range(self.strip.numPixels()):
				self.setLedColor(i, 0, 0, 0)
				self.strip.show()
				time.sleep(1 / (self.delayMs*10))
