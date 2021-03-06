from agents.dqn import AIAgent
from agents.random import RandomAgent
from game import *
from datetime import datetime
from matplotlib import pyplot as plt


def plot_rewards(values, wins, title=''):
    f, ax = plt.subplots(nrows=1, ncols=3, figsize=(12, 5))
    f.suptitle(title)
    ax[0].plot(values, label='reward per episode')
    ax[0].axhline(1, c='red', ls='--', label='goal')
    ax[0].set_xlabel('Episodes')
    ax[0].set_ylabel('Reward')
    x = range(len(values))
    ax[0].legend()
    # Calculate the trend
    try:
        z = np.polyfit(x, values, 1)
        p = np.poly1d(z)
        ax[0].plot(x, p(x), "--", label='trend')
    except:
        print('')

    # Plot the histogram of results
    ax[1].hist(values[-50:])
    ax[1].axvline(95, c='red', label='goal')
    ax[1].set_xlabel('Rewards per Last 50 Episodes')
    ax[1].set_ylabel('Frequency')
    ax[1].legend()

    ax[2].plot(wins, label='accumulated win % per episode')
    ax[2].set_xlabel('Episode')
    ax[2].set_ylabel('Accumulated win %')
    ax[2].axhline(1, c='red', ls='--', label='100% win rate')
    ax[2].legend()
    plt.show()


if __name__ == '__main__':
    print('Training Machine with 3 previously trained DQN agents')
    rewards = []
    trials = 100
    trial_len = 300
    updateTargetNetwork = 100
    num_of_players = 4
    dqn_agent = AIAgent('./models/checkpoint1592326865.162749')
    wins = [0]
    game = Game([dqn_agent, *(AIAgent('./models/checkpoint1592326865.162749') for i in range(num_of_players - 1))])
    steps = []
    for trial in range(trials):
        print(f"Trial {trial+1}/{trials}")
        game.reset()
        episode_rewards = []
        cur_state = game.observation(agent=0)
        for step in range(trial_len):
            prev = len(game.hands[0])
            action = dqn_agent.act(cur_state, list(map(lambda x: action_to_scalar(*x), game.valid_moves())))
            curr, done = (-1, False)
            turns = 0
            while curr != 0 and not done:  # fast forward until it's our turn again
                # print(curr)
                turns += 1
                done, curr = game.next_turn()
            new_state = game.observation(agent=0)
            reward = 1 if done and curr == 0 else (0 if not done else -1)
            if done and curr == 0:
                wins.append(wins[-1] + 1)
            elif done:
                wins.append(wins[-1])
            # print(reward, 'step', step)
            episode_rewards.append(reward)
            dqn_agent.remember(cur_state, action,
                               reward, new_state, done)
            if step % 4 == 0:
                dqn_agent.replay()  # Run replay buffer
            if step % updateTargetNetwork == 0:
                dqn_agent.target_train()  # Update target model
            cur_state = new_state
            if done:
                break
        dqn_agent.replay()  # Run replay buffer
        dqn_agent.target_train()  # Update target model
        rewards.append(sum(episode_rewards))
    plot_rewards(rewards, wins, 'Rewards over episodes')
    dqn_agent.model.save(f'./models/checkpoint{datetime.now().timestamp()}')
