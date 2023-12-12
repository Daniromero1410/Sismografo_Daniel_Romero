#Prueba 1 Sismografo
import serial
import matplotlib.pyplot as plt
import time

ser = serial.Serial('COM3', 9600)

x_values = []
y_values = [] 
z_values = []

is_loading = True
is_graph_visible = False
start_time = time.time() 

while True:

    if is_loading:
        # Pantalla de carga 
        plt.clf()
        plt.title("Cargando", fontsize=30)
        plt.draw()
        plt.pause(0.001)

        # Verificar si ha pasado 1 segundo
        if time.time() - start_time >= 1:
            is_loading = False
            is_graph_visible = True

    if is_graph_visible:
        # Leer datos del puerto serial
        data = ser.readline().decode('utf-8').rstrip()
        
        if data:
            # Extraer valores de X, Y, Z
            x, y, z = data.split(",")
            
            # Convertir a float
            x = float(x[2:])  
            y = float(y[2:])
            z = float(z[2:])
            
            # Mapear al rango del gráfico  
            x = (x + 80) / 160 * 100
            y = (y + 80) / 160 * 100 
            z = (z + 80) / 160 * 100
            
            # Guardar para graficar
            x_values.append(x) 
            y_values.append(y)
            z_values.append(z)

            # Graficar
            plt.clf()
            plt.title("SISMOGRAFO FISICA DE ONDAS UDES")
            plt.plot(x_values, 'b')
            plt.plot(y_values, 'g') 
            plt.plot(z_values, 'r')
            plt.ylim(0, 100)
            plt.draw()
            plt.pause(0.001)
            
ser.close()
