class DFA:

    def __init__(self, Q, alphabet, transition_func, q0, F):
        self.Q = Q
        self.alphabet = alphabet
        self.transition_func = transition_func
        self.q0 = q0
        self.F = F

    def process_word(self, w):
        cur_state = self.q0
        path = [cur_state]
        for c in w:
            try:
                next_state = self.transition_func[(cur_state, c)]
            except Exception as e:
                raise ValueError('character not from alphabet')
            cur_state = next_state
            path.append(next_state)
        return cur_state in self.F, path

def table_to_transition_func(table, Q, alphabet):
    x = {}
    for q_i, row in enumerate(table):
        for a_i, next_q in enumerate(row):
            x[(Q[q_i], alphabet[a_i])] = next_q
    return x

if __name__ == '__main__':
    # automaton that determines if a positive binary number is divisible by 5
    Q = ['qs', 'qf', 'q0', 'q1', 'q2', 'q3', 'q4']
    alphabet = ['0', '1']
    t_table = [
        ['qf', 'q1'],
        ['qf', 'qf'],
        ['q0', 'q1'],
        ['q2', 'q3'],
        ['q4', 'q0'],
        ['q1', 'q2'],
        ['q3', 'q4'],
    ]
    t_func = table_to_transition_func(t_table, Q, alphabet)
    q0 = 'qs'
    F = ['q0']
    d = DFA(Q, alphabet, t_func, q0, F)
    for i in range(1, 1000000):
        res, _ = d.process_word(bin(i)[2:])
        assert((i % 5 == 0) == res)
