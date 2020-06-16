from collections import deque

import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from game import *
strategy = tf.distribute.MirroredStrategy()
print("Number of GPUs: {}".format(strategy.num_replicas_in_sync))

# I would like to thank https://towardsdatascience.com/reinforcement-learning-w-keras-openai-dqns-1eed3a5338c
# for making an easy to read tutorial on DQN with Keras, I didn't know how to implement this and it really helped.


def valid_action_mask(actions):
    res = np.zeros(63)
    for i in actions:
        res[i] = 1
    return np.array(res)


class AIAgent:

    def __init__(self, seed=42, gamma=0.99, epsilon=1.0, epsilon_min=0.1, epsilon_max=1.0, batch_size=32,
                 max_steps_per_epsiode=10000, epsilon_decay=0.995, learning_rate=0.01, load_model=None):
        super(AIAgent, self).__init__()
        self.seed = seed
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_max = epsilon_max
        self.memory = deque(maxlen=2000)
        self.epsilon_decay = epsilon_decay
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.max_steps_per_episode = max_steps_per_epsiode
        with strategy.scope():
            self.model = self.create_model()
            self.target_model = self.create_model()
            if load_model is not None:
                self.model.load_weights(filepath=load_model)
                self.target_model.load_weights(filepath=load_model)

    def create_model(self):
        model = keras.Sequential()
        model.add(layers.Dense(124, input_dim=1,
                               activation="relu"))
        model.add(layers.Dense(64, activation="relu"))
        model.add(layers.Dense(63))
        model.compile(loss="mean_squared_error",
                      optimizer=keras.optimizers.Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])

    def replay(self):
        if len(self.memory) < self.batch_size:
            return
        samples = random.sample(self.memory, self.batch_size)
        for sample in samples:
            state, action, reward, new_state, done = sample
            target = self.target_model.predict(state)
            if done:
                target[0][action] = reward
            else:
                Q_future = max(
                    self.target_model.predict(new_state)[0])
                target[0][action] = reward + Q_future * self.gamma
            self.model.fit(state, target, epochs=1, verbose=0)

    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i]
        self.target_model.set_weights(target_weights)

    def act(self, state, actions):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
        if np.random.random() < self.epsilon:
            return random.choice(actions)
        return actions[np.argmax(self.model.predict(state)[0][actions])]

    def play(self, game):
        state = game.observation()
        action = self.act(state, list(map(lambda x: action_to_scalar(*x), game.valid_moves())))
        return scalar_to_action(action)
