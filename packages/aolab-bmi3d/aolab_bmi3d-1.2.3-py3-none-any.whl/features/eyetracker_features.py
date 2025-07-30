'''
Features for the eyetracker system
'''

import tempfile
import numpy as np
from riglib import calibrations
from riglib.experiment import traits
from riglib.gpio import ArduinoGPIO
from riglib.oculomatic import oculomatic
from riglib.pupillabs import utils
from built_in_tasks.target_graphics import *
from built_in_tasks.target_capture_task import ScreenTargetCapture
from riglib.stereo_opengl.primitives import AprilTag
from .peripheral_device_features import *

import aopy
import glob
import os

###### CONSTANTS
sec_per_min = 60

class EyeCalibration(traits.HasTraits):
    '''
    Calculates 'calibrated_eye_pos' from 'eye_pos' (added by EyeStreaming feature) by regressing previous
    recorded cursor position and eye position when cursor enters targets. Must specify taskid for calibration. 
    '''

    taskid_for_eye_calibration = traits.Int(0, desc="directory where hdf file lives")
    show_eye_pos = traits.Bool(False, desc="Whether to show eye positions")
    eye_target_calibration = traits.Bool(False, desc="Whether to regress eye positions against target positions")

    def __init__(self, *args, **kwargs): #, start_pos, calibration):
        super(EyeCalibration,self).__init__(*args, **kwargs)
        
        # proc_exp # preprocess cursor data only
        taskid = self.taskid_for_eye_calibration
        hdf_dir = '/storage/hdf'
        hdf_file = glob.glob(os.path.join(hdf_dir, f'*{taskid}*'))[0]
        ecube_file = glob.glob(f'/media/NeuroAcq/*{taskid}*')[0]
        files = {}
        files['hdf'] = hdf_file
        files['ecube'] = ecube_file
        print(files)

        if not self.keyboard_control:
            bmi3d_data, bmi3d_metadata = aopy.preproc.proc_exp(hdf_dir, files, 'hoge', 'hoge', overwrite=True, save_res=False)

            # load raw eye data
            # raw_eye_data, raw_eye_metadata = aopy.preproc.parse_oculomatic(hdf_dir, files, debug=False)
            eye_interp = aopy.data.get_interp_kinematics(bmi3d_data,bmi3d_metadata,datatype='eye',samplerate=bmi3d_metadata['cursor_interp_samplerate'])

            # calculate coefficients to calibrate eye data
            events = bmi3d_data['events']

            if not self.eye_target_calibration:
                self.eye_coeff,_,_,_ = aopy.preproc.calc_eye_calibration\
                    (bmi3d_data['cursor_interp'],bmi3d_metadata['cursor_interp_samplerate'],\
                    eye_interp[:,:4], bmi3d_metadata['cursor_interp_samplerate'],events['timestamp'], events['code'],return_datapoints=True)

            else:
                def get_target_locations(data, target_indices):

                    try:
                        trials = data['trials']
                    except:
                        trials = data['bmi3d_trials']
                    locations = np.nan*np.zeros((len(target_indices), 3))
                    for i in range(len(target_indices)):
                        trial_idx = np.where(trials['index'] == target_indices[i])[0]
                        if len(trial_idx) > 0:
                            locations[i,:] = trials['target'][trial_idx[0]][[0,2,1]] # use x,y,z format
                        else:
                            raise ValueError(f"Target index {target_indices[i]} not found")
                    return np.round(locations,4)

                target_pos = get_target_locations(bmi3d_data, [1,2,3,4,5,6,7,8])
                
                self.eye_coeff, _ = aopy.preproc.calc_eye_target_calibration(eye_interp[:,:4], \
                    bmi3d_metadata['cursor_interp_samplerate'], events['timestamp'], events['code'], target_pos)
            
            print("Calibration complete:", self.eye_coeff)

        # Set up eye cursor
        self.eye_cursor = VirtualCircularTarget(target_radius=.5, target_color=(0., 1., 0., 0.75))
        self.target_location = np.array(self.starting_pos).copy()
        self.calibrated_eye_pos = np.zeros((2,))*np.nan
        for model in self.eye_cursor.graphics_models:
            self.add_model(model)
        
    def init(self):
        self.add_dtype('calibrated_eye', 'f8', (2,))
        super().init()

    #### STATE FUNCTIONS ####
    def _start_wait(self):
        super()._start_wait()

        if self.calc_trial_num() == 0:
            if self.show_eye_pos:
                self.eye_cursor.show()
            else:
                self.eye_cursor.hide()

    def _cycle(self):
        self._update_eye_pos()

        # Do calibration
        ave_pos = self.eye_pos
        if not self.keyboard_control:
            calibrated_pos = aopy.postproc.get_calibrated_eye_data(self.eye_pos[:4],self.eye_coeff)
            ave_pos = np.array([(calibrated_pos[0] + calibrated_pos[2])/2, (calibrated_pos[1] + calibrated_pos[3])/2])
        
        # Save calibration
        self.calibrated_eye_pos = ave_pos
        self.task_data['calibrated_eye'] = ave_pos

        super(EyeStreaming, self)._cycle()

        # Move the eye cursor
        if np.any(np.isnan(self.calibrated_eye_pos)):
            pass
        else:
            self.eye_cursor.move_to_position([self.calibrated_eye_pos[0],0,self.calibrated_eye_pos[1]])
            if self.show_eye_pos:
                self.eye_cursor.show()


