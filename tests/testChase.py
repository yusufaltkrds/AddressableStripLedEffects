import py_compile
import sys

sys.path.append('..')
print(sys.path)

from LED import LED

led = LED(29, 12)

led.chase()
