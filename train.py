from agents.dqn import AIAgent
from agents.random import RandomAgent
from game import *
from datetime import datetime

if __name__ == '__main__':
    print('Training Machine with 3 random agents')
    trials = 300
    trial_len = 500
    updateTargetNetwork = 1000
    num_of_players = 4
    dqn_agent = AIAgent()
    game = Game([dqn_agent, *(RandomAgent() for i in range(num_of_players - 1))])
    steps = []
    for trial in range(trials):
        game.reset()
        cur_state = game.observation(agent=0)
        for step in range(trial_len):
            action = dqn_agent.act(cur_state, list(map(lambda x: action_to_scalar(*x), game.valid_moves())))
            curr, done = (-1, False)
            while curr != 0 and not done:  # fast forward until it's our turn again
                done, curr = game.next_turn()
            new_state = game.observation(agent=0)
            reward = 1 if done and curr == 0 else -len(game.hands[0])
            dqn_agent.remember(cur_state, action,
                               reward, new_state, done)

            dqn_agent.replay()
            dqn_agent.target_train()
            cur_state = new_state
            if done:
                break
        if step >= 199:
            print("Failed to complete trial")
        else:
            print("Completed in {} trials".format(trial))
            break
    dqn_agent.model.save(f'./models/checkpoint{datetime.now().timestamp()}')
