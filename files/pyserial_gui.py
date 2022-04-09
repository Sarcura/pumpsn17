# pip install pySerial
# pip install pySerialTransfer
# pip install dearpygui>=1.4

from dis import disco
import logging
from pyserial_connection_arduino import Arduino
# from pySerialTransfer import pySerialTransfer as txfer
import serial.tools.list_ports
import numpy as np
import dearpygui.dearpygui as dpg
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
    motor0_enable = 0
    motor1_enable = 0
    motor2_enable = 0
    motor3_enable = 0
    comport = "COM9"
    data_list = [motor0_enable, motor0_direction, dpg.get_value(item=slider_4int)[0], motor1_enable, motor1_direction, dpg.get_value(item=slider_4int)[1],
        motor2_enable, motor2_direction, dpg.get_value(item=slider_4int)[2], motor3_enable, motor3_direction, dpg.get_value(item=slider_4int)[3]]
    # import the "Arduino" object that has a connection:
    teensy1 = dpg.get_item_user_data("search_button")
    print(teensy1)
    if teensy1:
        teensy1.send_to_arduino(data_list)
    else:
        print("No open Arduino connection.")
def send_stop_values(sender, callback):
    print(f"Values in the list: {dpg.get_value(item=slider_4int)}")
    # global var, need for eradication!
    motor0_enable = 1
    motor1_enable = 1
    motor2_enable = 1
    motor3_enable = 1

    comport = "COM9"
    data_list = [motor0_enable, motor0_direction, dpg.get_value(item=slider_4int)[0], motor1_enable, motor1_direction, dpg.get_value(item=slider_4int)[1],
        motor2_enable, motor2_direction, dpg.get_value(item=slider_4int)[2], motor3_enable, motor3_direction, dpg.get_value(item=slider_4int)[3]]
    # import the "Arduino" object that has a connection:
    teensy1 = dpg.get_item_user_data("search_button")
    print(teensy1)
    if teensy1:
        teensy1.send_to_arduino(data_list)
    else:
        print("No open Arduino connection.")

def connect_usb(sender, app_data, user_data):
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}") #shows if connected or not

    if not user_data:
        print("if not")
        dpg.set_item_user_data(sender, True)
        user_data = Arduino(port=sender) # sender is the comport
        user_data.connect() #user_data is now an Arduino object
        dpg.configure_item(item=sender, label=f"Click to disconnect {sender}")

    else:
        print("else")
        user_data.disconnect() #user_data is an Arduino object
        user_data = False
        dpg.configure_item(item=sender, label=f"Connect to {sender}")

    dpg.set_item_user_data(sender, user_data) # set the user data from sender (COMx button!) to Arduino object
    dpg.set_item_user_data("search_button", user_data) # set the user_data from sender (COMx button!) to connected Arduino object

def find_teensys(sender, app_data, user_data, callback):
    hardwareID = user_data
    hardwareID = "(?i)" + hardwareID  # forces case insensitive
    teensy_list = []
    if len(teensy_list) == 0:
        teensy_list = []
        for port in serial.tools.list_ports.grep(hardwareID):
            teensy_list.append(port[0])
    print(teensy_list)
    for element in teensy_list:
        print(element)
        dpg.add_button(label=f"Connect to teensy on {element}", before="search_teensy_button", parent="search_teensy_button", tag=element, callback=connect_usb, user_data=False)

def find_comports(sender, callback):
    # # print and delete children
    # print(dpg.get_item_children(item="search_button"), 1)
    # print(dpg.get_item_children(item="motor_window"), 1)
    # print(dpg.get_item_children(dpg.last_root(), 1))
    # dpg.delete_item(item="search_button", children_only=True)
    # dpg.delete_item(item="search_teensy_button", children_only=True)
    # print(dpg.get_item_children(item="search_button"), 1)
    # print(dpg.get_item_children(item="motor_window"), 1)
    # print(dpg.get_item_children(dpg.last_root(), 1))

    #print(list_available_ports())
    # print(f"Some Text Item: {dpg.does_item_exist('search_button')}")
    # print(f"Some Text Alias: {dpg.does_alias_exist('search_button')}")
    # dpg.delete_item('search_button', children_only=True)
    # print(f"Some Text Item (After deleted): {dpg.does_item_exist('search_button')}")
    # print(f"Some Text Alias (After deleted): {dpg.does_alias_exist('search_button')}")
    comport_list = list(serial.tools.list_ports.comports())
    for element in comport_list:
        print(element.device)
        dpg.delete_item(item=element.device)
        dpg.add_button(label=f"Connect to {element}", before="search_button", parent="search_button", tag=element.device, callback=connect_usb, user_data=False)

with dpg.window(label="Motor Window", tag="motor_window", height=300):

    dpg.add_text("To adjust the position of the motors, enter values and click on the respective send value.", wrap=500, bullet=True)
    dpg.add_text("Press the 'print-log' button to display all values in an log", wrap = 500, bullet=True)
    # button for listing all available COM ports and adding "connect" buttons for each of them
    dpg.add_button(label="Search COM Ports", callback=find_comports, tag="search_button")
    dpg.add_button(label="Search Teensys", callback=find_teensys, tag="search_teensy_button", user_data="16C0:0483")

    # print(dpg.get_item_theme("search_button"))
    # dpg.set_item_theme
    dpg.add_text("Please search COM Ports and connect the COM Port where the microcontroller is located.")
    
    dpg.add_text("Please choose position for any/all motors:")
    slider_4int = dpg.add_slider_intx(label="Motor 0,1,2,3", min_value=-10000, max_value=10000, width=500)
    
    dpg.add_button(label="Send to Arduino", callback=send_motor_values)
    dpg.add_button(label="Stop motors", callback=send_stop_values)
    # print children
    print(dpg.get_item_children(item="search_button"), 1)
    print(dpg.get_item_children(item="motor_window"), 1)
    print(dpg.get_item_children(dpg.last_root(), 1))
    # dpg.delete_item(item="search_button", children_only=True)




# with dpg.theme() as unclicked_theme:
#     with dpg.theme_component(dpg.mvAll):
#         dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (20, 200, 10), category=dpg.mvThemeCat_Core)
#         dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0, category=dpg.mvThemeCat_Core)
# with dpg.theme() as clicked_theme:
#     with dpg.theme_component(dpg.mvAll):
#         dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (20, 20, 100), category=dpg.mvThemeCat_Core)
#         dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0, category=dpg.mvThemeCat_Core)
# dpg.bind_item_theme("search_button", unclicked_theme)

# this function starts the dearpygui
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()