import serial
import serial.tools.list_ports
port_list = list(serial.tools.list_ports.comports())
print(port_list[0].pid) # 1155 for Teensy
print(port_list[0].vid) # 5824 for Teensy
print(port_list[0].hwid)
print(port_list[0].device)
# print(port_list.device)
for thingy in port_list:
    print(thingy.device)
print(port_list[0].location)
print(port_list[0].manufacturer)
print(port_list[0].product)
print(port_list[0].description)
print(port_list[0].interface)
print(port_list[0].name)
print(port_list[0].serial_number)
print(port_list[0].__dict__)
print(port_list[1])
print(port_list[2])

def find_teensys(hardwareID="16C0:0483"):
    hardwareID = "(?i)" + hardwareID  # forces case insensitive
    comport_list = []
    if len(comport_list) == 0:
        comport_list = []
        for port in serial.tools.list_ports.grep(hardwareID):
            comport_list.append(port[0])
    return comport_list

comport_list = find_teensys()
print(comport_list)
# import dearpygui.dearpygui as dpg

# dpg.create_context()

# with dpg.window(label="Tutorial"):

#     # configuration set when button is created
#     dpg.add_button(label="Apply", width=300)

#     # user data and callback set any time after button has been created
#     btn = dpg.add_button(label="Apply 2")
#     dpg.set_item_label(btn, "Button 57")
#     dpg.set_item_width(btn, 200)

# dpg.show_item_registry()

# dpg.create_viewport(title='Custom Title', width=800, height=600)
# dpg.setup_dearpygui()
# dpg.show_viewport()
# dpg.start_dearpygui()
# dpg.destroy_context()

# import dearpygui.dearpygui as dpg

# dpg.create_context()

# with dpg.window(label="Tutorial", pos=(20, 50), width=275, height=225) as win1:
#     t1 = dpg.add_input_text(default_value="some text")
#     t2 = dpg.add_input_text(default_value="some text")
#     with dpg.child_window(height=100):
#         t3 = dpg.add_input_text(default_value="some text")
#         dpg.add_input_int()
#     dpg.add_input_text(default_value="some text")

# with dpg.window(label="Tutorial", pos=(320, 50), width=275, height=225) as win2:
#     dpg.add_input_text(default_value="some text")
#     dpg.add_input_int()

# with dpg.theme() as global_theme:
#     with dpg.theme_component(dpg.mvAll):
#         dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 140, 23), category=dpg.mvThemeCat_Core)
#         dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

#     with dpg.theme_component(dpg.mvInputInt):
#         dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (140, 255, 23), category=dpg.mvThemeCat_Core)
#         dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

# with dpg.theme() as container_theme:
#     with dpg.theme_component(dpg.mvAll):
#         dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (150, 100, 100), category=dpg.mvThemeCat_Core)
#         dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

#     with dpg.theme_component(dpg.mvInputInt):
#         dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (100, 150, 100), category=dpg.mvThemeCat_Core)
#         dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

# with dpg.theme() as item_theme:
#     with dpg.theme_component(dpg.mvAll):
#         dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (200, 200, 100), category=dpg.mvThemeCat_Core)
#         dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0, category=dpg.mvThemeCat_Core)

# dpg.bind_theme(global_theme)
# dpg.bind_item_theme(win1, container_theme)
# dpg.bind_item_theme(t2, item_theme)

# dpg.show_style_editor()

# dpg.create_viewport(title='Custom Title', width=800, height=600)
# dpg.setup_dearpygui()
# dpg.show_viewport()
# dpg.start_dearpygui()
# dpg.destroy_context()