import numpy as np
import gymnasium as gym

class RubiksEnv(gym.Env):
    def __init__(self, cube, n_shuffle):
        self.cube = cube
        self.color_map = {'W': 0, 'Y': 1, 'G': 2, 'B': 3, 'O': 4, 'R': 5}
        self.solved_state = self._get_state()
        self.n_shuffle = n_shuffle

        self.observation_space = gym.spaces.Box(low=0, high=5, shape=(54,), dtype=np.int8)
        self.action_space = gym.spaces.Discrete(12)
        self._action_to_move = {
            0: lambda: self.cube.move_F(False),
            1: lambda: self.cube.move_F(True),
            2: lambda: self.cube.move_B(False),
            3: lambda: self.cube.move_B(True),
            4: lambda: self.cube.move_U(False),
            5: lambda: self.cube.move_U(True),
            6: lambda: self.cube.move_D(False),
            7: lambda: self.cube.move_D(True),
            8: lambda: self.cube.move_L(False),
            9: lambda: self.cube.move_L(True),
            10: lambda: self.cube.move_R(False),
            11: lambda: self.cube.move_R(True)
        }

    def _get_state(self):
        """Convert the cube's 2D faces into a 1D numeric array."""
        state = []
        for face in ['U', 'D', 'F', 'B', 'L', 'R']:
            for row in self.cube.faces[face]:
                for sticker in row:
                    state.append(self.color_map[sticker])
        # make sure its int8
        return np.array(state, dtype=np.int8).flatten()
        return np.array(state).flatten() #reshape(1, -1)  # Return as a 1D array wrapped in 2D shape (1, 54)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.cube.reset()
        self.cube.shuffle(self.n_shuffle)
        state = self._get_state()
        return state, {}
    
    def step(self, action):
        self._action_to_move[action]()
        new_state = self._get_state()
        reward = 100 if np.array_equal(new_state, self.solved_state) else -1
        done = reward == 100
        truncated = False
        return new_state, reward, done, truncated, {}
    
    def pprint_state(self, mode="human"):
        self.cube.pretty_print()

    def print_solved(self, mode="human"):
        print(self.solved_state)

    def print_state(self, mode="human"):
        print(self._get_state())

    def get_solved_state(self):
        return self.solved_state

    def get_state(self):
        return self._get_state()