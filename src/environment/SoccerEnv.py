# Derived from the previous SoccerEnv created by Alexandre Muzio

# General imports
import grpc
import numpy as np
from mpi4py import MPI
import gymnasium as gym
from gymnasium import spaces

import logging
logger = logging.getLogger(__name__)

# Protobuf imports
import protobufgen.soccer3d_pb2 as soccer3d_pb2 
import protobufgen.soccer3d_pb2_grpc as soccer3d_pb2_grpc 

class Soccer3DEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self, id=0, eval=False):
        # Start connection with server
        if eval:
            id += 10
        self.channel = grpc.insecure_channel(MPI.Get_processor_name() + ':' + str(5000 + id))
        self.stub = soccer3d_pb2_grpc.DDPGTrainerStub(self.channel)

        setup = self.stub.SetupEnvironment(soccer3d_pb2.SetupEnvRequest())
        logger.info(setup.num_state_dim, setup.num_action_dim, setup.action_bound)

        self.action_space = spaces.Box(low=-np.array(setup.action_bound), high=np.array(setup.action_bound))
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(setup.num_state_dim,))

    def reset(self):
        response = self.stub.StartEpisode(soccer3d_pb2.EpisodeRequest())
        return np.array(response.state.observation)

    def step(self, action):
        response = self.stub.Simulate(soccer3d_pb2.SimulationRequest(action=soccer3d_pb2.Action(action=action)))
        logger.debug(action, response.state, response.reward)
        
        return np.array(response.state.observation), response.reward, response.done, {}

    def render(self, mode='human', close=False):
        return

    def close(self):
        self.stub.CloseEnvironment(soccer3d_pb2.CloseRequest())
        return
