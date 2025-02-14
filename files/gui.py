
# TODO: create automated switching on/off for all channels with timing variable
# TODO: setting a new 0 position after setup for sw endstop calculation
# TODO: test sw endstops at better values HINT: slight increase, try experimentally - changed  from 1e6 to 1.1e6 
# TODO: Progress bar would be nice to have, maybe even with ml scale - should be related to calculated time and update on?
# TODO: rename folders according to conventions https://stackoverflow.com/questions/22842691/what-is-the-meaning-of-the-dist-directory-in-open-source-projects
# TODO: create an input script for flowspeed-motorspeed to produce a graph for output parameters

import dearpygui.dearpygui as dpg
from themes import create_theme_imgui_light, create_theme_client, create_theme_server
from arduino import Arduino
from flowspeed_motorspeed import calculate_stepspeed, calculate_sorting_parameters
import threading
import yaml
import logging
import datetime
today_date = str(datetime.date.today())+".log"
logging.basicConfig(
    filename=today_date,
    # filemode='+w',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

class serial_ui():
    CLIENT_THEME = None
    SERVER_THEME = None

    def __init__(self):
        # dict for saving motor values:
        self.data_list = {"motor0_enable": 0, "motor0_direction": 0, "position_1": 100000, "stepspeed_1": 0, 
            "motor1_enable": 0, "motor1_direction": 0, "position_2": 100000, "stepspeed_2": 0, 
            "motor2_enable": 0, "motor2_direction": 0, "position_3": 100000, "stepspeed_3": 0,
            "motor3_enable": 0, "motor3_direction": 0, "position_4": 100000, "stepspeed_4": 0}
        # additional values for motor control
        self.sw_endstop = 1100000
        self.max_speed = 15000

        self.my_serial = Arduino(findusbport_hwid="16C0:0483")
        # self.update_ports_callback()
        # self.my_serial.hwid =  # should be changed by dropdown to search teensy, ardunio..
        try:
            self.portList  = self.my_serial.get_availabile_port_list()
            logging.info(self.portList)
        except:
            self.portList  = []
            logging.info("No devices found.")
        self.SELECTED_DEVICE = ""
        self.dpg_setup()
        self.create_primary_window()
        serial_ui.CLIENT_THEME = create_theme_client()
        serial_ui.SERVER_THEME = create_theme_server()
        self.dpg_show_view_port()
        LIGHT_THEME = create_theme_imgui_light()
        dpg.bind_item_theme(self.prime_window, LIGHT_THEME)
        dpg.set_primary_window(self.prime_window, True)
        while dpg.is_dearpygui_running():
            if self.my_serial.link:

                # maybe use asyncio? or switch to https://github.com/BadSugar/serialGUI
                # import asyncio

                # async def tcp_echo_client(message):
                #     reader, writer = await asyncio.open_connection(
                #         '127.0.0.1', 8888)

                #     print(f'Send: {message!r}')
                #     writer.write(message.encode())
                #     await writer.drain()

                #     data = await reader.read(100)
                #     print(f'Received: {data.decode()!r}')

                #     print('Close the connection')
                #     writer.close()
                #     await writer.wait_closed()

                # asyncio.run(tcp_echo_client('Hello World!'))
                ####################################################

                # logging.info(self.stepspeed)
                pass
                # logging.info("teensy connected")
                # recv_msg = self.my_serial.read_serial()
                # if recv_msg:
                #     max_length = 122
                #     if len(recv_msg) > max_length:
                #         truncated_msg = recv_msg[0:122-3] + "..."
                #         self.log_msg(truncated_msg, serial_ui.SERVER_THEME)
                #     else:
                #         self.log_msg(recv_msg, serial_ui.SERVER_THEME)
                #     logging.info(f"Received: {recv_msg}")
                #     self.log_msg(recv_msg, serial_ui.SERVER_THEME)
            try:
                dpg.render_dearpygui_frame()
            except KeyboardInterrupt:
                return
            dpg.set_exit_callback(self.exit_callback)
        self.dpg_cleanup()

    def calculate_motors(self):
        self.calculate_cannel_ratios()
        # the channel speeds are multiplied with the fractional value per channel
        stepspeed1 = calculate_stepspeed(float(self.channel_ratio_1)*float(dpg.get_value(self.channel_m_per_s)), float(dpg.get_value(self.syringe_diameter_1)), float(dpg.get_value(self.channel_area_sqmm)))
        stepspeed2 = calculate_stepspeed(float(self.channel_ratio_2)*float(dpg.get_value(self.channel_m_per_s)), float(dpg.get_value(self.syringe_diameter_2)), float(dpg.get_value(self.channel_area_sqmm)))
        stepspeed3 = calculate_stepspeed(float(self.channel_ratio_3)*float(dpg.get_value(self.channel_m_per_s)), float(dpg.get_value(self.syringe_diameter_3)), float(dpg.get_value(self.channel_area_sqmm)))
        stepspeed4 = calculate_stepspeed(float(self.channel_ratio_4)*float(dpg.get_value(self.channel_m_per_s)), float(dpg.get_value(self.syringe_diameter_4)), float(dpg.get_value(self.channel_area_sqmm)))
        
        self.data_list['stepspeed_1'] = int(round(stepspeed1))*dpg.get_value(self.nr_of_sorters)
        self.data_list['stepspeed_2'] = int(round(stepspeed2))*dpg.get_value(self.nr_of_sorters)
        self.data_list['stepspeed_3'] = int(round(stepspeed3))*dpg.get_value(self.nr_of_sorters)
        self.data_list['stepspeed_4'] = int(round(stepspeed4))*dpg.get_value(self.nr_of_sorters)

    def calculate_sorting(self):
        # this is now calculated for channel 4 as standard sample channel 
        
        self.calculate_cannel_ratios()

        self.channel_µl_per_s, self.cell_per_s, self.total_sorting_time, self.additional_cell_media, self.sheath_fluid, self.additional_sheath_fluid = calculate_sorting_parameters(
            float(dpg.get_value(self.channel_m_per_s)), float(self.channel_ratio_4),
            round(float(dpg.get_value(self.channel_area_sqmm)), 5),
            int(dpg.get_value(self.cell_concentration_per_ml)), float(dpg.get_value(self.cell_volume_ml)),
            float(dpg.get_value(self.sorting_speed)), float(dpg.get_value(self.max_sorting_speed)),
            float(dpg.get_value(self.maximum_sorting_time)), dpg.get_value(item="medium_calculation")
        )

        output1 = f"Sample speed in channel [µl/s]: {self.channel_µl_per_s}, [Cells/s]: {self.cell_per_s}, Sorting duration [h]: {self.total_sorting_time}"
        output2 = f"Additionally needed cell media [ml]: {self.additional_cell_media}, Total needed sheath fluid [ml]: {round(self.sheath_fluid+self.additional_sheath_fluid, 2)}"

        self.ul_xy_per_s = round((self.channel_ratio_1)*self.channel_µl_per_s, 2)
        self.ul_z1_per_s = round((self.channel_ratio_2)*self.channel_µl_per_s, 2)
        self.ul_z2_per_s = round((self.channel_ratio_3)*self.channel_µl_per_s, 2)
        self.ul_sample_per_s = round((self.channel_ratio_4)*self.channel_µl_per_s, 2)
        output3 = f"Channel xy, z1, z2 & sample [µl/s]: {self.ul_xy_per_s, self.ul_z1_per_s, self.ul_z2_per_s, self.ul_sample_per_s}"
        dpg.set_value("sorting_simulation1", output1)
        dpg.set_value("sorting_simulation2", output2)
        dpg.set_value("sorting_simulation3", output3)

    def update_ports_callback(self):
        self.my_serial.get_availabile_port_list()
        dpg.configure_item("__listPortsTag", items=self.my_serial.comport_list)

    def create_logger_window(self):
        ## this creates a window at bottom
        child_logger_id = dpg.add_child_window(tag="logger", width=870, height=340)
        self.filter_id = dpg.add_filter_set(parent=child_logger_id)

    # def show_hide_loading(self):
    #     if dpg.hide_item
    #     dpg.add_loading_indicator(circle_count=3)

    def save_state(self, sender, app_data, user_data):
        file_name = "pump_settings.yaml"
        # keep in mind the floating point arithmetics
        speed_position = [
            float(dpg.get_value(self.channel_m_per_s)),
            float(dpg.get_value(self.channel_value_1)), float(dpg.get_value(self.syringe_diameter_1)), float(dpg.get_value(self.channel_area_sqmm)),
            float(dpg.get_value(self.channel_value_2)), float(dpg.get_value(self.syringe_diameter_2)), float(dpg.get_value(self.channel_area_sqmm)),
            float(dpg.get_value(self.channel_value_3)), float(dpg.get_value(self.syringe_diameter_3)), float(dpg.get_value(self.channel_area_sqmm)),
            float(dpg.get_value(self.channel_value_4)), float(dpg.get_value(self.syringe_diameter_4)), float(dpg.get_value(self.channel_area_sqmm)),
        ]
        logging.info(speed_position)
        with open(file_name, 'w+') as f:
            yaml.safe_dump(speed_position, f, default_flow_style=False)

    def load_state(self, sender, app_data, user_data):
        file_name = "pump_settings.yaml"
        with open(file_name) as f:
            doc = yaml.safe_load(f)
            logging.info("loaded data:")
            logging.info(doc)
            speed_position = doc
        
        dpg.set_value(self.channel_m_per_s, speed_position[0])
        dpg.set_value(self.channel_value_1, speed_position[1]), dpg.set_value(self.syringe_diameter_1, speed_position[2]), dpg.set_value(self.channel_area_sqmm, speed_position[3]),
        dpg.set_value(self.channel_value_2, speed_position[4]), dpg.set_value(self.syringe_diameter_2, speed_position[5]), dpg.set_value(self.channel_area_sqmm, speed_position[6]),
        dpg.set_value(self.channel_value_3, speed_position[7]), dpg.set_value(self.syringe_diameter_3, speed_position[8]), dpg.set_value(self.channel_area_sqmm, speed_position[9]),
        dpg.set_value(self.channel_value_4, speed_position[10]), dpg.set_value(self.syringe_diameter_4, speed_position[11]), dpg.set_value(self.channel_area_sqmm, speed_position[12])


    def create_setup(self):
        with dpg.group(label="pump_setup"):
            pumplist = [1,2,3,4]
            dpg.add_text(default_value=f"Please setup pumps and reconnect device afterwards.")
            for element in pumplist:
                buttonsize=50,50
                with dpg.group(horizontal=True, parent=element):
                    dpg.add_text(default_value=f"Pump {element} control")
                    dpg.add_button(label="<<", width=buttonsize[0], height=buttonsize[1], user_data=[f"pump", element, "fast_backward"], callback=self.send_speed_to_arduino, tag=f"fast_backward_pump_{element}")
                    dpg.add_button(label="<", width=buttonsize[0], height=buttonsize[1], user_data=[f"pump", element, "normal_backward"], callback=self.send_speed_to_arduino, tag=f"normal_backward_pump_{element}")
                    dpg.add_button(label="||", width=buttonsize[0], height=buttonsize[1], user_data=[f"pump", element, "stop"], callback=self.send_speed_to_arduino, tag=f"stop_pump_{element}")
                    dpg.add_button(label=">", width=buttonsize[0], height=buttonsize[1], user_data=[f"pump", element, "normal_forward"], callback=self.send_speed_to_arduino, tag=f"normal_forward_pump_{element}")
                    dpg.add_button(label=">>", width=buttonsize[0], height=buttonsize[1], user_data=[f"pump", element, "fast_forward"], callback=self.send_speed_to_arduino, tag=f"fast_forward_pump_{element}")
                    dpg.add_loading_indicator(tag=f"setup_movement_indicator_{element}", radius = 4, speed=0)

    def create_send_speed(self):
        with dpg.group(horizontal=True):
            with dpg.group() as text_group:
                dpg.add_text(default_value="Sample speed [m/s]", parent=text_group)
                dpg.add_text(default_value="Pump 1 xy sheath [m/s fraction]", parent=text_group)
                dpg.add_text(default_value="Pump 2 z1 sheath [m/s fraction]", parent=text_group)
                dpg.add_text(default_value="Pump 3 z2 sheath [m/s fraction]", parent=text_group)
                dpg.add_text(default_value="Pump 4 sample [m/s fraction]", parent=text_group)
                dpg.add_text(default_value="Sample channel size [mm²]", parent=text_group)
                dpg.add_text(default_value="Number of sorters", parent=text_group)
                dpg.add_text(default_value="Save/Load Values:", parent=text_group)
                
                # dpg.add_image(texture_tag="sarcura", value="sarcura.svg") # this leads to errors during build and should be avoided
            # 100 µl sheath, 50 µl z1 / 50 µl z2, 20 µl sample = 0.1, 0.45, 0.225, 0.225
            with dpg.group() as inp_values_group:
                self.channel_m_per_s = dpg.add_input_float(tag="channel_flow_speed",
                        default_value=1, max_value=3, width=180,
                        parent=inp_values_group)
                self.channel_value_1 = dpg.add_input_float(tag="flow_speed_pump_1", # sample
                        default_value=0.45, max_value=3, width=180,
                        parent=inp_values_group)
                self.channel_value_2 = dpg.add_input_float(tag="flow_speed_pump_2", # xy sheath
                        default_value=0.225, max_value=3, width=180,
                        parent=inp_values_group)
                self.channel_value_3 = dpg.add_input_float(tag="flow_speed_pump_3", # z1 sheath
                        default_value=0.225, max_value=3, width=180,
                        parent=inp_values_group)
                self.channel_value_4 = dpg.add_input_float(tag="flow_speed_pump_4", #z2 sheath
                        default_value=0.1, max_value=3, width=180,
                        parent=inp_values_group)
                self.channel_area_sqmm = dpg.add_input_float(tag="channel_area_sqmm",
                        default_value=0.003, max_value=100, width=180,
                        parent=inp_values_group)
                self.nr_of_sorters = dpg.add_input_int(tag="nr_of_sorters",
                        default_value=1, max_value=100, width=180,
                        parent=inp_values_group)
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Save Data", callback=self.save_state, tag="save_data")
                    dpg.add_button(label="Load Data", callback=self.load_state, tag="load_data")

            with dpg.group(horizontal=True) as syringe_values_group:
                syringe_diameters = [4.65, 8.66, 12.36, 14.5, 19.13, 21.7, 26.7] # BD plastic
                with dpg.group():
                    dpg.add_text(default_value="syringe 1 Ø [mm]")
                    self.syringe_diameter_1 = dpg.add_listbox(syringe_diameters, default_value = str("12.36"), tag="syringe_dia_1", width=80, num_items=7)
                with dpg.group():
                    dpg.add_text(default_value="syringe 2 Ø [mm]")
                    self.syringe_diameter_2 = dpg.add_listbox(syringe_diameters, default_value = str("12.36"), tag="syringe_dia_2", width=80, num_items=7)
                with dpg.group():
                    dpg.add_text(default_value="syringe 3 Ø [mm]")
                    self.syringe_diameter_3 = dpg.add_listbox(syringe_diameters, default_value = str("12.36"), tag="syringe_dia_3", width=80, num_items=7)
                with dpg.group():
                    dpg.add_text(default_value="syringe 4 Ø [mm]")
                    self.syringe_diameter_4 = dpg.add_listbox(syringe_diameters, default_value = str("4.65"), tag="syringe_dia_4", width=80, num_items=7)

        dpg.add_separator()

        with dpg.group(horizontal=True) as send_group:
            dpg.add_button(tag="sendSpeedBtn", label="Start system",
                callback=self.send_speed_to_arduino, parent=send_group,
                height=50)
            dpg.add_button(tag="sendSpeedBtn05ms", user_data={"speed": 0.5}, label="Set system to 0.5 m/s",
                callback=self.send_speed_to_arduino, parent=send_group,
                height=50)
            dpg.add_button(tag="sendSpeedBtn10ms", user_data={"speed": 1.0}, label="Set system to 1 m/s",
                callback=self.send_speed_to_arduino, parent=send_group,
                height=50)
            dpg.add_button(tag="sendSpeedBtn15ms", user_data={"speed": 1.5}, label="Set system to 1.5 m/s",
                callback=self.send_speed_to_arduino, parent=send_group,
                height=50)
            dpg.add_button(tag="sendSpeedBtn20ms", user_data={"speed": 2}, label="Set system to 2 m/s",
                callback=self.send_speed_to_arduino, parent=send_group,
                height=50)
            dpg.add_button(tag="sendSet0", user_data={"go_to_endstops" : True}, label="Run back motors to software 0",
                callback=self.send_speed_to_arduino, parent=send_group,
                height=50)
            dpg.add_button(tag="sendStop", user_data={"set_speed_zero" : True}, label="Stop Pumps",
                callback=self.send_speed_to_arduino, parent=send_group,
                height=50)
            dpg.add_loading_indicator(tag="pumping_indicator", speed=0)

        dpg.add_separator()

    def create_automate(self):
        with dpg.group():
            dpg.add_checkbox(label="Automate Pump 1", tag="automate_1")
            dpg.add_checkbox(label="Automate Pump 2", tag="automate_2")
            dpg.add_checkbox(label="Automate Pump 3", tag="automate_3")
            dpg.add_checkbox(label="Automate Pump 4", tag="automate_4")
            dpg.add_input_int(label="Set interval time [s]", tag="interval",default_value=1, width=180)
            with dpg.group(horizontal=True):
                dpg.add_button(label="Start Automation", height=50, callback=self.automate_pumps, user_data=True, tag="start_auto")
                dpg.add_button(label="Stop Automation", height=50, callback=self.automate_pumps, user_data=False, tag="stop_auto")
                dpg.add_loading_indicator(tag="automated_indicator", speed=0)

    def create_calculate(self):
        with dpg.group(horizontal=True):
            with dpg.group() as text_group:
                dpg.add_text(default_value="Cell concentration [ml]", parent=text_group)
                dpg.add_text(default_value="Cell volume [ml]", parent=text_group)
                dpg.add_text(default_value="Sorting speed [Hz]", parent=text_group)
                dpg.add_text(default_value="Maximum sorting speed [Hz]", parent=text_group)
                dpg.add_text(default_value="Maximum sorting time [h]", parent=text_group)
                dpg.add_text(default_value="Simulation output: ", parent=text_group)

                # dpg.add_image(texture_tag="sarcura", value="sarcura.svg")
            with dpg.group() as inp_values_group:
                self.cell_concentration_per_ml = dpg.add_input_int(tag="cell_concentration_per_ml",
                        default_value=1000000, step=500000,  width=180,
                        parent=inp_values_group)
                self.cell_volume_ml = dpg.add_input_float(tag="cell_volume_ml",
                        default_value=1, step=1,  max_value=1000, width=180,
                        parent=inp_values_group)
                self.sorting_speed = dpg.add_input_int(tag="sorting_speed",
                        default_value=1000, step=500, width=180,
                        parent=inp_values_group)
                self.max_sorting_speed = dpg.add_input_int(tag="max_sorting_speed",
                        default_value=5000, step=500, width=180,
                        parent=inp_values_group)
                self.maximum_sorting_time = dpg.add_input_int(tag="maximum_sorting_time",
                        default_value=4, step=1,  width=180,
                        parent=inp_values_group)
                self.sorting_simulation = dpg.add_input_text(tag="sorting_simulation1",
                        default_value="not yet calculated", width=700,
                        parent=inp_values_group)
                self.sorting_simulation = dpg.add_input_text(tag="sorting_simulation2",
                        default_value="please enter values and start calculation", width=700,
                        parent=inp_values_group) 
                self.sorting_simulation = dpg.add_input_text(tag="sorting_simulation3",
                        default_value="please enter values and start calculation", width=700,
                        parent=inp_values_group)        
                        
                # self.cell_concentration_per_ml cell concentration in medium
                # self.cell_volume_ml amount of cell medium
                # self.sorting_speed Hz
                # self.max_sorting_speed Hz, heater capability
                # self.maximum_sorting_time Maximum amount of hours a full sorting is allowed to take
                
                with dpg.group(horizontal=True):
                    with dpg.theme(tag="sarcura_button_theme"):
                        with dpg.theme_component(dpg.mvButton):
                            dpg.add_theme_color(dpg.mvThemeCol_Button, (224, 36, 36))
                            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (224, 36, 36))
                            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (204, 46, 46))
                            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)
                            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 3, 3)

                    dpg.add_button(label="Calculate Sorting", callback=self.calculate_sorting, tag="calculate_sorting")
                    dpg.bind_item_theme(dpg.last_item(), "sarcura_button_theme")

        dpg.add_checkbox(label="Calculate medium and sorting time for selected sorting speed per sorter.", tag="medium_calculation")
        dpg.add_separator()

        # width, height, channels, data = dpg.load_image("sarcura.png") 
        # with dpg.texture_registry():
        #     texture_id = dpg.add_static_texture(width, height, data) 
        # dpg.add_image(texture_id)

