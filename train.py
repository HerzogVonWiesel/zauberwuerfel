from rubiks import RubiksCube
from environment import RubiksCubeEnvironment
from agent import DQNAgent

def train_dqn(agent, env, episodes=1000, n_shuffle=3):
    for episode in range(episodes):
        state = env.reset()
        done = False
        step_count = 0

        while not done:
            # Agent takes an action
            action = agent.act(state)

            # if step_count % 100 == 0:
            #     print(state)
            #     print(action)
            #     print(agent.model.predict(state))
            #     print(step_count)

            # Take the action in the environment
            next_state, reward, done = env.step(action)

            # Remember the experience for replay
            agent.remember(state, action, reward, next_state, done)

            # Move to the next state
            state = next_state
            step_count += 1

            # If done (cube is solved), print the result
            if done:
                print(f"Episode {episode + 1}: Solved in {step_count} steps.")
                break

            # maximum of n_shuffle*2 steps
            if step_count > 2 * n_shuffle:
                print(f"Episode {episode + 1}: Could not solve in {step_count} steps")
                break
        # Train the agent with experience replay
        if done:
            agent.replay()

# Assuming RubiksCube class is provided and working
cube = RubiksCube()
n_shuffle = 1
env = RubiksCubeEnvironment(cube, n_shuffle=n_shuffle)
state_size = 54  # 54 stickers on the cube
action_size = 12  # 12 possible actions
agent = DQNAgent(state_size, action_size)

# Train the agent
train_dqn(agent, env, episodes=500, n_shuffle=n_shuffle)
agent.save("rubiks_dqn_model.weights.h5")  # Save the trained agent
