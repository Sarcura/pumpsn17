from arduino import Arduino
class Solenoids(Arduino):
  # constructor method
  def __init__(self, findusbport_hwid=None, port=None):
    super().__init__(findusbport_hwid, port)
    # dict for saving solenoid values:
    # self.name = "Solenoids"
    self.nr_of_solenoids = 8
    self.create_solenoids()

  def create_solenoids(self):
    self.data_list = [0] * self.nr_of_solenoids

class Steppermotors(Arduino):
  # dict for saving motor values:
  def __init__(self, max_speed = 15000, sw_endstop = 1100000, findusbport_hwid=None, port=None):
    super().__init__(findusbport_hwid, port)
    self.data_dict = {"motor0_enable": 0, "motor0_direction": 0, "position_1": 100000, "stepspeed_1": 0, 
        "motor1_enable": 0, "motor1_direction": 0, "position_2": 100000, "stepspeed_2": 0, 
        "motor2_enable": 0, "motor2_direction": 0, "position_3": 100000, "stepspeed_3": 0,
        "motor3_enable": 0, "motor3_direction": 0, "position_4": 100000, "stepspeed_4": 0}
    # additional values for motor control
    self.sw_endstop = sw_endstop
    self.max_speed = max_speed

if __name__ == "__main__":
  sol = Solenoids()
  stp = Steppermotors(findusbport_hwid="16C0:0483")
  
  # method calling
  print(stp.sw_endstop)
  print(sol.data_list)
  sol.nr_of_solenoids = 10
  sol.create_solenoids()
  print(sol.data_list)