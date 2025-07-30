'''
A generic target capture task
'''
import numpy as np
import random

from riglib.experiment import traits, Sequence
from riglib import plants

from riglib.stereo_opengl.window import Window
from .target_graphics import *

## Plants
# List of possible "plants" that a subject could control either during manual or brain control
cursor = plants.CursorPlant()
shoulder_anchor = np.array([2., 0., -15])
chain_kwargs = dict(link_radii=.6, joint_radii=0.6, joint_colors=(181/256., 116/256., 96/256., 1), link_colors=(181/256., 116/256., 96/256., 1))
chain_20_20_endpt = plants.EndptControlled2LArm(link_lengths=[20, 20], base_loc=shoulder_anchor, **chain_kwargs)
chain_20_20 = plants.RobotArmGen2D(link_lengths=[20, 20], base_loc=shoulder_anchor, **chain_kwargs)

plantlist = dict(
    cursor=cursor,
    chain_20_20=chain_20_20,
    chain_20_20_endpt=chain_20_20_endpt)

class TargetCapture(Sequence):
    '''
    This is a generic cued target capture skeleton, to form as a common ancestor to the most
    common type of motor control task.
    '''
    status = dict(
        wait = dict(start_trial="target"),
        target = dict(enter_target="hold", timeout="timeout_penalty"),
        hold = dict(leave_target="hold_penalty", hold_complete="delay"),
        delay = dict(leave_target="delay_penalty", delay_complete="targ_transition"),
        targ_transition = dict(trial_complete="reward", trial_abort="wait", trial_incomplete="target"),
        timeout_penalty = dict(timeout_penalty_end="targ_transition", end_state=True),
        hold_penalty = dict(hold_penalty_end="targ_transition", end_state=True),
        delay_penalty = dict(delay_penalty_end="targ_transition", end_state=True),
        reward = dict(reward_end="wait", stoppable=False, end_state=True)
    )

    # initial state
    state = "wait"

    target_index = -1 # Helper variable to keep track of which target to display within a trial
    tries = 0 # Helper variable to keep track of the number of failed attempts at a given trial.

    sequence_generators = []

    reward_time = traits.Float(.5, desc="Length of reward dispensation")
    hold_time = traits.Float(.2, desc="Length of hold required at targets before next target appears")
    hold_penalty_time = traits.Float(1, desc="Length of penalty time for target hold error")
    delay_time = traits.Float(0, desc="Length of time after a hold while the next target is on before the go cue")
    delay_penalty_time = traits.Float(1, desc="Length of penalty time for delay error")
    timeout_time = traits.Float(10, desc="Time allowed to go between targets")
    timeout_penalty_time = traits.Float(1, desc="Length of penalty time for timeout error")
    max_attempts = traits.Int(10, desc='The number of attempts of a target chain before skipping to the next one')
    num_targets_per_attempt = traits.Int(2, desc="Minimum number of target acquisitions to be counted as an attempt")

    def init(self):
        self.trial_dtype = np.dtype([('trial', 'u4'), ('index', 'u4'), ('target', 'f8', (3,))])
        super().init()

    def _start_wait(self):
        # Call parent method to draw the next target capture sequence from the generator
        super()._start_wait()

        # number of times this sequence of targets has been attempted
        self.tries = 0

        # index of current target presented to subject
        self.target_index = -1

        # number of targets to be acquired in this trial
        self.chain_length = len(self.targs)

    def _parse_next_trial(self):
        '''Check that the generator has the required data'''
        self.gen_indices, self.targs = self.next_trial
        # TODO error checking
        
        # Update the data sinks with trial information
        self.trial_record['trial'] = self.calc_trial_num()
        for i in range(len(self.gen_indices)):
            self.trial_record['index'] = self.gen_indices[i]
            self.trial_record['target'] = self.targs[i]
            self.sinks.send("trials", self.trial_record)

    def _start_target(self):
        self.target_index += 1

    def _end_target(self):
        '''Nothing generic to do.'''
        pass

    def _start_hold(self):
        '''Nothing generic to do.'''
        pass

    def _while_hold(self):
        '''Nothing generic to do.'''
        pass

    def _end_hold(self):
        '''Nothing generic to do.'''
        pass

    def _start_delay(self):
        '''Nothing generic to do.'''
        pass

    def _while_delay(self):
        '''Nothing generic to do.'''
        pass

    def _end_delay(self):
        '''Nothing generic to do.'''
        pass

    def _start_targ_transition(self):
        '''Nothing generic to do. Child class might show/hide targets'''
        pass

    def _while_targ_transition(self):
        '''Nothing generic to do.'''
        pass

    def _end_targ_transition(self):
        '''Nothing generic to do.'''
        pass

    def _increment_tries(self):
        if self.target_index >= self.num_targets_per_attempt-1:
            self.tries += 1 # only count errors if the minimum number of targets have been acquired
        self.target_index = -1

        if self.tries < self.max_attempts: 
            self.trial_record['trial'] += 1
            for i in range(len(self.gen_indices)):
                self.trial_record['index'] = self.gen_indices[i]
                self.trial_record['target'] = self.targs[i]
                self.sinks.send("trials", self.trial_record)

    def _start_timeout_penalty(self):
        self._increment_tries()

    def _while_timeout_penalty(self):
        '''Nothing generic to do.'''
        pass

    def _end_timeout_penalty(self):
        '''Nothing generic to do.'''
        pass

    def _start_hold_penalty(self):
        self._increment_tries()

    def _while_hold_penalty(self):
        '''Nothing generic to do.'''
        pass

    def _end_hold_penalty(self):
        '''Nothing generic to do.'''
        pass

    def _start_delay_penalty(self):
        self._increment_tries()

    def _while_delay_penalty(self):
        '''Nothing generic to do.'''
        pass

    def _end_delay_penalty(self):
        '''Nothing generic to do.'''
        pass

    def _start_reward(self):
        '''Nothing generic to do.'''
        pass

    def _while_reward(self):
        '''Nothing generic to do.'''
        pass

    def _end_reward(self):
        '''Nothing generic to do.'''
        pass

    ################## State transition test functions ##################
    def _test_start_trial(self, time_in_state):
        '''Start next trial automatically. You may want this to instead be
            - a random delay
            - require some initiation action
        '''
        return True

    def _test_timeout(self, time_in_state):
        return time_in_state > self.timeout_time or self.pause

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
        return time_in_state > self.hold_time

    def _test_delay_complete(self, time_in_state):
        '''
        Test whether the delay period, when the cursor must stay in place
        while another target is being presented, is over. There should be 
        no delay on the last target in a chain.
        '''
        return self.target_index + 1 == self.chain_length or time_in_state > self.delay_time

    def _test_trial_complete(self, time_in_state):
        '''Test whether all targets in sequence have been acquired'''
        return self.target_index == self.chain_length-1

    def _test_trial_abort(self, time_in_state):
        '''Test whether the target capture sequence should just be skipped due to too many failures'''
        return (not self._test_trial_complete(time_in_state)) and (self.tries==self.max_attempts)

    def _test_trial_incomplete(self, time_in_state):
        '''Test whether the target capture sequence needs to be restarted'''
        return (not self._test_trial_complete(time_in_state)) and (self.tries<self.max_attempts) and not self.pause

    def _test_timeout_penalty_end(self, time_in_state):
        return time_in_state > self.timeout_penalty_time

    def _test_hold_penalty_end(self, time_in_state):
        return time_in_state > self.hold_penalty_time

    def _test_delay_penalty_end(self, time_in_state):
        return time_in_state > self.delay_penalty_time

    def _test_reward_end(self, time_in_state):
        return time_in_state > self.reward_time

    def _test_enter_target(self, time_in_state):
        '''This function is task-specific and not much can be done generically'''
        return False

    def _test_leave_target(self, time_in_state):
        '''This function is task-specific and not much can be done generically'''
        return self.pause

    def update_report_stats(self):
        '''
        see experiment.Experiment.update_report_stats for docs
        '''
        super().update_report_stats()
        self.reportstats['Trial #'] = self.calc_trial_num()
        self.reportstats['Reward/min'] = np.round(self.calc_events_per_min('reward', 120.), decimals=2)

