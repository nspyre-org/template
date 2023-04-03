"""
Example GUI elements.
"""
from nspyre import FlexLinePlotWidget
from nspyre import ExperimentWidget
from pyqtgraph import SpinBox
from pyqtgraph.Qt import QtWidgets

import template.experiments.odmr

class ODMRWidget(ExperimentWidget):
    def __init__(self):
        params_config = {
            'start_freq': {
                'display_text': 'Start Frequency',
                'widget': SpinBox(
                    value=3e9,
                    suffix='Hz',
                    siPrefix=True,
                    bounds=(100e3, 10e9),
                    dec=True,
                ),
            },
            'stop_freq': {
                'display_text': 'Stop Frequency',
                'widget': SpinBox(
                    value=4e9,
                    suffix='Hz',
                    siPrefix=True,
                    bounds=(100e3, 10e9),
                    dec=True,
                ),
            },
            'num_points': {
                'display_text': 'Number of Scan Points',
                'widget': SpinBox(value=101, int=True, bounds=(1, None), dec=True),
            },
            'iterations': {
                'display_text': 'Number of Experiment Repeats',
                'widget': SpinBox(value=50, int=True, bounds=(1, None), dec=True),
            },
            'dataset': {
                'display_text': 'Data Set',
                'widget': QtWidgets.QLineEdit('odmr'),
            },
        }

        super().__init__(params_config, 
                        template.experiments.odmr,
                        'SpinMeasurements',
                        'odmr_sweep',
                        title='ODMR')

class FlexLinePlotWidgetWithODMRDefaults(FlexLinePlotWidget):
    """This is meant to give the user some hints as to how to use the FlexSinkLinePlotWidget."""
    def __init__(self):
        super().__init__()
        self.add_plot('avg',        series='series1',   scan_i='',     scan_j='',  processing='Average')
        self.add_plot('latest',     series='series1',   scan_i='-1',   scan_j='',  processing='Average')
        self.add_plot('first',      series='series1',   scan_i='0',    scan_j='1', processing='Average')
        self.add_plot('latest_10',  series='series1',   scan_i='-10',  scan_j='',  processing='Average')
        self.hide_plot('first')
        self.hide_plot('latest_10')
        self.line_plot.plot_item().setXRange(3.0, 4.0)
        self.line_plot.plot_item().setYRange(-100, 4500)
        self.datasource_lineedit.setText('odmr')
