import tkinter as tk
from tkinter import Canvas

from automaton_logic import PDA

class PDAGraphicalInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("PDA Visualization")
    
        # Create a PDA instance
        self.pda = PDA()

        # Create a Canvas for drawing the PDA diagram
        self.evaluate_button = tk.Button(self.master, text="Evaluate", command=self.evaluate_input)
        self.evaluate_button.pack()
        self.canvas = Canvas(self.master, width=800, height=600)
        self.canvas.pack()

        # Create a button to trigger PDA evaluation
        

    def evaluate_input(self):
        input_string = "abba"  # Replace this with your input string
        result = self.pda.is_even_palindrome(input_string)

        # Visualize the PDA state, stack, and symbols here
        self.visualize_pda()

    def visualize_pda(self):
        # Clear the canvas before redrawing
        self.canvas.delete("all")

        # Draw PDA nodes
        for state in self.pda.states:
            x, y = self.get_node_coordinates(state)
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="lightblue")
            self.canvas.create_text(x, y, text=state)

        # Draw PDA transitions
        for transition, destination in self.pda.transitions.items():
            current_state, symbol, stack_symbol = transition
            new_state, push_symbols = destination
            self.draw_transition(current_state, new_state, f"{symbol}, {stack_symbol} -> {''.join(push_symbols)}")

        self.master.mainloop()

    def draw_transition(self, current_state, new_state, label):
        x1, y1 = self.get_node_coordinates(current_state)
        x2, y2 = self.get_node_coordinates(new_state)

        if current_state == new_state:
            # Draw a curved arrow using create_arc
            self.canvas.create_arc(x1 - 30, y1 - 30, x1 + 30, y1 + 30, start=180, extent=-180, style=tk.ARC)

            # Draw an arrowhead using create_line (arrow=tk.LAST)
            self.canvas.create_line(x1 - 40, y1, x1 - 20, y1, arrow=tk.LAST)
        else:
            # Draw a straight arrow
            self.canvas.create_line(x1 + 20, y1, x2 - 20, y2, arrow=tk.LAST)

        # Calculate the middle point of the line for label placement
        label_x, label_y = self.calculate_label_position(x1, y1, x2, y2)

        # Add a label at the adjusted position
        self.canvas.create_text(label_x, label_y, text=label)

    def calculate_label_position(self, x1, y1, x2, y2):
        # Calculate the middle point of the line for label placement
        label_x = (x1 + x2) / 2
        label_y = y1 - 30 

        # Check if there is already a label at this position
        overlapping_labels = self.canvas.find_overlapping(label_x - 10, label_y - 10, label_x + 10, label_y + 10)

        # Adjust the y-coordinate if there is an overlapping label
        while overlapping_labels:
            label_y -= 10
            overlapping_labels = self.canvas.find_overlapping(label_x - 10, label_y - 10, label_x + 10, label_y + 10)

        return label_x, label_y

    def get_node_coordinates(self, state):
        # Calculate x, y coordinates based on the state number
        state_number = int(state[1:])
        x = 100 + state_number * 150
        y = 300
        return x, y

if __name__ == "__main__":
    root = tk.Tk()
    app = PDAGraphicalInterface(root)
    root.mainloop()
