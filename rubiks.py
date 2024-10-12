import random
import copy

class RubiksCube:
    def __init__(self):
        # Initialize the cube with colors for each face
        self.faces = {
            'U': [['W']*3 for _ in range(3)],  # Up face (white)
            'D': [['Y']*3 for _ in range(3)],  # Down face (yellow)
            'F': [['G']*3 for _ in range(3)],  # Front face (green)
            'B': [['B']*3 for _ in range(3)],  # Back face (blue)
            'L': [['O']*3 for _ in range(3)],  # Left face (orange)
            'R': [['R']*3 for _ in range(3)],  # Right face (red)
        }
        self.initial_state = copy.deepcopy(self.faces)

    def get_state(self):
        return self.faces

    def rotate_face(self, face):
        """ Rotate a face 90 degrees clockwise """
        self.faces[face] = [list(row) for row in zip(*self.faces[face][::-1])]

    def move_F(self, counterclockwise=False): # CHECKED
        """ Rotate the front face clockwise (or counterclockwise if specified) """
        if counterclockwise:
            for _ in range(3):
                self.move_F()  # Do clockwise move 3 times to simulate counterclockwise
            return
        
        self.rotate_face('F')
        
        U_row = self.faces['U'][2]
        self.faces['U'][2] = [self.faces['L'][i][2] for i in range(3)][::-1]
        for i in range(3):
            self.faces['L'][i][2] = self.faces['D'][0][i]
        self.faces['D'][0] = [self.faces['R'][i][0] for i in range(3)][::-1]
        for i in range(3):
            self.faces['R'][i][0] = U_row[i]

    def move_B(self, counterclockwise=False): # CHECKED
        """ Rotate the back face clockwise (or counterclockwise if specified) """
        if counterclockwise:
            for _ in range(3):
                self.move_B()
            return
        
        self.rotate_face('B')

        U_row = self.faces['U'][0]
        self.faces['U'][0] = [self.faces['R'][i][2] for i in range(3)]
        for i in range(3):
            self.faces['R'][i][2] = self.faces['D'][2][2-i]
        self.faces['D'][2] = [self.faces['L'][i][0] for i in range(3)]
        for i in range(3):
            self.faces['L'][i][0] = U_row[2-i]

    def move_U(self, counterclockwise=False): # CHECKED
        """ Rotate the up face clockwise (or counterclockwise if specified) """
        if counterclockwise:
            for _ in range(3):
                self.move_U()
            return

        self.rotate_face('U')

        B_row = self.faces['B'][0]
        self.faces['B'][0] = self.faces['L'][0]
        self.faces['L'][0] = self.faces['F'][0]
        self.faces['F'][0] = self.faces['R'][0]
        self.faces['R'][0] = B_row

    def move_D(self, counterclockwise=False): #CHECKED
        """ Rotate the down face clockwise (or counterclockwise if specified) """
        if counterclockwise:
            for _ in range(3):
                self.move_D()
            return
        
        self.rotate_face('D')

        B_row = self.faces['B'][2]
        self.faces['B'][2] = self.faces['R'][2]
        self.faces['R'][2] = self.faces['F'][2]
        self.faces['F'][2] = self.faces['L'][2]
        self.faces['L'][2] = B_row

    def move_L(self, counterclockwise=False): # CHECKED
        """ Rotate the left face clockwise (or counterclockwise if specified) """
        if counterclockwise:
            for _ in range(3):
                self.move_L()
            return
        
        self.rotate_face('L')

        U_col = [self.faces['U'][i][0] for i in range(3)]
        for i in range(3):
            self.faces['U'][i][0] = self.faces['B'][2-i][2]
            self.faces['B'][2-i][2] = self.faces['D'][i][0]
            self.faces['D'][i][0] = self.faces['F'][i][0]
            self.faces['F'][i][0] = U_col[i]

    def move_R(self, counterclockwise=False): # CHECKED
        """ Rotate the right face clockwise (or counterclockwise if specified) """
        if counterclockwise:
            for _ in range(3):
                self.move_R()
            return
        
        self.rotate_face('R')

        U_col = [self.faces['U'][i][2] for i in range(3)]
        for i in range(3):
            self.faces['U'][i][2] = self.faces['F'][i][2]
            self.faces['F'][i][2] = self.faces['D'][i][2]
            self.faces['D'][i][2] = self.faces['B'][2-i][0]
            self.faces['B'][2-i][0] = U_col[i]
    
    def do_moves(self, move_list):
        """ Perform a list of moves on the cube """
        for move in move_list:
            counterclockwise = move.endswith('`')
            move = move.strip('`')
            getattr(self, f'move_{move}')(counterclockwise)

    def reset(self):
        """ Reset the cube to the initial state """
        self.faces = copy.deepcopy(self.initial_state)
        return self.faces

    def shuffle(self, moves=20):
        """ Shuffle the cube by performing random moves. Save moves """
        move_list = []
        for _ in range(moves):
            move = random.choice(['U', 'D', 'F', 'B', 'L', 'R'])
            counterclockwise = random.choice([True, False])
            move_list.append(f'{move}{"`" if counterclockwise else ""}')
        self.do_moves(move_list)
        return move_list

    def reverse_moves(self, move_list):
        """ Return a reversed list of moves """
        moves = []
        for move in reversed(move_list):
            if move.endswith('`'):
                move = move.strip('`')
            else:
                move += '`'
            moves.append(move)
        return moves

    def print_2d(self, print_s=True):
        """ Print the cube in a 2D representation """
        U, D, F, B, L, R = self.faces['U'], self.faces['D'], self.faces['F'], self.faces['B'], self.faces['L'], self.faces['R']
        
        def print_face(face):
            return '\n'.join(' '.join(row) for row in face)

        string = "       "+print_face(U).replace('\n', '\n       ') + "\n"
        string += print_face(L).split('\n')[0] + '  ' + print_face(F).split('\n')[0] + '  ' + print_face(R).split('\n')[0] + '  ' + print_face(B).split('\n')[0] + "\n"
        string += print_face(L).split('\n')[1] + '  ' + print_face(F).split('\n')[1] + '  ' + print_face(R).split('\n')[1] + '  ' + print_face(B).split('\n')[1] + "\n"
        string += print_face(L).split('\n')[2] + '  ' + print_face(F).split('\n')[2] + '  ' + print_face(R).split('\n')[2] + '  ' + print_face(B).split('\n')[2] + "\n"
        string += "       "+print_face(D).replace('\n', '\n       ')
        if print_s:
            print(string)
        return string
    
    def pretty_print(self):
        """ Print the cube using emojis instead of chars """
        string = self.print_2d(print_s=False)
        string = string.replace("W", "⬜").replace("Y", "🟨").replace("G", "🟩").replace("B", "🟦").replace("O", "🟧").replace("R", "🟥")
        print(string)


# Example usage
# cube = RubiksCube()
# moves = cube.shuffle(10)
# print("\n")
# print(*moves, sep=', ')
# print("\n")
# cube.pretty_print()
# moves = cube.reverse_moves(moves)
# cube.do_moves(moves)
# print("\n")
# cube.pretty_print()