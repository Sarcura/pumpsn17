import dearpygui.dearpygui as dpg
from pyserial_connection_arduino import connect_to_arduino, list_available_ports
import numpy as np

dpg.create_context()
#set_main_window_size(800, 500)

# for saving variables
comport = 'COM17'
motor0_enable = 1
motor0_direction = 0
motor0_speed = 0
motor1_enable = 1
motor1_direction = 0
motor1_speed = 0
motor2_enable = 1
motor2_direction = 0
motor2_speed = 0
motor3_enable = 1
motor3_direction = 0
motor3_speed = 0

# callback
def retrieve_log(sender, callback):
    dpg.show_logger()
    for element in pump_count:
        dpg.log_info(dpg.get_value(f"pump {element}##inputtext"))

    # log_info(get_value("comport##inputtext")

# list all available exceptions
# print(dir(locals()['__builtins__']))

def send_motor_values(sender, callback):

    # this should be generative code instead
    # nr_of_motors = 4
    value_list_to_send = []
    for element in pump_count:
        try:
            print(f"Printing value of pump {element}")
            print(dpg.get_value(f"pump {element}##inputtext"))
            value_list_to_send.append(int(dpg.get_value(f"pump {element}##inputtext")))
        except ValueError:
            value_list_to_send.append(0)

    print(f"Values in the list: {value_list_to_send}")

    # this should be generative code instead
    motor0_speed = value_list_to_send[0]
    motor1_speed = value_list_to_send[1]
    motor2_speed = value_list_to_send[2]
    motor3_speed = value_list_to_send[3]

    comport = dpg.get_value("comport##inputtext")
    results = np.array(connect_to_arduino(comport,motor0_enable,motor0_direction,motor0_speed,
        motor1_enable,motor1_direction,motor1_speed,motor2_enable,motor2_direction,motor2_speed,motor3_enable,motor3_direction,motor3_speed))
    print(f"Received values: {results}")
    # take ony every thrid value, those are the pump values
    motorvalues = (results[2],results[5],results[8],results[11])
    print(motorvalues)
    nr_of_pump = 0
    for rcvd_value in motorvalues:
        print(rcvd_value)
        dpg.set_value(f"received value pump {nr_of_pump}", rcvd_value)
        nr_of_pump += 1

def adjust_comport(sender, callback):
    print(dpg.get_value("comport##inputtext"))
    # for some reason, this does not work:
    # comport = get_value("comport##inputtext")

def find_comports(sender, callback):
    #print(list_available_ports())
    dpg.set_value("Click button for new search", list_available_ports())

with dpg.window(label="Motor Window"):

    dpg.add_text("To adjust the speed of the pumps, enter values and click on the respective send value.", wrap=500, bullet=True)
    dpg.add_text("Press the 'print-log' button to display all values in an log", wrap = 500, bullet=True)
    # button for listing all available COM ports
    dpg.add_button(label="Search COM Ports", callback=find_comports)
    # dpg.add_label_text("Click button for new search")
    dpg.set_value("Click button for new search", "No values where received yet")

    dpg.add_text("Please choose the COM Port where the microcontroller is connected:")
    dpg.add_input_text("comport##inputtext", hint="enter port, e.g. COM0", callback=adjust_comport)
    # text input fields for all pumps are created
    # for each value there is a button to send the entered value to the pump
    dpg.add_text("Please choose speed for any/all pumps:")
    pump_count = [0,1,2,3]
    for element in pump_count:
        dpg.add_input_text(f"pump {element}##inputtext", hint="enter speed in ticks", decimal=True)
        # dpg.add_label_text(f"received value pump {element}")
        dpg.set_value(f"received value pump {element}", "No values where received yet")

    dpg.add_button(label="send pump values to microcontroller", callback=send_motor_values)
    dpg.add_button(label="print-log", callback=retrieve_log)

# def print_me(sender, data):
#     print(get_value("syringe_diameter"))
# add_radio_button("syringe_diameter", ['10', '15', '20'], default_value=1, callback=print_me)

# this function starts the dearpygui
dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

# ↨
# ↑
# ↓
# →
# ←
# ↔
# ▲
# ▼
# ►
# ◄