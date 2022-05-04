import math 

def calculate_sorting_parameters(channel_m_per_s_total = 1.5, sample_to_sheath_ratio = 0.1, channel_area_mm2 = 0.003,
        cell_concentration_per_ml = 1e06, cell_volume_ml = 10.5,
        sorting_speed = 2000, max_sorting_speed = 5000, maximum_sorting_time = 4,
        calculate_medium_for_sorting_speed = True):

    # internally, everything is calculated for the real cell concentration with sheath and the cell concentration in the sample+sheath
    cell_volume_ml = cell_volume_ml/sample_to_sheath_ratio
    cell_concentration_per_ml = sample_to_sheath_ratio*cell_concentration_per_ml

    channel_m_per_s = channel_m_per_s_total # the total m/s of the sample are channel speed 
    channel_m3_per_s = channel_m_per_s*(channel_area_mm2*1e-06)
    channel_l_per_s = channel_m3_per_s*1e03
    channel_ml_per_s = channel_l_per_s*1e03
    channel_µl_per_s = channel_l_per_s*1e06
    total_sorting_time = cell_volume_ml/channel_ml_per_s/3600 # if volume is not optimized, time is longer/shorter than needed 
    print(f"total volume to run trought machine: [µl/min]: {cell_volume_ml:.2f}")
    print(f"total estimated time [h]: {total_sorting_time:.2f}")
    print(f"channel volume: [µl/min]: {channel_µl_per_s:.2f}")
    print(f"sample to sheath ratio (true for speed and volume) {sample_to_sheath_ratio:.2f}")

    cell_concentration_per_µl = cell_concentration_per_ml*1e-03 # smaller fraction = less cells/µl
    cell_per_s = cell_concentration_per_µl*channel_µl_per_s # cell_per_s is equal to the needed (!) sorting frequency
    total_cells = cell_concentration_per_ml*cell_volume_ml

    # print(cell_concentration_per_µl)
    # print(channel_µl_per_s)
    # print(sorting_speed)
    # print(cell_per_s)

    # calculate the sorter capacity #! needs to be triple checked, should be correct
    max_cell_concentration_per_ml = sorting_speed/(channel_µl_per_s*1e03) # needed for ml 
    max_cell_concentration_per_ml_max_speed = max_sorting_speed/(channel_µl_per_s*1e03) # needed for ml
    print(f"The cell concentration before dilution in the sample stream is {cell_concentration_per_ml/sample_to_sheath_ratio:.2e} cells per ml")
    print(f"The cell concentration before dilution in the channel is {cell_concentration_per_ml:.2e} cells per ml")
    print(f"The max cell concentration per ml for a sorting speed of {sorting_speed} Hz is: {max_cell_concentration_per_ml/sample_to_sheath_ratio:.2e} cells per ml")
    print(f"The max cell concentration per ml for a sorting speed of {max_sorting_speed} Hz is: {max_cell_concentration_per_ml_max_speed/sample_to_sheath_ratio:.2e} cells per ml")
    
    # sorter_cap_factor = cell_concentration_per_ml/max_cell_concentration_per_ml
    sorter_cap_factor = cell_per_s/sorting_speed
    print(f"Sorter capacity factor: {sorter_cap_factor:.2f}")

    captured_events = cell_per_s-sorting_speed
    if sorter_cap_factor <= 1:
        print(f"All cells passing by in a speed of {cell_per_s:.1f} [cells/s] and will be sorted by {sorting_speed} Hz. ✓")
        print(f"{captured_events*-1:.1f} [cells/s] more could be measured.")
    else:
        print(f"All cells passing by in a speed of {cell_per_s:.1f} [cells/s] and will be sorted by {sorting_speed} Hz. ✘")
        print(f"This would lead to {captured_events:.1f} [cells/s] missed.")

    if calculate_medium_for_sorting_speed is True:
        # according to selected sorting speed, calculate if more medium is needed:
        # it could also do the same for max conc max speed
        cell_volume_additional_ml = (sorter_cap_factor*cell_volume_ml)-(cell_volume_ml)
        if cell_volume_additional_ml > 0:
            print(f"Cell volume additionaly needed to sort with {sorting_speed} Hz: {cell_volume_additional_ml*sample_to_sheath_ratio:.1f} ml")
            print(f"Addtionally {cell_volume_additional_ml*(1-sample_to_sheath_ratio):.2f} ml of sheath will be needed.")
            print(f"Sorting a cell concentration of {cell_concentration_per_ml/sorter_cap_factor/sample_to_sheath_ratio:.2e} / ml with a volume of {cell_volume_ml*sample_to_sheath_ratio} ml")
            print(f"    equaling to {total_cells:.2e} total cells.")
        # cell_volume_additional_ml = 0
        else:
            print(f"No additional dilution needed. {cell_volume_additional_ml*-1*sample_to_sheath_ratio:.2f} ml of medium could have been saved.")
            print(f"Addtionally {cell_volume_additional_ml*-1*(1-sample_to_sheath_ratio):.2f} ml of sheath could have been saved.")
            print(f"Sorting a cell concentration of {cell_concentration_per_ml/sample_to_sheath_ratio:.2e} / ml with a volume of {cell_volume_ml*sample_to_sheath_ratio:.1f} ml")
            print(f"    equaling to {total_cells:.2e} total cells.")
        # print(f"cell events: [cell/min]: {cell_per_s}")
        cell_per_s = cell_concentration_per_µl/sorter_cap_factor*channel_µl_per_s # calculated anew with the new concentration -> is now the selected
        sorting_speed = cell_per_s # ! sorting time should go up if cells are in lower dilution calculated in calculate_medium_for_sorting_speed
        print(sorting_speed)
        total_sorting_time = total_cells/sorting_speed/3600 # calculate from seconds to hours
    else:
        print("No media optimization.")
        cell_volume_additional_ml = 0



    # ! sorting time should go up if cells are in lower dilution calculated in calculate_medium_for_sorting_speed

    

    print(f"Sorting will be completed in {round(total_sorting_time, 2)} hours.")
    sorting_percentage = maximum_sorting_time/(total_sorting_time)*100# for 4 hours maximum time
    if total_sorting_time > maximum_sorting_time:
        print(f"Complete sample sorting cannot be completed under {maximum_sorting_time} hours.")
        print(f"{sorting_percentage:.1f}% of the sample could be sorted in time.")
    # ! sorting time should go up if cells are in lower dilution
    # total_sorting_time = 0

    return round(channel_µl_per_s, 5), round(cell_per_s), round(total_sorting_time, 2), round(cell_volume_additional_ml*sample_to_sheath_ratio, 3)

