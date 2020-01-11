from game import Agent, Action
from keras.models import Sequential
from keras.layers import Dense, InputLayer


class AIAgent(Agent):

    def __init__(self):
        super().__init__()
        self.model = Sequential()
        self.model.add(InputLayer(batch_input_shape=(1, 10)))
        self.model.add(Dense(10, activation='sigmoid'))
        self.model.add(Dense(len(Action.value), activation='linear'))
        self.model.compile(loss='mse', optimizer='adam', metrics=['mae'])

    def play(self, game, obs):
        return self.model.predict(obs)[0]
