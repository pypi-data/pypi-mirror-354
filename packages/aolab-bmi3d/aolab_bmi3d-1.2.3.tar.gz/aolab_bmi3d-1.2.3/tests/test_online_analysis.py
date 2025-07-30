import time
from riglib import experiment
from analysis import online_analysis
from features.debug_features import OnlineAnalysis, ReplayCursor, ReplayEye
from features.peripheral_device_features import MouseControl
from built_in_tasks.manualcontrolmultitasks import ManualControl
from riglib.stereo_opengl.window import Window2D
import unittest
import numpy as np
import os
import threading

class TestOnlineAnalysis(unittest.TestCase):

    @unittest.skip("")
    def test_manual_run(self):

        analysis = online_analysis.OnlineDataServer('localhost', 5000)

        Exp = experiment.make(experiment.Experiment, feats=[OnlineAnalysis])
        exp = Exp(fps=1, session_length=5, online_analysis_ip='localhost', online_analysis_port=5000)
        print(exp.dtype)
        exp.init()

        t0 = time.time()
        while time.time() - t0 < 2:
            analysis.update()
        print('done updating')
        self.assertEqual(analysis.task_params['experiment_name'], 'Experiment')

        threading.Thread(target=exp.run).start()
        time.sleep(1)

        while True:
            if not analysis.update():
                break
        self.assertTrue(analysis.is_running)
        self.assertFalse(analysis.is_completed)
        self.assertEqual(analysis.state, 'wait')

        time.sleep(6)
        while True:
            if not analysis.update():
                break
        self.assertTrue(analysis.is_completed)
        self.assertFalse(analysis.is_running)
        self.assertEqual(analysis.state, None)

        analysis._stop()

    @unittest.skip("")
    def test_threaded(self):

        analysis = online_analysis.OnlineDataServer('localhost', 5000)

        # Start exp 1
        Exp = experiment.make(experiment.Experiment, feats=[OnlineAnalysis])
        exp = Exp(fps=10, session_length=18, online_analysis_ip='localhost', online_analysis_port=5000)
        print(exp.dtype)
        exp.init()

        # Start analysis
        analysis.start()
        time.sleep(1)
        exp.run()

        # Wrap up
        analysis.stop()
        analysis.join()

    def test_cursor(self):

        analysis = online_analysis.OnlineDataServer('localhost', 5000)

        # Load replay data
        import tables
        test_dir = os.path.dirname(os.path.abspath(__file__))
        hdf_filepath = os.path.join(test_dir, 'test_data/beig20240419_21_te16793.hdf')
        with tables.open_file(hdf_filepath, 'r') as f:
            task = f.root.task.read()
            trial = f.root.trials.read()
        targets = []
        for trial in trial:
            trial_num = trial['trial']
            if len(targets) <= trial_num:
                targets.append(([],[]))
            targets[trial_num][0].append(trial['index'])
            targets[trial_num][1].append(trial['target'])
        cursor = task['cursor']
        eye = task['eye']

        # Start exp 1
        os.environ['DISPLAY'] = ':0.0'
        seq = targets
        Exp = experiment.make(ManualControl, feats=[Window2D, ReplayCursor, ReplayEye, OnlineAnalysis])
        exp = Exp(seq, fps=120, session_length=28, online_analysis_ip='localhost', online_analysis_port=5000,
                  fullscreen=False, window_size=(800,600), replay_cursor_data=cursor,
                  replay_eye_data=eye, wait_time=0)

        print(exp.dtype)
        exp.init()

        # Start analysis
        analysis.start()
        exp.run()

        # Wrap up
        analysis.stop()
        analysis.join()



if __name__ == '__main__':
    unittest.main()