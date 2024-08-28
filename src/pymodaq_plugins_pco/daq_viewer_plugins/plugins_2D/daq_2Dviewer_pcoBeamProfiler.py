from qtpy.QtCore import QThread, Slot, QRectF
from qtpy import QtWidgets
import numpy as np
from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, main, comon_parameters

from pymodaq.utils.daq_utils import ThreadCommand
from pymodaq.utils.data import DataFromPlugins, Axis, DataToExport
from pymodaq.utils.parameter import Parameter
from pymodaq.utils.parameter.utils import iter_children

import laserbeamsize as lbs

from pymodaq_plugins_pco.daq_viewer_plugins.plugins_2D.daq_2Dviewer_pcoCam import DAQ_2DViewer_pcoCam, main
class DAQ_2DViewer_pcoBeamProfiler(DAQ_2DViewer_pcoCam):

    #def grab_data(self, Naverage=1, **kwargs):




    def grab_data(self, Naverage=1, **kwargs):


        self.controller.record()
        data_array = self.controller.image()[0]



        dwa = DataFromPlugins(name='BeamProfiler', data=[data_array],
                              axes=[self.x_axis, self.y_axis])#, do_plot=False, do_save=True)

        x, y, dx, dy, phi = lbs.beam_size(data_array)

        dwa0D = DataFromPlugins(name='Pos', data=[np.array([dx]), np.array([dy])],
                        dim='Data0D', labels = ['X', 'Y'])#, do_plot=True, do_save=False)


        dwa0D2 = DataFromPlugins(name='Width', data=[np.array([x]), np.array([y])],
                        dim='Data0D', labels = ['X width', 'Y width'])#, do_plot=True, do_save=False)



        data = DataToExport('BProfiler', data=[dwa, dwa0D, dwa0D2])
        self.dte_signal.emit(data)












if __name__ == '__main__':
    main(__file__)
