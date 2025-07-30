from .pyeCubeStream import eCubeStream
import numpy as np
import time
from .file import *
import aopy
from riglib.source import DataSourceSystem

'''
eCube streaming sources
'''

analog_voltsperbit = 3.0517578125e-4
headstage_voltsperbit = 1.907348633e-7
TRIG_THRESH = 2.5

def multi_chan_generator(data_block, channels, downsample=1):
    for idx in range(len(channels)):
        yield (channels[idx], data_block[::downsample,idx]) # yield one channel at a time

class Broadband(DataSourceSystem):
    '''
    Wrapper class for pyecubestream compatible with using in DataSource for
    buffering neural data. Compatible with riglib.source.MultiChanDataSource
    '''
    # Required by DataSourceSystem: update_freq and dtype (see make() below)
    update_freq = 25000.
    dtype = np.dtype('float')

    def __init__(self, headstage=7, channels=[1]):
        '''
        Constructor for ecube.Broadband

        Inputs:
            headstages int: headstage number (1-indexed)
            channels [int array]: channel list (1-indexed)
        '''
        # Initialize the servernode-control connection
        self.conn = eCubeStream(debug=False)
        self.headstage = headstage
        self.channels = channels

    def start(self):
        print("Starting ecube streaming datasource...")

        # Remove all existing sources
        subscribed = self.conn.listadded()
        if len(subscribed[0]) > 0:
            self.conn.remove(('Headstages', self.headstage))
        if len(subscribed[1]) > 0:
            self.conn.remove(('AnalogPanel',))
        if len(subscribed[2]) > 0:
            self.conn.remove(('DigitalPanel',))

        # Add the requested headstage channels if they are available
        available = self.conn.listavailable()[0][self.headstage-1] # (headstages, analog, digital); hs are 1-indexed
        for ch in self.channels:
            if ch > available:
                raise RuntimeError('requested channel {} is not available ({} connected)'.format(
                    ch, available))
            self.conn.add(('Headstages', self.headstage, (ch, ch))) # add channels one at a time
        subscribed = self.conn.listadded() # in debug mode this prints out the added channels

        # Start streaming
        self.conn.start()

        # Start with an empty generator
        self.gen = iter(())

        # Call get once to make sure we have the right channels
        data_block = self.conn.get()
        assert data_block[1] == "Headstages"
        assert data_block[2].shape[1] == len(self.channels)
        print(f"Started streaming from ecube, packet size {data_block[2].shape[0]}")
    
    def stop(self):

        # Stop streaming
        if not self.conn.stop():
            del self.conn # try to force the streaming to end by deleting the ecube connection object
            self.conn = eCubeStream(debug=True)

        # Remove the added sources
        self.conn.remove(('Headstages', self.headstage))
        
    def get(self):
        '''data
        Retrieve a packet from the server
        '''
        try:
            return next(self.gen)
        except StopIteration:
            data_block = self.conn.get() # in the form of (time_stamp, data_source, data_content)
            # while data_block[1] != "Headstages":
            #     data_block = self.conn.get() # ideally this shouldn't happen.
            self.gen = multi_chan_generator(data_block[2], self.channels)
            return next(self.gen)

class LFP(Broadband):
    '''
    Downsample the incoming data to 1000Hz. Compatible with riglib.source.MultiChanDataSource
    '''

    update_freq = 1000.

    def get(self):
        '''data
        Retrieve a packet from the server
        '''
        try:
            return next(self.gen)
        except StopIteration:
            data_block = self.conn.get() # in the form of (time_stamp, data_source, data_content)
            self.gen = multi_chan_generator(data_block[2], self.channels, downsample=25)
            return next(self.gen)

