from serial.tools import list_ports
import serial
import time
import csv

#find the port corresponding to the Arduino
ports = list_ports.comports()
for port in ports: print(port)

#setup the file for saving voltage data from the accel/Arduino
f=open("data.csv","w",newline='')
f.truncate()

serialCom = serial.Serial('COM5',115200) #ENSURE the correct COM#

#Reset the arduino
serialCom.setDTR(False)
time.sleep(1)
serialCom.flushInput()
serialCom.setDTR(True)

#read from the Arduino
kmax=2000 #number of data points to record
#kmax* sampling rate in millisec delay = total time of data recorded
for k in range(kmax):
    try:
        #read a line of data
        s_bytes = serialCom.readline()
        #Decode binary
        decoded_bytes = s_bytes.decode("utf-8").strip('\r\n')
        #print(decoded_bytes)
        
        #parse lines
        if k==0:
            values = [x for x in decoded_bytes.split(",")]
        else:
            values = [float(x) for x in decoded_bytes.split()]
        print(values)
        
        writer = csv.writer(f,delimiter=",")
        writer.writerow(values)
        
        
    except:
        print("ERROR. Line was not recorded.")

f.close() #close csv file



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#import data using padas
data = pd.read_csv("data.csv",skiprows=1)
data.columns = ["time", "accel-x", "accel-y", "accel-z"]    #using three channels
# data.columns = ["time", "accel-x"]                        #using one channel
# print(data)

#retrieve data columns
D=data.to_numpy();
time=(D[:,0])/1000000       #Arduino prints time in micro-second
x_accel=D[:,1]
y_accel=D[:,2]
z_accel=D[:,3]


signal=(x_accel**2)**0.5    #sum y and z for rms in the future

# first method of removing dc component.
i=1
dc_component=[]
for i in range(1,10):
    dc_component.append(signal[i])

signal=x_accel-np.average(dc_component)

#setup doesn't provide data with uniform time-interval
#create an array of all successive time steps to see the spread later
i=1
delta_t=[]
#find the average time step in the array 'time'
for i in range(1,len(time)):
    delta_t.append(time[i]-time[i-1])

dt=np.average(delta_t)  #average time step
fs=1/dt                 #sampling frequency
N=len(time)             #number of samples
f_step=fs/N             #req interval

freq=np.linspace(0,(N-1)*f_step,N) #construct the frequency array


# time=np.linspace(0,(N-1)*dt,N)    #Test time array
# y=1*np.sin(2*np.pi*1*time)        #Test sine signal
x=np.fft.fft(signal)                #perform a fast fourier transform
x_mag = np.abs(x)/N                 #obtain the magnitude of the transform

freq_plot=freq[0:int(N/2+1)]
x_mag_plot=2*x_mag[0:int(N/2+1)] #enter, Nyquist
x_mag_plot[0]=x_mag_plot[0]/2    #DC component does not need to be multiplied by 2

# plot
fig,[ax1,ax2] = plt.subplots(figsize=(7.5,5),nrows=2,ncols=1,constrained_layout=True)
ax1.plot(time,signal)
ax1.set_title('Time History')
ax1.set_xlabel('time(s)')
ax1.set_ylabel('Voltage(V)')
# plt.xlim([min(time),max(time)])
ax2.plot(freq_plot,x_mag_plot)
ax2.set_title('Frequency Spectrum')
ax2.set_xlabel('Frequency(Hz)')
ax2.set_ylabel('Amplitude')
plt.show()
