import datetime
from itertools import tee
import numpy as np
from pySerialTransfer import pySerialTransfer as txfer
# please make sure to pip install pySerialTransfer==1.2
# connection will not work with pySerialTransfer==2.0
# requirement: pip install pyserial (works with 3.4 and most likely newer but not much older versions)
# on teensy: include "SerialTransfer.h" Version 2.0
# connecting multiple arduinos is not implemented

class Arduino:
    def __init__(self, port):
        self.port = port
        self.link = False
        self.data_list = False
        self.rec_data_list = False
        self.age = False

    def __str__(self):
        if self.link:
            return f"Connection on port {self.port} opened at {self.age} "
        else:
            return f"No connection on port {self.port} currently opened. ({datetime.datetime.now()})"
    def connect(self):
        try:
            print(f"Connecting to {self.port}")
            self.link = txfer.SerialTransfer(self.port)
            self.link.open()
            self.age = datetime.datetime.now()
            # time.sleep(1) # allow some time for the Arduino to completely reset
        except:
            import traceback
            traceback.print_exc()
            self.link.close()

    def disconnect(self):
        try:
            self.link.close()
            self.link = False
        except:
            import traceback
            traceback.print_exc()

    def search_arduinos():
        # not implemented
        pass

    def send_to_arduino(self, data_list):
        try:
            # reset send_size
            send_size = 0
            # Send a list
            print(f"Data list sent:     {data_list}")
            self.data_list = data_list
            print(f"Data list received: {self.data_list}")

            data_listsize = self.link.tx_obj(data_list)
            send_size += data_listsize
            
            # Transmit all the data to send in a single packet
            self.link.send(send_size)
            print("Message sent...")
            
            # Wait for a response and report any errors while receiving packets
            while not self.link.available():
                if self.link.status < 0:
                    if self.link.status == -1:
                        print('ERROR: CRC_ERROR')
                    elif self.link.status == -2:
                        print('ERROR: PAYLOAD_ERROR')
                    elif self.link.status == -3:
                        print('ERROR: STOP_BYTE_ERROR')

            # Parse response list
            ###################################################################
            self.rec_data_list  = self.link.rx_obj(obj_type=type(data_list),
                                        obj_byte_size=data_listsize,
                                        list_format='i')
    
            # print(f'SENT: {self.data_list}')
            # print(f'RCVD: {self.rec_data_list}')

        except:
            import traceback
            traceback.print_exc()
            self.link.close()

if __name__ == "__main__":
    comport = 'COM9'
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

    data_list = [motor0_enable, motor0_direction, motor0_speed, motor1_enable, motor1_direction,  motor1_speed,
        motor2_enable, motor2_direction, motor2_speed, motor3_enable, motor3_direction, motor3_speed]

    teensy1 = Arduino(comport)
    teensy1.connect()
    # import time
    # time.sleep(1)
    # print(teensy1)
    teensy1.send_to_arduino(data_list)
    # print(teensy1)
    teensy1.disconnect()
    # print(teensy1.link) # this is false is no link exists
    # print(teensy1)
    # print(teensy1.data_list)
    # print(teensy1.rec_data_list)

# def data_listavailable_ports():
#     ports = txfer.open_ports()
#     print("Available ports:")
#     print(ports)
#     return ports

# def connect_arduino(comport):
#     try:
#         print(f"Connecting to {comport}")
#         link = txfer.SerialTransfer(comport)
        
#         link.open()
#         return link
#         # time.sleep(1) # allow some time for the Arduino to completely reset
#     except:
#         import traceback
#         traceback.print_exc()
#         link.close()

# def disconnect_arduino(link):
#     try:
#         link.close()
#     except:
#         import traceback
#         traceback.print_exc()
        
# def send_to_arduino(link,motor0_enable,motor0_direction,motor0_speed,
#         motor1_enable,motor1_direction,motor1_speed,motor2_enable,motor2_direction,motor2_speed,motor3_enable,motor3_direction,motor3_speed):
#     try:
#         # reset send_size
#         send_size = 0
        
#         # Send a list
#         data_list = [motor0_enable, motor0_direction, motor0_speed, motor1_enable, motor1_direction,  motor1_speed,
#             motor2_enable, motor2_direction, motor2_speed, motor3_enable, motor3_direction, motor3_speed]
#         data_listsize = link.tx_obj(data_list)
#         send_size += data_listsize
        
#         # Transmit all the data to send in a single packet
#         link.send(send_size)
#         print("Message sent...")
        
#         # Wait for a response and report any errors while receiving packets
#         while not link.available():
#             if link.status < 0:
#                 if link.status == -1:
#                     print('ERROR: CRC_ERROR')
#                 elif link.status == -2:
#                     print('ERROR: PAYLOAD_ERROR')
#                 elif link.status == -3:
#                     print('ERROR: STOP_BYTE_ERROR')

#         # Parse response list
#         ###################################################################
#         rec_data_list  = link.rx_obj(obj_type=type(data_list),
#                                     obj_byte_size=data_listsize,
#                                     data_listformat='i')
 
#         print(f'SENT: {data_list}')
#         print(f'RCVD: {rec_data_list}')

#         return rec_data_list

#     # except KeyboardInterrupt:
#     #     link.close()

#     except:
#         import traceback
#         traceback.print_exc()
#         link.close()

# if __name__ == "__main__":
#     # data_listavailable_ports()
#     comport = 'COM9'
#     motor0_enable = 1
#     motor0_direction = 0
#     motor0_speed = 1000
#     motor1_enable = 1
#     motor1_direction = 0
#     motor1_speed = 1000
#     motor2_enable = 1
#     motor2_direction = 0
#     motor2_speed = 1000
#     motor3_enable = 1
#     motor3_direction = 0
#     motor3_speed = 1000

#     link = connect_arduino(comport)
#     results = np.array(send_to_arduino(link,motor0_enable,motor0_direction,motor0_speed,
#         motor1_enable,motor1_direction,motor1_speed,motor2_enable,motor2_direction,motor2_speed,motor3_enable,motor3_direction,motor3_speed))
#     disconnect_arduino(link)
#     print(results)