class Digital(Broadband):
    '''
    Wrapper class for pyecubestream compatible with using in DataSource for
    buffering digital data. Compatible with riglib.source.MultiChanDataSource
    '''
    # Required by DataSourceSystem: update_freq and dtype (see make() below)
    update_freq = 25000.
    dtype = np.dtype('bool')

    def __init__(self, channels=[1]):
        '''
        Inputs:
            channels [int array]: channel list (1-indexed)
        '''
        # Initialize the servernode-control connection
        self.conn = eCubeStream(debug=False)
        self.channels = channels

    def start(self):
        # Remove all existing sources
        subscribed = self.conn.listadded()
        if len(subscribed[0]) > 0:
            self.conn.remove(('Headstages', self.headstage))
        if len(subscribed[1]) > 0:
            self.conn.remove(('AnalogPanel',))
        if len(subscribed[2]) > 0:
            self.conn.remove(('DigitalPanel',))

        # Add the requested headstage channels if they are available
        available = self.conn.listavailable()[2] # (headstages, analog, digital)
        for ch in self.channels:
            if ch > available:
                raise RuntimeError('requested channel {} is not available ({} connected)'.format(
                    ch, available))
            self.conn.add(('DigitalPanelAsChans', (ch, ch))) # add channels one at a time
        subscribed = self.conn.listadded() # in debug mode this prints out the added channels

        # Start streaming
        self.conn.start()

        # Start with an empty generator
        self.gen = iter(())

        # Call get once to make sure we have the right channels
        data_block = self.conn.get()
        assert data_block[1] == "DigitalPanelAsChans"
        assert data_block[2].shape[1] == len(self.channels)
        print(f"Started streaming from ecube, packet size {data_block[2].shape[0]}")
    
    def stop(self):

        # Stop streaming
        if not self.conn.stop():
            del self.conn # try to force the streaming to end by deleting the ecube connection object
            self.conn = eCubeStream(debug=True)

        # Remove the added sources
        self.conn.remove(('DigitalPanelAsChans',))

class Analog(Broadband):
    '''
    Wrapper class for pyecubestream compatible with using in DataSource for
    buffering analog data. Compatible with riglib.source.MultiChanDataSource
    '''

    def __init__(self, channels=[1]):
        '''
        Inputs:
            channels [int array]: channel list (1-indexed)
        '''
        # Initialize the servernode-control connection
        self.conn = eCubeStream(debug=False)
        self.channels = channels

    def start(self):
        # Remove all existing sources
        subscribed = self.conn.listadded()
        if len(subscribed[0]) > 0:
            self.conn.remove(('Headstages', self.headstage))
        if len(subscribed[1]) > 0:
            self.conn.remove(('AnalogPanel',))
        if len(subscribed[2]) > 0:
            self.conn.remove(('DigitalPanel',))

        # Add the requested headstage channels if they are available
        available = self.conn.listavailable()[1] # (headstages, analog, digital)
        for ch in self.channels:
            if ch > available:
                raise RuntimeError('requested channel {} is not available ({} connected)'.format(
                    ch, available))
            self.conn.add(('AnalogPanel', (ch, ch))) # add channels one at a time
        subscribed = self.conn.listadded() # in debug mode this prints out the added channels

        # Start streaming
        self.conn.start()

        # Start with an empty generator
        self.gen = iter(())

        # Call get once to make sure we have the right channels
        data_block = self.conn.get()
        assert data_block[1] == "AnalogPanel"
        assert data_block[2].shape[1] == len(self.channels)
        print(f"Started streaming from ecube, packet size {data_block[2].shape[0]}")
    
    def stop(self):

        # Stop streaming
        if not self.conn.stop():
            del self.conn # try to force the streaming to end by deleting the ecube connection object
            self.conn = eCubeStream(debug=True)

        # Remove the added sources
        self.conn.remove(('AnalogPanel',))

class File(DataSourceSystem):
    '''
    Wrapper class for pyecubestream compatible with using in DataSource for
    buffering neural data. Compatible with riglib.source.MultiChanDataSource
    '''
    # Required by DataSourceSystem: update_freq and dtype (see make() below)
    update_freq = 1000.
    chunksize = 728
    dtype = np.dtype('float')

    def __init__(self, ecube_bmi_filename, channels):

        # Open the file
        self.channels = channels
        zero_idx_channels = [ch-1 for ch in channels]
        self.file = aopy.data.load_ecube_data_chunked(ecube_bmi_filename, "Headstages", channels=zero_idx_channels, chunksize=self.chunksize)

    def get(self):
        '''data
        Read a "packet" worth of data from the file
        '''
        try:
            return next(self.gen)
        except (StopIteration, AttributeError):
            time.sleep(1./(25000/self.chunksize))
            try:
                data_block = next(self.file)
            except StopIteration:
                data_block = np.zeros((int(728/25),1))
            self.gen = multi_chan_generator(data_block, self.channels, downsample=25)
            return next(self.gen)

