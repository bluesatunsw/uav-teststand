from threading import Thread
import serial 
import struct
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation 
import collections
import pandas as pd
import os
import csv

class serialPlot:
    def __init__(self, comPort="COM5", baudrate =9600, numBytes = 4, max_entries = 100):
        self.port = comPort
        self.baud = baudrate
        self.serialData = bytearray(numBytes)           # create an array of numbyte size and initialise with null bytes (utf-16)
        self.thread = None
        self.running = True                             # Serial port is running
        self.isReceiving = False                        # Start receiving serial raw data
        self.maxLen = max_entries
        self.rpmValues = collections.deque([0.0]*max_entries, maxlen=max_entries)
        self.forceValues = collections.deque([0.0]*max_entries, maxlen=max_entries)
        self.csvData = pd.DataFrame(columns=["RPM", "Thurst"])
        self.startNullReceive = False
        self.endNullReceive = False
        print("Connecting to: " + str(comPort) + " at "+ str(baudrate) + " Baud.")
        try: 
            # reference to the successful serial connection
            self.serialConnection = serial.Serial(comPort, baudrate, timeout=1)
            print("Successful connection!")
        except:
            print("Failed to connect with " + str(comPort)  + " at "+ str(baudrate) + " Baud.")

    def update(self):
        # append value for rpm and thurst force 
        rpm, = struct.unpack("i", self.serialData[:4])
        force, = struct.unpack("i", self.serialData[4:])
        print(rpm, force)
        self.rpmValues.append(rpm)            # using float for 4 bytes rpm 
        self.forceValues.append(force)

        a0.set_data(self.rpmValues, self.forceValues)
        # self.csvData.append([{"RPM": self.rpmValues[-1], "Thurst": self.forceValues[-1]}], ignore_index=True)
        new_row = pd.Series({"RPM": self.rpmValues[-1], "Thurst": self.forceValues[-1]})
        self.csvData = pd.concat([self.csvData, new_row], ignore_index=True)
        
    def readSerial(self):
        if self.thread == None:
            assert(self.startNullReceive==False)
            mes = struct.pack("BB", 0xF0, 0xF0)
            print(mes)
            print(struct.pack("BB", 1, 2))
            self.serialConnection.write(struct.pack('bb', 1, 2))
            # bytes("s", 'utf-8')
            # self.serialConnection.write(0)

            while True:
                # read up to len(b) bytes into bytearray b 
                s = self.serialConnection.readline()
                if s == "":
                    print("What is worng!")
                print(s)
                time.sleep(.5)
            # print(rbyte)


            # self.thread = Thread(target=self.readThread)
            # self.thread.start()
            # # Wait until isReceiving live 
            # while self.isReceiving != True:
            #     time.sleep(0.1)   


    def readThread(self):
        print("readThread!")
        self.serialConnection.flushInput()

        time.sleep(1)           # time for retrieving data 

        while (self.running):

            print("Running!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            self.serialConnection.readinto(self.serialData)
            print(self.serialData)
            # read up to len(b) bytes into bytearray b 
            self.serialConnection.readinto(self.serialData)
            if self.startNullReceive == True:
                # this will avoid storing the useless nulls 
                self.isReceiving = True
            if bytes(self.serialData) == 0x0000:
                print("I got null!")
                if self.startNullReceive == False:
                    print("Start receiving!!!")
                    self.startNullReceive = True
                elif self.endNullReceive == False:
                    self.endNullReceive = True
                
    def close(self):
        self.running = False
        self.thread.join()
        self.serialConnection.flush()
        self.serialConnection.close()
        print("Exited....")

        path = os.getcwd() + "\\data.csv"
        if os.path.exists(path):
            # append dataframe to csv file 
            self.csvData.to_csv(path, mode='a', index=False, header=False)
        else:
            # else create csv file from dataframe 
            self.csvData.to_csv(path)
        # print message
        print("Data appended successfully.")

def main():
    comPort = "COM5"
    baudrate = 115200
    numBytes = 2                
    max_entries = 100
    ser = serialPlot(comPort, baudrate, numBytes,max_entries)
    ser.readSerial()

    # strat plot 
    # fig = plt.figure()
    # min_rpm = 0
    # max_rpm = 2000
    # min_thurst = 0
    # max_thurst = 2000
    # ax = plt.axes(xlim=(min_rpm, max_rpm), ylim=(min_thurst, max_thurst))
    # ax.set_title("RPM vs Thurst Force produced")
    # ax.set_xlabel("RPM values")
    # ax.set_ylabel("Force produced")

    # line = ax.plot([], [])
    # anim = animation.FuncAnimation(fig, ser.update, fargs=(line), interval=30)
    # plt.show()
    # ser.close()
    
if __name__ == "__main__":
    main()
