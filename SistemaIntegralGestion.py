print("Hellman Enrique Piñeros Rodriguez")
print("Grupo: 213023")
print("Fase 4 Componente práctico Prácticas simuladas")
print("SistemasIntegralGestión")
print("Codigo fuente autoria propia")
import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod

# ----------------- Logger -----------------
class Logger:
    @staticmethod
    def log(msg):
        with open("log.txt", "a") as f:
            f.write(msg + "\n")

# ----------------- Entidad Base -----------------
class EntidadSistema(ABC):
    @abstractmethod
    def validar(self):
        pass

# ----------------- Cliente -----------------
class Cliente(EntidadSistema):
    def __init__(self, nombre, correo):
        if not nombre or not correo:
            raise ValueError("Datos inválidos para cliente")
        self.__nombre = nombre
        self.__correo = correo

    def validar(self):
        return "@" in self.__correo

    def __str__(self):
        return f"{self.__nombre} ({self.__correo})"

# ----------------- Servicio -----------------
class Servicio(EntidadSistema, ABC):
    @abstractmethod
    def calcular_costo(self, duracion=1):
        pass

class ReservaSala(Servicio):
    def validar(self): return True
    def calcular_costo(self, duracion=1): return 50 * duracion
    def __str__(self): return "Reserva de Sala"

class AlquilerEquipo(Servicio):
    def validar(self): return True
    def calcular_costo(self, duracion=1): return 30 * duracion
    def __str__(self): return "Alquiler de Equipo"

class Asesoria(Servicio):
    def validar(self): return True
    def calcular_costo(self, duracion=1): return 100 * duracion
    def __str__(self): return "Asesoría Especializada"

# ----------------- Reserva -----------------
class Reserva:
    def __init__(self, cliente, servicio, duracion):
        if not cliente.validar() or not servicio.validar():
            raise ValueError("Cliente o servicio inválido")
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def confirmar(self):
        self.estado = "Confirmada"

    def cancelar(self):
        self.estado = "Cancelada"

    def __str__(self):
        return f"{self.servicio} para {self.cliente} ({self.estado})"

# ----------------- Sistema -----------------
class SistemaFJ:
    def __init__(self):
        self.clientes = []
        self.reservas = []

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)

    def crear_reserva(self, cliente, servicio, duracion):
        try:
            reserva = Reserva(cliente, servicio, duracion)
            reserva.confirmar()
            self.reservas.append(reserva)
            return reserva
        except Exception as e:
            Logger.log(f"Error creando reserva: {e}")
            raise

# ----------------- Interfaz Tkinter -----------------
class App:
    def __init__(self, root, sistema):
        self.sistema = sistema
        root.title("Software FJ - Gestión")

        tk.Label(root, text="Nombre Cliente").grid(row=0, column=0)
        tk.Label(root, text="Correo Cliente").grid(row=1, column=0)

        self.nombre = tk.Entry(root)
        self.correo = tk.Entry(root)
        self.nombre.grid(row=0, column=1)
        self.correo.grid(row=1, column=1)

        tk.Button(root, text="Registrar Cliente", command=self.registrar_cliente).grid(row=2, column=0, columnspan=2)

        tk.Button(root, text="Crear Reserva Sala", command=lambda: self.crear_reserva(ReservaSala())).grid(row=3, column=0)
        tk.Button(root, text="Crear Alquiler Equipo", command=lambda: self.crear_reserva(AlquilerEquipo())).grid(row=3, column=1)
        tk.Button(root, text="Crear Asesoría", command=lambda: self.crear_reserva(Asesoria())).grid(row=4, column=0)

    def registrar_cliente(self):
        try:
            cliente = Cliente(self.nombre.get(), self.correo.get())
            self.sistema.agregar_cliente(cliente)
            messagebox.showinfo("Éxito", f"Cliente {cliente} registrado")
        except Exception as e:
            Logger.log(f"Error registrando cliente: {e}")
            messagebox.showerror("Error", str(e))

    def crear_reserva(self, servicio):
        if not self.sistema.clientes:
            messagebox.showerror("Error", "No hay clientes registrados")
            return
        cliente = self.sistema.clientes[-1]  # último cliente
        try:
            reserva = self.sistema.crear_reserva(cliente, servicio, 1)
            messagebox.showinfo("Reserva", f"Reserva creada: {reserva}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# ----------------- Main -----------------
if __name__ == "__main__":
    sistema = SistemaFJ()
    root = tk.Tk()
    app = App(root, sistema)
    root.mainloop()
