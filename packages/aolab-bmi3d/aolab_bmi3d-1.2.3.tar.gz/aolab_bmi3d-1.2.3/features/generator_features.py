'''
Features which have task-like functionality w.r.t. task...
'''

import random
import numpy as np
from scipy.spatial.transform import Rotation as R
from riglib.experiment import traits
from built_in_tasks.target_graphics import *

class Autostart(traits.HasTraits):
    '''
    Automatically begins the trial from the wait state, 
    with a random interval drawn from `rand_start`. Doesn't really
    work if there are multiple trials in between wait states.
    '''
    rand_start = traits.Tuple((0., 0.), desc="Start interval")
    exclude_parent_traits = ['wait_time']

    def _start_wait(self):
        '''
        At the start of the 'wait' state, determine how long to wait before starting the trial
        by drawing a sample from the rand_start interval
        '''
        s, e = self.rand_start
        self.wait_time = random.random()*(e-s) + s
        super(Autostart, self)._start_wait()
        
    def _test_start_trial(self, ts):
        '''
        Test if the required random wait time has passed
        '''
        return ts > self.wait_time and not self.pause

class AdaptiveGenerator(object):
    '''
    Deprecated--this class appears to be unused
    '''
    def __init__(self, *args, **kwargs):
        super(AdaptiveGenerator, self).__init__(*args, **kwargs)
        assert hasattr(self.gen, "correct"), "Must use adaptive generator!"

    def _start_reward(self):
        self.gen.correct()
        super(AdaptiveGenerator, self)._start_reward()
    
    def _start_incorrect(self):
        self.gen.incorrect()
        super(AdaptiveGenerator, self)._start_incorrect()


class IgnoreCorrectness(object):
    '''Deprecated--this class appears to be unused and not compatible with Sequences
    Allows any response to be correct, not just the one defined. Overrides for trialtypes'''
    def __init__(self, *args, **kwargs):
        super(IgnoreCorrectness, self).__init__(*args, **kwargs)
        if hasattr(self, "trial_types"):
            for ttype in self.trial_types:
                del self.status[ttype]["%s_correct"%ttype]
                del self.status[ttype]["%s_incorrect"%ttype]
                self.status[ttype]["correct"] = "reward"
                self.status[ttype]["incorrect"] = "penalty"

    def _test_correct(self, ts):
        return self.event is not None

    def _test_incorrect(self, ts):
        return False


class MultiHoldTime(traits.HasTraits):
    '''
    Deprecated--Use RandomDelay instead. 
    Allows the hold time parameter to be multiple values per target in a given sequence chain. For instance,
    center targets and peripheral targets can have different hold times.
    '''

    multi_hold_time = traits.List([.2,], desc="Length of hold required at targets before next target appears. \
        Can be a single number or a list of numbers to apply to each target in the sequence (center, out, etc.)")
    exclude_parent_traits = ['hold_time']
    
    def _test_hold_complete(self, time_in_state):
        '''
        Test whether the target is held long enough to declare the
        trial a success

        Possible options
            - Target held for the minimum requred time (implemented here)
            - Sensorized object moved by a certain amount
            - Sensorized object moved to the required location
            - Manually triggered by experimenter
        '''
        if len(self.multi_hold_time) == 1:
            multi_hold_time = self.multi_hold_time[0]
        else:
            multi_hold_time = self.multi_hold_time[self.target_index]
        return time_in_state > multi_hold_time

class Progressbar_fixation(traits.HasTraits):

    progress_bar_color = traits.OptionsList("blue", *target_colors, desc="Color of the eye target", bmi3d_input_options=list(target_colors.keys()))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Instantiate the targets
        instantiate_targets = kwargs.pop('instantiate_targets', True)
        if instantiate_targets:

            # Target 1 and 2 are for saccade. Target 3 is for hand
            self.bar = VirtualCircularTarget(target_radius=0.5, target_color=target_colors[self.progress_bar_color], starting_pos=[-5,0,-5])

    def _start_wait(self):
        super()._start_wait()

        if self.calc_trial_num() == 0:

            for model in self.bar.graphics_models:
                self.add_model(model)
                self.bar.hide()

    def _start_fixation(self):
        super()._start_fixation()
        self.fixation_frame_index = 0

    def _while_fixation(self):
        super()._while_fixation()
        self.fixation_frame_index += 1
        fixation_time = self.fixation_frame_index*2/self.fps
        if fixation_time <= self.hold_time:
            radius = fixation_time/self.hold_time*(self.fixation_radius-self.fixation_radius_buffer)
        else:
            radius = (self.fixation_radius-self.fixation_radius_buffer)

        if hasattr(self, 'bar'):
            for model in self.bar.graphics_models:
                self.remove_model(model)
            del self.bar

        self.bar = VirtualCircularTarget(target_radius=radius, target_color=target_colors[self.progress_bar_color], \
                                         starting_pos=self.targs[self.target_index]+[0,-0.5,0]) # [0,-0.5,0] is for visualization
        for model in self.bar.graphics_models:
            self.add_model(model)
        self.bar.show()

    def _start_targ_transition(self):
        super()._start_targ_transition()
        self.bar.hide()


class RandomDelay(traits.HasTraits):
    '''
    Replaces 'delay_time' with 'rand_delay', an interval on which the delay period is selected uniformly.
    '''
    
    rand_delay = traits.Tuple((0., 0.), desc="Delay interval")
    exclude_parent_traits = ['delay_time']
    prob_catch_trials = traits.Float(0., desc="Probability of catch trials")
    short_delay_catch_trials = traits.List([.2,], desc="Delay intervals for catch trials")

    def _start_wait(self):
        '''
        At the start of the 'wait' state, draw a sample from the rand_delay interval for this trial.
        '''

        # Catch trial condition
        if random.random() < self.prob_catch_trials:
            self.delay_time = random.choice(self.short_delay_catch_trials)

        # Normal trial condition
        else:
            s, e = self.rand_delay
            self.delay_time = random.random()*(e-s) + s
        super()._start_wait()

