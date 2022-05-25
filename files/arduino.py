import datetime
from itertools import tee
import numpy as np
from pySerialTransfer import pySerialTransfer as txfer
# please make sure to pip install pySerialTransfer==1.2
# connection will not work with pySerialTransfer==2.0
# requirement: pip install pyserial (works with 3.4 and most likely newer but not much older versions)
# on teensy: include "SerialTransfer.h" Version 2.0
# connecting multiple arduinos is not implemented
import serial.tools.list_ports
class Arduino:
    def __init__(self, findusbport_hwid=None, port=None):
        self.hwid = findusbport_hwid
        if findusbport_hwid and not port:
            print(f"No port specified, looking for devides with hwid {findusbport_hwid}")
            self.get_availabile_port_list()
        else: # means, even if both are set
            self.port = port
        self.link = False
        self.data_list = False
        self.rec_data_list = False
        self.age = False
        self.comport_list = False
        self.found_multiple_devices = False

    def __str__(self):
        if self.link:
            return f"Connection on port {self.port} opened at {self.age} "
        else:
            return f"No connection on port {self.port} currently opened. ({datetime.datetime.now()})"

    def get_availabile_port_list(self):
        if self.hwid:
            self.hwid = "(?i)" + self.hwid  # forces case insensitive
            comport_list = []
            if len(comport_list) == 0:
                comport_list = []
                for port in serial.tools.list_ports.grep(self.hwid):
                    comport_list.append(port[0])
            self.comport_list = comport_list
            if len(self.comport_list) == 1:
                print(f"Warning, multiple devies with the same hwid found. Access by comport_list.")
                print(f"First device of the list will be used for connection: {self.comport_list}")
                self.found_multiple_devices = True # all found devices are stored for later access
                self.port = comport_list[0] # only takes the first device with the queried hardware id
        else:
            print("No hwid specified, search aborted.")

    def connect(self):
        try:
            print(f"Connecting to {self.port}")
            self.link = txfer.SerialTransfer(self.port)
            self.link.open()
            self.age = datetime.datetime.now()
            # self.connected = True
            # time.sleep(1) # allow some time for the Arduino to completely reset
        except:
            import traceback
            traceback.print_exc()
            self.link.close()

    def disconnect(self):
        try:
            print(f"Disconnecting {self.port}")
            self.link.close()
            self.link = False
            # self.connected = False
        except:
            import traceback
            traceback.print_exc()

    def search_arduinos():
        # not implemented
        pass

    # def connect(self, port) -> bool:
    #     baud_rate    = self.baud_rate
    #     time_to_wait = self.time_to_wait
    #     self.ser     = serial.Serial(port=port, baudrate=baud_rate, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
    #             bytesize=serial.EIGHTBITS, timeout=time_to_wait)
    #     if not self.ser:
    #         print("Can't connect to |%s|" % (port))
    #         return False
    #     print("Connected to |%s|" % (port) )
    #     self.connected = True
    #     return True

    # untested reading
    def read_serial(self) -> str:
        # return self.link.read_all()
        return self.link.available()

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
            if self.link:
                self.link.close()
            else:
                print("no open link found")

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

    teensy1 = Arduino(findusbport_hwid="16C0:0483")
    # teensy1 = Arduino(port="COM9")

    teensy1.connect()
    # import time
    # time.sleep(1)
    # print(teensy1)
    teensy1.send_to_arduino(data_list)
    # print(teensy1)
    teensy1.disconnect()
    # print(teensy1.link) # this is false if no link exists
    # print(teensy1)
    # print(teensy1.data_list)
    # print(teensy1.rec_data_list)

# def findusbport_hwid(hardwareID="16C0:0483")-> str:
#     hardwareID = "(?i)" + hardwareID  # forces case insensitive
#     comport_list = []
#     if len(comport_list) == 0:
#         comport_list = []
#         for port in serial.tools.list_ports.grep(hardwareID):
#             comport_list.append(port[0])
#     return comport_list