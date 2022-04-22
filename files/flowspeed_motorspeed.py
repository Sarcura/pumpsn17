import math 

def calculate_stepspeed(channel_m_per_s = 1, syringe_diameter = 12.08, channel_area_sqmm = 0.003) -> float:
    # from: https://www.harvardapparatus.com/media/harvard/pdf/Syringe%20Selection%20Guide.pdf
    syringe_area_sqmm = (syringe_diameter**2)/4*math.pi
    print(f"syringe area [mm²]: {syringe_area_sqmm}")

    # equation of continuity, valid for incompressible fluids, the flow rate stays the same no matter the cross section: Q1=Q2  A1v1=A2v2
    # A1 = syringe_area_sqmm, A2 = channel_area_sqmm
    syringe_m_second = float(channel_m_per_s)*float(channel_area_sqmm)/float(syringe_area_sqmm)
    print(f"water movement in syringe [m/s]: {syringe_m_second}")

    # 0.317 mm per thread (80 thread per inch), 6400 steps per revolution
    microstep_in_m = 0.317/6400/1000
    # stepspeed = 528 # pulses per second
    stepspeed =  syringe_m_second/microstep_in_m
    stepspeed =  int(round(stepspeed))
    print(f"motor stepspeed: {stepspeed}")
    return stepspeed
    
if __name__ == '__main__':
    print(calculate_stepspeed(1,12.08,0.03*0.1))