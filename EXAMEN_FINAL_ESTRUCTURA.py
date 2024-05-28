import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QTextEdit, QFormLayout, QMessageBox
from PyQt6.QtGui import QPainter, QPen, QBrush
from PyQt6.QtCore import Qt

# Clase Nodo, representa un nodo del árbol
class Nodo:
    def __init__(self, estudiante):
        self.estudiante = estudiante
        self.izquierda = None
        self.derecha = None

# Clase Estudiante para almacenar los detalles del estudiante
class Estudiante:
    def __init__(self, id, nombre, carnet, telefono, correo):
        self.id = id
        self.nombre = nombre
        self.carnet = carnet
        self.telefono = telefono
        self.correo = correo

    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Carnet: {self.carnet}, Teléfono: {self.telefono}, Correo: {self.correo}"

# Clase ABB, es la que se encarga del árbol en general
class ABB:
    def __init__(self):
        self.raiz = None
        self.camino = []

    # Insertar un estudiante en el árbol
    def insertar(self, nodo, estudiante):
        if not nodo:
            return Nodo(estudiante)
        elif estudiante.id < nodo.estudiante.id:
            nodo.izquierda = self.insertar(nodo.izquierda, estudiante)
        else:
            nodo.derecha = self.insertar(nodo.derecha, estudiante)
        return nodo

    def insertar_estudiante(self, estudiante):
        self.raiz = self.insertar(self.raiz, estudiante)

    # Buscar un estudiante por ID
    def buscar(self, nodo, id):
        self.camino = []
        return self._buscar(nodo, id)

    def _buscar(self, nodo, id):
        if not nodo:
            return None
        self.camino.append(nodo.estudiante.id)
        if nodo.estudiante.id == id:
            return nodo
        elif id < nodo.estudiante.id:
            return self._buscar(nodo.izquierda, id)
        else:
            return self._buscar(nodo.derecha, id)

    def buscar_estudiante(self, id):
        return self.buscar(self.raiz, id)

    # Eliminar un estudiante del árbol por ID
    def eliminar(self, nodo, id):
        if not nodo:
            return nodo
        if id < nodo.estudiante.id:
            nodo.izquierda = self.eliminar(nodo.izquierda, id)
        elif id > nodo.estudiante.id:
            nodo.derecha = self.eliminar(nodo.derecha, id)
        else:
            if nodo.izquierda is None:
                return nodo.derecha
            elif nodo.derecha is None:
                return nodo.izquierda
            temp = self.obtener_min(nodo.derecha)
            nodo.estudiante = temp.estudiante
            nodo.derecha = self.eliminar(nodo.derecha, temp.estudiante.id)
        return nodo

    def eliminar_estudiante(self, id):
        self.raiz = self.eliminar(self.raiz, id)

    def obtener_min(self, nodo):
        while nodo.izquierda:
            nodo = nodo.izquierda
        return nodo

    def listar_inorden(self, nodo, resultado):
        if nodo:
            self.listar_inorden(nodo.izquierda, resultado)
            resultado.append(nodo.estudiante)
            self.listar_inorden(nodo.derecha, resultado)

    def listar_estudiantes(self):
        resultado = []
        self.listar_inorden(self.raiz, resultado)
        return resultado

