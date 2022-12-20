import psutil, wmi, os
from PyQt5 import QtWidgets, QtCore, QtGui

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Establece el fondo como transparente
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Crea un objeto QIcon a partir de un archivo de imagen
        icon_path = os.path.join(os.path.dirname(__file__), 'widget_icon.ico')
        icon = QtGui.QIcon(icon_path)

        # Establece el icono de la ventana
        self.setWindowIcon(icon)

        # Crea una etiqueta para la temperatura
        self.label = QtWidgets.QLabel()
        self.label.setAlignment(QtCore.Qt.AlignLeft)
        self.label.setStyleSheet('color: #ffa500; font-size: 12pt;')

        # Crea un diseño y añade la etiqueta
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label)

        # Establece el temporizador para actualizar la temperatura cada 1 segundo
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_temp)
        self.timer.start(1000)

        # Establece un flags a la ventana para que esté siempre por encima de las demás
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # Elimina el marco de la ventana
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        # Establece el tamaño y la posición de la ventana
        self.resize(200, 100)
        self.move(0, 970)

    def update_temp(self):
        # Obtiene las temperaturas de la GPU y CPU en un diccionario
        temps = get_temps()

        # Obtiene el uso de la RAM
        memoryUsage = get_ram_usage()

        if gpuTemp:
            # Establece la etiqueta para el texto de la temperatura
            self.label.setText(f'GPU: {str(temps["GPU"])[:-2]}ºC\nCPU: {str(temps["CPU"])[:-2]}ºC\nRAM: {memoryUsage:.0f} MB')

def get_temps():
    try:
        # Ejecuta el comando WMI para listar los sensores y obtiene el resultado
        w = wmi.WMI(namespace="root\OpenHardwareMonitor")
        temperature_infos = w.Sensor()
        
        # Inicializa el diccionario de temperaturas
        temps = {'GPU': None, 'CPU': None}

        # Analiza el resultado filtrando por 'sensor.Name' y 'sensor.SensorType' para encontrar la temperatura
        '''
        Lo ideal para monitorizar es filtrar con 'sensor.Name' y 'sensor.SensorType' especificando
        el sensor exacto y el tipo del mismo como se ve a continuación.
        '''
        for sensor in temperature_infos:
            if sensor.Name == u'GPU Core' and sensor.SensorType == u'Temperature':
                temps['GPU'] = sensor.Value
            elif sensor.Name == u'CPU Package' and sensor.SensorType == u'Temperature':
                temps['CPU'] = sensor.Value
        
        # Devuelve el diccionario con las temperaturas de la GPU y CPU
        return temps
    except Exception as e:
        print(f'Error occurred: {e}')
    return None

def get_ram_usage():
    # Obtiene información sobre la memoria del sistema
    memory_info = psutil.virtual_memory()
    
    # Obtiene la cantidad de memoria usada en bytes
    used_memory = memory_info.used

    # Convierte la memoria a megabytes
    used_memory_mb = used_memory / (1024 ** 2)

    return used_memory_mb

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