class LFP_Plus_Trigger(DataSourceSystem):
    '''
    Adds a single analog trigger as channel 0. Compatible with riglib.source.MultiChanDataSource
    '''
    # Required by DataSourceSystem: update_freq and dtype (see make() below)
    update_freq = 1000.
    dtype = np.dtype('float')

    def __init__(self, headstage=7, trigger_ach=0, channels=[1], trig_included_in_channels=False):
        '''
        Constructor for ecube.Broadband
        Inputs:
            headstages int: headstage number (1-indexed)
            channels [int array]: channel list (1-indexed)
        '''
        # Initialize the servernode-control connection
        self.conn = eCubeStream(debug=False)
        self.headstage = headstage
        self.trig_channel = trigger_ach
        if trig_included_in_channels:
            self.channels = channels[1:]
        else:
            self.channels = channels

    def start(self):
        print("Starting ecube streaming datasource...")

        # Remove all existing sources
        subscribed = self.conn.listadded()
        if len(subscribed[0]) > 0:
            self.conn.remove(('Headstages', self.headstage))
        if len(subscribed[1]) > 0:
            self.conn.remove(('AnalogPanel',))
        if len(subscribed[2]) > 0:
            self.conn.remove(('DigitalPanel',))

        # Add the requested headstage channels if they are available
        available = self.conn.listavailable()[0][self.headstage-1] # (headstages, analog, digital); hs are 1-indexed
        for ch in self.channels:
            if ch > available:
                raise RuntimeError('requested channel {} is not available ({} connected)'.format(
                    ch, available))
            self.conn.add(('Headstages', self.headstage, (ch, ch))) # add channels one at a time

        # Add the digital panel for triggering
        self.conn.add(('AnalogPanel', (self.trig_channel, self.trig_channel)))
        subscribed = self.conn.listadded() # in debug mode this prints out the added channels

        # Start streaming
        self.conn.start()

        # Start with an empty generator for the headstage channels
        self.gen = iter(())

    
    def stop(self):

        # Stop streaming
        if not self.conn.stop():
            del self.conn # try to force the streaming to end by deleting the ecube connection object
            self.conn = eCubeStream(debug=True)

        # Remove the added sources
        self.conn.remove(('Headstages', self.headstage))
        self.conn.remove(('AnalogPanel',))
        
    def get(self):
        '''data
        Retrieve a packet from the server
        '''
        try:
            return next(self.gen)
        except StopIteration:
            data_block = self.conn.get() # in the form of (time_stamp, data_source, data_content)
            if data_block[1] == "Headstages":
                self.gen = multi_chan_generator(data_block[2], self.channels, downsample=25)
                return next(self.gen)
            else:
                return 0, data_block[2][::25] # The trigger data
    
    

class LFP_Plus_Trigger_File(DataSourceSystem):
    '''
    Adds a single analog trigger as channel 0, but reading from file. Compatible with riglib.source.MultiChanDataSource
    '''
    # Required by DataSourceSystem: update_freq and dtype (see make() below)
    update_freq = 1000.
    chunksize = 728
    dtype = np.dtype('float')

    def __init__(self, channels, ecube_bmi_filename=None, trig_channel=0, trig_included_in_channels=False):
        
        if not ecube_bmi_filename:
            ecube_bmi_filename = "/Users/leoscholl/2023-10-10_BMI3D_te11503"

        # Open the file
        self.trig_channel = trig_channel
        if trig_included_in_channels:
            self.channels = channels[1:]
        else:
            self.channels = channels
        zero_idx_channels = [ch-1 for ch in self.channels]
        self.file = aopy.data.load_ecube_data_chunked(ecube_bmi_filename, "Headstages", channels=zero_idx_channels, chunksize=self.chunksize)
        self.trig_file = aopy.data.load_ecube_data_chunked(ecube_bmi_filename, "AnalogPanel", channels=[self.trig_channel], chunksize=self.chunksize)
        self.trig_flag = True
        
    def get(self):
        '''data
        Read a "packet" worth of data from the file
        '''
        try:
            return next(self.gen)
        except (StopIteration, AttributeError):
            time.sleep(1./(25000/self.chunksize))
            if self.trig_flag:
                try:
                    trig_chunk = next(self.trig_file)[::25]
                except StopIteration:
                    trig_chunk = np.zeros((int(728/25),1))
                self.trig_flag = False
                return 0, np.squeeze(trig_chunk)
            try:
                data_block = next(self.file)
                self.trig_flag = True
            except StopIteration:
                data_block = np.zeros((int(728/25),len(self.channels)))
            self.gen = multi_chan_generator(data_block, self.channels, downsample=25)
            return next(self.gen)
        
