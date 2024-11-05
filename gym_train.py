from tqdm import tqdm
import gymnasium as gym
import gym_rubiks
from gym_rubiks.rubiks_gym_agent import RubiksAgent
from rubiks import RubiksCube

# hyperparameters
learning_rate = 0.01
n_episodes = 100_000
start_epsilon = 1.0
epsilon_decay = start_epsilon / (n_episodes / 2)  # reduce the exploration over time
final_epsilon = 0.1

env = gym.make("RubiksCube-v0", cube=RubiksCube(), n_shuffle=3)
env = gym.wrappers.RecordEpisodeStatistics(env)#, deque_size=n_episodes)
agent = RubiksAgent(
    env = env,
    learning_rate=learning_rate,
    initial_epsilon=start_epsilon,
    epsilon_decay=epsilon_decay,
    final_epsilon=final_epsilon,
)

for episode in tqdm(range(n_episodes)):
    obs = env.reset()
    done = False

    # play one episode
    while not done:
        action = agent.get_action(obs)
        next_obs, reward, terminated, truncated, info = env.step(action)

        # update the agent
        agent.update(obs, action, reward, terminated, next_obs)

        # update if the environment is done and the current obs
        done = terminated
        obs = next_obs

    agent.decay_epsilon()