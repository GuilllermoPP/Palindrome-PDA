import tkinter as tk  # Importa la librería tkinter para construir la interfaz gráfica
from tkinter import ttk  # Importa ttk, que proporciona widgets con un estilo mejorado
import time  # Importa la librería time para manejar pausas en el programa
from tkinter import Canvas, Scale  # Importa elementos gráficos de tkinter
from googletrans import Translator  # Importa el traductor de texto de googletrans
from automaton_logic import PDA  # Importa la lógica del autómata de pila
import pyttsx3  # Importa pyttsx3 para la funcionalidad de texto a voz

# Define una clase llamada PDAGraphicalInterface que manejará la interfaz gráfica
class PDAGraphicalInterface:
    def __init__(self, master):
        # Inicializa la ventana principal de la aplicación
        self.master = master
        self.master.title("PDA Visualization")
        
        # Crea una instancia del autómata de pila
        self.pda = PDA()
        
        # Inicializa el traductor de idiomas
        self.translator = Translator()
        self.current_language = "en"
        
        # Define los idiomas disponibles
        self.languages = { "en": "English", "es": "Spanish", "fr": "French"}
        
        # Inicializa la funcionalidad de texto a voz
        self.init_text_to_speech()
        
        # Crea una etiqueta para seleccionar el idioma
        self.language_label = ttk.Label(master, text=self.translate("Select a language:"))
        self.language_label.pack()
        
        # Crea un cuadro combinado para seleccionar el idioma
        self.language_selector = ttk.Combobox(master, values=list(self.languages.values()), state="readonly")
        self.language_selector.current(0)
        self.language_selector.pack()
        self.language_selector.bind("<<ComboboxSelected>>", self.change_language)
        
        # Crea una etiqueta para la entrada de texto
        self.input_label = tk.Label(master, text=self.translate("Enter an expression to validate if it's an even-length palindrome"))
        self.input_label.pack()

        # Crea un campo de entrada de texto
        self.input_entry = tk.Entry(self.master)
        self.input_entry.pack()

        # Crea una etiqueta para mostrar el resultado
        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

        # Crea un botón para validar la entrada
        self.evaluate_button = tk.Button(self.master, text=self.translate("VALIDATE"), command=self.validate_input)
        self.evaluate_button.pack()
        
        # Crea una escala para ajustar la velocidad de visualización
        self.speed_scale = Scale(self.master, label="Speed", from_=1, to=10, orient=tk.HORIZONTAL)
        self.speed_scale.set(5)
        self.speed_scale.pack()

        # Crea una etiqueta para mostrar los símbolos evaluados
        self.evaluated_symbol = tk.Label(master, text="")
        self.evaluated_symbol.pack()

        # Crea un lienzo para visualizar el autómata de pila
        self.canvas = Canvas(self.master, width=800, height=600)
        self.canvas.pack()
       
        # Visualización inicial del autómata de pila
        self.visualize_pda()

        # Inicialización de la variable de control para el bucle principal
        self.running = False

    def init_text_to_speech(self):
        # Inicializa el motor de texto a voz
        self.engine = pyttsx3.init()

    def change_language(self, event):
        # Cambia el idioma actual en respuesta a la selección del usuario
        selected_language = list(self.languages.keys())[list(self.languages.values()).index(self.language_selector.get())]
        self.current_language = selected_language
        self.update_ui_language()

        # Solicita entrada en el idioma seleccionadon to v
        self.speak_text(self.translate("Please enter an expressioalidate if it's an even-length palindrome"))

    def update_ui_language(self):
        # Actualiza la interfaz de usuario con el idioma seleccionado
        self.language_label.config(text=self.translate("Select a language:"))
        self.input_label.config(text=self.translate("Enter an expression to validate if it's an even-length palindrome"))
        self.evaluate_button.config(text=self.translate("VALIDATE"))

        # Traduce la etiqueta de la escala de velocidad
        speed_label_text = self.translate("Speed")
        self.speed_scale.config(label=speed_label_text)
        
        # Traduce la variable stack_text
        stack_text = self.translate("Stack:")
        self.draw_stack_label.config(text=stack_text)

    def validate_input(self):
        # Valida la entrada de texto
        self.result_label.config(text="-")
        input_string = self.input_entry.get()
        self.pda.reset()
        length = len(input_string)
        half_length = length // 2
        evaluated_symbols = self.translate("String Evaluation:\n" )

        for i, symbol in enumerate(input_string):
            evaluated_symbols += symbol
            self.evaluated_symbol.config(text=evaluated_symbols)
            self.update_visualization(symbol)
            if not self.pda.transition(symbol):
                self.result_label.config(text=self.translate("The expression is not a palindrome of even length\n"))
                self.speak_text(self.translate("The expression is not a palindrome of even length"))
                return

            if i == half_length - 1:
                self.update_visualization('')
                self.pda.transition('')

        self.check_final_state()

    def check_final_state(self):
        if self.pda.stack[-1] == '#' and self.pda.current_state == 'q1':
            self.update_visualization('')
            self.pda.transition('')

        self.update_visualization('')

        if self.pda.current_state == self.pda.accept_state:
            self.result_label.config(text=self.translate("The expression is a palindrome of even length\n"))
            self.speak_text(self.translate("The expression is a palindrome of even length"))
        else:
            self.result_label.config(text=self.translate("The expression is not a palindrome of even length\n"))
            self.speak_text(self.translate("The expression is not a palindrome of even length"))

    def update_visualization(self, input_symbol):
        speed = self.speed_scale.get()
        self.visualize_pda(input_symbol=input_symbol)
        self.master.update()
        time.sleep(5 / speed) 

    def visualize_pda(self, input_symbol=None):
        # Limpia el lienzo
        self.clear_canvas()
        # Dibuja los nodos (estados)
        self.draw_nodes()
        # Dibuja las transiciones
        self.draw_transitions(input_symbol)
        # Dibuja la pila
        self.draw_stack()

    def clear_canvas(self):
        # Borra todos los elementos en el lienzo
        self.canvas.delete("all")

    def draw_nodes(self):
        for state in self.pda.states:
            x, y = self.get_node_coordinates(state)
            fill_color = "lightgreen" if state == self.pda.current_state else "lightblue"
            border_width = 3 if state == self.pda.accept_state else 1
            self.draw_node(x, y, fill_color, state, border_width)

    def draw_node(self, x, y, fill_color, state, border_width):
        # Dibuja un nodo (estado)
        self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=fill_color, width=border_width)
        self.canvas.create_text(x, y, text=state)

    def draw_transitions(self, input_symbol):
        for transition, destination in self.pda.transitions.items():
            current_state, symbol, stack_symbol = transition
            new_state, push_symbols = destination
            color = "red" if current_state == self.pda.current_state and symbol == input_symbol and stack_symbol == self.pda.stack[-1] else "black"
            self.draw_transition(current_state, new_state, f"{symbol if symbol != '' else 'λ'}, {stack_symbol} -> {''.join(push_symbols if push_symbols != '' else 'λ')}", color)

    def draw_stack(self):
        # Dibuja la representación gráfica de la pila en el lienzo
        stack_text = self.translate("Stack:")
        for i, symbol in enumerate(self.pda.stack[::-1]):
            x, y = 600, 100 + i * 30
            self.canvas.create_rectangle(x - 15, y - 15, x + 15, y + 15, outline="black", fill="lightyellow")
            self.canvas.create_text(x, y, text=symbol, font=('Helvetica', 12), anchor=tk.CENTER)

        self.canvas.create_text(600, 100 + len(self.pda.stack) * 30 + 20, text=stack_text, font=('Helvetica', 12), anchor=tk.W)

    def draw_transition(self, current_state, new_state, label, color):
        # Dibuja una transición en el lienzo
        x1, y1 = self.get_node_coordinates(current_state)
        x2, y2 = self.get_node_coordinates(new_state)

        if current_state == new_state:
            self.canvas.create_arc(x1 - 30, y1 - 30, x1 + 30, y1 + 30, start=180, extent=-180, style=tk.ARC)
            self.canvas.create_line(x1 - 40, y1, x1 - 20, y1, arrow=tk.LAST)
        else:
            self.canvas.create_line(x1 + 20, y1, x2 - 20, y2, arrow=tk.LAST)

        label_x, label_y = self.calculate_label_position(x1, y1, x2, y2)
        self.canvas.create_text(label_x, label_y, text=label, fill=color)

    def calculate_label_position(self, x1, y1, x2, y2):
        # Calcula la posición de la etiqueta de la transición
        label_x = (x1 + x2) / 2
        label_y = y1 - 30

        overlapping_labels = self.canvas.find_overlapping(label_x - 10, label_y - 10, label_x + 10, label_y + 10)

        while overlapping_labels:
            label_y -= 10
            overlapping_labels = self.canvas.find_overlapping(label_x - 10, label_y - 10, label_x + 10, label_y + 10)

        return label_x, label_y

    def get_node_coordinates(self, state):
        # Obtiene las coordenadas de un nodo (estado) en el lienzo
        state_number = int(state[1:])
        x = 100 + state_number * 150
        y = 300
        return x, y

    def run(self):
        # Ejecuta el bucle principal
        self.running = True
        while self.running:
            try:
                self.master.update_idletasks()
                self.master.update()
                time.sleep(0.01)
            except tk.TclError:
                break

    def translate(self, text):
        # Traduce el texto a otro idioma
        return self.translator.translate(text, src="en", dest=self.current_language).text

    def speak_text(self, text):
        # Convierte texto en voz y lo reproduce
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == "__main__":
    # Inicia la aplicación creando una instancia de la clase PDAGraphicalInterface y ejecutando su bucle principal
    root = tk.Tk()
    app = PDAGraphicalInterface(root)
    app.run()