# dictionary_name[key] = value
                # dpg.add_button(label="Clear Filter",
                #     callback=lambda: dpg.delete_item(self.filter_id,
                #         children_only=True), parent=button_group)

    # def create_msg_and_filter_columns(self):
    #     with dpg.group(horizontal=True):
    #         with dpg.group() as text_group:
    #             dpg.add_text(default_value="Pump 1", parent=text_group)
    #             dpg.add_text(default_value="Filter", parent=text_group)
    #         with dpg.group() as inp_text_group:
    #             user_msg = dpg.add_input_text(tag="usrMsgTxt",
    #                     default_value="help", width=720,
    #                     parent=inp_text_group)
    #             dpg.add_input_text(callback=lambda sender: 
    #                     dpg.set_value(self.filter_id, dpg.get_value(sender)),
    #                     width=720, parent=inp_text_group)
    #         with dpg.group() as button_group:
    #             dpg.add_button(tag="sendMsgBtn", label="Send",
    #                 callback=self.send_msg_to_serial_port_callback,
    #                 user_data={'userMsgTag': user_msg}, parent=button_group)
    #             dpg.add_button(label="Clear Filter",
    #                 callback=lambda: dpg.delete_item(self.filter_id,
    #                     children_only=True), parent=button_group)

    def create_primary_window(self):
        with dpg.window(tag="Primary Window", autosize=True) as self.prime_window:
            with dpg.tab_bar():
                with dpg.tab(label="Connection"):
                    with dpg.group(horizontal=True):
                        # After clicking it will show a list view of ports
                        dpg.add_button(tag="avPortsBtn", height=50, label="Refresh Available Ports", callback=self.update_ports_callback)
                        if not self.portList:
                            dpg.add_listbox(["No Ports available"], tag="__listPortsTag",
                                    width=300,
                                    num_items=3, callback=self.selected_port_callback)
                        else:
                            dpg.add_listbox(self.portList, tag="__listPortsTag",
                                width=300, num_items=2,
                                callback=self.selected_port_callback)
                    dpg.add_loading_indicator(circle_count=2, tag="connected_indicator", speed=0)

                with dpg.tab(label="Setup"):
                    self.create_setup()

                with dpg.tab(label="Pumps"):
                    self.create_send_speed()

                with dpg.tab(label="Automate"):
                    self.create_automate()

                with dpg.tab(label="Simulations"):
                    self.create_calculate()
                    # self.create_msg_and_filter_columns()
                    # self.create_logger_window()

    def dpg_setup(self):
        dpg.create_context()
        windowWidth  = 1100
        windowHeight = 435
        dpg.create_viewport(title='Syringe Pump Control', width=windowWidth, height=windowHeight)
        dpg.setup_dearpygui()

    def selected_port_callback(self, Sender):
        self.SELECTED_DEVICE = dpg.get_value(Sender).split(' ')[0]
        logging.info("selected device: ")
        logging.info(self.SELECTED_DEVICE)
        # logging.info(self.SELECTED_DEVICE.count(" "))
        # logging.info(len(self.SELECTED_DEVICE))
        # logging.info(type(self.SELECTED_DEVICE))
        self.my_serial.port = self.SELECTED_DEVICE
        self.my_serial.connect()
        if self.my_serial.link:
            dpg.configure_item(item="connected_indicator", speed=dpg.get_value(self.channel_m_per_s))
        else:
            dpg.configure_item(item="connected_indicator", speed=0)

        logging.info(f"User selected: {self.SELECTED_DEVICE}")

    def dpg_show_view_port(self):
        dpg.set_viewport_resizable(False)
        dpg.show_viewport()

    def dpg_start_dearpygui(self):
        dpg.start_dearpygui()

    def dpg_cleanup(self):
        dpg.destroy_context()

    def exit_callback(self):
        dpg.stop_dearpygui()
