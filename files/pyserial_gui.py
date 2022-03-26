# pip install pySerial
# pip install pySerialTransfer
# pip install dearpygui

from dis import disco
import logging
from pyserial_connection_arduino import Arduino
from pySerialTransfer import pySerialTransfer as txfer

    # teensy1 = Arduino(comport)
    # teensy1.connect()
    # # import time
    # # time.sleep(1)
    # # print(teensy1)
    # teensy1.send_to_arduino(data_list)
    # # print(teensy1)
    # teensy1.disconnect()

import numpy as np
try:
    import dearpygui.dearpygui as dpg
except:
    print("dearpygui not installed")
# for saving variables
comport = '/dev/ttyACM0'
motor0_enable = 1
motor0_direction = 0
motor0_speed = 1000
motor1_enable = 1
motor1_direction = 0
motor1_speed = 1000
motor2_enable = 1
motor2_direction = 0
motor2_speed = 1000
motor3_enable = 1
motor3_direction = 0
motor3_speed = 1000

dpg.create_context()
dpg.create_viewport(title='PytonPyserialPumps', width=700, height=400)
dpg.setup_dearpygui()

def send_motor_values(sender, callback):
    print(f"Values in the list: {dpg.get_value(item=slider_4int)}")

    comport = "COM9"
    data_list = [motor0_enable, motor0_direction, dpg.get_value(item=slider_4int)[0], motor1_enable, motor1_direction, dpg.get_value(item=slider_4int)[1],
        motor2_enable, motor2_direction, dpg.get_value(item=slider_4int)[2], motor3_enable, motor3_direction, dpg.get_value(item=slider_4int)[3]]
    teensy1 = Arduino(comport)
    teensy1.connect()


    
    teensy1.send_to_arduino(data_list)
    teensy1.disconnect()

def connect_usb(sender, app_data, user_data):
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")

    if not user_data:
        try:
            user_data = Arduino(sender) # sender is the comport
            user_data.connect() #user_data is now an Arduino object
        except:
            print("Nothing to disconnect")
            user_data = False
    else:
        user_data.disconnect() #user_data is an Arduino object
        user_data = False
        dpg.set_item_user_data(sender, False)
        # dpg.set_value(item=sender, value=f"Disconnect {sender}")
        dpg.configure_item(item=sender, label=f"Disconnect {sender}")
        # print(dpg.is_item_hovered(sender))
        # print(dpg.is_item_activated(sender))
        # print(dpg.is_item_deactivated(sender))

    dpg.set_item_user_data(sender, user_data) # set the user data from sender to Arduino object
    # dpg.set_value(item=sender, value=f"Disconnect {sender}")
    # dpg.configure_item(item=sender, enabled=True, label=f"Connect {sender}")
    dpg.configure_item(item=sender, label=f"Connect {sender}")

def find_comports(sender, callback):
    #print(list_available_ports())
    comport_list = txfer.open_ports()
    for element in comport_list:
        print(element)
        # dpg.add_button(label=f"{element}", after="search_button", parent="motor_window", tag=f"new_button{element}")
        dpg.add_button(label=f"Connect to {element}", before="search_button", parent="motor_window", tag=element, callback=connect_usb, user_data=False)
        dpg.add_radio_button(label=f"Connect too {element}", before="search_button", parent="motor_window", tag=f"toggle{element}", callback=connect_usb, user_data=False)
    # dpg.set_value(item="Click button for new search", value=comport_list)
    # this takes the first found comport and puts it into the comport to connect
    # on Raspberry, this *should* enable a quick connection
    # dpg.set_value(item="comport##inputtext", value=comport_list[0])

with dpg.window(label="Motor Window", tag="motor_window"):

    dpg.add_text("To adjust the position of the motors, enter values and click on the respective send value.", wrap=500, bullet=True)
    dpg.add_text("Press the 'print-log' button to display all values in an log", wrap = 500, bullet=True)
    # button for listing all available COM ports
    dpg.add_button(label="Search COM Ports", callback=find_comports, tag="search_button")
    # dpg.add_label_text("Click button for new search")
    # dpg.set_value(item="Search COM Ports", value=("Click button for new search", "No values where received yet"))

    dpg.add_text("Please choose the COM Port where the microcontroller is connected:")
    # dpg.add_input_text("comport##inputtext", hint="enter port, e.g. COM0")
    # text input fields for all motors are created
    # for each value there is a button to send the entered value to the motor
    dpg.add_text("Please choose position for any/all motors:")
    slider_4int = dpg.add_slider_intx(label="Motor 0,1,2,3", max_value=10000, width=500)
    
    dpg.add_button(label="Send to Arduino", callback=send_motor_values)
    # dpg.add_button(label="print-log", callback=retrieve_log)

    # set main window & size
    # dpg.set_main_window_size(800, 550)
    # dpg.set_primary_window("Motor Window", True)
    # dpg.set_main_window_title("Motor Control")

    # edit button colors
    #https://github.com/hoffstadt/DearPyGui/discussions/615
    #dpg.show_style_editor()

# this function starts the dearpygui
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()