class EyeStreaming(traits.HasTraits):
    '''
    Adds eye_data streamed from oculomatic.
    '''

    keyboard_control = traits.Bool(False, desc="Whether to replace eye control with keyboard control")
    eye_labels = traits.Array(value=['le_x', 'le_y', 're_x', 're_y', 'le_diam', 're_diam'], desc="Description of eye data columns")

    hidden_traits = ['eye_labels']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Visualize eye positions
        if self.keyboard_control:
            self.eye_data = Eye([0,0])
            self.eye_pos = np.zeros((2,))*np.nan
        else:
            from riglib import source
            from riglib.oculomatic import System
            self.eye_data = source.DataSource(System)
            self.eye_pos = np.zeros((6,))*np.nan


    def init(self):
        if self.keyboard_control:
            self.add_dtype('eye', 'f8', (2,))
        else:
            self.add_dtype('eye', 'f8', (6,))
        super().init()

    def run(self):
        '''
        Code to execute immediately prior to the beginning of the task FSM executing, or after the FSM has finished running. 
        See riglib.experiment.Experiment.run(). This 'run' method starts the motiondata source and stops it after the FSM has finished running
        '''
        if not self.keyboard_control:
            self.eye_data.start()
        try:
            super().run()
        finally:
            if not self.keyboard_control:
                print("Stopping streaming eye data")
                self.eye_data.stop()

    def _update_eye_pos(self):
        if not self.keyboard_control:
            eye_pos = self.eye_data.get() # This is (n,6) array of new values since we last checked
            if eye_pos.ndim < 2 or eye_pos.size == 0:
                eye_pos = np.zeros((6,))*np.nan
            else:
                eye_pos = eye_pos[-1,:] # the most recent position
        else:
            eye_pos = self.eye_data.get() # A list of lists of of x,y keyboard pos
            eye_pos = eye_pos[0]
        self.eye_pos = eye_pos
        self.task_data['eye'] = eye_pos

    def _cycle(self):
        self._update_eye_pos()
        super()._cycle()


class EyeConstrained(ScreenTargetCapture):
    '''
    Add a penalty state when subjects looks away. Only tested in center-out task.
    '''

    fixation_dist = traits.Float(2.5, desc="Distance from center that is considered a broken fixation")
    fixation_penalty_time = traits.Float(0., desc="Time in fixation penalty state")
    fixation_target_color = traits.OptionsList("cyan", *target_colors, desc="Color of the center target under fixation state", bmi3d_input_options=list(target_colors.keys()))
    
    status = dict(
        wait = dict(start_trial="target"),
        target = dict(timeout="timeout_penalty",gaze_target="fixation"),
        fixation = dict(enter_target="hold", fixation_break="target"),
        hold = dict(leave_target="hold_penalty", hold_complete="delay", fixation_break="fixation_penalty"),
        delay = dict(leave_target="delay_penalty", delay_complete="targ_transition", fixation_break="fixation_penalty"),
        targ_transition = dict(trial_complete="reward", trial_abort="wait", trial_incomplete="target"),
        timeout_penalty = dict(timeout_penalty_end="targ_transition", end_state=True),
        hold_penalty = dict(hold_penalty_end="targ_transition", end_state=True),
        delay_penalty = dict(delay_penalty_end="targ_transition", end_state=True),
        fixation_penalty = dict(fixation_penalty_end="targ_transition",end_state=True),
        reward = dict(reward_end="wait", stoppable=False, end_state=True)
    )
 
    def _test_gaze_target(self,ts):
        '''
        Check whether eye positions are within the fixation distance
        Only apply this to the first target (1st target)
        '''
        if self.target_index <= 0:     
            d = np.linalg.norm(self.calibrated_eye_pos)
            return d < self.fixation_dist
        else:
            return True
        
    def _test_fixation_break(self,ts):
        '''
        Triggers the fixation_penalty state when eye positions are outside fixation distance
        Only apply this to the first hold and delay period
        '''
        if self.target_index <= 0:   
            d = np.linalg.norm(self.calibrated_eye_pos)
            return (d > self.fixation_dist) or self.pause
        else:
            return self.pause
    
    def _test_fixation_penalty_end(self,ts):
        # d = np.linalg.norm(self.calibrated_eye_pos)
        return (ts > self.fixation_penalty_time) # (d < self.fixation_dist) and 
    
    def _start_wait(self):
        super()._start_wait()
        self.num_fixation_state = 0 # Initializa fixation state

    def _start_target(self):
        if self.num_fixation_state == 0:
            super()._start_target() # target index shouldn't be incremented after fixation break loop
        else:
            self.sync_event('FIXATION', 0)
            self.targets[0].reset() # reset target color after fixation break

    def _start_fixation(self):
        self.num_fixation_state = 1
        self.targets[0].sphere.color = target_colors[self.fixation_target_color] # change target color in fixation state
        if self.target_index == 0:
            self.sync_event('FIXATION', 1)
    
    def _start_timeout_penalty(self):
        super()._start_timeout_penalty()
        self.num_fixation_state = 0

    def _start_hold(self):
        super()._start_hold()
        self.num_fixation_state = 0 # because target state comes again after hold state in a trial

    def _start_fixation_penalty(self):
        self._increment_tries()
        self.sync_event('FIXATION_PENALTY') 

        # Hide targets
        for target in self.targets:
            target.hide()
            target.reset()

    def _end_fixation_penalty(self):
        self.sync_event('TRIAL_END')