class ScreenTargetCapture(TargetCapture, Window):
    """Concrete implementation of TargetCapture task where targets
    are acquired by "holding" a cursor in an on-screen target"""

    limit2d = traits.Bool(True, desc="Limit cursor movement to 2D")

    sequence_generators = [
        'out_2D', 'centerout_2D', 'centeroutback_2D', 'centerout_2D_select', 'rand_target_chain_2D', 
        'rand_target_chain_3D', 'corners_2D', 'centerout_tabletop',
    ]

    hidden_traits = ['cursor_color', 'target_color', 'cursor_bounds', 'cursor_radius', 'plant_hide_rate', 'starting_pos']

    is_bmi_seed = True

    # Runtime settable traits
    target_radius = traits.Float(2, desc="Radius of targets in cm")
    target_color = traits.OptionsList("yellow", *target_colors, desc="Color of the target", bmi3d_input_options=list(target_colors.keys()))
    plant_hide_rate = traits.Float(0.0, desc='If the plant is visible, specifies a percentage of trials where it will be hidden')
    plant_type = traits.OptionsList(*plantlist, bmi3d_input_options=list(plantlist.keys()))
    plant_visible = traits.Bool(True, desc='Specifies whether entire plant is displayed or just endpoint')
    cursor_radius = traits.Float(.5, desc='Radius of cursor in cm')
    cursor_color = traits.OptionsList("dark_purple", *target_colors, desc='Color of cursor endpoint', bmi3d_input_options=list(target_colors.keys()))
    cursor_bounds = traits.Tuple((-10., 10., -10., 10., -10., 10.), desc='(x min, x max, y min, y max, z min, z max)')
    starting_pos = traits.Tuple((5., 0., 5.), desc='Where to initialize the cursor') 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize the plant
        if not hasattr(self, 'plant'):
            self.plant = plantlist[self.plant_type]
        self.plant.set_bounds(np.array(self.cursor_bounds))
        self.plant.set_color(target_colors[self.cursor_color])
        self.plant.set_cursor_radius(self.cursor_radius)
        self.plant_vis_prev = True
        self.cursor_vis_prev = True

        # Add graphics models for the plant and targets to the window
        if hasattr(self.plant, 'graphics_models'):
            for model in self.plant.graphics_models:
                self.add_model(model)

        # Instantiate the targets
        instantiate_targets = kwargs.pop('instantiate_targets', True)
        if instantiate_targets:

            # 2 targets for delay
            target1 = VirtualCircularTarget(target_radius=self.target_radius, target_color=target_colors[self.target_color])
            target2 = VirtualCircularTarget(target_radius=self.target_radius, target_color=target_colors[self.target_color])

            self.targets = [target1, target2]

        self.target_location = np.array(self.starting_pos).copy()

        # Declare any plant attributes which must be saved to the HDF file at the _cycle rate
        for attr in self.plant.hdf_attrs:
            self.add_dtype(*attr)

    def init(self):
        self.add_dtype('trial', 'u4', (1,))
        self.add_dtype('plant_visible', '?', (1,))
        super().init()
        self.plant.set_endpoint_pos(np.array(self.starting_pos))

    def _cycle(self):
        '''
        Calls any update functions necessary and redraws screen
        '''
        self.move_effector()

        ## Run graphics commands to show/hide the plant if the visibility has changed
        self.update_plant_visibility()
        self.task_data['plant_visible'] = self.plant_visible

        ## Save plant status to HDF file
        plant_data = self.plant.get_data_to_save()
        for key in plant_data:
            self.task_data[key] = plant_data[key]

        # Update the trial index
        self.task_data['trial'] = self.calc_trial_num()

        super()._cycle()

    def move_effector(self):
        '''Move the end effector, if a robot or similar is being controlled'''
        pass

    def run(self):
        '''
        See experiment.Experiment.run for documentation.
        '''
        # Fire up the plant. For virtual/simulation plants, this does little/nothing.
        self.plant.start()
        
        # Include some cleanup in case the parent class has errors
        try:
            super().run()
        finally:
            self.plant.stop()

    ##### HELPER AND UPDATE FUNCTIONS ####
    def update_plant_visibility(self):
        ''' Update plant visibility'''
        if self.plant_visible != self.plant_vis_prev:
            self.plant_vis_prev = self.plant_visible
            self.plant.set_visibility(self.plant_visible)

    #### TEST FUNCTIONS ####
    def _test_enter_target(self, ts):
        '''
        return true if the distance between center of cursor and target is smaller than the cursor radius
        '''
        cursor_pos = self.plant.get_endpoint_pos()
        d = np.linalg.norm(cursor_pos - self.targs[self.target_index])
        return d <= (self.target_radius - self.cursor_radius) or super()._test_enter_target(ts)

    def _test_leave_target(self, ts):
        '''
        return true if cursor moves outside the exit radius
        '''
        cursor_pos = self.plant.get_endpoint_pos()
        d = np.linalg.norm(cursor_pos - self.targs[self.target_index])
        rad = self.target_radius - self.cursor_radius
        return d > rad or super()._test_leave_target(ts)

    #### STATE FUNCTIONS ####
    def _start_wait(self):
        super()._start_wait()

        if self.calc_trial_num() == 0:

            # Instantiate the targets here so they don't show up in any states that might come before "wait"
            for target in self.targets:
                for model in target.graphics_models:
                    self.add_model(model)
                    target.hide()

    def _start_target(self):
        super()._start_target()

        # Show target if it is hidden (this is the first target, or previous state was a penalty)
        target = self.targets[self.target_index % 2]
        if self.target_index == 0:
            target.move_to_position(self.targs[self.target_index])
            target.show()
            self.sync_event('TARGET_ON', self.gen_indices[self.target_index])
        self.target_location = self.targs[self.target_index] # save for BMILoop

    def _start_hold(self):
        super()._start_hold()
        self.sync_event('CURSOR_ENTER_TARGET', self.gen_indices[self.target_index])

    def _start_delay(self):
        super()._start_delay()

        # Make next target visible unless this is the final target in the trial
        next_idx = (self.target_index + 1)
        if next_idx < self.chain_length:
            target = self.targets[next_idx % 2]
            target.move_to_position(self.targs[next_idx])
            target.show()
            self.sync_event('TARGET_ON', self.gen_indices[next_idx])
        else:
            # This delay state should only last 1 cycle, don't sync anything
            pass

    def _start_targ_transition(self):
        super()._start_targ_transition()
        if self.target_index == -1:

            # Came from a penalty state
            pass
        elif self.target_index + 1 < self.chain_length:

            # Hide the current target if there are more
            self.targets[self.target_index % 2].hide()
            self.sync_event('TARGET_OFF', self.gen_indices[self.target_index])

    def _start_hold_penalty(self):
        self.sync_event('HOLD_PENALTY') 
        super()._start_hold_penalty()
        # Hide targets
        for target in self.targets:
            target.hide()
            target.reset()

    def _end_hold_penalty(self):
        super()._end_hold_penalty()
        self.sync_event('TRIAL_END')

    def _start_delay_penalty(self):
        self.sync_event('DELAY_PENALTY') 
        super()._start_delay_penalty()
        # Hide targets
        for target in self.targets:
            target.hide()
            target.reset()

    def _end_delay_penalty(self):
        super()._end_delay_penalty()
        self.sync_event('TRIAL_END')
        
    def _start_timeout_penalty(self):
        self.sync_event('TIMEOUT_PENALTY')
        super()._start_timeout_penalty()
        # Hide targets
        for target in self.targets:
            target.hide()
            target.reset()

    def _end_timeout_penalty(self):
        super()._end_timeout_penalty()
        self.sync_event('TRIAL_END')

    def _start_reward(self):
        self.targets[self.target_index % 2].cue_trial_end_success()
        self.sync_event('REWARD')
        
    def _end_reward(self):
        super()._end_reward()
        self.sync_event('TRIAL_END')

        # Hide targets
        for target in self.targets:
            target.hide()
            target.reset()
            
    #### Generator functions ####
    '''
    Note to self: because of the way these get into the database, the parameters don't
    have human-readable descriptions like the other traits. So it is useful to define
    the descriptions elsewhere, in models.py under Generator.to_json().

    Ideally someone should take the time to reimplement generators as their own classes
    rather than static methods that belong to a task.
    '''
    @staticmethod
    def static(pos=(0,0,0), ntrials=0):
        '''Single location, finite (ntrials!=0) or infinite (ntrials==0)'''
        if ntrials == 0:
            while True:
                yield [0], np.array(pos)
        else:
            for _ in range(ntrials):
                yield [0], np.array(pos)

    @staticmethod
    def out_2D(nblocks=100, ntargets=8, distance=10, origin=(0,0,0)):
        '''
        Generates a sequence of 2D (x and z) targets at a given distance from the origin

        Parameters
        ----------
        nblocks : int
            The number of ntarget pairs in the sequence.
        ntargets : int
            The number of equally spaced targets
        distance : float
            The distance in cm between the center and peripheral targets.
        origin : 3-tuple
            Location of the central targets around which the peripheral targets span

        Returns
        -------
        [nblocks*ntargets x 1] array of tuples containing trial indices and [1 x 3] target coordinates

        '''
        rng = np.random.default_rng()
        for _ in range(nblocks):
            order = np.arange(ntargets) + 1 # target indices, starting from 1
            rng.shuffle(order)
            for t in range(ntargets):
                idx = order[t]
                theta = 2*np.pi*(3-idx)/ntargets # put idx 1 at 12 o'clock
                pos = np.array([
                    distance*np.cos(theta),
                    0,
                    distance*np.sin(theta)
                ]).T
                yield [idx], [pos + origin]

    @staticmethod
    def centerout_2D(nblocks=100, ntargets=8, distance=10, origin=(0,0,0)):
        '''
        Pairs of central targets at the origin and peripheral targets centered around the origin

        Returns
        -------
        [nblocks*ntargets x 1] array of tuples containing trial indices and [2 x 3] target coordinates
        '''
        gen = ScreenTargetCapture.out_2D(nblocks, ntargets, distance, origin)
        for _ in range(nblocks*ntargets):
            idx, pos = next(gen)
            targs = np.zeros([2, 3]) + origin
            targs[1,:] = pos[0]
            indices = np.zeros([2,1])
            indices[1] = idx
            yield indices, targs

    @staticmethod
    def centerout_2D_select(nblocks=100, ntargets=8, distance=10, origin=(0,0,0), target_idx=[]):
        '''
        Generates a sequence of 2D (x and z) targets at a given distance from the origin, 
        but lets you select which targets out of the total number you want to keep
        '''
        if type(target_idx) not in (list, tuple) or len(target_idx) == 0:
            raise ValueError(f'Malformed target_idx selection "{target_idx}"! Input a list of [idx1, idx2, ...]')
        gen = ScreenTargetCapture.centerout_2D(nblocks, ntargets, distance, origin)
        while True:
            try:
                next_indices, next_targs = next(gen)
                if next_indices[1] in target_idx:
                    yield next_indices, next_targs # only yield the targets that match target_idx
            except StopIteration:
                break

    @staticmethod
    def centeroutback_2D(nblocks=100, ntargets=8, distance=10, origin=(0,0,0)):
        '''
        Triplets of central targets, peripheral targets, and central targets

        Returns
        -------
        [nblocks*ntargets x 1] array of tuples containing trial indices and [3 x 3] target coordinates
        '''
        gen = ScreenTargetCapture.out_2D(nblocks, ntargets, distance, origin)
        for _ in range(nblocks*ntargets):
            idx, pos = next(gen)
            targs = np.zeros([3, 3]) + origin
            targs[1,:] = pos[0]
            indices = np.zeros([3,1])
            indices[1] = idx
            yield indices, targs
    
    @staticmethod
    def rand_target_chain_2D(ntrials=100, chain_length=1, boundaries=(-12,12,-12,12)):
        '''
        Generates a sequence of 2D (x and z) target pairs.

        Parameters
        ----------
        ntrials : int
            The number of target chains in the sequence.
        chain_length : int
            The number of targets in each chain
        boundaries: 4 element Tuple
            The limits of the allowed target locations (-x, x, -z, z)

        Returns
        -------
        [ntrials x chain_length x 3] array of target coordinates
        '''
        rng = np.random.default_rng()
        idx = 0
        for t in range(ntrials):

            # Choose a random sequence of points within the boundaries
            pts = rng.uniform(size=(chain_length, 3))*((boundaries[1]-boundaries[0]),
                0, (boundaries[3]-boundaries[2]))
            pts = pts+(boundaries[0], 0, boundaries[2])
            yield idx+np.arange(chain_length), pts
            idx += chain_length
    
    @staticmethod
    def rand_target_chain_3D(ntrials=100, chain_length=1, boundaries=(-12,12,-10,10,-12,12)):
        '''
        Generates a sequence of 3D target pairs.
        Parameters
        ----------
        ntrials : int
            The number of target chains in the sequence.
        chain_length : int
            The number of targets in each chain
        boundaries: 6 element Tuple
            The limits of the allowed target locations (-x, x, -y, y, -z, z)

        Returns
        -------
        [ntrials x chain_length x 3] array of target coordinates
        '''
        rng = np.random.default_rng()
        idx = 0
        for t in range(ntrials):

            # Choose a random sequence of points within the boundaries
            pts = rng.uniform(size=(chain_length, 3))*((boundaries[1]-boundaries[0]),
                (boundaries[3]-boundaries[2]), (boundaries[5]-boundaries[4]))
            pts = pts+(boundaries[0], boundaries[2], boundaries[4])
            yield idx+np.arange(chain_length), pts
            idx += chain_length

    @staticmethod
    def corners_2D(nblocks=5, chain_length=1, corners=(-8,8,-8,8)):
        '''
        Generates a sequence of 2D (x and z) targets at the given 4 corners

        Parameters
        ----------
        nblocks : 3-tuple
            Number of blocks
        chain_length : int
            The number of targets in each chain before a reward is given
        corners : 4-tuple
            Location of the edges of the screen (-x, x, -y, y)

        Returns
        -------
        [nblocks*4 x 1] array of tuples containing trial indices and [1 x 3] target coordinates

        '''
        ntargets = 4
        corners = np.array([
            [corners[0], 0, corners[2]],
            [corners[0], 0, corners[3]],
            [corners[1], 0, corners[2]],
            [corners[1], 0, corners[3]]
        ])
        target_order = []
        rng = np.random.default_rng()
        for _ in range(nblocks):
            order = np.arange(ntargets) + 1 # target indices, starting from 1
            rng.shuffle(order)
            target_order = np.concatenate((target_order, order), axis=0)

        # Spit out trials in groups of chain_length
        ntrials = nblocks*4//chain_length
        for t in range(ntrials):
            idx = target_order[int(t*chain_length):int(t*chain_length+chain_length)]
            pos = [corners[int(i-1),:] for i in idx]
            yield idx, pos

    @staticmethod
    def centerout_tabletop(nblocks=100, ntargets=8, distance=10, origin=(0,0,0)):
        '''
        Generates a sequence of 2D (x and y) targets at a given distance from the origin.
        Exactly the same as centerout_2D but on the xy plane instead of the xz plane.
        '''
        targets = ScreenTargetCapture.centerout_2D(nblocks, ntargets, distance, origin)
        for idx, pos in targets:
            targs = [t[[0,2,1]] for t in pos]
            yield idx, targs

