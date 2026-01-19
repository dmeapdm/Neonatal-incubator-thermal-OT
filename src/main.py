import serial
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns
import csv
import os

# ----------------------------
# CONFIGURACIÓN
# ----------------------------
arduino_port = "/dev/ttyUSB0"  # cambiar por tu puerto
baud_rate = 9600
num_sensores = 6
setpoint = 35.0  # Temperatura objetivo de la incubadora

# Archivo CSV para guardar datos
csv_filename = "datos_incubadora.csv"

# ----------------------------
# INICIALIZAR SERIAL
# ----------------------------
ser = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)  # espera que Arduino se reinicie

# ----------------------------
# INICIALIZAR ESTILO Y GRÁFICOS
# ----------------------------
sns.set()  # Aplica estilo seaborn a matplotlib
temps_list = [[] for _ in range(num_sensores)]
tiempos = []
temps_promedio = []

# Gráfico de los 6 sensores
fig1, ax1 = plt.subplots()
lineas = [ax1.plot([], [], label=f"Sensor {i+1}")[0] for i in range(num_sensores)]
linea_setpoint, = ax1.plot([], [], 'k--')
legend_sensores = ax1.legend([...], [...], loc='upper right')
ax1.add_artist(legend_sensores)  # Esto agrega la primera leyenda y permite agregar la segunda
ax1.legend([linea_setpoint], ['Setpoint'], loc='center left', bbox_to_anchor=(-0.15, 0.5))

ax1.set_xlabel("Tiempo (s)")
ax1.set_ylabel("Temperatura (°C)")
ax1.legend()
ax1.grid(True)



# Gráfico de temperatura promedio
fig2, ax2 = plt.subplots()
linea_promedio, = ax2.plot([], [], 'r-', label="Promedio")
ax2.set_xlabel("Tiempo (s)")
ax2.set_ylabel("Temperatura promedio (°C)")
ax2.legend()
ax2.grid(True)

start_time = time.time()



# Texto en la gráfica de los 6 sensores
textos_sensores = [ax1.text(0.8, 0.6 - 0.05*i, '', transform=ax1.transAxes, color='C'+str(i))
                    for i in range(num_sensores)]
#text_setpoint = ax.text(0.8, 0.95, '', transform=ax1.transAxes, color='k')

# Coordenadas en porcentaje del gráfico (0 a 1)
#text_setpoint = ax1.text(0.8, 0.95, '', transform=ax1.transAxes, color='k', fontsize=10, fontweight='bold')
# Texto del setpoint en la esquina superior izquierda
text_setpoint = ax1.text(0.02, 0.95, f"Setpoint: {setpoint:.1f}°C",
                         transform=ax1.transAxes, color='k', fontsize=10, fontweight='bold',
                         verticalalignment='top', horizontalalignment='left')


# Texto en la gráfica de promedio
text_promedio = ax2.text(0.1, 0.95, '', transform=ax2.transAxes, color='r', fontsize=12, fontweight='bold')

# ----------------------------
# FUNCION PARA ACTUALIZAR GRAFICOS
# ----------------------------
def update(frame):
    global temps_list, tiempos, temps_promedio
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        if line:
            try:
                temps = [float(t) for t in line.split(",")]
                tiempo_actual = time.time() - start_time
                tiempos.append(tiempo_actual)
                
                # Actualizar lista de cada sensor
                for i in range(num_sensores):
                    temps_list[i].append(temps[i])
                
                # Calcular y guardar promedio
                promedio = sum(temps)/num_sensores
                temps_promedio.append(promedio)
                
                # Guardar en CSV
                if not os.path.isfile(csv_filename):
                    with open(csv_filename, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(["Tiempo"] + [f"Sensor{i+1}" for i in range(num_sensores)] + ["Promedio"])
                with open(csv_filename, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([tiempo_actual] + temps + [promedio])
                
                # Actualizar gráfico de sensores
                for i, linea in enumerate(lineas):
                    linea.set_data(tiempos, temps_list[i])
                    # Actualizar texto con la última lectura de cada sensor
                    textos_sensores[i].set_text(f"S{i+1}: {temps[i]:.1f}°C")
                #linea_setpoint.set_data(tiempos, [setpoint]*len(tiempos))
                #text_setpoint.set_text(f"Setpoint: {setpoint}°C")
                linea_setpoint.set_data(tiempos, [setpoint]*len(tiempos))
                text_setpoint.set_text(f"Setpoint: {setpoint:.1f}°C")

                ax1.relim()
                ax1.autoscale_view()
                
                # Actualizar gráfico de promedio
                linea_promedio.set_data(tiempos, temps_promedio)
                text_promedio.set_text(f"Promedio: {promedio:.2f}°C")
                ax2.relim()
                ax2.autoscale_view()
                
            except Exception as e:
                print("Error leyendo línea:", line, e)



# ----------------------------
# INICIAR ANIMACION
# ----------------------------
ani1 = FuncAnimation(fig1, update, interval=1000)
ani2 = FuncAnimation(fig2, update, interval=1000)
plt.show()

# ----------------------------
# CERRAR SERIAL AL TERMINAR
# ----------------------------
ser.close()
print("Datos guardados en", csv_filename)
