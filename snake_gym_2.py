import snake_2
import gym 
import numpy as np
import random 
import cv2




class SnakeGym(gym.Env):
    
    """ Env guide from: https://github.com/openai/gym/blob/master/gym/core.py """ 

    """The main OpenAI Gym class. It encapsulates an environment with
    arbitrary behind-the-scenes dynamics. An environment can be
    partially or fully observed.
    The main API methods that users of this class need to know are:
        step, reset, render, close, seed
    And set the following attributes:
        action_space: The Space object corresponding to valid actions
        observation_space: The Space object corresponding to valid observations
        reward_range: A tuple corresponding to the min and max possible rewards
    Note: a default reward range set to [-inf,+inf] already exists. Set it if you want a narrower range.
    The methods are accessed publicly as "step", "reset", etc...
    """

    metadata = {'render.modes': ['human', 'ansi', 'rgb_array']}
    spec = None
    reward_range = {
        'alive':-0.01,
        'died':-1,
        'ate':1,
        'won':10
        }  

    def __init__(self):
        super(SnakeGym, self).__init__()
        self.env = snake_2.Environment()
        self.observation_shape = (self.env.height, self.env.height,3)   
        self.observation_space = gym.spaces.Box(low = 0,
                high = 1,
                shape = self.observation_shape,
                dtype = np.float32)
        self.action_space = gym.spaces.Discrete(4)
        self.reset()
    
    def reset(self):
        """Resets the environment to an initial state and returns an initial
        observation.
        Note that this function should not reset the environment's random
        number generator(s); random variables in the environment's state should
        be sampled independently between multiple calls to `reset()`. In other
        words, each call of `reset()` should yield an environment suitable for
        a new episode, independent of previous episodes.
        Returns:
            observation (object): the initial observation.
        """
        self.env.reset()
        self.done = False 
        return self.env.canvas
    
    def step(self, action):
        """Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.
        Accepts an action and returns a tuple (observation, reward, done, info).
        Args:
            action (object): an action provided by the agent
        Returns:
            observation (object): agent's observation of the current environment
            reward (float) : amount of reward returned after previous action
            done (bool): whether the episode has ended, in which case further step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning)
        """

        if self.done:
            self.reset()

        status = self.env.update_environment(action)
        if status == 0:
            reward = self.reward_range['died'] 
            self.done = True
        elif status == 1:
            reward = self.reward_range['alive']
        elif status == 2:
            reward = self.reward_range['ate']
        elif status == 3:
            reward = self.reward_range['won']
            self.done = True
        info = {} #empty for now
        return self.env.canvas, reward, self.done, info

    def render(self, mode = 'human'):
        return self.env.render(mode)
    
    @property
    def unwrapped(self):
        """Completely unwrap this env.
        Returns:
            gym.Env: The base non-wrapped gym.Env instance
        """
        return self

    def __str__(self):
        if self.spec is None:
            return '<{} instance>'.format(type(self).__name__)
        else:
            return '<{}<{}>>'.format(type(self).__name__, self.spec.id)

    def __enter__(self):
        """Support with-statement for the environment. """
        return self

    def __exit__(self, *args):
        """Support with-statement for the environment. """
        self.close()
        # propagate exception
        return False

def keypress_to_direction(k, vb):

    if k == 119:    
        return 0 

    elif k == 100:
        return 3 
    
    elif k == 115:
        return 1 
    
    elif k == 97:
        return 2 
    
    elif k == -1:
        return vb  



# Test functionalities
if __name__ == '__main__':
    env = SnakeGym()
    env.reset()

    alt_reward_range = {
        'alive':1,
        'died':-2,
        'won':10,
        'ate':3
        }
    env.reward_range = alt_reward_range
    init_obs = env.reset()
    last_reward = -1
    kk = 0    
    while env.env.game_state:
        _, last_reward, _, _ = env.step(kk)
        k = env.render('human')
        value_before = kk
        kk = keypress_to_direction(k, value_before)