class TransparentDelayTarget(traits.HasTraits):
    '''
    Feature to make the delay period show a semi-transparent target rather than the full target. Used 
    for training the go cue. Gradually increase the alpha from 0 to 0.75 once a long enough delay 
    period has been established.
    '''

    delay_target_alpha = traits.Float(0.25, desc="Transparency of the next target during delay periods")

    def _start_delay(self):
        super()._start_delay()

        # Set the alpha of the next target
        next_idx = (self.target_index + 1)
        if next_idx < self.chain_length:
            target = self.targets[next_idx % 2]
            self._old_target_color = np.copy(target.sphere.color)
            new_target_color = list(target.sphere.color)
            new_target_color[3] = self.delay_target_alpha
            target.sphere.color = tuple(new_target_color)

    def _start_target(self):
        super()._start_target()

        # Reset the transparency of the current target
        if self.target_index > 0:
            target = self.targets[self.target_index % 2]
            target.sphere.color = self._old_target_color

class PoissonWait(traits.HasTraits):
    '''
    Draw each trial's wait time from a poisson random distribution    
    '''
    
    poisson_mu = traits.Float(0.5, desc="Mean duration between trials (s)")
    exclude_parent_traits = ['wait_time']

    def _parse_next_trial(self):
        self.wait_time = np.random.exponential(self.poisson_mu)
        super()._parse_next_trial()

class IncrementalRotation(traits.HasTraits):
    '''
    Gradually change the perturbation rotation over trials
    '''
    exclude_parent_traits = ['pertubation_rotation', 'perturbation_rotation_z', 'perturbation_rotation_x']

    init_rotation_y  = traits.Float(0.0, desc="initial rotation about bmi3d y-axis in degrees")
    final_rotation_y = traits.Float(0.0, desc="final rotation about bmi3d y-axis in degrees")

    init_rotation_z  = traits.Float(0.0, desc="initial rotation about bmi3d z-axis in degrees")
    final_rotation_z = traits.Float(0.0, desc="final rotation about bmi3d z-axis in degrees")
    
    init_rotation_x  = traits.Float(0.0, desc="inital rotation about bmi3d x-axis in degrees")
    final_rotation_x = traits.Float(0.0, desc="final rotation about bmi3d x-axis in degrees")

    delta_rotation_y = traits.Float(0.0, desc="rotation step size about bmi3d y-axis in degrees")
    delta_rotation_z = traits.Float(0.0, desc="rotation step size about bmi3d z-axis in degrees")
    delta_rotation_x = traits.Float(0.0, desc="rotation step size about bmi3d x-axis in degrees")

    trials_per_increment = traits.Int(1, desc="number of successful trials per rotation step")
    final_tracking_out_time = traits.Float(1.6, desc="Time allowed to be tracking outside the target for final rotation") # AKA tolerance time

    def init(self):    
        super().init()
        self.num_trials_success = 0
        self.num_increments_y = 0
        self.num_increments_z = 0
        self.num_increments_x = 0

        if self.final_rotation_y != self.init_rotation_y:
            self.num_increments_y = int( (self.final_rotation_y-self.init_rotation_y) / self.delta_rotation_y+1 )
        if self.final_rotation_z != self.init_rotation_z:
            self.num_increments_z = int( (self.final_rotation_z-self.init_rotation_z) / self.delta_rotation_z+1 )
        if self.final_rotation_x != self.init_rotation_x:
            self.num_increments_x = int( (self.final_rotation_x-self.init_rotation_x) / self.delta_rotation_x+1 )

        self.max_num_increments = np.max([self.num_increments_y, self.num_increments_z, self.num_increments_x])
        self.pertubation_rotation = self.init_rotation_y
        self.perturbation_rotation_z = self.init_rotation_z
        self.perturbation_rotation_x = self.init_rotation_x

        print("Y", self.pertubation_rotation, "Z", self.perturbation_rotation_z, "X", self.perturbation_rotation_x)
    
    def incremental_start_wait(self):
        # determine the current rotation step
        num_deltas = int(self.num_trials_success / self.trials_per_increment)

        # increment the current perturbation rotation by delta
        self.pertubation_rotation = self.init_rotation_y + self.delta_rotation_y*num_deltas
        self.perturbation_rotation_z = self.init_rotation_z + self.delta_rotation_z*num_deltas
        self.perturbation_rotation_x = self.init_rotation_x + self.delta_rotation_x*num_deltas

        # change tracking out time of final rotation
        if num_deltas+1 == self.max_num_increments:
            self.tracking_out_time = self.final_tracking_out_time

        # stop incrementing once final perturbation rotation reached
        if self.num_trials_success >= self.num_increments_y * self.trials_per_increment:
            self.pertubation_rotation = self.final_rotation_y
        if self.num_trials_success >= self.num_increments_z * self.trials_per_increment:
            self.perturbation_rotation_z = self.final_rotation_z
        if self.num_trials_success >= self.num_increments_x * self.trials_per_increment:
            self.perturbation_rotation_x = self.final_rotation_x
        
        print("Y", self.pertubation_rotation, "Z", self.perturbation_rotation_z, "X", self.perturbation_rotation_x)
        print(self.tracking_out_time, "tracking out")
    
    def _start_wait(self):
        super()._start_wait()
        self.incremental_start_wait()

    def _start_wait_retry(self):
        super()._start_wait_retry()
        self.incremental_start_wait()

    def _start_reward(self):
        super()._start_reward()
        self.num_trials_success += 1