def map_channels_for_multisource(headstage_channels=[], analog_channels=[], digital_channels=[]):
    '''
    Utility to convert the channel numbers to the format used by the MultiSource class

    Args:
        headstage_channels (list): list of 1-indexed headstage channels
        analog_channels (list): list of 1-indexed analog channels
        digital_channels (list): list of 1-indexed digital channels

    Returns:
        np.array: channel numbers in the format used by the MultiSource class
    '''
    return np.concatenate((analog_channels, np.array(digital_channels)+32, np.array(headstage_channels)+96))

class MultiSource(DataSourceSystem):
    '''
    Adds all Analog, Digital and Broadband channels. Compatible with riglib.source.MultiChanDataSource.
    Because of the way the system is set up, Analog channels map from 1-32, Digital channels 
    from 33-96, and Broadband channels from 97- onwards. Use the mapping utility to convert channels.
    Not tested for use with BMI, as the latency is likely higher than streaming only broadband data.
    '''
    # Required by DataSourceSystem: update_freq and dtype (see make() below)
    update_freq = 25000.
    dtype = np.dtype('float')

    @classmethod
    def pre_init(cls, headstage=7, n_digital_channels=64, n_analog_channels=32, n_headstage_channels=256):
        '''
        Set up servernode with all the possible channels you want to use
        '''
        conn = eCubeStream(autoshutdown=False, debug=True)

        # Remove all existing sources
        subscribed = conn.listadded()
        if len(subscribed[0]) > 0:
            conn.remove(('Headstages', headstage))
        if len(subscribed[1]) > 0:
            conn.remove(('AnalogPanel',))
        if len(subscribed[2]) > 0:
            conn.remove(('DigitalPanel',))

        # Add all available channels
        conn.add(('Headstages', headstage, (1, n_headstage_channels)))
        conn.add(('AnalogPanel', (1, n_analog_channels)))
        conn.add(('DigitalPanelAsChans', (1, n_digital_channels)))

        subscribed = conn.listadded() # in debug mode this prints out the added channels

    def __init__(self, headstage=7, channels=[]):
        '''
        Inputs:
            headstages int: headstage number (1-indexed)
            channels [int array]: channel list (1-indexed) where channels 1-32 are analog, 
                33-96 are digital, and 97- are broadband channels
        '''
        self.conn = eCubeStream(autoshutdown=False, debug=True)
        channels = np.array(channels)
        self.analog_channels = (channels[channels <= 32]).astype(int).tolist()
        self.digital_channels = (channels[(channels > 32) & (channels <= 96)] - 32).astype(int).tolist()
        self.headstage = headstage
        self.headstage_channels = (channels[channels > 96] - 96).astype(int).tolist()
        headstage_sub, analog_sub, digital_sub = self.conn.listadded()
        assert np.all(headstage_sub[0] == self.headstage) # can't handle multiple headstages yet
        self.headstage_idx = np.isin(headstage_sub[1], self.headstage_channels)
        self.analog_idx = np.isin(analog_sub, self.analog_channels)
        self.digital_idx = np.isin(digital_sub, self.digital_channels)
        print('digital channels matched', np.sum(self.digital_idx))

    def start(self):
        print("Starting ecube streaming datasource...")
        self.conn.start()

        # Start with an empty generator
        self.gen = iter(())
        print('...started!')
    
    def stop(self):

        # Stop streaming
        if not self.conn.stop():
            del self.conn # try to force the streaming to end by deleting the ecube connection object
        
    def get(self):
        '''
        Retrieve a packet from the server
        '''
        try:
            return next(self.gen)
        except StopIteration:
            data_block = self.conn.get() # in the form of (time_stamp, data_source, data_content)
            if data_block[1] == "AnalogPanel":
                if np.sum(self.analog_idx):
                    self.gen = multi_chan_generator(data_block[2][:,self.analog_idx], self.analog_channels)
                else:
                    return self.get()
            elif data_block[1] == "DigitalPanel": # If you subscribe to all digital channels this happens
                if np.sum(self.digital_idx):
                    digital_data = aopy.utils.convert_digital_to_channels(data_block[2])[:,self.digital_channels]
                    self.gen = multi_chan_generator(digital_data, [ch+32 for ch in self.digital_channels])
                else:
                    return self.get()
            elif data_block[1] == "DigitalPanelAsChans":
                if np.sum(self.digital_idx):
                    self.gen = multi_chan_generator(data_block[2][:,self.digital_idx], [ch+32 for ch in self.digital_channels])
                else:
                    return self.get()
            elif data_block[1] == "Headstages":
                if np.sum(self.headstage_idx):
                    self.gen = multi_chan_generator(data_block[2][:,self.headstage_idx], [ch+96 for ch in self.headstage_channels])
                else:
                    return self.get()
            else:
                return self.get()
            return next(self.gen)
    
