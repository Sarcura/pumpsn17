# pip install pySerial
# pip install pySerialTransfer
# pip install dearpygui

import logging
from pyserial_connection_arduino import connect_arduino, disconnect_arduino, send_to_arduino, list_available_ports
import numpy as np
try:
    import dearpygui.dearpygui as dpg
except:
    print("dearpygui not installed")
# for saving variables
comport = '/dev/ttyACM0'
motor0_enable = 0
motor0_direction = 0
motor0_position = 0
motor1_enable = 0
motor1_direction = 0
motor1_position = 0
motor2_enable = 0
motor2_direction = 0
motor2_position = 0
motor3_enable = 1
motor3_direction = 0
motor3_position = 0

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

# callback
def retrieve_log(sender, callback):
    dpg.show_logger()
    for element in motor_count:
        dpg.log_info(dpg.get_value(f"motor {element}##inputtext"))

    # log_info(get_value("comport##inputtext")

# list all available exceptions
# print(dir(locals()['__builtins__']))

def send_motor_values(sender, callback):

    # this should be generative code instead
    # nr_of_motors = 4
    value_list_to_send = []
    for element in motor_count:
        try:
            print(f"Printing value of motor {element}")
            print(dpg.get_value(f"motor {element}##inputtext"))
            # set comport to first found comport
            print(dpg.get_value(f"motor {0}##inputtext"))
            value_list_to_send.append(int(dpg.get_value(f"motor {element}##inputtext")))
        except ValueError:
            value_list_to_send.append(0)

    print(f"Values in the list: {value_list_to_send}")

    # this should be generative code instead
    motor0_position = value_list_to_send[0]
    motor1_position = value_list_to_send[1]
    motor2_position = value_list_to_send[2]
    motor3_position = value_list_to_send[3]

    # comport = dpg.get_value("comport##inputtext")
    # comport = dpg.get_value()
    comport = "COM9"
    link = connect_arduino(comport)
    results = np.array(send_to_arduino(link,motor0_enable,motor0_direction,motor0_position,
        motor1_enable,motor1_direction,motor1_position,motor2_enable,motor2_direction,motor2_position,motor3_enable,motor3_direction,motor3_position))
    print(f"Received values: {results}")
    # take ony every thrid value, those are the motor values
    motorvalues = (results[2],results[5],results[8],results[11])
    print(motorvalues)
    nr_of_motor = 0
    for rcvd_value in motorvalues:
        print(rcvd_value)
        dpg.set_value(f"received value motor {nr_of_motor}", rcvd_value)
        nr_of_motor += 1

# def adjust_comport(sender, callback):
#     print(dpg.get_value("comport##inputtext"))
    # for some reason, this does not work:
    # comport = get_value("comport##inputtext")

# def connect_usb():
#     print(element)
def connect_usb(sender, app_data, user_data):
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")
    if user_data:
        dpg.set_item_user_data(sender, False)
        # dpg.set_value(item=sender, value=f"Disconnect {sender}")
        dpg.configure_item(item=sender, label=f"Disconnect {sender}")
        # print(dpg.is_item_hovered(sender))
        # print(dpg.is_item_activated(sender))
        # print(dpg.is_item_deactivated(sender))
    else:
        dpg.set_item_user_data(sender, True)
        # dpg.set_value(item=sender, value=f"Disconnect {sender}")
        # dpg.configure_item(item=sender, enabled=True, label=f"Connect {sender}")
        dpg.configure_item(item=sender, label=f"Connect {sender}")

def find_comports(sender, callback):
    #print(list_available_ports())
    comport_list = list_available_ports()
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
    motor_count = [0,1,2,3]
    for element in motor_count:
        dpg.add_input_text(label=f"motor {element}##inputtext")
        # dpg.add_input_text(f"motor {element}##inputtext", hint="enter position in ticks, 6400 ticks are 360°", decimal=True)
        # dpg.add_label_text(label=f"received value motor {element}")
        print(f"element name {element}")
        # dpg.set_value(item=element, value="No values where received yet")
    
    dpg.add_button(label="Go to numerically define positions", callback=send_motor_values)
    dpg.add_button(label="print-log", callback=retrieve_log)

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