# Widget para mostrar el árbol
class ABBWidget(QWidget):
    def __init__(self, arbol):
        super().__init__()
        self.arbol = arbol
        self.setMinimumSize(800, 600)

    # Dibujar el árbol
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.dibujar_nodo(painter, self.arbol.raiz, self.width() // 2, 30, self.width() // 4)

    def dibujar_nodo(self, painter, nodo, x, y, x_offset):
        if not nodo:
            return

        painter.setPen(QPen(Qt.GlobalColor.black))
        painter.setBrush(QBrush(Qt.GlobalColor.white))

        if nodo.estudiante.id in self.arbol.camino:
            painter.setBrush(QBrush(Qt.GlobalColor.yellow))

        painter.drawEllipse(x - 20, y - 20, 40, 40)
        painter.drawText(x - 10, y + 5, str(nodo.estudiante.id))

        if nodo.izquierda:
            painter.drawLine(x, y, x - x_offset, y + 50)
            self.dibujar_nodo(painter, nodo.izquierda, x - x_offset, y + 50, x_offset // 2)

        if nodo.derecha:
            painter.drawLine(x, y, x + x_offset, y + 50)
            self.dibujar_nodo(painter, nodo.derecha, x + x_offset, y + 50, x_offset // 2)

class ABBWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.arbol = ABB()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("ABB Tree Visualization")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        self.abb_widget = ABBWidget(self.arbol)
        layout.addWidget(self.abb_widget)

        form_layout = QFormLayout()

        self.id_field = QLineEdit()
        self.id_field.setPlaceholderText("Ingrese el ID")
        form_layout.addRow("ID:", self.id_field)

        self.nombre_field = QLineEdit()
        self.nombre_field.setPlaceholderText("Ingrese el nombre")
        form_layout.addRow("Nombre:", self.nombre_field)

        self.carnet_field = QLineEdit()
        self.carnet_field.setPlaceholderText("Ingrese el carnet")
        form_layout.addRow("Carnet:", self.carnet_field)

        self.telefono_field = QLineEdit()
        self.telefono_field.setPlaceholderText("Ingrese el teléfono")
        form_layout.addRow("Teléfono:", self.telefono_field)

        self.correo_field = QLineEdit()
        self.correo_field.setPlaceholderText("Ingrese el correo")
        form_layout.addRow("Correo:", self.correo_field)

        layout.addLayout(form_layout)

        self.insert_button = QPushButton("Insertar")
        self.insert_button.clicked.connect(self.insertar_estudiante)
        layout.addWidget(self.insert_button)

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Buscar por ID")
        layout.addWidget(self.search_field)

        self.search_button = QPushButton("Buscar")
        self.search_button.clicked.connect(self.buscar_estudiante)
        layout.addWidget(self.search_button)

        self.delete_field = QLineEdit()
        self.delete_field.setPlaceholderText("Eliminar por ID")
        layout.addWidget(self.delete_field)

        self.delete_button = QPushButton("Eliminar")
        self.delete_button.clicked.connect(self.eliminar_estudiante)
        layout.addWidget(self.delete_button)

        self.list_button = QPushButton("Listar Estudiantes")
        self.list_button.clicked.connect(self.listar_estudiantes)
        layout.addWidget(self.list_button)

        self.export_button = QPushButton("Exportar Lista")
        self.export_button.clicked.connect(self.exportar_lista)
        layout.addWidget(self.export_button)

        self.instructions_button = QPushButton("Instrucciones")
        self.instructions_button.clicked.connect(self.mostrar_instrucciones)
        layout.addWidget(self.instructions_button)

        self.message_label = QLabel("")
        layout.addWidget(self.message_label)

        self.list_output = QTextEdit()
        self.list_output.setReadOnly(True)
        layout.addWidget(self.list_output)

    # Función para insertar un estudiante
    def insertar_estudiante(self):
        try:
            id = int(self.id_field.text())
            nombre = self.nombre_field.text()
            carnet = self.carnet_field.text()
            telefono = self.telefono_field.text()
            correo = self.correo_field.text()
            estudiante = Estudiante(id, nombre, carnet, telefono, correo)
            self.arbol.insertar_estudiante(estudiante)
            self.id_field.clear()
            self.nombre_field.clear()
            self.carnet_field.clear()
            self.telefono_field.clear()
            self.correo_field.clear()
            self.abb_widget.update()
            self.message_label.setText(f"Estudiante {nombre} insertado.")
        except ValueError:
            self.message_label.setText("Por favor, ingrese datos válidos.")

    # Función para buscar un estudiante por ID
    def buscar_estudiante(self):
        try:
            id = int(self.search_field.text())
            resultado = self.arbol.buscar_estudiante(id)
            self.search_field.clear()
            self.abb_widget.update()
            if resultado:
                estudiante = resultado.estudiante
                self.message_label.setText(f"Estudiante encontrado: {estudiante}")
            else:
                self.message_label.setText(f"Estudiante con ID {id} no encontrado.")
        except ValueError:
            self.message_label.setText("Por favor, ingrese un ID válido.")

    # Función para eliminar un estudiante por ID
    def eliminar_estudiante(self):
        try:
            id = int(self.delete_field.text())
            self.arbol.eliminar_estudiante(id)
            self.delete_field.clear()
            self.abb_widget.update()
            self.message_label.setText(f"Estudiante con ID {id} eliminado.")
        except ValueError:
            self.message_label.setText("Por favor, ingrese un ID válido.")

    # Función para listar los estudiantes en el árbol
    def listar_estudiantes(self):
        resultado = self.arbol.listar_estudiantes()
        self.list_output.setText("\n".join(map(str, resultado)))

    # Función para exportar la lista de estudiantes a un archivo de texto
    def exportar_lista(self):
        resultado = self.arbol.listar_estudiantes()
        try:
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            file_path = os.path.join(desktop_path, 'lista_estudiantes.txt')

            # Verificar si el directorio existe, si no, crearlo
            if not os.path.exists(desktop_path):
                os.makedirs(desktop_path)

            with open(file_path, 'w', encoding='utf-8') as file:
                for estudiante in resultado:
                    file.write(str(estudiante) + '\n')
            self.message_label.setText(f"Lista exportada exitosamente a: {file_path}")
        except Exception as e:
            self.message_label.setText(f"Error al exportar la lista: {e}")



    # Función para mostrar las instrucciones en una ventana separada
    def mostrar_instrucciones(self):
        instrucciones = (
            "Instrucciones para usar el programa:\n"
            "1. Insertar Estudiante:\n"
            "   - Ingrese el ID, nombre, carnet, teléfono y correo del estudiante en los campos correspondientes.\n"
            "   - Presione el botón 'Insertar' para agregar el estudiante al árbol.\n"
            "2. Buscar Estudiante:\n"
            "   - Ingrese el ID del estudiante que desea buscar en el campo 'Buscar por ID'.\n"
            "   - Presione el botón 'Buscar' para buscar el estudiante en el árbol.\n"
            "3. Eliminar Estudiante:\n"
            "   - Ingrese el ID del estudiante que desea eliminar en el campo 'Eliminar por ID'.\n"
            "   - Presione el botón 'Eliminar' para eliminar el estudiante del árbol.\n"
            "4. Listar Estudiantes:\n"
            "   - Presione el botón 'Listar Estudiantes' para ver una lista de todos los estudiantes en el árbol.\n"
            "5. Exportar Lista:\n"
            "   - Presione el botón 'Exportar Lista' para guardar la lista de estudiantes en un archivo de texto en su escritorio.\n"
        )

        QMessageBox.information(self, "Instrucciones", instrucciones)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ABBWindow()
    window.show()
    sys.exit(app.exec())
