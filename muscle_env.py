import numpy as np

class _NumericCalc(object):
    """Helper for differentiating and integrating forward in time"""

    @staticmethod
    def diff(x1,x0,dt):
        """differentiate x to dx forward from t0 to t1"""
        return (x1-x0)/dt

    @staticmethod
    def integrate(dx1,dx0,x0,dt):
        """integrate dx to x forward from t0 to t1,
        assuming linear change"""
        return ((1/2)*(dx1-dx0)*dt) + (dx0*t) + x0

class _Kin1D(_NumericCalc):
    """A helper class to perform forward kinematics."""

    def __init__(self, kin_state = [0,0,0,0]):
        #state: position, velocity, acc, jerk
        self._kin_state = kin_state


    def inverse_kin(self: _Kin1D,
                    state0: np.ndarray,
                    state1: int,
                    order: int,
                    dt: float) -> np.ndarray:
        """
        takes observation of order n at time t1
        and estimates other variables at that time point.
        state0 is np.array and indicates original position.
        state1 is constant indicating new state of order variable order.
        dt represents time change.
        """
        assert 0 <= order <= 3, "Order must be between 0 and 3"

        # creating new state
        new_state = [0,0,0,0]
        new_state[order] = state1

        # have to cascade values out from changed one
        # ie if velocity changed, have to diff up to acc and
        # jerk, as well as integreate down to position
        integrals_done, derivatives_done = False, False
        i=order
        while not (integrals_done and derivatives_done):
            
            i-=1 # walk down integrals
            j=abs(order-i)+order # walk up derivatives
            
            if i >= 0:
                new_state[i] = self.integrate(dx1=new_state[i+1],
                                              dx0=state0[i+1],
                                              x0=state0[i],
                                              dt=dt)
            else:
                integrals_done=True
                                            
            if j <= 3:
                new_state[j] = self.diff(x1=new_state[j-1],
                                              x0=state0[j-1],
                                              dt=dt)
            else:
                derivatives_done=True

        return new_state


class MuscleEnv1D(_Kin1D):
    """Muscle modeled as a damped spring"""
        # model MuscleEnv1D as a reinforcement
        # learning environment similar to gymnasium.
        # see:
        # https://www.gymlibrary.dev
        # we want to model as a gym environment so an agent
        # (possibly an ML algorithm) can enact with an environment
        # through the muscle.

    def __init__(self, ):
        pass

    def step(self):
        """step the system forward in time given some action."""
        pass

    def reset(self):
        pass

    def render(self):
        pass

    def close(self):
        pass
    

    
# action space: lambda shifts, or weight changes.
# observation space: equilibrium point.

    

