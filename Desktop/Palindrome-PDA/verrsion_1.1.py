import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt

class PDA:
    def __init__(self):
        self.states = {'q0', 'q1', 'q2'}
        self.input_alphabet = {'a', 'b'}
        self.stack_alphabet = {'#', 'A', 'B'}
        self.transitions = {
            ('q0', 'a', '#'): ('q0', '#A'),
            ('q0', 'b', '#'): ('q0', '#B'),
            ('q0', 'b', 'B'): ('q0', 'BB'),
            ('q0', 'a', 'A'): ('q0', 'AA'),
            ('q0', 'a', 'B'): ('q0', 'BA'),
            ('q0', 'b', 'A'): ('q0', 'AB'),
            ('q0', '', 'A'): ('q1', 'A'),
            ('q0', '', 'B'): ('q1', 'B'),
            ('q1', 'b', 'B'): ('q1', ''),
            ('q1', 'a', 'A'): ('q1', ''),
            ('q1', '', '#'): ('q2', '#'),
        }
        self.initial_state = 'q0'
        self.accept_state = 'q2'
        self.stack = ['#']

    def transition(self, symbol):
        current_state = self.current_state
        if (current_state, symbol, self.stack[-1]) in self.transitions:
            new_state, push_symbols = self.transitions[(current_state, symbol, self.stack[-1])]
            self.stack.pop()
            self.stack.extend(push_symbols)
            self.current_state = new_state
            return True
        return False
    
    def is_even_palindrome(self, input_string):
        self.current_state = self.initial_state
        length = len(input_string)
        half_length = length // 2
        strr=""

        for i, symbol in enumerate(input_string):
            strr+=symbol
            
            if not self.transition(symbol):
                return False
            if i == half_length -1:
                self.transition('')
        if self.stack[-1]=='#' and self.current_state == 'q1':
            self.transition('')
        return self.current_state == self.accept_state

# Función para manejar el botón "Verificar"
def verificar():
    input_string = entry.get()
    result = pda.is_even_palindrome(input_string)
    if result:
        result_label.config(text=f"'{input_string}' es un palíndromo de longitud par.")
    else:
        result_label.config(text=f"'{input_string}' no es un palíndromo de longitud par.")

def mostrar_grafo():
    G = nx.DiGraph()
    for (state, symbol, stack_top), (new_state, push_symbols) in pda.transitions.items():
        G.add_edge(f"{state}, {symbol}, {stack_top}", f"{new_state}, {','.join(push_symbols)}")

    # Identificamos los nodos con transiciones
    nodos_con_transiciones = set()
    for edge in G.edges():
        nodos_con_transiciones.add(edge[0])
        nodos_con_transiciones.add(edge[1])

    # Creamos un subgrafo con los nodos que tienen transiciones
    G_sub = G.subgraph(nodos_con_transiciones)

    pos = nx.circular_layout(G_sub)  # Usamos circular_layout
    nx.draw(G_sub, pos, with_labels=True, font_weight='bold', node_size=1000, node_color='skyblue')
    nx.draw_networkx_edge_labels(G_sub, pos, edge_labels={(k, v): f"{k.split(',')[1]},{k.split(',')[2]} -> {v.split(',')[1]}" for k, v in G_sub.edges()})
    plt.show()
    
pda = PDA()

# Crear ventana
root = tk.Tk()
root.title("Verificador de Palíndromos")

# Etiqueta e input para la cadena
input_label = tk.Label(root, text="Ingresa una cadena:")
input_label.pack()

entry = tk.Entry(root)
entry.pack()

# Botón de verificar
verificar_button = tk.Button(root, text="Verificar", command=verificar)
verificar_button.pack()

# Botón para mostrar el grafo
mostrar_grafo_button = tk.Button(root, text="Mostrar Grafo", command=mostrar_grafo)
mostrar_grafo_button.pack()

# Etiqueta para mostrar el resultado
result_label = tk.Label(root, text="")
result_label.pack()

# Iniciar bucle de la GUI
root.mainloop()
