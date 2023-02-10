import numpy as np
import matplotlib.pyplot as plt

from muscle_env import _Kin1D as kin

# starting out
init_state = [0,0,0,0] #[position, velocity, acceleration, jerk]
kinematics = kin(init_state) # making a kinematics object

states = [init_state] # to track states as time progresses

### parameters
# which order of x is being defined? I.e.,
# position: order = 0
# velocity: order = 1
# acceleration: order = 2
# jerk: order = 3
order = 0

for t in range(1005):

    # load current state
    cur_state = states[t]

    # change to next state using only position
    next_position = np.sin(np.pi*t/500) + 1
    next_state = kinematics.inverse_kin(state0=cur_state,
                                 state1=next_position,
                                 order=order,
                                 dt=1/1000)
    
    states.append(next_state)


# plotting simulated data
np_states = np.array(states)
fig, axs = plt.subplots(4,1,sharex=True,figsize=(10,8))
titles = ["position", "velocity", "acceleration", "jerk"]

for i in range(4):
    # clipping off beginning to avoid impulse in motion initialization
    axs[i].plot(np_states[5:,i])
    axs[i].set(title=titles[i])

# showing plot
plt.show()
    