class PupilLabStreaming(traits.HasTraits):
    '''
    Adds eye_data from pupil labs. Optionally displays AprilTag markers on the screen for
    surface tracking. Requires a task with the Window feature enabled.
    '''

    surface_marker_size = traits.Float(2., desc="Size in cm of apriltag surface markers")
    surface_marker_count = traits.Int(0, desc="How many surface markers to draw")
    eye_labels = traits.Array(value=[
        'gaze_x', 'gaze_y', 'gaze_z', 
        'norm_x', 'norm_y', 
        'timestamp', 
        're_x', 're_y', 
        're_diam', 
        'le_x', 'le_y', 
        'le_diam'
        ], 
        desc="Description of eye data columns")

    hidden_traits = ['eye_labels']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add apriltag models
        centers = utils.calculate_square_positions(self.screen_half_height, self.window_size, 
                                                   self.surface_marker_count, self.surface_marker_size)
        for id, (x, z) in enumerate(centers):
            tag = AprilTag(id, self.surface_marker_size).translate(x, 0, z)
            self.add_model(tag)

        # Visualize eye positions
        from riglib import source
        from riglib.pupillabs import System, NoSurfaceTracking
        if self.surface_marker_count > 0:
            self.eye_data = source.DataSource(System)
        else:
            self.eye_data = source.DataSource(NoSurfaceTracking)
        self.eye_pos = np.zeros((8,))*np.nan

    def init(self):
        self.add_dtype('eye', 'f8', (12,))
        super().init()

    def run(self):
        '''
        Code to execute immediately prior to the beginning of the task FSM executing, or after the FSM has finished running. 
        See riglib.experiment.Experiment.run(). This 'run' method starts the motiondata source and stops it after the FSM has finished running
        '''
        self.eye_data.start()
        try:
            super().run()
        finally:
            print("Stopping streaming eye data")
            self.eye_data.stop()

    def _start_None(self):
        '''
        Code to run before the 'None' state starts (i.e., the task stops)
        '''
        self.eye_data.stop()
        super()._start_None()

    def _update_eye_pos(self):
        eye_pos = self.eye_data.get() # This is (n,11) array of new values since we last checked
        if eye_pos.ndim < 2 or eye_pos.size == 0:
            eye_pos = np.zeros((12,))*np.nan
        else:
            eye_pos = eye_pos[-1,:] # the most recent position
        self.eye_pos = eye_pos
        self.task_data['eye'] = eye_pos

    def _cycle(self):
        self._update_eye_pos()
        super()._cycle()

