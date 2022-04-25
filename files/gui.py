import dearpygui.dearpygui as dpg
from themes import create_theme_imgui_light, create_theme_client, create_theme_server
from arduino import Arduino
from flowspeed_motorspeed import calculate_stepspeed

class serial_ui():
    CLIENT_THEME = None
    SERVER_THEME = None

    def __init__(self):
        # self.my_serial = mySerial()s
        self.channel_m_per_s = 1 # total flow in channel
        self.channel_m_per_s_1 = 1/4 # this is a percentage of the total flow
        self.syringe_diameter_1 = 12.08
        self.channel_area_sqmm_1 = 0.03*0.1
        self.channel_m_per_s_2 = 1/4
        self.syringe_diameter_2 = 12.08
        self.channel_area_sqmm_2 = 0.03*0.1
        self.channel_m_per_s_3 = 1/4
        self.syringe_diameter_3 = 12.08
        self.channel_area_sqmm_3 = 0.03*0.1
        self.channel_m_per_s_4 = 1/4
        self.syringe_diameter_4 = 12.08
        self.channel_area_sqmm_4 = 0.03*0.1
        self.stepspeed_1 = 0
        self.stepspeed_2 = 0
        self.stepspeed_3 = 0
        self.stepspeed_4 = 0
        self.motor_speed()
        self.my_serial = Arduino(findusbport_hwid="16C0:0483")
        # self.my_serial.hwid =  # should be changed by dropdown to search teensy, ardunio..
        try:
            self.portList  = self.my_serial.get_availabile_port_list()
        except:
            self.portList  = ["COMx"]
            print("no devices found.")
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
                # print(self.stepspeed)
                pass
                # print("teensy connected")
                # recv_msg = self.my_serial.read_serial()
                # if recv_msg:
                #     max_length = 122
                #     if len(recv_msg) > max_length:
                #         truncated_msg = recv_msg[0:122-3] + "..."
                #         self.log_msg(truncated_msg, serial_ui.SERVER_THEME)
                #     else:
                #         self.log_msg(recv_msg, serial_ui.SERVER_THEME)
                #     print(f"Received: {recv_msg}")
                #     self.log_msg(recv_msg, serial_ui.SERVER_THEME)
            try:
                dpg.render_dearpygui_frame()
            except KeyboardInterrupt:
                return
            dpg.set_exit_callback(self.exit_callback)
        self.dpg_cleanup()

    def motor_speed(self):
        # the channel speeds are multiplied with the fractional value per channel
        stepspeed1 = calculate_stepspeed(self.channel_m_per_s_1*self.channel_m_per_s, self.syringe_diameter_1, self.channel_area_sqmm_1)
        stepspeed2 = calculate_stepspeed(self.channel_m_per_s_2*self.channel_m_per_s, self.syringe_diameter_2, self.channel_area_sqmm_2)
        stepspeed3 = calculate_stepspeed(self.channel_m_per_s_3*self.channel_m_per_s, self.syringe_diameter_3, self.channel_area_sqmm_3)
        stepspeed4 = calculate_stepspeed(self.channel_m_per_s_4*self.channel_m_per_s, self.syringe_diameter_4, self.channel_area_sqmm_4)
        
        self.stepspeed_1 =  int(round(stepspeed1))
        self.stepspeed_2 =  int(round(stepspeed2))
        self.stepspeed_3 =  int(round(stepspeed3))
        self.stepspeed_4 =  int(round(stepspeed4))

    def update_ports_callback(self):
        self.my_serial.get_availabile_port_list()
        dpg.configure_item("__listPortsTag", items=self.my_serial.comport_list)

    def create_logger_window(self):
        ## this creates a window at bottom
        child_logger_id = dpg.add_child_window(tag="logger", width=870, height=340)
        self.filter_id = dpg.add_filter_set(parent=child_logger_id)

    def create_send_speed(self):
        with dpg.group(horizontal=True):
            with dpg.group() as text_group:
                dpg.add_text(default_value="Channel [m/s]", parent=text_group)
                dpg.add_text(default_value="Pump 1 [m/s fraction]", parent=text_group)
                dpg.add_text(default_value="Pump 2 [m/s fraction]", parent=text_group)
                dpg.add_text(default_value="Pump 3 [m/s fraction]", parent=text_group)
                dpg.add_text(default_value="Pump 4 [m/s fraction]", parent=text_group)
                dpg.add_text(default_value="Channel 1 [mm²]", parent=text_group)
                dpg.add_text(default_value="Channel 2 [mm²]", parent=text_group)
                dpg.add_text(default_value="Channel 3 [mm²]", parent=text_group)
                dpg.add_text(default_value="Channel 4 [mm²]", parent=text_group)
                dpg.add_text(default_value="Please set Pump 1-4 to match 100 %", parent=text_group)
                
                # dpg.add_image(texture_tag="sarcura", value="sarcura.svg")
            with dpg.group() as inp_values_group:
                channel_flow_speed = dpg.add_input_float(tag="sendSpeedFloat",
                        default_value=1, max_value=3, width=180,
                        parent=inp_values_group)
                user_msg1 = dpg.add_input_float(tag="sendSpeedFloat1",
                        default_value=1/4, max_value=3, width=180,
                        parent=inp_values_group)
                user_msg2 = dpg.add_input_float(tag="sendSpeedFloat2",
                        default_value=1/4, max_value=3, width=180,
                        parent=inp_values_group)
                user_msg3 = dpg.add_input_float(tag="sendSpeedFloat3",
                        default_value=1/4, max_value=3, width=180,
                        parent=inp_values_group)
                user_msg4 = dpg.add_input_float(tag="sendSpeedFloat4",
                        default_value=1/4, max_value=3, width=180,
                        parent=inp_values_group)
                channel_area_sqmm_1 = dpg.add_input_float(tag="channel_area_sqmm_1",
                        default_value=0.003, max_value=100, width=180,
                        parent=inp_values_group)
                channel_area_sqmm_2 = dpg.add_input_float(tag="channel_area_sqmm_2",
                        default_value=0.003, max_value=100, width=180,
                        parent=inp_values_group)
                channel_area_sqmm_3 = dpg.add_input_float(tag="channel_area_sqmm_3",
                        default_value=0.003, max_value=100, width=180,
                        parent=inp_values_group)
                channel_area_sqmm_4 = dpg.add_input_float(tag="channel_area_sqmm_4",
                        default_value=0.003, max_value=100, width=180,
                        parent=inp_values_group)

                # self.syringe_diameter_1 = 12.08
                # self.channel_area_sqmm_1 = 0.03*0.1
                # self.syringe_diameter_2 = 12.08
                # self.channel_area_sqmm_2 = 0.03*0.1
                # self.syringe_diameter_3 = 12.08
                # self.channel_area_sqmm_3 = 0.03*0.1
                # self.syringe_diameter_4 = 12.08
                # self.channel_area_sqmm_4 = 0.03*0.1
            with dpg.group(horizontal=True) as syringe_values_group:
                syringe_areas = [4.78, 8.66, 12.06, 14.5, 19.13, 21.7, 26.7] # BD plastic
                with dpg.group():
                    dpg.add_text(default_value="syringe 1 Ø [mm]")
                    syringearea_1 = dpg.add_listbox(syringe_areas, tag="__listSyringes1", width=80, num_items=7) 
                with dpg.group():
                    dpg.add_text(default_value="syringe 2 Ø [mm]")
                    syringearea_2 = dpg.add_listbox(syringe_areas, tag="__listSyringes2", width=80, num_items=7) 
                with dpg.group():
                    dpg.add_text(default_value="syringe 3 Ø [mm]")
                    syringearea_3 = dpg.add_listbox(syringe_areas, tag="__listSyringes3", width=80, num_items=7) 
                with dpg.group():
                    dpg.add_text(default_value="syringe 4 Ø [mm]")
                    syringearea_4 = dpg.add_listbox(syringe_areas, tag="__listSyringes4", width=80, num_items=7)

            # self.channel_volumetric_flow_4 = self.channel_m_per_s_4*self.channel_area_sqmm_4
            # print(self.channel_volumetric_flow_4)
            # print(type(self.channel_volumetric_flow_4))

            # with dpg.group() as button_group:
                # dpg.add_button(tag="sendSpeedBtn1", label="Set Pump 1",
                #     callback=self.send_speed_to_arduino,
                #     user_data={'userSpeedTag1': user_msg1}, parent=button_group)
                # dpg.add_button(tag="sendSpeedBtn2", label="Set Pump 2",
                #     callback=self.send_speed_to_arduino,
                #     user_data={'userSpeedTag2': user_msg2}, parent=button_group)
                # dpg.add_button(tag="sendSpeedBtn3", label="Set Pump 3",
                #     callback=self.send_speed_to_arduino,
                #     user_data={'userSpeedTag3': user_msg3}, parent=button_group)
                # dpg.add_button(tag="sendSpeedBtn4", label="Set Pump 4",
                #     callback=self.send_speed_to_arduino,
                #     user_data={'userSpeedTag4': user_msg4}, parent=button_group)

        dpg.add_separator()

        with dpg.group() as send_group:
            dpg.add_button(tag="sendSpeedBtn", label="Start Pumps",
                callback=self.send_speed_to_arduino,
                user_data={'channel_flow_speed': channel_flow_speed,
                    'userSpeedTag1': user_msg1, 'userSpeedTag2': user_msg2,
                    'userSpeedTag3': user_msg3,'userSpeedTag4': user_msg4,
                    'channel_area_sqmm_1': channel_area_sqmm_1, 'channel_area_sqmm_2': channel_area_sqmm_2, 
                    'channel_area_sqmm_3': channel_area_sqmm_3, 'channel_area_sqmm_4': channel_area_sqmm_4, 
                    'syringe_area_1' : syringearea_1, 'syringe_area_2' : syringearea_2, 
                    'syringe_area_3' : syringearea_3, 'syringe_area_4' : syringearea_4, 
                    }, parent=send_group)
                    
            dpg.add_button(tag="sendSpeedBtn2ms", label="Set Pumps to 2 m/s",
                callback=self.set_ms_and_send_speed_to_arduino,
                user_data={'channel_flow_speed': channel_flow_speed,
                    'userSpeedTag1': user_msg1, 'userSpeedTag2': user_msg2,
                    'userSpeedTag3': user_msg3,'userSpeedTag4': user_msg4,
                    'channel_area_sqmm_1': channel_area_sqmm_1, 'channel_area_sqmm_2': channel_area_sqmm_2, 
                    'channel_area_sqmm_3': channel_area_sqmm_3, 'channel_area_sqmm_4': channel_area_sqmm_4, 
                    'syringe_area_1' : syringearea_1, 'syringe_area_2' : syringearea_2, 
                    'syringe_area_3' : syringearea_3, 'syringe_area_4' : syringearea_4, 
                    }, parent=send_group)

        width, height, channels, data = dpg.load_image("sarcura.png") 
        with dpg.texture_registry():
            texture_id = dpg.add_static_texture(width, height, data) 
        dpg.add_image(texture_id)

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
            with dpg.group(horizontal=True):
                # After clicking it will show a list view of ports
                dpg.add_button(tag="avPortsBtn", label="Refresh Available Ports", callback=self.update_ports_callback)
                if not self.portList:
                    dpg.add_listbox(["No Ports available"], tag="__listPortsTag",
                            width=300,
                            num_items=-1, callback=self.selected_port_callback)
                else:
                    dpg.add_listbox(self.portList, tag="__listPortsTag",
                        width=300, num_items=2,
                        callback=self.selected_port_callback)

            self.create_send_speed()
            # self.create_msg_and_filter_columns()
            self.create_logger_window()

    def dpg_setup(self):
        dpg.create_context()
        windowWidth  = 1100
        windowHeight = 525
        dpg.create_viewport(title='Serial GUI', width=windowWidth, height=windowHeight)
        dpg.setup_dearpygui()

    def selected_port_callback(self, Sender):
        self.SELECTED_DEVICE = dpg.get_value(Sender).split(' ')[0]
        print("selected device: ")
        print(self.SELECTED_DEVICE)
        # print(self.SELECTED_DEVICE.count(" "))
        # print(len(self.SELECTED_DEVICE))
        # print(type(self.SELECTED_DEVICE))
        self.my_serial.port = self.SELECTED_DEVICE
        self.my_serial.connect()
        print(f"User selected: {self.SELECTED_DEVICE}")

    def dpg_show_view_port(self):
        dpg.set_viewport_resizable(False)
        dpg.show_viewport()

    def dpg_start_dearpygui(self):
        dpg.start_dearpygui()

    def dpg_cleanup(self):
        dpg.destroy_context()

    def exit_callback(self):
        dpg.stop_dearpygui()

    def send_speed_to_arduino(self, sender, app_data, user_data):
        print(f"user data: {user_data}")
        print(f"user data: {user_data['channel_flow_speed']}")
        print(f"user data: {type(user_data['channel_flow_speed'])}")
        print(f"user data: {dpg.get_value(user_data['channel_flow_speed'])}")
        print(f"user data type: {type(dpg.get_value(user_data['channel_flow_speed']))}")
        print(f"user data type: {float(dpg.get_value(user_data['channel_flow_speed']))}")
        print(f"user data type: {type(dpg.get_value(user_data['channel_flow_speed']))}")

        # dpg.set_value("sendSpeedFloat", float(user_data['channel_flow_speed'])) # if the value is not set but send to function
        # dpg.set_value("sendSpeedFloat", (user_data['channel_flow_speed'])) # if the value is not set but send to function
        # self.channel_m_per_s_1, self.channel_m_per_s_2, self.channel_m_per_s_3, self.channel_m_per_s_4 = dpg.get_value(user_data[0]),dpg.get_value(user_data[1]),dpg.get_value(user_data[2]),dpg.get_value(user_data[3])
        self.channel_m_per_s = float(dpg.get_value(user_data['channel_flow_speed']))
        self.channel_m_per_s_1, self.channel_m_per_s_2, self.channel_m_per_s_3, self.channel_m_per_s_4 = dpg.get_value(user_data['userSpeedTag1']),dpg.get_value(user_data['userSpeedTag2']),dpg.get_value(user_data['userSpeedTag3']),dpg.get_value(user_data['userSpeedTag4'])
        self.syringe_diameter_1 = float(dpg.get_value(user_data['syringe_area_1']))
        self.syringe_diameter_2 = float(dpg.get_value(user_data['syringe_area_2']))
        self.syringe_diameter_3 = float(dpg.get_value(user_data['syringe_area_3']))
        self.syringe_diameter_4 = float(dpg.get_value(user_data['syringe_area_4']))
        self.channel_area_sqmm_1 = float(dpg.get_value(user_data['channel_area_sqmm_1']))
        self.channel_area_sqmm_2 = float(dpg.get_value(user_data['channel_area_sqmm_2']))
        self.channel_area_sqmm_3 = float(dpg.get_value(user_data['channel_area_sqmm_3']))
        self.channel_area_sqmm_4 = float(dpg.get_value(user_data['channel_area_sqmm_4']))

        # self.channel_m_per_s_1 = dpg.get_value(user_data['userSpeedTag1'])
        # self.channel_m_per_s_2 = dpg.get_value(user_data['userSpeedTag2'])
        # self.channel_m_per_s_3 = dpg.get_value(user_data['userSpeedTag3'])
        # self.channel_m_per_s_4 = dpg.get_value(user_data['userSpeedTag4'])
        
        self.motor_speed()
        motor0_enable = 1
        motor0_direction = 0
        motor1_enable = 1
        motor1_direction = 0
        motor2_enable = 1
        motor2_direction = 0
        motor3_enable = 1
        motor3_direction = 0
        data_list = [motor0_enable, motor0_direction, self.stepspeed_1, self.stepspeed_1,
            motor1_enable, motor1_direction, self.stepspeed_2, self.stepspeed_2,
            motor2_enable, motor2_direction, self.stepspeed_3, self.stepspeed_3,
            motor3_enable, motor3_direction, self.stepspeed_4, self.stepspeed_4]

            # motor1_enable, motor1_direction, dpg.get_value(user_data['userSpeedTag1']), dpg.get_value(user_data['userSpeedTag1']),
            # motor2_enable, motor2_direction, dpg.get_value(user_data['userSpeedTag2']), dpg.get_value(user_data['userSpeedTag2']),
            # motor3_enable, motor3_direction, dpg.get_value(user_data['userSpeedTag3']), dpg.get_value(user_data['userSpeedTag3'])]

        # data_list = [motor0_enable, motor0_direction, dpg.get_value(item=slider_position_4int)[0], dpg.get_value(item=slider_speed_4int)[0],
        #     motor1_enable, motor1_direction, dpg.get_value(item=slider_position_4int)[1], dpg.get_value(item=slider_speed_4int)[1],
        #     motor2_enable, motor2_direction, dpg.get_value(item=slider_position_4int)[2], dpg.get_value(item=slider_speed_4int)[2],
        #     motor3_enable, motor3_direction, dpg.get_value(item=slider_position_4int)[3], dpg.get_value(item=slider_speed_4int)[3]]

        self.my_serial.send_to_arduino(data_list)

    def set_ms_and_send_speed_to_arduino(self, sender, app_data, user_data):
        dpg.set_value("sendSpeedFloat", float(2))
        self.send_speed_to_arduino(self, app_data, user_data)



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
    #         print("User is not selected any device.")
    #     elif not self.my_serial.link:
    #         print("Device is not connected")
    #     elif not msg_to_send:
    #         print("No message.")
    #     else:
    #         self.my_serial.write_to_serial(msg_to_send)
    #         self.log_msg(msg_to_send, serial_ui.CLIENT_THEME)
    #         print(f"Sent |{msg_to_send}| to {self.SELECTED_DEVICE}")
    #         dpg.configure_item("usrMsgTxt", default_value="")


    def log_msg(self, message, custom_theme):
        new_log = dpg.add_text(message, parent=self.filter_id, filter_key=message)
        dpg.bind_item_theme(new_log, custom_theme)

if __name__ == "__main__":
    gui = serial_ui()