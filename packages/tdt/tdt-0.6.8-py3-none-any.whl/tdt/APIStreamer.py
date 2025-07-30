import threading
from threading import Lock
import time

import numpy as np

from .SynapseAPI import SynapseAPI

class APIStreamer:
    def __init__(self,
                host='localhost',
                gizmo='APIStreamerMC1',
                history_seconds=1,
                callback=None,
                verbose=True,
                time_array=200):
        
        self.syn = SynapseAPI(host)
        self.gizmo = gizmo
        self.history_seconds = history_seconds
        self.callback = callback
        self.verbose = verbose
        
        self.data_lock = Lock()
        
        self.data = np.zeros(1)
        self.ts = np.zeros(1)
        self.time_array = np.zeros(time_array)
        self.result = None
        
        if self.syn.getMode() >= 2:
            self.reset()
    
        self.threads = []
        self.t = threading.Thread(target=self.worker)
        self.t.start()
        self.threads.append(self.t)
    
    def update_values(self):
        vals = self.syn.getParameterValues(self.gizmo, 'mon', 4)
        self.curr_index = int(vals[0])
        self.curr_looptime = vals[1]
        self.curr_loop = int(vals[2])
        self.decimation = int(vals[3])
        
    def reset(self):
        if self.verbose:
            print(f"resetting {self.gizmo}")
        
        info = self.syn.getGizmoInfo(self.gizmo)
        if len(info) == 0:
            raise Exception(f"Couldn't find gizmo {self.gizmo}")
    
        # Set up variables, determine sampling rate
        samp_rates = self.syn.getSamplingRates()
        parent = self.syn.getGizmoParent(self.gizmo)
        
        vals = self.syn.getParameterValues(self.gizmo, 'mon', 6)
        
        self.nchan = int(vals[4])
        self.buff_size = int(vals[5])
        
        self.update_values()
        
        self.device_fs = samp_rates[parent]
        self.fs = self.device_fs / self.decimation
        
        if self.verbose:
            print(f"{self.gizmo}: {self.nchan} channels in {self.buff_size} sample buffer at {self.fs:.2f} Hz")
        
        self.sample_limit = np.floor(self.fs / 4)
        self.sample_limit = max(1000, self.sample_limit - np.mod(self.sample_limit, 1000))
        
        # Fetch the first data points and set up numpy memory buffer
        self.prev_index = self.curr_index
        
        with self.data_lock:
            self.data = np.zeros([self.nchan, int(np.round(self.history_seconds * self.fs))])
            self.ts = np.zeros(self.data.shape[1])
            self.result = None
    
    def get_data(self):
        if self.callback:
            return self.result
        else:
            with self.data_lock:
                return self.ts, self.data

    def worker(self):
        start = time.perf_counter()
        ind = 0
        while True:
            try:
                # Look for new data
                self.update_values()
                #print('curr:', self.curr_index, 'prev:', self.prev_index)
                self.new_data = None
                if self.curr_index != self.prev_index:
                    if self.curr_index > self.prev_index:
                        self.npts = self.curr_index - self.prev_index
                    elif self.prev_index > self.curr_index:
                        # buffer wrapped back to the beginning
                        # just read up until the end of the buffer this time around
                        self.npts = self.buff_size - self.prev_index
                    
                    self.npts = int(self.npts)
                    if self.nchan > 3:
                        self.npts -= self.npts % self.nchan
                        self.npts = np.round(min(self.npts, self.nchan * self.sample_limit))
                    else:
                        self.npts = np.round(min(self.npts, self.sample_limit))
                    
                    if self.nchan < 4:
                        self.new_data = np.zeros([self.nchan, self.npts])
                        for ch in range(self.nchan):
                            self.new_data[ch,:] = np.array(self.syn.getParameterValues(self.gizmo, f"data{ch+1}", self.npts, self.prev_index)).T
                        self.curr_time = (2 + self.prev_index + self.npts + self.curr_loop * self.buff_size) / self.device_fs
                    else:
                        self.new_data = np.array(self.syn.getParameterValues(self.gizmo, 'data', self.npts, self.prev_index)).reshape([-1, self.nchan]).T
                        self.curr_time = (2 + (self.prev_index + self.npts + self.curr_loop * self.buff_size) / self.nchan) / self.device_fs
                    
                    if self.new_data is not None:
                        with self.data_lock:
                            
                            if self.nchan > 3:
                                test_pts = self.new_data.shape[1]
                            else:
                                test_pts = self.npts
                            
                            if test_pts > self.data.shape[1]:
                                print('Warning: polling too slow, removing points')
                                self.data = self.new_data[:, -self.data.shape[1]:]
                            else:
                                self.data = np.roll(self.data, -test_pts, axis=1)
                                self.data[:, -test_pts:] = self.new_data
                            
                            self.ts = self.curr_time + np.arange(-self.data.shape[1], 0) / self.fs
                    
                    # DO PROCESSING HERE
                    if self.new_data is not None and self.callback is not None:
                        self.result = self.callback(self)
                    
                    # Update TDT buffer index variable for next loop
                    if self.new_data is not None:
                        self.prev_index += self.npts
                        if self.prev_index >= self.buff_size:
                            self.prev_index -= self.buff_size
            
            except:
                if self.syn.getMode() < 2:
                    print('Waiting for Synapse to enter run mode before continuing.')
                    while self.syn.getMode() < 2:
                        time.sleep(0.5)
                    self.reset()
            
            # Get/show delay stats
            if self.verbose:
                self.time_array = np.roll(self.time_array, -1)
                self.time_array[-1] = time.perf_counter() - start
                ind += 1
                if np.mod(ind, len(self.time_array)) == 0:
                    times = np.diff(self.time_array) * 1e3
                    print(f"{len(self.time_array)} data reads: max delay: {np.max(times):.2f} ms; min delay: {np.min(times):.2f} ms; mean: {np.mean(times):.2f} ms")

    def __del__(self):
        for t in self.threads:
            t.do_run = False
            t.join()
    
if __name__ == '__main__':
    s = APIStreamer()
