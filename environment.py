import numpy as np

class RubiksCubeEnvironment:
    def __init__(self, cube, n_shuffle):
        self.cube = cube  # Assume this is an instance of the provided RubiksCube class
        self.color_map = {'W': 0, 'Y': 1, 'G': 2, 'B': 3, 'O': 4, 'R': 5}  
        self.solved_state = self.get_state()  # Store the solved state for reference
        self.n_shuffle = n_shuffle

    def get_state(self):
        """Convert the cube's 2D faces into a 1D numeric array."""
        state = []
        for face in ['U', 'D', 'F', 'B', 'L', 'R']:
            for row in self.cube.faces[face]:
                for sticker in row:
                    state.append(self.color_map[sticker])
        return np.array(state).reshape(1, -1)  # Return as a 1D array wrapped in 2D shape (1, 54)

    def reset(self):
        """Reset the cube (scramble it) and return the new state."""
        self.cube.reset()
        self.cube.shuffle(self.n_shuffle)
        return self.get_state()

    def step(self, action):
        """Take a step in the environment by performing an action on the cube."""
        action_map = [
            lambda: self.cube.move_F(False),  # 0 -> move_F (clockwise)
            lambda: self.cube.move_F(True),   # 1 -> move_F (counterclockwise)
            lambda: self.cube.move_B(False),  # 2 -> move_B (clockwise)
            lambda: self.cube.move_B(True),   # 3 -> move_B (counterclockwise)
            lambda: self.cube.move_U(False),  # 4 -> move_U (clockwise)
            lambda: self.cube.move_U(True),   # 5 -> move_U (counterclockwise)
            lambda: self.cube.move_D(False),  # 6 -> move_D (clockwise)
            lambda: self.cube.move_D(True),   # 7 -> move_D (counterclockwise)
            lambda: self.cube.move_L(False),  # 8 -> move_L (clockwise)
            lambda: self.cube.move_L(True),   # 9 -> move_L (counterclockwise)
            lambda: self.cube.move_R(False),  # 10 -> move_R (clockwise)
            lambda: self.cube.move_R(True)    # 11 -> move_R (counterclockwise)
        ]

        # Perform the selected action
        action_map[action]()
        
        # Get the new state after performing the action
        new_state = self.get_state()
        
        # Reward: +100 if solved, otherwise -1 per move
        if np.array_equal(self.get_state(), self.solved_state):
            reward = 100
            done = True
        else:
            reward = -1
            done = False

        return new_state, reward, done

