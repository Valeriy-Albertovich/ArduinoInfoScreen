import os
import serial
import time
import clr

arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
info_list = []  # list with info about hardware
log = ''  # string that is sent to arduino

openhardwaremonitor_hwtypes = [
    'Mainboard', 'SuperIO', 'CPU', 'RAM', 'GpuNvidia', 'GpuAti', 'TBalancer', 'Heatmaster', 'HDD'
]
openhardwaremonitor_sensortypes = [
    'Voltage', 'Clock', 'Temperature', 'Load', 'Fan', 'Flow', 'Control', 'Level',
    'Factor', 'Power', 'Data', 'SmallData'
]


def initialize_openhardwaremonitor():
    dir = os.path.abspath(os.path.dirname(__file__))
    dll_file_name = dir + R'\OpenHardwareMonitorLib.dll'
    clr.AddReference(dll_file_name)

    from OpenHardwareMonitor import Hardware
    handle = Hardware.Computer()
    handle.MainboardEnabled = True
    handle.CPUEnabled = True
    handle.RAMEnabled = True
    handle.GPUEnabled = True
    handle.HDDEnabled = True
    handle.Open()
    return handle


def fetch_stats(handle):
    for i in handle.Hardware:
        i.Update()
        for sensor in i.Sensors:
            parse_sensor(sensor)

        for j in i.SubHardware:
            j.Update()
            for subsensor in j.Sensors:
                parse_sensor(subsensor)


def parse_sensor(sensor):  # CPU usage, CPU temp, RAM usage, GPU temp, GPU usage
    tegL = 'Load'
    tegT = 'Temperature'

    if sensor.Value is None:
        return

    if sensor.SensorType == openhardwaremonitor_sensortypes.index(tegL):  # usage
        type_name = openhardwaremonitor_hwtypes[sensor.Hardware.HardwareType]
        if sensor.Name == 'CPU Total' or sensor.Name == 'Memory' or sensor.Name == 'GPU Core':
            info_list.append(int(sensor.Value))

    if sensor.SensorType == openhardwaremonitor_sensortypes.index(tegT):  # temperatures
        type_name = openhardwaremonitor_hwtypes[sensor.Hardware.HardwareType]
        if sensor.Name == 'CPU Package' or sensor.Name == 'GPU Core':
            info_list.append(int(sensor.Value))


def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data


if __name__ == "__main__":
    time.sleep(5)
    while True:
        HardwareHandle = initialize_openhardwaremonitor()
        fetch_stats(HardwareHandle)
        for i in info_list:
            if i > 99:
                log = log + str(99) + ' '
            elif i == 0:
                log = log + str(1) + ' '
            else:
                log = log + str(i) + ' '
        log = log.rstrip(' ')
        value = write_read(log)
        print(log)
        log = ''
        info_list = []
        time.sleep(10)  # delay between sending log
