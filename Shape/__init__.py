from gym.envs.registration import register

register(
    id='shape-v0',
    entry_point='Shape.envs:ShapeEnv',
)