class ScreenReachAngle(ScreenTargetCapture):
    '''
    A modified task that requires the cursor to move in the right direction towards the target, 
    without actually needing to arrive at the target. If the maximum angle is exceeded, a reach 
    penalty is applied. No hold or delay period.

    Only works for sequences with 1 target in a chain. 
    '''

    status = dict(
        wait = dict(start_trial="target"),
        target = dict(reach_success="targ_transition", timeout="timeout_penalty", leave_bounds="reach_penalty"),
        targ_transition = dict(trial_complete="reward", trial_abort="wait", trial_incomplete="target"),
        timeout_penalty = dict(timeout_penalty_end="targ_transition", end_state=True),
        reach_penalty = dict(reach_penalty_end="targ_transition", end_state=True),
        reward = dict(reward_end="wait", stoppable=False, end_state=True)
    )

    sequence_generators = [
        'out_2D', 'rand_target_chain_2D', 'rand_target_chain_3D', 'discrete_targets_2D',
    ]

    max_reach_angle = traits.Float(90., desc="Angle defining the boundaries between the starting position of the cursor and the target")
    reach_penalty_time = traits.Float(1, desc="Length of penalty time for target hold error")
    reach_fraction = traits.Float(0.5, desc="Fraction of the distance between the reach start and the target before a reward")
    start_radius = traits.Float(1., desc="Buffer around reach start allowed in bounds (cm)")

    exclude_parent_traits = ['hold_time', 'hold_penalty_time', 'delay_time', 'delay_penalty_time']

    def _start_target(self):
        super()._start_target()

        # Define a reach start and reach target position whenever the target appears
        self.reach_start = self.plant.get_endpoint_pos().copy()
        self.reach_target = self.targs[self.target_index]

    def _test_leave_bounds(self, ts):
        '''
        Check whether the cursor is in the boundary defined by reach_start, target_pos,
        and max_reach_angle.
        '''

        # Calculate the angle between the vectors from the start pos to the current cursor and target
        a = self.plant.get_endpoint_pos() - self.reach_start
        b = self.reach_target - self.reach_start
        cursor_target_angle = np.arccos(np.dot(a, b)/np.linalg.norm(a)/np.linalg.norm(b))

        # If that angle is more than half the maximum, we are outside the bounds
        out_of_bounds = np.degrees(cursor_target_angle) > self.max_reach_angle / 2

        # But also allow a target radius around the reach_start 
        away_from_start = np.linalg.norm(self.plant.get_endpoint_pos() - self.reach_start) > self.start_radius

        return away_from_start and out_of_bounds

    def _test_reach_success(self, ts):
        dist_traveled = np.linalg.norm(self.plant.get_endpoint_pos() - self.reach_start)
        dist_total = np.linalg.norm(self.reach_target - self.reach_start)
        dist_total -= (self.target_radius - self.cursor_radius)
        return dist_traveled/dist_total > self.reach_fraction

    def _start_reach_penalty(self):
        self.sync_event('OTHER_PENALTY')
        self._increment_tries()
        
        # Hide targets
        for target in self.targets:
            target.hide()
            target.reset()

    def _end_reach_penalty(self):
        self.sync_event('TRIAL_END')

    def _test_reach_penalty_end(self, ts):
        return ts > self.reach_penalty_time

    @staticmethod
    def discrete_targets_2D(nblocks=100, ntargets=3, boundaries=(-6,6,-3,3)):
        '''
        Generates a sequence of 2D (x and z) target pairs that don't overlap

        Parameters
        ----------
        nblocks : int
            The number of ntarget pairs in the sequence.
        ntargets : int
            The number of unique targets (up to 9 maximum)
        boundaries: 4 element Tuple
            The limits of the allowed target locations (-x, x, -z, z)

        Returns
        -------
        [ntrials x ntargets x 3] array of target coordinates
        '''
        targets = np.array([
            [0, 0.5],
            [1, 0.5],
            [1, 0],
            [0, 0],
            [0.25, 0.25],
            [0.75, 0.25],
            [0.25, 0.75],
            [0.75, 0.75],
            [0.5, 1],
        ])
        rng = np.random.default_rng()
        for _ in range(nblocks):
            order = np.arange(ntargets) # target indices
            rng.shuffle(order)
            for t in range(ntargets):
                idx = order[t]
                pts = targets[idx]*((boundaries[1]-boundaries[0]),
                    (boundaries[3]-boundaries[2]))
                pts = pts+(boundaries[0], boundaries[2])
                pos = np.array([pts[0], 0, pts[1]])
                yield [idx], [pos]


