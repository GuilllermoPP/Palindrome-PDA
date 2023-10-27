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
                print(self.current_state,strr,self.stack)
            print(self.current_state,strr,self.stack)
        if self.stack[-1]=='#' and self.current_state == 'q1':
            self.transition('')
            print(self.current_state,strr,self.stack)
        return self.current_state == self.accept_state


# Ejemplo de uso
pda = PDA()

# Solicitar entrada del usuario
input_string = input("Ingresa una cadena para verificar si es un palíndromo de longitud par: ")

result = pda.is_even_palindrome(input_string)

if result:
    print(f"'{input_string}' es un palíndromo de longitud par.")
else:
    print(f"'{input_string}' no es un palíndromo de longitud par.")
