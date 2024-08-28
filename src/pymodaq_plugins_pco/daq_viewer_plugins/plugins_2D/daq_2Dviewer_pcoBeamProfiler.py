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

        PixNbr = self.settings.child('PixNbr').value()
        PixSize = self.settings.child('PixSize').value()*1e-3 #in mm

        data_x_axis = np.linspace(-int(PixNbr/2)*PixSize ,int(PixNbr/2-1)*PixSize,PixNbr)
        self.x_axis = Axis(data=data_x_axis, label='x', units='mm', index=1)

        # get the y_axis (you may want to to this also in the commit settings if y_axis may have changed
        #data_y_axis = self.controller.your_method_to_get_the_y_axis()  # if possible

        data_y_axis = np.linspace(-int(PixNbr/2)*PixSize, int(PixNbr/2-1)*PixSize,PixNbr)
        self.y_axis = Axis(data=data_y_axis, label='y', units='mm', index=0)


        self.controller.record()
        data_array = self.controller.image()[0]



        dwa = DataFromPlugins(name='BeamProfiler', data=[data_array],
                              axes=[self.x_axis, self.y_axis])#, do_plot=False, do_save=True)

        x, y, dx, dy, phi = lbs.beam_size(data_array)
        x *= PixSize
        y *= PixSize
        dx *= PixSize
        dy *= PixSize
        '''
        dwa0D = DataFromPlugins(name='Pos', data=[np.array([x]), np.array([y])],
                        dim='Data0D', labels = ['X', 'Y'])#, do_plot=True, do_save=False)

        '''
        dwa0D2 = DataFromPlugins(name='Width', data=[np.array([dx]), np.array([dy])],
                        dim='Data0D', labels = ['X width', 'Y width'])#, do_plot=True, do_save=False)



        data = DataToExport('BProfiler', data=[dwa, dwa0D2])
        self.dte_signal.emit(data)












if __name__ == '__main__':
    main(__file__)