class SequenceCapture(ScreenTargetCapture):

    '''
    This is a sequence task in which a 2nd target appears after subjects acquire the 1st target, and
    a 3rd target (additional target) appears while they are moving the cursor to the 2nd target.
    '''

    status = dict(
        wait = dict(start_trial="target"),
        target = dict(enter_target="hold", timeout="timeout_penalty", show_additional_target='additional_target'),
        additional_target = dict(enter_target="hold", timeout="timeout_penalty", enter_incorrect_target="incorrect_target_penalty"),
        hold = dict(leave_target="hold_penalty", hold_complete="delay"),
        delay = dict(leave_target="delay_penalty", delay_complete="targ_transition"),
        targ_transition = dict(trial_complete="reward", trial_abort="wait", trial_incomplete="target"),
        timeout_penalty = dict(timeout_penalty_end="targ_transition", end_state=True),
        hold_penalty = dict(hold_penalty_end="targ_transition", end_state=True),
        delay_penalty = dict(delay_penalty_end="targ_transition", end_state=True),
        incorrect_target_penalty = dict(incorrect_target_penalty_end="targ_transition", end_state=True),
        reward = dict(reward_end="wait", stoppable=False, end_state=True)
    )

    sequence_generators = ['out_2D_sequence','sequence_2D', 'centerout_2D_different_center']
    incorrect_target_penalty_time = traits.Float(1, desc="Length of penalty time for acquiring an incorrect target")
    random_target_appearance_dist = traits.Tuple((3.5, 3.5), desc="Another target appear when the cursor passed a certain distance from the 1st target in cm")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Instantiate the targets
        instantiate_targets = kwargs.pop('instantiate_targets', True)
        if instantiate_targets:

            # Need three targets for sequence task
            target1 = VirtualCircularTarget(target_radius=self.target_radius, target_color=target_colors[self.target_color])
            target2 = VirtualCircularTarget(target_radius=self.target_radius, target_color=target_colors[self.target_color])
            target3 = VirtualCircularTarget(target_radius=self.target_radius, target_color=target_colors[self.target_color])

            self.targets = [target1, target2, target3]

    #### STATE FUNCTIONS ####

    def _start_wait(self):
        '''
        Target apperance distance is sampled from the uniform distribution at the beginning of wait state.
        '''
        super()._start_wait()
        s, e = self.random_target_appearance_dist
        self.target_appearance_distance = random.uniform(s,e)

    def _start_delay(self):
        next_idx = (self.target_index + 1)
        if next_idx == 1 and next_idx < self.chain_length: # Delay period is only for the 2nd target
            target = self.targets[next_idx % self.chain_length]
            target.move_to_position(self.targs[next_idx])
            target.show()
            self.sync_event('TARGET_ON', self.gen_indices[next_idx])     
        else:
            # Don't sync anything when the 1st target and 3rd target appear
            pass

    def _start_targ_transition(self):
        if self.target_index == -1:

            # Came from a penalty state
            pass
        elif self.target_index + 1 < self.chain_length:

            # Hide the current target if there are more
            self.targets[self.target_index % self.chain_length].hide()
            self.sync_event('TARGET_OFF', self.gen_indices[self.target_index])

    def _start_additional_target(self):
        next_idx = (self.target_index + 1)
        target = self.targets[next_idx % self.chain_length]
        target.move_to_position(self.targs[next_idx])
        target.show()
        self.sync_event('TARGET_ON', self.gen_indices[next_idx])    

    def _start_incorrect_target_penalty(self):
        self._increment_tries()
        self.sync_event('OTHER_PENALTY') 
        # Hide targets
        for target in self.targets:
            target.hide()
            target.reset()

    def _end_incorrect_target_penalty(self):
        self.sync_event('TRIAL_END') 

    def _start_reward(self):
        self.targets[self.target_index % self.chain_length].cue_trial_end_success()
        self.sync_event('REWARD')

    #### TEST FUNCTIONS ####

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
        if self.target_index == 0: # the 1st target
            hold_state = time_in_state > self.hold_time
        elif self.target_index == self.chain_length-1: # the last target
            hold_state = time_in_state > self.hold_time
        else:
            hold_state = True
        return hold_state

    def _test_delay_complete(self, time_in_state):
        '''
        Test whether the delay period, when the cursor must stay in place
        while another target is being presented, is over. There should be 
        no delay on the last target in a chain.
        '''
        if self.target_index == 0:
            delay_state = time_in_state > self.delay_time
        else:
            delay_state = True # No delay period for the 3rd target
        return delay_state

    def _test_enter_incorrect_target(self, ts):
        cursor_pos = self.plant.get_endpoint_pos()
        d = np.linalg.norm(cursor_pos - self.targs[self.target_index+1]) # Measure distance between the cursor and the next target
        rad = self.target_radius - self.cursor_radius

        return d < rad   

    def _test_incorrect_target_penalty_end(self, time_in_state):
        return time_in_state > self.incorrect_target_penalty_time

    def _test_show_additional_target(self,ts):
        cursor_pos = self.plant.get_endpoint_pos()
        d = np.linalg.norm(cursor_pos - self.targs[self.target_index-1]) # Measure distance between the cursor and the previous target
        rad = self.target_radius - self.cursor_radius

        if self.chain_length < 3: # The 3rd targets isn't shown if chain_length is less than 3 (ex. standard center out task)
           additional_target_state = False
        elif self.target_index == 1: # Target_index == 1 is when the subject is moving the cursor to the 2nd target 
            additional_target_state = d > self.target_appearance_distance
        else:
            additional_target_state = False
        return additional_target_state


    #### Generator functions ####
    @staticmethod
    def out_2D_sequence(nblocks=100, distance=6.8):
        '''
        Generates a sequence of 2D (x and z) targets at a given distance from the origin
        The center target positions change depnding on the peripheral target at each trial
        The number of targets are fixed to 8.

        Parameters
        ----------
        nblocks : int
            The number of ntarget pairs in the sequence.
        distance : float
            The distance in cm between the center and peripheral targets.

        Returns
        -------
        [nblocks*ntargets x 1] array of tuples containing trial indices and [1 x 3] target coordinates

        '''
        ntargets = 8
        rng = np.random.default_rng()
        for _ in range(nblocks):
            order = np.arange(ntargets) + 1 # target indices, starting from 1
            rng.shuffle(order)
            for t in range(ntargets):
                idx = order[t]
                theta = 2*np.pi*(1-idx)/4 + np.pi/2 # put idx 1 at 12 o'clock
                print(theta)
                if idx <= 4:
                    pos = np.array([distance*np.cos(theta)+distance/2,0,distance*np.sin(theta)]).T
                elif idx >=5:
                    pos = np.array([distance*np.cos(theta)-distance/2,0,distance*np.sin(theta)]).T
                yield [idx], [pos]

    @staticmethod
    def centerout_2D_different_center(nblocks=100, distance=6.8):
        '''
        Pairs of a center target and a peripheral target. 
        The center target position changes depending on the periphetal target at each trial.
        The number of targets is fixed to 8.

        Returns
        -------
        [nblocks*ntargets x 1] array of tuples containing trial indices and [2 x 3] target coordinates
        '''
        ntargets = 8
        gen = SequenceCapture.out_2D_sequence(nblocks=nblocks, distance=distance)
        for _ in range(nblocks*ntargets):
            idx, pos = next(gen)
            targs = np.zeros([2, 3])
            if idx[0] <= 4:
                targs[0,:] = np.array([distance/2,0,0])
            else:
                targs[0,:] = np.array([-distance/2,0,0])
            targs[1,:] = pos[0]
            indices = np.zeros([2,1])
            indices[1] = idx
            yield indices, targs

    @staticmethod
    def sequence_2D(nblocks=100, distance=6.8):
        '''
        Pairs of the 1st, 2nd, and 3rd target for the sequence task.

        Returns
        -------
        [nblocks*ntargets x 1] array of tuples containing trial indices and [3 x 3] target coordinates
        '''
        ntargets = 8
        gen = SequenceCapture.out_2D_sequence(nblocks=nblocks, distance=distance)
        for _ in range(nblocks*ntargets):
            idx, pos = next(gen)
            targs = np.zeros([3, 3])
            indices = np.zeros([3,1])
            idx = idx[0]
            pos = pos[0]

            if idx >= 5:
                targs[0,:] = np.array([distance/2,0,0]).T
                indices[0] = 0 # The target for trial initiation is 0

                targs[1,:] = np.array([-distance/2,0,0]).T
                indices[1] = 4

                targs[2,:] = pos
                indices[2] = idx
            
            elif idx <= 4:
                targs[0,:] = np.array([-distance/2,0,0]).T
                indices[0] = 0 #The target for trial initiation is 0

                targs[1,:] = np.array([distance/2,0,0]).T
                indices[1] = 6

                targs[2,:] = pos            
                indices[2] = idx

            yield indices, targs


