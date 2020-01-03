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
env.actual_init(30, 30, 4, 0) # args - (width, height, num_agents, goal_color[0 - blue, 1 - green, 2 - red])
env.reset()
rendered = env.render('human')
action = [1,2,0,3] # list of size 4 for 4 agents. 0 - right 1 - down 2 - right 3-up
obs, reward, done, info = env.step(action)
```
The maximum timesteps are 50