'''
Old code not currently used in aolab
'''
class EyeData(traits.HasTraits):
    '''
    Pulls data from the eyetracking system and make it available on self.eyedata
    '''
    def init(self):
        '''
        Secondary init function. See riglib.experiment.Experiment.init()
        Prior to starting the task, this 'init' sets up the 'eyedata' DataSource and registers it with the 
        SinkRegister so that the data gets saved to file as it is collected.
        '''
        from riglib import source
        from riglib import sink
        sink_manager = sink.SinkManager.get_instance()

        src, ekw = self.eye_source
        #f = open('/home/helene/code/bmi3d/log/eyetracker', 'a')
        self.eyedata = source.DataSource(src, **ekw)
        sink_manager.register(self.eyedata)
        f.write('instantiated source\n')
        super(EyeData, self).init()
        #f.close()
    
    @property
    def eye_source(self):
        '''
        Docstring

        Parameters
        ----------

        Returns
        -------
        '''
        from riglib import eyetracker
        return eyetracker.System, dict()

    def run(self):
        '''
        Code to execute immediately prior to the beginning of the task FSM executing, or after the FSM has finished running. 
        See riglib.experiment.Experiment.run(). This 'run' method starts the 'eyedata' source and stops it after the FSM has finished running
        '''
        #f = open('/home/helene/code/bmi3d/log/eyetracker', 'a')
        self.eyedata.start()
        #f.write('started eyedata\n')
        #f.close()
        try:
            super(EyeData, self).run()
        finally:
            self.eyedata.stop()
    
    def join(self):
        '''
        Docstring

        Parameters
        ----------

        Returns
        -------
        '''
        self.eyedata.join()
        super(EyeData, self).join()
    
    def _start_None(self):
        '''
        Docstring

        Parameters
        ----------

        Returns
        -------
        '''
        self.eyedata.pause()
        self.eyefile = tempfile.mktemp()
        print("retrieving data from eyetracker...")
        self.eyedata.retrieve(self.eyefile)
        print("Done!")
        self.eyedata.stop()
        super(EyeData, self)._start_None()
    
    def set_state(self, state, **kwargs):
        '''
        Docstring

        Parameters
        ----------

        Returns
        -------
        '''
        self.eyedata.sendMsg(state)
        super(EyeData, self).set_state(state, **kwargs)

    def cleanup(self, database, saveid, **kwargs):
        '''
        Docstring

        Parameters
        ----------

        Returns
        -------
        '''
        
        super(EyeData, self).cleanup(database, saveid, **kwargs)
        dbname = kwargs['dbname'] if 'dbname' in kwargs else 'default'
        if dbname == 'default':
            database.save_data(self.eyefile, "eyetracker", saveid)
        else:
            database.save_data(self.eyefile, "eyetracker", saveid, dbname=dbname)

class SimulatedEyeData(EyeData):
    '''Simulate an eyetracking system using a series of fixations, with saccades interpolated'''
    fixations = traits.Array(value=[(0,0), (-0.6,0.3), (0.6,0.3)], desc="Location of fixation points")
    fixation_len = traits.Float(0.5, desc="Length of a fixation")

    @property
    def eye_source(self):
        '''
        Docstring

        Parameters
        ----------

        Returns
        -------
        '''
        from riglib import eyetracker
        return eyetracker.Simulate, dict(fixations= self.fixations)

    def _cycle(self):
        '''
        Docstring
        basically, extract the data and do something with it


        Parameters
        ----------

        Returns
        -------
        '''
        #retrieve data
        data_temp = self.eyedata.get()

        #send the data to sinks
        if data_temp is not None:
            self.sinks.send(self.eyedata.name, data_temp)

        super(SimulatedEyeData, self)._cycle()

class CalibratedEyeData(EyeData):
    '''Filters eyetracking data with a calibration profile'''
    cal_profile = traits.Instance(calibrations.EyeProfile)

    def __init__(self, *args, **kwargs):
        '''
        Docstring

        Parameters
        ----------

        Returns
        -------
        '''
        super(CalibratedEyeData, self).__init__(*args, **kwargs)
        self.eyedata.set_filter(self.cal_profile)

class FixationStart(CalibratedEyeData):
    '''Triggers the start_trial event whenever fixation exceeds *fixation_length*'''
    fixation_length = traits.Float(2., desc="Length of fixation required to start the task")
    fixation_dist = traits.Float(50., desc="Distance from center that is considered a broken fixation")

    def __init__(self, *args, **kwargs):
        '''
        Docstring

        Parameters
        ----------

        Returns
        -------
        '''
        super(FixationStart, self).__init__(*args, **kwargs)
        self.status['wait']['fixation_break'] = "wait"
        self.log_exclude.add(("wait", "fixation_break"))
    
    def _start_wait(self):
        '''
        Docstring

        Parameters
        ----------

        Returns
        -------
        '''
        self.eyedata.get()
        super(FixationStart, self)._start_wait()

    def _test_fixation_break(self, ts):
        '''
        Docstring

        Parameters
        ----------

        Returns
        -------
        '''
        return (np.sqrt((self.eyedata.get()**2).sum(1)) > self.fixation_dist).any()
    
    def _test_start_trial(self, ts):
        '''
        Docstring

        Parameters
        ----------

        Returns
        -------
        '''
        return ts > self.fixation_length