class HandConstrainedEyeCapture(ScreenTargetCapture):
    '''
    Saccade task with holding another target with hand. Subjects need to hold an initial target with their hand. 
    Then they need to fixate the first eye target and make a saccade for the second eye target 
    '''

    fixation_radius = traits.Float(2.5, desc="Distance from center that is considered a broken fixation")
    fixation_penalty_time = traits.Float(1.0, desc="Time in fixation penalty state")
    fixation_target_color = traits.OptionsList("cyan", *target_colors, desc="Color of the eye target under fixation state", bmi3d_input_options=list(target_colors.keys()))
    eye_target_color = traits.OptionsList("white", *target_colors, desc="Color of the eye target", bmi3d_input_options=list(target_colors.keys()))
    fixation_radius_buffer = traits.Float(.5, desc="additional radius for eye target")

    status = dict(
        wait = dict(start_trial="target"),
        target = dict(leave_target2="hold_penalty",timeout="timeout_penalty",enter_target="hold"),
        hold = dict(leave_target2="hold_penalty",leave_target="target", gaze_target="fixation"), # must hold an initial hand-target and eye-target
        fixation = dict(leave_target="delay_penalty",hold_complete="delay", fixation_break="fixation_penalty"), # must hold an initial hand-target and eye-target to initiate a trial
        delay = dict(leave_target="delay_penalty", delay_complete="targ_transition", fixation_break="fixation_penalty"),
        targ_transition = dict(trial_complete="reward", trial_abort="wait", trial_incomplete="target"),
        timeout_penalty = dict(timeout_penalty_end="targ_transition", end_state=True),
        hold_penalty = dict(hold_penalty_end="targ_transition", end_state=True),
        delay_penalty = dict(delay_penalty_end="targ_transition", end_state=True),
        fixation_penalty = dict(fixation_penalty_end="targ_transition",end_state=True),
        reward = dict(reward_end="wait", stoppable=False, end_state=True)
    )
 
    sequence_generators = ['row_target','sac_hand_2d']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Instantiate the targets
        instantiate_targets = kwargs.pop('instantiate_targets', True)
        if instantiate_targets:

            # Target 1 and 2 are for saccade. Target 3 is for hand
            target1 = VirtualCircularTarget(target_radius=self.fixation_radius, target_color=target_colors[self.eye_target_color])
            target2 = VirtualCircularTarget(target_radius=self.fixation_radius, target_color=target_colors[self.eye_target_color])
            target3 = VirtualCircularTarget(target_radius=self.target_radius, target_color=target_colors[self.target_color])

            self.targets = [target1, target2]
            self.targets_hand = [target3]
        
    def _parse_next_trial(self):
        '''Check that the generator has the required data'''
        self.gen_indices, self.targs = self.next_trial # 2 target positions for hand and eye

        # Update the data sinks with trial information
        self.trial_record['trial'] = self.calc_trial_num() # TODO save both eye and hand target positions
        for i in range(len(self.gen_indices)):
            self.trial_record['index'] = self.gen_indices[i]
            self.trial_record['target'] = self.targs[i]
            self.sinks.send("trials", self.trial_record)

    def _test_gaze_target(self,ts):
        '''
        Check whether eye positions from a target are within the fixation distance
        '''
        # Distance of an eye position from a target position
        eye_pos = self.calibrated_eye_pos
        target_pos = np.delete(self.targs[self.target_index],1)
        d_eye = np.linalg.norm(eye_pos - target_pos)
        return (d_eye <= self.fixation_radius + self.fixation_radius_buffer) or self.pause
        
    def _test_fixation_break(self,ts):
        '''
        Triggers the fixation_penalty state when eye positions are outside fixation distance
        '''
        # Distance of an eye position from a target position
        eye_pos = self.calibrated_eye_pos
        target_pos = np.delete(self.targs[self.target_index],1)
        d_eye = np.linalg.norm(eye_pos - target_pos)
        return (d_eye > self.fixation_radius + self.fixation_radius_buffer) or self.pause
    
    def _test_fixation_penalty_end(self,ts):
        return (ts > self.fixation_penalty_time)
    
    def _test_enter_target(self, ts):
        '''
        return true if the distance between center of cursor and target is smaller than the cursor radius
        '''
        cursor_pos = self.plant.get_endpoint_pos()
        d = np.linalg.norm(cursor_pos - self.targs[-1]) # hand must be within the initial target
        return d <= (self.target_radius - self.cursor_radius) or self.pause

    def _test_leave_target(self, ts):
        '''
        return true if cursor moves outside the exit radius
        '''
        cursor_pos = self.plant.get_endpoint_pos()
        d = np.linalg.norm(cursor_pos - self.targs[-1]) # hand must be within the initial target
        return d > (self.target_radius - self.cursor_radius) or self.pause

    def _test_leave_target2(self, ts):
        '''
        return true if cursor moves outside the exit radius (This is for the second target state)
        '''
        if self.target_index > 0:
            cursor_pos = self.plant.get_endpoint_pos()
            d = np.linalg.norm(cursor_pos - self.targs[-1]) # hand must be within the initial target
            return d > (self.target_radius - self.cursor_radius) or self.pause
    
    def _start_wait(self):
        super()._start_wait()
        # Redefine chain length because targs in this task has both eye and hand targets
        self.chain_length = len(self.targets)

        # Initialize fixation state
        self.num_hold_state = 0

        if self.calc_trial_num() == 0:

            # Instantiate the targets here so they don't show up in any states that might come before "wait"
            for target in self.targets:
                for model in target.graphics_models:
                    self.add_model(model)
                    target.hide()

            for target in self.targets_hand:
                for model in target.graphics_models:
                    self.add_model(model)
                    target.hide()

    def _start_target(self):
        if self.num_hold_state == 0:
            self.target_index += 1 # target index shouldn't be incremented after hold break loop

            # Show target if it is hidden (this is the first target, or previous state was a penalty)
            target_hand = self.targets_hand[0]
            if self.target_index == 0:
                target_hand.move_to_position(self.targs[-1])
                target_hand.show()
                self.sync_event('TARGET_ON', self.gen_indices[-1])
                
        else:
            target = self.targets[self.target_index % 2]
            target.hide() # hide hand target
            self.sync_event('EYE_TARGET_OFF', self.gen_indices[self.target_index % 2])

    def _start_hold(self):
        #self.sync_event('CURSOR_ENTER_TARGET', self.gen_indices[self.target_index])
        self.num_hold_state = 1

        # Show target if it is hidden (this is the first target, or previous state was a penalty)
        target = self.targets[self.target_index % 2]
        if self.target_index == 0:
            target.move_to_position(self.targs[self.target_index])
            target.show()
            self.sync_event('EYE_TARGET_ON', self.gen_indices[self.target_index])

    def _start_fixation(self):
        self.num_hold_state = 0
        self.targets[self.target_index].sphere.color = target_colors[self.fixation_target_color] # change target color in fixation state
        self.sync_event('FIXATION', self.gen_indices[self.target_index])

    def _while_fixation(self):
        pass

    def _end_fixation(self):
        pass

    def _start_delay(self):
        # Make next target visible unless this is the final target in the trial
        next_idx = (self.target_index + 1)
        if next_idx < self.chain_length:
            target = self.targets[next_idx % 2]
            target.move_to_position(self.targs[next_idx % 2])
            target.show()
            self.sync_event('EYE_TARGET_ON', self.gen_indices[next_idx % 2])
        else:
            # This delay state should only last 1 cycle, don't sync anything
            pass

    def _start_targ_transition(self):
        if self.target_index == -1:

            # Came from a penalty state
            pass
        elif self.target_index + 1 < self.chain_length:

            # Hide the current target if there are more
            self.targets[self.target_index % 2].hide()
            self.sync_event('EYE_TARGET_OFF', self.gen_indices[self.target_index])

    def _start_timeout_penalty(self):
        super()._start_timeout_penalty()
        self.num_hold_state = 0
        for target in self.targets_hand:
            target.hide()
            target.reset()
            
    def _start_hold_penalty(self):
        super()._start_hold_penalty()
        self.num_hold_state = 0
        # Hide targets
        for target in self.targets_hand:
            target.hide()
            target.reset()

    def _start_delay_penalty(self):
        super()._start_delay_penalty()
        # Hide targets
        for target in self.targets_hand:
            target.hide()
            target.reset()

    def _start_fixation_penalty(self):
        self._increment_tries()
        self.sync_event('FIXATION_PENALTY') 

        # Hide targets
        for target in self.targets:
            target.hide()
            target.reset()

        for target in self.targets_hand:
            target.hide()
            target.reset()

    def _end_fixation_penalty(self):
        self.sync_event('TRIAL_END')

    def _start_reward(self):
        super()._start_reward()
        # Hide targets
        for target in self.targets_hand:
            target.hide()
            target.reset()        

    # Generator functions
    @staticmethod
    def row_target(nblocks=20, ntargets=3, dx=5.,offset1=(0,0,-2),offset2=(0,0,6.),offset3=(0,0,-7.5),origin=(0,0,0),seed=0):
        '''
        Generates a sequence of 3D for 2 eye targets and 1 hand target at a given distance from the origin

        Parameters
        ----------
        nblocks : int
            The number of ntarget pairs in the sequence.
        ntargets : int
            The number of equally spaced targets
        distance : float
            The distance in cm between targets
        offset1 : 3-tuple
            y location of the first eye target
        offset2 : 3-tuple
            y location of the second eye target
        offset3 : 3-tuple
            y location of the hand target
        origin : 3-tuple
            Location of the central targets

        Returns
        -------
        [nblocks*ntargets x 1] array of tuples containing trial indices and [1 x 3] target coordinates

        '''
        rng = np.random.default_rng(seed=seed)
        for _ in range(nblocks):
            order = np.arange(ntargets**3)
            rng.shuffle(order)
            x_pos_candidate = [-dx,0,dx]
            for t in range(ntargets**3):
                idx = np.base_repr(order[t],3).zfill(3) # convert a decimal number to ternary

                # Target index for hand target, initial eye target, final eye target
                idx1 = int(idx[0])
                idx2 = int(idx[1])
                idx3 = int(idx[2])

                # Get positions for each target
                x_pos1 = x_pos_candidate[idx1]
                x_pos2 = x_pos_candidate[idx2]
                x_pos3 = x_pos_candidate[idx3]
                pos1 = np.array([x_pos1,0,0]).T
                pos2 = np.array([x_pos2,0,0]).T
                pos3 = np.array([x_pos3,0,0]).T

                yield [idx1],[idx2],[idx3],[pos1+offset1+origin],[pos2+offset2+origin],[pos3+offset3+origin]

    @staticmethod
    def sac_hand_2d(nblocks=20, ntargets=3, dx=10,offset1=(0,0,-2),offset2=(0,0,6.),offset3=(0,0,-7.5),origin=(0,0,0),seed=0):
        '''
        Pairs of hand targets and eye targets

        Returns
        -------
        [nblocks*ntargets x 1] array of tuples containing trial indices and [3 x 3] target coordinates
        '''

        gen = HandConstrainedEyeCapture.row_target(nblocks=nblocks,ntargets=ntargets,dx=dx,offset1=offset1,offset2=offset2,offset3=offset3,origin=origin,seed=seed)
        for _ in range(nblocks*(ntargets**3)):
            idx1,idx2,idx3,pos1,pos2,pos3 = next(gen)

            targs = np.zeros([3, 3])
            targs[0,:] = pos1[0]
            targs[1,:] = pos2[0]
            targs[2,:] = pos3[0]

            indices = np.zeros([3,1])
            indices[0] = idx1[0]
            indices[1] = idx2[0] + ntargets
            indices[2] = idx3[0]

            yield indices, targs


