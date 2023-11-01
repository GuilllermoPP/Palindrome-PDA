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
        self.current_state= self.initial_state 
        self.stack = ['#']

    def transition(self, symbol):
        
        if (self.current_state, symbol, self.stack[-1]) in self.transitions:
            new_state, push_symbols = self.transitions[(self.current_state, symbol, self.stack[-1])]
            self.stack.pop()
            self.stack.extend(push_symbols)
            self.current_state = new_state
            return True
        return False

    def reset(self):
        """
        Reinicia los estados del autómata a su estado inicial.
        """
        self.current_state = self.initial_state
        self.stack = ['#']
        
