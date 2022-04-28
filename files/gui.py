from types import NoneType
import dearpygui.dearpygui as dpg
from themes import create_theme_imgui_light, create_theme_client, create_theme_server
from arduino import Arduino
from flowspeed_motorspeed import calculate_stepspeed
import yaml

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
        self.max_speed = 15000
        self.position_1 = 100000
        self.position_2 = 100000
        self.position_3 = 100000
        self.position_4 = 100000
        self.sw_endstop = 1000000
        self.motor0_direction, self.motor1_direction, self.motor2_direction, self.motor3_direction = 0, 0, 0, 0
        self.motor0_enable, self.motor1_enable, self.motor2_enable, self.motor3_enable = 0, 0, 0, 0 # enable on low = 0
        self.my_serial = Arduino(findusbport_hwid="16C0:0483")
        # self.update_ports_callback()
        # self.my_serial.hwid =  # should be changed by dropdown to search teensy, ardunio..
        try:
            self.portList  = self.my_serial.get_availabile_port_list()
            print(self.portList)
        except:
            self.portList  = []
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

    def calculate_motors(self):
        # the channel speeds are multiplied with the fractional value per channel
        # print((self.syringe_diameter_1))
        # print(float(self.syringe_diameter_1))        
        # print((self.stepspeed_1))
        # print(type(self.stepspeed_1))
        stepspeed1 = calculate_stepspeed(float(dpg.get_value(self.channel_m_per_s_1))*float(dpg.get_value(self.channel_m_per_s)), float(dpg.get_value(self.syringe_diameter_1)), float(dpg.get_value(self.channel_area_sqmm_1)))
        stepspeed2 = calculate_stepspeed(float(dpg.get_value(self.channel_m_per_s_2))*float(dpg.get_value(self.channel_m_per_s)), float(dpg.get_value(self.syringe_diameter_2)), float(dpg.get_value(self.channel_area_sqmm_2)))
        stepspeed3 = calculate_stepspeed(float(dpg.get_value(self.channel_m_per_s_3))*float(dpg.get_value(self.channel_m_per_s)), float(dpg.get_value(self.syringe_diameter_3)), float(dpg.get_value(self.channel_area_sqmm_3)))
        stepspeed4 = calculate_stepspeed(float(dpg.get_value(self.channel_m_per_s_4))*float(dpg.get_value(self.channel_m_per_s)), float(dpg.get_value(self.syringe_diameter_4)), float(dpg.get_value(self.channel_area_sqmm_4)))
        
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

    def save_state(self, sender, app_data, user_data):
        file_name = "pump_settings.yaml"
        print(file_name, user_data)

        speed_position = [
            float(dpg.get_value(self.channel_m_per_s)),
            float(dpg.get_value(self.channel_m_per_s_1)), float(dpg.get_value(self.syringe_diameter_1)), float(dpg.get_value(self.channel_area_sqmm_1)),
            float(dpg.get_value(self.channel_m_per_s_2)), float(dpg.get_value(self.syringe_diameter_2)), float(dpg.get_value(self.channel_area_sqmm_2)),
            float(dpg.get_value(self.channel_m_per_s_3)), float(dpg.get_value(self.syringe_diameter_3)), float(dpg.get_value(self.channel_area_sqmm_3)),
            float(dpg.get_value(self.channel_m_per_s_4)), float(dpg.get_value(self.syringe_diameter_4)), float(dpg.get_value(self.channel_area_sqmm_4)),
        ]
        print(speed_position)

        # with open(file_name) as f:
        #     doc = yaml.safe_load(f)
        # # doc = dpg.get_item_user_data("load_data", user_data=doc)
        #     print(doc)
        # if not doc:
        # print("no data stored")
        with open(file_name, 'w+') as f:
            yaml.safe_dump(speed_position, f, default_flow_style=False)

    def load_state(self, sender, app_data, user_data):
        file_name = "pump_settings.yaml"
        with open(file_name) as f:
            doc = yaml.safe_load(f)
            print("loaded data:")
            print(doc)
            speed_position = doc
        # dpg.set_item_user_data("load_data", user_data=doc) 
        
        dpg.set_value(self.channel_m_per_s, speed_position[0])
        dpg.set_value(self.channel_m_per_s_1, speed_position[1]), dpg.set_value(self.syringe_diameter_1, speed_position[2]), dpg.set_value(self.channel_area_sqmm_1, speed_position[3]),
        dpg.set_value(self.channel_m_per_s_2, speed_position[4]), dpg.set_value(self.syringe_diameter_2, speed_position[5]), dpg.set_value(self.channel_area_sqmm_2, speed_position[6]),
        dpg.set_value(self.channel_m_per_s_3, speed_position[7]), dpg.set_value(self.syringe_diameter_3, speed_position[8]), dpg.set_value(self.channel_area_sqmm_3, speed_position[9]),
        dpg.set_value(self.channel_m_per_s_4, speed_position[10]), dpg.set_value(self.syringe_diameter_4, speed_position[11]), dpg.set_value(self.channel_area_sqmm_4, speed_position[12])

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
                dpg.add_text(default_value="Please set Pump 1-4 to match 100% = 1.0", parent=text_group)
                
                # dpg.add_image(texture_tag="sarcura", value="sarcura.svg")
            with dpg.group() as inp_values_group:
                self.channel_m_per_s = dpg.add_input_float(tag="channel_flow_speed",
                        default_value=1, max_value=3, width=180,
                        parent=inp_values_group)
                self.channel_m_per_s_1 = dpg.add_input_float(tag="flow_speed_pump_1",
                        default_value=1/4, max_value=3, width=180,
                        parent=inp_values_group)
                self.channel_m_per_s_2 = dpg.add_input_float(tag="flow_speed_pump_2",
                        default_value=1/4, max_value=3, width=180,
                        parent=inp_values_group)
                self.channel_m_per_s_3 = dpg.add_input_float(tag="flow_speed_pump_3",
                        default_value=1/4, max_value=3, width=180,
                        parent=inp_values_group)
                self.channel_m_per_s_4 = dpg.add_input_float(tag="flow_speed_pump_4",
                        default_value=1/4, max_value=3, width=180,
                        parent=inp_values_group)
                self.channel_area_sqmm_1 = dpg.add_input_float(tag="channel_area_sqmm_1",
                        default_value=0.003, max_value=100, width=180,
                        parent=inp_values_group)
                self.channel_area_sqmm_2 = dpg.add_input_float(tag="channel_area_sqmm_2",
                        default_value=0.003, max_value=100, width=180,
                        parent=inp_values_group)
                self.channel_area_sqmm_3 = dpg.add_input_float(tag="channel_area_sqmm_3",
                        default_value=0.003, max_value=100, width=180,
                        parent=inp_values_group)
                self.channel_area_sqmm_4 = dpg.add_input_float(tag="channel_area_sqmm_4",
                        default_value=0.003, max_value=100, width=180,
                        parent=inp_values_group)
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Save Data", callback=self.save_state, tag="save_data")
                    dpg.add_button(label="Load Data", callback=self.load_state, tag="load_data")

            with dpg.group(horizontal=True) as syringe_values_group:
                syringe_diameters = [4.78, 8.66, 12.06, 14.5, 19.13, 21.7, 26.7] # BD plastic
                with dpg.group():
                    dpg.add_text(default_value="syringe 1 Ø [mm]")
                    self.syringe_diameter_1 = dpg.add_listbox(syringe_diameters, tag="syringe_dia_1", width=80, num_items=7)
                with dpg.group():
                    dpg.add_text(default_value="syringe 2 Ø [mm]")
                    self.syringe_diameter_2 = dpg.add_listbox(syringe_diameters, tag="syringe_dia_2", width=80, num_items=7)
                with dpg.group():
                    dpg.add_text(default_value="syringe 3 Ø [mm]")
                    self.syringe_diameter_3 = dpg.add_listbox(syringe_diameters, tag="syringe_dia_3", width=80, num_items=7)
                with dpg.group():
                    dpg.add_text(default_value="syringe 4 Ø [mm]")
                    self.syringe_diameter_4 = dpg.add_listbox(syringe_diameters, tag="syringe_dia_4", width=80, num_items=7)

        dpg.add_separator()

        with dpg.group(horizontal=True) as send_group:
            dpg.add_button(tag="sendSpeedBtn", label="Start Pumps",
                callback=self.send_speed_to_arduino, parent=send_group)
            dpg.add_button(tag="sendSpeedBtn05ms", user_data={"speed": 0.5}, label="Set Pumps to 0.5 m/s",
                callback=self.send_speed_to_arduino, parent=send_group)
            dpg.add_button(tag="sendSpeedBtn10ms", user_data={"speed": 1.0}, label="Set Pumps to 1 m/s",
                callback=self.send_speed_to_arduino, parent=send_group)
            dpg.add_button(tag="sendSpeedBtn15ms", user_data={"speed": 1.5}, label="Set Pumps to 1.5 m/s",
                callback=self.send_speed_to_arduino, parent=send_group)
            dpg.add_button(tag="sendSpeedBtn20ms", user_data={"speed": 2}, label="Set Pumps to 2 m/s",
                callback=self.send_speed_to_arduino, parent=send_group)
            dpg.add_button(tag="sendSet0", user_data={"go_to_endstops" : True}, label="Go Back to Zero",
                callback=self.send_speed_to_arduino, parent=send_group)
            dpg.add_button(tag="sendStop", user_data={"set_speed_zero" : True}, label="Stop Pumps",
                callback=self.send_speed_to_arduino, parent=send_group)

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
        windowHeight = 335
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
        self.position_1, self.position_2, self.position_3, self.position_4 = self.sw_endstop, self.sw_endstop, self.sw_endstop, self.sw_endstop

        if user_data is None:
            self.calculate_motors()
            data_list = [self.motor0_enable, self.motor0_direction, self.position_1, self.stepspeed_1, 
                self.motor1_enable, self.motor1_direction, self.position_2, self.stepspeed_2, 
                self.motor2_enable, self.motor2_direction, self.position_3, self.stepspeed_3,
                self.motor3_enable, self.motor3_direction, self.position_4, self.stepspeed_4]
        else:
            if "speed" in user_data:
                dpg.set_value("channel_flow_speed", user_data["speed"])
                self.calculate_motors()
                data_list = [self.motor0_enable, self.motor0_direction, self.position_1, self.stepspeed_1, 
                    self.motor1_enable, self.motor1_direction, self.position_2, self.stepspeed_2, 
                    self.motor2_enable, self.motor2_direction, self.position_3, self.stepspeed_3,
                    self.motor3_enable, self.motor3_direction, self.position_4, self.stepspeed_4]
            if "go_to_endstops" in user_data and user_data["go_to_endstops"] == True:
                self.position_1, self.position_2, self.position_3, self.position_4 = 0, 0, 0, 0
                data_list = [self.motor0_enable, self.motor0_direction, self.position_1, self.max_speed, 
                    self.motor1_enable, self.motor1_direction, self.position_2, self.max_speed, 
                    self.motor2_enable, self.motor2_direction, self.position_3, self.max_speed,
                    self.motor3_enable, self.motor3_direction, self.position_4, self.max_speed]
            if "set_speed_zero" in user_data and user_data["set_speed_zero"] == True:
                # disable on high, but not connected in hardware (?!)
                # self.motor0_enable, self.motor1_enable, self.motor2_enable, self.motor3_enable = 1, 1, 1, 1
                self.position_1, self.position_2, self.position_3, self.position_4 = 0, 0, 0, 0
                data_list = [self.motor0_enable, self.motor0_direction, self.position_1, 0, 
                    self.motor1_enable, self.motor1_direction, self.position_2, 0, 
                    self.motor2_enable, self.motor2_direction, self.position_3, 0,
                    self.motor3_enable, self.motor3_direction, self.position_4, 0]

        self.my_serial.send_to_arduino(data_list)

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