import dearpygui.dearpygui as dpg

dpg.create_context()

with dpg.window(label="Tutorial") as window:
    # When creating items within the scope of the context
    # manager, they are automatically "parented" by the
    # container created in the initial call. So, "window"
    # will be the parent for all of these items.

    button1 = dpg.add_button(label="Press Me!")

    slider_int = dpg.add_slider_int(label="Slide to the left!", width=100)
    slider_float = dpg.add_slider_float(label="Slide to the right!", width=100)

    # An item's unique identifier (tag) is returned when
    # creating items.
    print(f"Printing item tag's: {window}, {button1}, {slider_int}, {slider_float}")

# If you want to add an item to an existing container, you
# can specify it by passing the container's tag as the
# "parent" parameter.
button2 = dpg.add_button(label="Don't forget me!", parent=window)

dpg.create_viewport(title='Custom Title', width=600, height=200)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

# import dearpygui.dearpygui as dpg

# dpg.create_context()

# with dpg.value_registry():
#     dpg.add_bool_value(default_value=True, tag="bool_value")
#     dpg.add_string_value(default_value="Default string", tag="string_value")
#     dpg.add_string_value(default_value="Default string", tag="string_value")

# with dpg.window(label="Tutorial"):
#     dpg.add_checkbox(label="Radio Button1", source="bool_value")
#     dpg.add_checkbox(label="Radio Button2", source="bool_value")
    
#     dpg.add_input_text(label="Text Input 1", source="string_value")
#     dpg.add_input_text(label="Text Input 2", source="string_value", password=True)
    
# dpg.create_viewport(title='Custom Title', width=800, height=600)
# dpg.setup_dearpygui()
# dpg.show_viewport()
# dpg.start_dearpygui()
# dpg.destroy_context()