class MultiSource_File(DataSourceSystem):
    '''
    Adds digital, analog, and headstage data, but reading from file. Compatible with riglib.source.MultiChanDataSource
    '''
    # Required by DataSourceSystem: update_freq and dtype (see make() below)
    update_freq = 25000.
    chunksize = 728
    dtype = np.dtype('float')

    def __init__(self, channels, ecube_bmi_filename=None):
        
        if not ecube_bmi_filename:
            # ecube_bmi_filename = "/media/moor-data/raw/ecube/2024-03-04_BMI3D_te14929" # laser
            ecube_bmi_filename = "/media/moor-data/raw/ecube/2024-03-06_BMI3D_te15031" # mc
        # Open the file
        channels = np.array(channels)
        self.analog_channels = (channels[channels <= 32] - 1).astype('int')
        self.digital_channels = (channels[(channels > 32) & (channels <= 96)] - 33).astype('int')
        self.headstage_channels = (channels[channels > 96] - 97).astype('int')

        self.headstage_file = aopy.data.load_ecube_data_chunked(ecube_bmi_filename, "Headstages", channels=self.headstage_channels, chunksize=self.chunksize)
        self.analog_file = aopy.data.load_ecube_data_chunked(ecube_bmi_filename, "AnalogPanel", channels=self.analog_channels, chunksize=self.chunksize)
        self.digital_file = aopy.data.load_ecube_data_chunked(ecube_bmi_filename, "DigitalPanel", chunksize=self.chunksize)
        self.flag = "Headstages"
        self.gen = iter(())
        self.t0 = time.perf_counter()
        
    def _next_gen(self, file, channels):
        try:
            data_block = next(file)
        except StopIteration:
            data_block = np.zeros((int(self.chunksize),len(channels)))
        self.gen = multi_chan_generator(data_block, channels)
        return next(self.gen)

    def get(self):
        '''
        Read a "packet" worth of data from one of the files
        '''
        try:
            return next(self.gen)
        except (StopIteration, AttributeError):
            if self.flag == "Headstages" and len(self.headstage_channels) > 0:
                self.flag = "DigitalPanelAsChans"
                return self._next_gen(self.headstage_file, self.headstage_channels+97)
            elif self.flag == "Headstages":
                self.flag = "DigitalPanelAsChans"
            
            if self.flag == "DigitalPanelAsChans" and len(self.digital_channels) > 0:
                self.flag = "AnalogPanel"
                try:
                    # Special consideration for digital panel to convert bits to channels
                    data_block = next(self.digital_file)
                    data_block = aopy.utils.convert_digital_to_channels(data_block)[:,self.digital_channels]
                except StopIteration:
                    data_block = np.zeros((int(self.chunksize),len(self.digital_channels)))
                self.gen = multi_chan_generator(data_block, self.digital_channels+33)
                return next(self.gen)
            elif self.flag == "DigitalPanelAsChans":
                self.flag = "AnalogPanel"
            
            if self.flag == "AnalogPanel" and len(self.analog_channels) > 0:
                self.flag = "Headstages"
                while time.perf_counter() - self.t0 < 1./(25000/self.chunksize):
                    pass
                self.t0 = time.perf_counter()
                return self._next_gen(self.analog_file, self.analog_channels+1)
            elif self.flag == "AnalogPanel":
                self.flag = "Headstages"
                return self.get() # Try again
            

