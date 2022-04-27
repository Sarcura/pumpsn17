import math 

def calculate_stepspeed(channel_m_per_s = 1, syringe_diameter = 12.08, channel_area_sqmm = 0.003) -> float:
    # from: https://www.harvardapparatus.com/media/harvard/pdf/Syringe%20Selection%20Guide.pdf
    syringe_area_sqmm = (syringe_diameter**2)/4*math.pi
    print(f"syringe area [mm²]: {syringe_area_sqmm}")

    # equation of continuity (Venturi-effect), valid for incompressible fluids, the flow rate stays the same no matter the cross section: Q1=Q2  A1v1=A2v2
    # A1 = syringe_area_sqmm, A2 = channel_area_sqmm
    syringe_m_second = float(channel_m_per_s)*float(channel_area_sqmm)/float(syringe_area_sqmm)
    print(f"water movement in syringe [m/s]: {syringe_m_second}")

    # p1+1/2*ρ*V1 = p2+1/2*ρ*V2
    # V1*A1 = V2*A2
    # m = 
    # F = m*a
    # https://www.youtube.com/watch?v=xXaE54bl3yI 3.1 Pressure in a Syringe
    # calculate F from stepper motor?
    # https://www.pololu.com/blog/10/force-and-torque
    # https://forum.arduino.cc/t/stepper-motor-basics/275223
    p1 = 1000 #?? pressure = force ÷ area, furthermore: F = m*a = 
    ρ = 1000 #kg/m³ @ 4°C
    p2 = p1 + 1/2*ρ*syringe_m_second - 1/2*ρ*channel_m_per_s
    print(f"pressure 1: {p1}")
    print(f"pressure 2: {p2}")

    # 0.317 mm per thread (80 thread per inch), 6400 steps per revolution
    microstep_in_m = 0.317/6400/1000
    # stepspeed = 528 # pulses per second
    stepspeed =  syringe_m_second/microstep_in_m
    stepspeed =  int(round(stepspeed))
    print(f"motor stepspeed: {stepspeed}")
    return stepspeed
    
if __name__ == '__main__':
    print(calculate_stepspeed(1,12.08,0.03*0.1))