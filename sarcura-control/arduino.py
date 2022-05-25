import datetime
from itertools import tee
import numpy as np
from pySerialTransfer import pySerialTransfer as txfer
import logging
# please make sure to pip install pySerialTransfer==1.2
# connection will not work with pySerialTransfer==2.0
# requirement: pip install pyserial (works with 3.4 and most likely newer but not much older versions)
# on teensy: include "SerialTransfer.h" Version 2.0
# connecting multiple arduinos is not implemented
import serial.tools.list_ports
class Arduino:
    def __init__(self, findusbport_hwid=None, port=None):
        self.hwid = findusbport_hwid  
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
            if len(self.comport_list) > 1:
                logging.info(f"Multiple devies with the same hwid found.")
                self.found_multiple_devices = True # all found devices are stored for later access
                # self.port = comport_list[0] # only takes the first device with the queried hardware id
            else:
                self.found_multiple_devices = False
                logging.info(f"Only one devices with the defined hwid found.")

        else:
            logging.info(f"No hwid defined.")
            self.comport_list = list(serial.tools.list_ports.comports())
            # self.port = self.comport_list[0]
        logging.info(f"List of devices: {self.comport_list}")
        try:
            logging.info(f"List of devices: {self.port}")
        except:
            pass


    def connect(self):
        try:
            logging.info(f"Connecting to {self.port}")
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
            logging.info(f"Disconnecting {self.port}")
            self.link.close()
            self.link = False
            # self.connected = False
        except:
            import traceback
            traceback.print_exc()

    def search_arduinos():
        # not implemented, hwid unknown
        pass

    def send_to_arduino(self, data_list):
        try:
            # reset send_size
            send_size = 0
            # Send a list
            logging.info(f"Data list sent:     {data_list}")
            self.data_list = data_list
            data_listsize = self.link.tx_obj(data_list)
            send_size += data_listsize
            
            # Transmit all the data to send in a single packet
            self.link.send(send_size)
            logging.info("Message sent...")
            
            # Wait for a response and report any errors while receiving packets
            while not self.link.available():
                if self.link.status < 0:
                    if self.link.status == -1:
                        logging.info('ERROR: CRC_ERROR')
                    elif self.link.status == -2:
                        logging.info('ERROR: PAYLOAD_ERROR')
                    elif self.link.status == -3:
                        logging.info('ERROR: STOP_BYTE_ERROR')

            # Parse response list
            ###################################################################
            self.rec_data_list  = self.link.rx_obj(obj_type=type(data_list),
                                        obj_byte_size=data_listsize,
                                        list_format='i')

            logging.info(f"Data list received: {self.rec_data_list}")
            # logging.info(f'SENT: {self.data_list}')
            # logging.info(f'RCVD: {self.rec_data_list}')

        except:
            import traceback
            traceback.print_exc()
            if self.link:
                self.link.close()
            else:
                logging.info("no open link found")

if __name__ == "__main__":
    comport = 'COM5'
    # import itertools
    # bin_list = [0,0,0,0]
    # for item in itertools.permutations('1100'):
    #     logging.info(''.join(item))
    #     bin_list.append(item)

    # logging.info(bin_list)

    teensy1 = Arduino(findusbport_hwid="16C0:0483")
    # teensy1 = Arduino(port="COM9")

    teensy1.connect()
    import time

    # while True:
    #     data_list = [0,0,0,0,0,0,0,1]
    #     teensy1.send_to_arduino(data_list)

    while True:
        # data_list = [0,0,0,0,1,1,1,1]
        # data_list = [0,0,0,0,0,0,0,1]
        data_list = [0,0,0,0,0,0,0,1]

        teensy1.send_to_arduino(data_list)
        time.sleep(1)
        # data_list = [1,1,1,1,0,0,0,0]
        # data_list = [1,1,1,1,1,1,1,1]
        # data_list = [0,0,0,0,1,0,0,0]
        data_list = [0,0,0,0,1,0,0,0]
        teensy1.send_to_arduino(data_list)
        time.sleep(1)
    
    def binary_list(n):
        return [[int(j) for j in '{:0{}b}'.format(i, n)] for i in range(n*n-1)]

    newlist = binary_list(8)
    logging.info(f"new list: {newlist}")
    for element in newlist:
        # logging.info(data_list[element])
        logging.info(f"new list: {element}")
        teensy1.send_to_arduino(element)
        time.sleep(1)

    teensy1.disconnect()

    # teensy1.disconnect()

    # logging.info(teensy1.link) # this is false if no link exists
    # logging.info(teensy1)
    # logging.info(teensy1.data_list)
    # logging.info(teensy1.rec_data_list)

# def findusbport_hwid(hardwareID="16C0:0483")-> str:
#     hardwareID = "(?i)" + hardwareID  # forces case insensitive
#     comport_list = []
#     if len(comport_list) == 0:
#         comport_list = []
#         for port in serial.tools.list_ports.grep(hardwareID):
#             comport_list.append(port[0])
#     return comport_list



    # def binary_list(n):
    #     return [[int(j) for j in '{:0{}b}'.format(i, n)] for i in range(n*n-1)]

    # newlist = binary_list(8)
    # logging.info(f"new list: {newlist}")
    # for element in newlist:
    #     # logging.info(data_list[element])
    #     logging.info(f"new list: {element}")
    #     teensy1.send_to_arduino(element)
    #     time.sleep(1)

    # teensy1.disconnect()