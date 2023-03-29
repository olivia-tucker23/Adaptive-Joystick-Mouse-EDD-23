import time
import analogio
import board
import digitalio
import usb_hid
from adafruit_hid.mouse import Mouse
from digitalio import Pull

mouse = Mouse(usb_hid.devices)

x_axis = analogio.AnalogIn(board.A0)
y_axis = analogio.AnalogIn(board.A1)
joystick_click = digitalio.DigitalInOut(board.A2)
joystick_click.direction = digitalio.Direction.INPUT
joystick_click.pull = digitalio.Pull.UP

pot_min = 0.00
pot_max = 3.29
step = (pot_max - pot_min) / 20.0

def get_voltage(pin):
    return (pin.value * 3.3) / 65536

def steps(axis):
    return round((axis - pot_min) / step)

scale = 10

y_start1 = get_voltage(x_axis) * scale
x_start1 = get_voltage(y_axis) * scale
time.sleep(0.1)
y_start2 = get_voltage(x_axis) * scale
x_start2 = get_voltage(y_axis) * scale
time.sleep(0.1)
y_start3 = get_voltage(x_axis) * scale
x_start3 = get_voltage(y_axis) * scale

x_average = (x_start1 + x_start2 + x_start3) / 3
y_average = (y_start1 + y_start2 + y_start3) / 3

x_origin = int(x_average)
y_origin = int(y_average)

BUFFER_SIZE = 5
x_buffer = [0] * BUFFER_SIZE
y_buffer = [0] * BUFFER_SIZE

left_click = digitalio.DigitalInOut(board.D4)
left_click.pull = Pull.DOWN
right_click = digitalio.DigitalInOut(board.D5)
right_click.pull = Pull.DOWN

while True:
    y = get_voltage(x_axis)
    x = get_voltage(y_axis)

    x = x * scale
    y = y * scale

    intx = int(x)
    inty = int(y)

    intx = intx - x_origin
    inty = inty - y_origin
    x_buffer = [intx] + x_buffer[0 : BUFFER_SIZE - 1]
    y_buffer = [inty] + y_buffer[0 : BUFFER_SIZE - 1]
    average_x = int(sum(x_buffer) / BUFFER_SIZE)
    average_y = int(sum(y_buffer) / BUFFER_SIZE)

    # print("raw x-value: ", x)
    # print("intx: ", intx)
    # print("raw y-value: ", y)
    # print("inty: ", inty, "\n")

    mouse.move(average_x, inty)

    # if joystick_click.value is False:
    #     mouse.press(Mouse.LEFT_BUTTON)
    #     time.sleep(0.02)
    # if joystick_click.value is True:
    #     mouse.release(Mouse.LEFT_BUTTON)
    #     time.sleep(0.02)
    
    if left_click.value is False:
        mouse.release(Mouse.LEFT_BUTTON)
        time.sleep(0.02)
    if left_click.value is True:
        mouse.press(Mouse.LEFT_BUTTON)
    
    if right_click.value is False:
        mouse.release(Mouse.RIGHT_BUTTON)
        time.sleep(0.02)
    if right_click.value is True:
        mouse.press(Mouse.RIGHT_BUTTON)

    # print("Left click pressed?  ", left_click.value)
    # print("Right click pressed? ", right_click.value)

    time.sleep(0.005)