def calculate_stepspeed(channel_m_per_s = 1, syringe_diameter = 12.08, channel_area_mm2 = 0.003):
    # from: https://www.harvardapparatus.com/media/harvard/pdf/Syringe%20Selection%20Guide.pdf
    syringe_area_mm2 = (syringe_diameter**2)/4*math.pi
    # print(f"syringe area [mm²]: {syringe_area_mm2}")

    # equation of continuity (Venturi-effect), valid for incompressible fluids, the flow rate stays the same no matter the cross section: Q1=Q2  A1v1=A2v2
    # A1 = syringe_area_mm2, A2 = channel_area_mm2
    syringe_m_second = float(channel_m_per_s)*float(channel_area_mm2)/float(syringe_area_mm2)
    print(f"water movement in syringe [m/s]: {syringe_m_second:.3e}")

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
    # print(f"pressure 1: {p1}")
    # print(f"pressure 2: {p2}")

    # 0.317 mm per thread (80 thread per inch), 6400 steps per revolution
    microstep_in_m = 0.317/6400/1000
    # stepspeed = 528 # pulses per second
    stepspeed =  syringe_m_second/microstep_in_m
    stepspeed =  int(round(stepspeed))
    # print(f"motor stepspeed: {stepspeed}")
    return stepspeed
    
if __name__ == '__main__':
    # print(calculate_stepspeed(channel_m_per_s= 1/2, syringe_diameter = 12.08, channel_area_mm2 = 0.03*0.1))

    print(calculate_sorting_parameters(channel_m_per_s_total = 2, sample_to_sheath_ratio = 1/10, channel_area_mm2 = 0.03*0.1,
        cell_concentration_per_ml = 2*1e6, cell_volume_ml = 1, sorting_speed = 1500, max_sorting_speed = 5000,
        maximum_sorting_time = 4, calculate_medium_for_sorting_speed = True))
