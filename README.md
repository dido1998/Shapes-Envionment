# Shapes-Envionment
Gym implementation of the shape environment described in http://proceedings.mlr.press/v97/das19a/das19a.pdf

## Intallation
Run the following command - 
```
pip install -e .
```

## Usage
```
import Shape
env = gym.make('shape-v0')
env.actual_init(30, 30, 4, 0) # args - (width, height, num_agents, goal_color[0 - blue, 1 - greeen, 2 - red])
```
