from smbus2 import SMBus
from registers import *
import time

i2cbus = SMBus(1)



def write_reg(reg, mask, bits, start_pos):
    write_bits = i2cbus.read_byte_data(DEF_ADDR, reg)
    write_bits &= mask
    write_bits |= (bits << start_pos)
    i2cbus.write_byte_data(DEF_ADDR, reg, write_bits)

def enable_freq_track(enable):
    write_reg(TOP_CFG1, 0xF7, enable, 3)

def set_operation_mode(mode):
    write_reg(TOP_CTL1, 0xF8, mode, 0) 
    time.sleep(1)

def set_actuator_type(actuator):
    write_reg(TOP_CFG1, 0xDF, actuator, 5)

def set_actuator_abs_volt(abs_volt):
    if abs_volt < 0 or abs_volt > 6:
        return False
    abs_volt /= (23.4 * pow(10,-3))
    print(np.uint8(abs_volt))
    # write_reg(ACTUATOR2, 0x00, np.uint8(abs_volt), 0)

def set_actuator_nom_volt(nom_volt):
    if nom_volt < 0 or nom_volt > 3.3:
        return False
    nom_volt /= (23.4 * pow(10,-3))
    # write_reg(ACTUATOR2, 0x00, np.uint8(nom_volt), 0)

def set_actuator_curr_max(curr_max):
    if curr_max < 0 or curr_max > 300:
        return False
    curr_max = (curr_max-28.6)/7.2
    # write_reg(ACTUATOR3, 0xE0, np.uint8(nom_volt), 0)

# def set_actuator_impedance(impedance):
# def set_actuator_lra_freq(lra_freq):

# def set_default_motor():
#     motor_type = LRA_TYPE
#     nom_volt = 2.5
#     abs_volt = 2.5
#     curr_max = 165.4 # TODO determine whether we should lower this
#     impedance = 13.8
#     lra_freq = 170

#     set_actuator_type(motor_type)
#     set_actuator_abs_volt(abs_volt)
#     set_actuator_nom_volt(nom_volt)
#     set_actuator_curr_max(curr_max)
#     set_actuator_impedance(impedance)
#     set_actuator_lra_freq(lra_freq)

def set_vibrate(val):
    write_reg(TOP_CTL2, 0x00, val, 0)

def setup_motor():
    enable_freq_track(False)
    set_operation_mode(1)# set to DRO mode

def vibrate(pwr, dur):
    set_vibrate(pwr)
    time.sleep(dur)
    set_vibrate(0)


if __name__ == '__main__':
    res = i2cbus.read_byte_data(DEF_ADDR, CHIP_REV_REG)
    enable_freq_track(False)
    set_operation_mode(1)# set to DRO mode
    set_vibrate(50)
    time.sleep(0.1)
    set_vibrate(0)
    print(hex(res))



# def set_actuator_type(motor_type):
# def set_actuator_abs_volt(abs_volt):
# def set_actuator_nom_volt(nom_volt):
# def set_actuator_curr_max(curr_max):
# def set_actuator_impedance(impedance):
# def set_actuator_lra_freq(lra_freq):