################################### functions ################################

    def toggle(self):
        self.x = not self.x
        # toggle the speed of pump to 0

    def toggle_loop(self):
        global t
        self.toggle()
        self.data_list_toggle = self.data_list.copy()

        if dpg.get_value(item="automate_1"):
            print("pump1")
            self.data_list_toggle['stepspeed_1'] = 0
        if dpg.get_value(item="automate_2"):
            print("pump2")
            self.data_list_toggle['stepspeed_2'] = 0
        if dpg.get_value(item="automate_3"):
            print("pump3")
            self.data_list_toggle['stepspeed_3'] = 0
        if dpg.get_value(item="automate_4"):
            print("pump4")
            self.data_list_toggle['stepspeed_4'] = 0

        if self.x is True:
            self.my_serial.send_to_arduino(list(self.data_list_toggle.values()))
        else:
            self.my_serial.send_to_arduino(list(self.data_list.values()))

        t = threading.Timer(dpg.get_value(item="interval"), self.toggle_loop)
        t.start()

    def automate_pumps(self, user_data):
        self.x = True
        print(user_data)
        if "start_auto" in user_data:
            print("On")
            self.toggle_loop()
            dpg.configure_item(item="automated_indicator", speed=dpg.get_value(self.channel_m_per_s))

        else:
            print("Off")
            t.cancel()
            dpg.configure_item(item="automated_indicator", speed=0)


    def calculate_cannel_ratios(self):
        channel_value_1 = dpg.get_value(item="flow_speed_pump_1")
        channel_value_2 = dpg.get_value(item="flow_speed_pump_2")
        channel_value_3 = dpg.get_value(item="flow_speed_pump_3")
        channel_value_4 = dpg.get_value(item="flow_speed_pump_4")
        channel_combined_value = channel_value_1+channel_value_2+channel_value_3+channel_value_4
        self.channel_ratio_1 = channel_value_1/channel_combined_value
        self.channel_ratio_2 = channel_value_2/channel_combined_value
        self.channel_ratio_3 = channel_value_3/channel_combined_value
        self.channel_ratio_4 = channel_value_4/channel_combined_value

    def send_speed_to_arduino(self, sender, app_data, user_data):
        # overwrite the last settings with the standard position to go

        dpg.configure_item(item="pumping_indicator", speed=dpg.get_value(self.channel_m_per_s))

        if user_data is None:
            self.calculate_motors()
        else:
            if "speed" in user_data:
                dpg.set_value("channel_flow_speed", user_data["speed"])
                self.data_list['position_1'] = self.sw_endstop
                self.data_list['position_2'] = self.sw_endstop
                self.data_list['position_3'] = self.sw_endstop
                self.data_list['position_4'] = self.sw_endstop
                self.calculate_motors()
            elif "go_to_endstops" in user_data and user_data["go_to_endstops"] == True:
                self.data_list['position_1'] = 0
                self.data_list['position_2'] = 0
                self.data_list['position_3'] = 0
                self.data_list['position_4'] = 0
                self.data_list['stepspeed_1'] = self.max_speed
                self.data_list['stepspeed_2'] = self.max_speed
                self.data_list['stepspeed_3'] = self.max_speed
                self.data_list['stepspeed_4'] = self.max_speed
            elif "set_speed_zero" in user_data and user_data["set_speed_zero"] == True:
                # disable on high, but not connected in hardware (?!)
                # self.data_list['motor0_enable'] = 1
                self.data_list['stepspeed_1'] = 0
                self.data_list['stepspeed_2'] = 0
                self.data_list['stepspeed_3'] = 0
                self.data_list['stepspeed_4'] = 0
                dpg.configure_item(item="pumping_indicator", speed=0)
            elif "pump" and "fast_forward" in user_data:
                element = (user_data[1])
                print(f"Moving pump {element} fast_forward")
                #only the according pump is set
                self.data_list[f'position_{element}'] = self.sw_endstop
                self.data_list[f'stepspeed_{element}'] = self.max_speed
            elif "pump" and "normal_forward" in user_data:
                element = (user_data[1])
                print(f"Moving pump {element} fast_forward")
                #only the according pump is set
                self.data_list[f'position_{element}'] = self.sw_endstop
                self.data_list[f'stepspeed_{element}'] = int(self.max_speed/2)
            elif "pump" and "stop" in user_data:
                element = (user_data[1])
                print(f"Stopping pump {element}")
                self.data_list[f'stepspeed_{element}'] = 0
                dpg.configure_item(item=f"setup_movement_indicator_{element}", speed=0)
            elif "pump" and "normal_backward" in user_data:
                element = (user_data[1])
                print(f"Moving pump {element} fast_backward")
                # position needs to be negative
                #only the according pump is set
                self.data_list[f'position_{element}'] = -self.sw_endstop
                self.data_list[f'stepspeed_{element}'] = int(self.max_speed/2)
            elif "pump" and "fast_backward" in user_data:
                element = (user_data[1])
                print(f"Moving pump {element} fast_backward")
                # position needs to be negative
                #only the according pump is set
                self.data_list[f'position_{element}'] = -self.sw_endstop
                self.data_list[f'stepspeed_{element}'] = self.max_speed

        # only send the values from the dictionary to the arduino
        self.my_serial.send_to_arduino(list(self.data_list.values()))

    # def send_msg_to_serial_port_callback(self, sender, app_data, user_data) -> None:
    #     """
    #     Callbacks may have up to 3 arguments in the following order.

    #     sender:
    #     the id of the UI item that submitted the callback

    #     app_data:
    #     occasionally UI items will send their own data (ex. file dialog)

    #     user_data:
    #     any python object you want to send to the function
    #     """
    #     msg_to_send = dpg.get_value(user_data['userSpeedTag'])

    #     if not self.SELECTED_DEVICE:
    #         logging.info("User is not selected any device.")
    #     elif not self.my_serial.link:
    #         logging.info("Device is not connected")
    #     elif not msg_to_send:
    #         logging.info("No message.")
    #     else:
    #         self.my_serial.write_to_serial(msg_to_send)
    #         self.log_msg(msg_to_send, serial_ui.CLIENT_THEME)
    #         logging.info(f"Sent |{msg_to_send}| to {self.SELECTED_DEVICE}")
    #         dpg.configure_item("usrMsgTxt", default_value="")

    def log_msg(self, message, custom_theme):
        new_log = dpg.add_text(message, parent=self.filter_id, filter_key=message)
        dpg.bind_item_theme(new_log, custom_theme)

if __name__ == "__main__":
    gui = serial_ui()