class ScreenTargetCapture_Saccade(ScreenTargetCapture):
    '''
    Center-out saccade task. The controller for the cursor position is eye position.
    Hand cursor is also visible. You should remove the hand cursor by setting cursor_radius to 0 as needed.
    '''

    fixation_radius_buffer = traits.Float(.5, desc="additional radius for eye target")
    target_color = traits.OptionsList("white", *target_colors, desc="Color of the target", bmi3d_input_options=list(target_colors.keys()))
    fixation_target_color = traits.OptionsList("cyan", *target_colors, desc="Color of the eye target under fixation state", bmi3d_input_options=list(target_colors.keys()))

    def _test_enter_target(self, ts):
        '''
        Check whether eye positions from a target are within the fixation distance
        '''
        # Distance of an eye position from a target position
        eye_pos = self.calibrated_eye_pos
        target_pos = np.delete(self.targs[self.target_index],1)
        d_eye = np.linalg.norm(eye_pos - target_pos)
        return (d_eye <= self.target_radius + self.fixation_radius_buffer) or self.pause

    def _test_leave_target(self, ts):
        '''
        Check whether eye positions from a target are outside the fixation distance
        '''
        # Distance of an eye position from a target position
        eye_pos = self.calibrated_eye_pos
        target_pos = np.delete(self.targs[self.target_index],1)
        d_eye = np.linalg.norm(eye_pos - target_pos)
        return (d_eye > self.target_radius + self.fixation_radius_buffer) or self.pause
    
    def _start_hold(self):
        super()._start_hold()
        self.targets[self.target_index].sphere.color = target_colors[self.fixation_target_color] # change target color in fixating the target