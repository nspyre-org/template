"""
This is example script demonstrates most of the basic functionality of nspyre.
"""
import time

import numpy as np
from nspyre import DataSource
from nspyre import InstrumentGateway
from nspyre import experiment_widget_process_queue
from nspyre import StreamingList

class SpinMeasurements:
    """Perform spin measurements."""

    def odmr_sweep(self, dataset: str, start_freq: float, stop_freq: float, num_points: int, iterations: int, msg_queue=None):
        """Run a fake ODMR (optically detected magnetic resonance) PL (photoluminescence) sweep over a set of microwave frequencies.

        Args:
            dataset: name of the dataset to push data to
            start_freq (float): start frequency
            stop_freq (float): stop frequency
            num_points (int): number of points between start-stop (inclusive)
            iterations: number of times to repeat the experiment
            msg_queue: an optional multiprocessing message Queue object used for interprocess communication
        """

        # connect to the instrument server
        # connect to the data server and create a data set, or connect to an
        # existing one with the same name if it was created earlier.
        with InstrumentGateway() as gw, DataSource(dataset) as odmr_data:
            # set the signal generator amplitude for the scan (dBm).
            gw.drv.set_amplitude(6.5)
            gw.drv.set_output_en(True)

            # frequencies that will be swept over in the ODMR measurement
            frequencies = np.linspace(start_freq, stop_freq, num_points)

            # for storing the experiment data
            # list of numpy arrays of shape (2, num_points)
            sweep_list = StreamingList([])
            for i in range(iterations):
                # photon counts corresponding to each frequency
                # initialize to NaN
                counts = np.empty(num_points)
                counts[:] = np.nan
                sweep_list.append(np.stack([frequencies/1e9, counts]))

                # sweep counts vs. frequency.
                for f, freq in enumerate(frequencies):
                    # access the signal generator driver on the instrument server and set its frequency.
                    gw.drv.set_frequency(freq)
                    # read the number of photon counts received by the photon counter.
                    sweep_list[-1][1][f] = gw.drv.cnts(0.02)
                    # notify the streaminglist that this entry has updated so it will be pushed to the data server
                    sweep_list.updated_item(len(sweep_list)-1)

                    # save the current data to the data server.
                    odmr_data.push({'params': {'start': start_freq, 'stop': stop_freq, 'num_points': num_points, 'iterations': iterations},
                                    'title': 'Optically Detected Magnetic Resonance',
                                    'xlabel': 'Frequency (GHz)',
                                    'ylabel': 'Counts',
                                    'datasets': {'series1' : sweep_list}
                    })
                    if experiment_widget_process_queue(msg_queue) == 'stop':
                        # the GUI has asked us nicely to exit
                        return

if __name__ == '__main__':
    exp = SpinMeasurements()
    exp.odmr_sweep('odmr', 3e9, 4e9, 100, 20)
