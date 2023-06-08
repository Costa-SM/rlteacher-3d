from gymnasium.envs.registration import register

register(
    id="SoccerEnv-v0", 
    entry_point='src.environment:Soccer3DEnv',
    max_episode_steps=50
)