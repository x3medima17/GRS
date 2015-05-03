import serial
from websocket import create_connection
import time
import sys
 



def init(ser):
    print "------------------------------------------"
    print "Init"
    usart = ser.readline()
    if not usart:
        print "Communication failed (USART)."
        sys.exit(1)
    print "USART init done."

    for i in range(0, 4):
        initData = ser.readline()
        if not initData:
            print "Sensor initialization failed."
            sys.exit(1)
        else:
            print initData
    print "Initialization done."
    print "------------------------------------------"
 
def split(lst,size):
        return [lst[i:i+size] for i  in range(0, len(lst), size)]
 
def getdata(ser):
        filter_N =      5
        frequency = 600 * filter_N
        period = 1.0/frequency
        total = 0
        fail = 0
        rate = 0
        SAMPLES = 1000;
        
        
        f1 = open("s1_raw.txt", "w")
        f2 = open("s2_raw.txt", "w")
        f3 = open("s3_raw.txt", "w")
        f4 = open("s4_raw.txt", "w")
        f5 = open("s5_raw.txt", "w")
        f6 = open("s6_raw.txt", "w")

        ser.write("G")
        print "Debug getdata"
        for i in range(0, SAMPLES):
                tick = time.time()
                sums = [0.0] * 18
                curr_fails = 0
 
                ser.write("G")       
                data = ser.readline().replace("\n","").replace("\r","")
                # print data,data[0],data[len(data)-1]
                if not data or data[0] != 's' or data[len(data)-1] != 'f':
                        fail+=1
                        curr_fails += 1
                        print "Check sensors or just late data"
                        print data
                        continue
                data = data[1:-1]
                print data
                print "Fail rate: %s\n" % rate
                data.replace(" ", "\t");
                sensorData = data.split(';')
                print sensorData
                print "Frequ: %s" % (1.0/ (time.time()-tick+0.0000001))
                tick = time.time()

                f1.write(sensorData[0] + "\n")
                f2.write(sensorData[1] + "\n")
                f3.write(sensorData[2] + "\n")
                f4.write(sensorData[3] + "\n")
                f5.write(sensorData[4] + "\n")
                f6.write(sensorData[5] + "\n")
    
        f1.close()
        f2.close()
        f3.close()
        f4.close()
        f5.close()
        f6.close()
        ser.write("S")
     
def calibrate(ser):
        filter_N =      5
        frequency = 600 * filter_N
        period = 1.0/frequency
        total = 0
        fail = 0
        rate = 0
        calibr = ""
    

        
        f_calibrate = open("calibration.txt", "r").readlines()
        #print f_calibrate

        ser.write("C")
        print "Debug calibrate"
        data = ser.readline();
         # print data,data[0],data[len(data)-1]
        if not data: 
                print "Check sensors or just late data"
        print data
                
        print "Calibrated data from file:"
        for line in f_calibrate:
                calibr = line
                print "calibration=", calibr
                calibr = calibr.replace("\n", "")
                calibr = calibr.replace(" ", "")
                ser.write(calibr+"\n\r")
                data = ser.readline()
                print data
                print "----------------------"
        print "All data sent"
        ser.write("S")


 
def senddata(ser,server = "188.166.48.28"):
        filter_N =      5
        frequency = 600 * filter_N
        period = 1.0/frequency
        total = 0
        fail = 0
        rate = 0

        try:
                ws = create_connection("ws://"+server+":9090/ws")
        except:
                print "Cannot connect to WebSocket Server"
                sys.exit(2)
        #ws.send("Hello from Win7 !")
 
        while(1):
                tick = time.time()
                sums = [0.0] * 18
                curr_fails = 0
 
                ser.write("S")
                data = ser.readline().replace("\n","").replace("\r","")
                # print data,data[0],data[len(data)-1]
                if not data or data[0] != 's' or data[len(data)-1] != 'f':
                        fail+=1
                        curr_fails += 1
                        print "Check sensors or just late data"
                        continue
                data = data[1:-1]
       
                print data
                print "Fail rate: %s\n" % rate
                # print fail,total,rate
 
                ws.send(data)
 
                print "Frequ: %s" % (1.0/ (time.time()-tick+0.0000001))
                tick = time.time()

        ws.close()

def testcalibration(ser):
    calibrate(ser)
    senddata(ser)

if __name__ == "__main__":
    argument = sys.argv[2]
    
    comp_port = sys.argv[1]

    try:
        server = sys.argv[3]
    except:
        server = "188.166.48.28"

    # Init
    try:
        ser = serial.Serial(comp_port,19200,timeout=0.1)
    except:
        print "Cannot open COM Port"
        sys.exit(1)
    
    init(ser);

    if argument == "S":
        senddata(ser,server)
    elif argument == "T":
        testcalibration(ser)
    elif argument == "C":
        calibrate(ser)
    elif argument == "G":
        getdata(ser)
    else:
        print "Please specify argument"
    ser.close()