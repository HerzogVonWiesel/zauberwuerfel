import numpy as np
import random
from collections import deque
import tensorflow as tf
from tensorflow.keras import models, layers, optimizers

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size  # Rubik's Cube state representation (54 values)
        self.action_size = action_size  # 12 possible actions (6 rotations clockwise/counterclockwise)
        self.memory = deque(maxlen=2000)  # Replay memory
        self.gamma = 0.99  # Discount factor
        self.epsilon = 1.0  # Exploration rate (starts high for exploration)
        self.epsilon_min = 0.01  # Minimum exploration rate
        self.epsilon_decay = 0.995  # Decay rate for epsilon
        self.learning_rate = 0.001
        self.batch_size = 16
        self.model = self._build_model()  # Neural network to predict Q-values

    def _build_model(self):
        """Builds a simple neural network model for Q-value prediction."""
        model = models.Sequential()
        model.add(layers.Dense(128, input_dim=self.state_size, activation='elu'))
        model.add(layers.Dense(128, activation='elu'))
        model.add(layers.Dense(self.action_size, activation='linear'))  # Output layer for Q-values
        model.compile(loss='mse', optimizer=optimizers.Adam(learning_rate=self.learning_rate))
        print(model.summary())
        return model

    def remember(self, state, action, reward, next_state, done):
        """Store experience in replay memory."""
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        """Choose an action based on the current state."""
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)  # Random action (exploration)
        q_values = self.model.predict(state)  # Predict Q-values from the model
        return np.argmax(q_values[0])  # Select action with highest Q-value (exploitation)

    def replay(self):
        """Train the model using a batch of past experiences."""
        if len(self.memory) < self.batch_size:
            return  # Don't train if we don't have enough experiences

        minibatch = random.sample(self.memory, self.batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward

            # print(state)
            if not done:
                # Reshape state and next_state to ensure they are 2D arrays
                next_state = np.reshape(next_state, [1, self.state_size])
                target += self.gamma * np.amax(self.model.predict(next_state)[0])

            # Reshape state to ensure it's a 2D array
            state = np.reshape(state, [1, self.state_size])
            target_f = self.model.predict(state)
            target_f[0][action] = target  # Update the target for the specific action

            # Train the model on this sample
            self.model.fit(state, target_f, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

