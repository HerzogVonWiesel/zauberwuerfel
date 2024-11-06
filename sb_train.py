from tqdm import tqdm
import gymnasium as gym
import gym_rubiks
from gym_rubiks.rubiks_gym_agent import RubiksAgent
from rubiks import RubiksCube

import numpy as np

# stable-baselines3 Reinformencement Learning agent
from stable_baselines3 import DQN
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy

env = gym.make("RubiksCube-v0", cube=RubiksCube(), n_shuffle=1)
env = gym.wrappers.TimeLimit(env, max_episode_steps=10)

model = DQN("MlpPolicy", env, verbose=1)
# Train the agent and display a progress bar
model.learn(total_timesteps=int(2e6), progress_bar=True)
# Save the agent
model.save("RubiksCube")
del model

# Load the trained agent
# NOTE: if you have loading issue, you can pass `print_system_info=True`
# to compare the system on which the model was trained vs the current one
# model = DQN.load("dqn_lunar", env=env, print_system_info=True)
model = DQN.load("RubiksCube", env=env)

# Evaluate the agent
# NOTE: If you use wrappers with your environment that modify rewards,
#       this will be reflected here. To evaluate with original rewards,
#       wrap environment in a "Monitor" wrapper before other wrappers.
mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)

# Enjoy trained agent
vec_env = model.get_env()
solved_ratio = 0
repeats = 144
for evaluation in range(repeats):
    obs = vec_env.reset()
    print("-------------------")
    vec_env.env_method(method_name='print_state')
    #vec_env.env_method(method_name='print_step')
    for i in range(10):
        action, _states = model.predict(obs, deterministic=True)
        obs, rewards, dones, info = vec_env.step(action)
        if dones:
            solved_ratio += 1
            #vec_env.env_method(method_name='print_step')
            print(rewards)
            #vec_env.env_method(method_name='print_solved')
            vec_env.env_method(method_name='print_state')
            print(np.array_equal(vec_env.env_method(method_name='get_state'), vec_env.env_method(method_name='get_solved_state')))
            break
print(f"Solved ratio: {solved_ratio}/{repeats}")

env.close()