class LFP_Blanking(LFP_Plus_Trigger):
    '''
    Blanks LFP data in the interval when the trigger is on. Compatible with riglib.source.MultiChanDataSource.

    Limitation: only blanks one chunk at a time, so smaller chunks are better! But -- the analog panel stream
    arrives in more frequent 22-sample packets; once the headstage packets are that size then there is no 
    benefit to making the hs packets any smaller! 
    
    Warning: untested! Use at your own risk.
    '''

    blanking = 0
    headstage_buffer = []
    trig_buffer = []
    
    def get(self):
        '''data
        Retrieve a packet from the server
        '''
        try:
            return next(self.gen)        
        except StopIteration:
            data_block = self.conn.get() # in the form of (time_stamp, data_source, data_content)
            while data_block[1] != "Headstages": # new packet of trigger data
                self.trig_buffer = np.concatenate((self.trig_buffer, np.squeeze(data_block[2])), axis=0)
                data_block = self.conn.get() # in the form of (time_stamp, data_source, data_content)

            if len(self.trig_buffer) == 0:
                self.blanking = 1
            else:
                trig_chunk_volts = analog_voltsperbit*np.array(self.trig_buffer)
            if self.blanking:
                self.blanking -= 1
            elif (trig_chunk_volts[-1] > TRIG_THRESH and trig_chunk_volts[0] < TRIG_THRESH):
                self.blanking = 1
            elif (trig_chunk_volts[-1] < TRIG_THRESH and trig_chunk_volts[0] > TRIG_THRESH):
                self.blanking = 1
            self.trig_buffer = [] # reset the trigger accumulation

            if self.blanking:
                self.gen = multi_chan_generator(self.headstage_buffer, self.channels, downsample=25)
            else:
                self.headstage_buffer = data_block[2].copy() # save this good hs data for later if blanking is needed
                self.gen = multi_chan_generator(data_block[2], self.channels, downsample=25)
            return next(self.gen)


class LFP_Blanking_File(LFP_Plus_Trigger_File):
    '''
    Blanks LFP data in the interval when the trigger is on. Compatible with riglib.source.MultiChanDataSource
    '''

    blanking = 0
    headstage_buffer = []
    
    def get(self):
        '''data
        Read a "packet" worth of data from the file
        '''
        try:
            return next(self.gen)        
        except (StopIteration, AttributeError):
            time.sleep(1./(25000/self.chunksize))
            
            # Get a chunk of trigger data
            try:
                trig_chunk = next(self.trig_file)
            except StopIteration:
                trig_chunk = np.zeros((self.chunksize,))
            trig_chunk_volts = analog_voltsperbit*trig_chunk
            if self.blanking:
                self.blanking -= 1
            elif (trig_chunk_volts[-1] > TRIG_THRESH and trig_chunk_volts[0] < TRIG_THRESH):
                self.blanking = 1
            elif (trig_chunk_volts[-1] < TRIG_THRESH and trig_chunk_volts[0] > TRIG_THRESH):
                self.blanking = 1
                  
            # Get a chunk of hs data
            try:
                data_block = next(self.file)
            except StopIteration:
                data_block = np.zeros((self.chunksize,len(self.channels)))
                
            # Make the new generator and return the first channel
            if self.blanking:
                data_block = self.headstage_buffer.copy() # copy the last good headstage data for this channel
            else:
                self.headstage_buffer = data_block.copy() # save this good hs data for later if blanking is needed
            self.gen = multi_chan_generator(data_block, self.channels, downsample=25)
            return next(self.gen)
    
def make_source_class(cls, trigger_ach):
    
    def init(self, **kwargs):
        super(self.__class__, self).__init__(trigger_ach=trigger_ach, **kwargs)
        
    return type(cls.__name__, (cls,), dict(__init__=init))

# e.g.
# cls = make_source_class(LFP_Plus_Trigger, 17) # laser ch 2