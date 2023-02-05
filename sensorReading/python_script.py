import serial 
import time
import matplotlib.pyplot as plt
import csv
def readSerial(COMport, baudrate, timestamp=False):
    fileName = "rpm-data.csv"
    file = open(fileName, "a")      # append to existing file 
    print(f"{fileName} file is created")
    ser = serial.Serial(COMport, baudrate, timeout=1)
    time.sleep(2)
    rpm_data = []

    while True:
        data = ser.readline().decode("utf-8").strip()
        print(type(data), data)

        if data and timestamp:
            timestamp = time.strftime('%H:%M:%S')
            print(f"{timestamp} > {data}")
        elif data:
            print(data)
        rpm_data.append(data)
    ser.close()

    # plot the data
    plt.plot(rpm_data)
    plt.xlabel("Time")
    plt.ylabel("Sensor Reading")
    plt.title("Sensor reading vs Time")
    plt.show()

    # create csv
    # with open(fileName, 'w', encoding='utf-8',errors='ignore') as f:
    with open(fileName, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(rpm_data)
    print(f"Data has been written to {fileName}!")
    file.close()

if __name__ == "__main__":
    readSerial('COM5', 9600, True)