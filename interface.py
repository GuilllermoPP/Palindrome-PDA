import tkinter as tk

import time
from tkinter import Canvas, Scale
from automaton_logic import PDA

class PDAGraphicalInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("PDA Visualization")


    
        # Create a PDA instance
        self.pda = PDA()

        self.input_label = tk.Label(master, text="Ingrese una expresion para evaluar si es Palindromo de longitud par")
        self.input_label.pack()

        # Create an Entry for input
        self.input_entry = tk.Entry(self.master)
        self.input_entry.pack()

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

        # Create a Button to trigger PDA evaluation
        self.evaluate_button = tk.Button(self.master, text="Evaluate", command=self.validate_input)
        self.evaluate_button.pack()
         # Create a Scale for controlling speed
        self.speed_scale = Scale(self.master, label="Speed", from_=1, to=10, orient=tk.HORIZONTAL)
        self.speed_scale.set(5)  # Default speed
        self.speed_scale.pack()

        self.evaluated_symbol = tk.Label(master, text="")
        self.evaluated_symbol.pack()

        # Create a Canvas for drawing the PDA diagram
        self.canvas = Canvas(self.master, width=800, height=600)
        self.canvas.pack()
       
        # Initialize visualization
        self.visualize_pda()

        # Create a boolean flag to control the loop
        self.running = False

    def validate_input(self):
        self.result_label.config(text="-")
        input_string = self.input_entry.get()
        self.pda.reset()
        length = len(input_string)
        half_length = length // 2
        evaluated_symbols = "simbolos evaluado: "

        for i, symbol in enumerate(input_string):
            evaluated_symbols += symbol
            self.evaluated_symbol.config(text=evaluated_symbols)
            self.update_visualization(symbol)
            if not self.pda.transition(symbol):
                self.result_label.config(text="Rechazado")
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
            self.result_label.config(text="Aceptado")
        else:
            self.result_label.config(text="Rechazado")

    def update_visualization(self, input_symbol):
        speed = self.speed_scale.get()
        self.visualize_pda(input_symbol=input_symbol)
        self.master.update()
        time.sleep(5 / speed) 



    def visualize_pda(self, input_symbol=None):
        self.clear_canvas()
        self.draw_nodes()
        self.draw_transitions(input_symbol)
        self.draw_stack()

    def clear_canvas(self):
        self.canvas.delete("all")

    def draw_nodes(self):
        for state in self.pda.states:
            x, y = self.get_node_coordinates(state)
            fill_color = "lightgreen" if state == self.pda.current_state else "lightblue"
            border_width = 3 if state == self.pda.accept_state else 1
            self.draw_node(x, y, fill_color, state, border_width)

    def draw_node(self, x, y, fill_color, state, border_width):
        self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=fill_color, width=border_width)
        self.canvas.create_text(x, y, text=state)

    def draw_transitions(self, input_symbol):
        for transition, destination in self.pda.transitions.items():
            current_state, symbol, stack_symbol = transition
            new_state, push_symbols = destination
            color = "red" if current_state == self.pda.current_state and symbol == input_symbol and stack_symbol == self.pda.stack[-1] else "black"
            self.draw_transition(current_state, new_state, f"{symbol if symbol != '' else 'λ'}, {stack_symbol} -> {''.join(push_symbols if push_symbols != '' else 'λ')}", color)

    def draw_stack(self):
        stack_text = "Pila:"
        for i, symbol in enumerate(self.pda.stack[::-1]):
            x, y = 600, 100 + i * 30
            self.canvas.create_rectangle(x - 15, y - 15, x + 15, y + 15, outline="black", fill="lightyellow")
            self.canvas.create_text(x, y, text=symbol, font=('Helvetica', 12), anchor=tk.CENTER)

        self.canvas.create_text(600, 100 + len(self.pda.stack) * 30 + 20, text=stack_text, font=('Helvetica', 12), anchor=tk.W)

    def draw_transition(self, current_state, new_state, label, color):
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
        label_x = (x1 + x2) / 2
        label_y = y1 - 30

        overlapping_labels = self.canvas.find_overlapping(label_x - 10, label_y - 10, label_x + 10, label_y + 10)

        while overlapping_labels:
            label_y -= 10
            overlapping_labels = self.canvas.find_overlapping(label_x - 10, label_y - 10, label_x + 10, label_y + 10)

        return label_x, label_y

    def get_node_coordinates(self, state):
        state_number = int(state[1:])
        x = 100 + state_number * 150
        y = 300
        return x, y

    def run(self):
        # Run the main loop
        self.running = True
        while self.running:
            try:
                self.master.update_idletasks()
                self.master.update()
                time.sleep(0.01)
            except tk.TclError:
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = PDAGraphicalInterface(root)
    app.run()
