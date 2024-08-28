from pymodaq.utils.daq_utils import ThreadCommand
from pymodaq.utils.data import DataFromPlugins, Axis, DataToExport
from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters, main
from pymodaq.utils.parameter import Parameter

import pco
import numpy as np

# TODO:
# (1) change the name of the following class to DAQ_2DViewer_TheNameOfYourChoice
# (2) change the name of this file to daq_2Dviewer_TheNameOfYourChoice ("TheNameOfYourChoice" should be the SAME
#     for the class name and the file name.)
# (3) this file should then be put into the right folder, namely IN THE FOLDER OF THE PLUGIN YOU ARE DEVELOPING:
#     pymodaq_plugins_my_plugin/daq_viewer_plugins/plugins_2D
class DAQ_2DViewer_pcoCam(DAQ_Viewer_base):


    params = comon_parameters + [

        {'title': 'Trigger mode',
         'name': 'Trigger',
         'type': 'itemselect',
         'value': dict(all_items=[
             "No trigger", "Trigger"], selected=["No trigger"])},


        {'title': 'Exposure time (ms):', 'name': 'expTime', 'type': 'slide', 'value': 10, 'default': 10,
         'min': 1,
         'max': 10000, 'subtype': 'linear'},

        {'title': 'Pixel nbr:',
         'name': 'PixNbr',
         'type': 'int',
         'value': 2048, 'default': 2048},

        {'title': 'Pixel size (µm):',
         'name': 'PixSize',
         'type': 'float',
         'value': 6.5, 'default': 6.5},

    #add ROI and other parameters

    ]

    def ini_attributes(self):
        #  TODO declare the type of the wrapper (and assign it to self.controller) you're going to use for easy
        #  autocompletion
        self.controller: pco.Camera() = None

        # TODO declare here attributes you want/need to init with a default value

        self.x_axis = None
        self.y_axis = None

    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """
        # TODO for your custom plugin
        if param.name() == "a_parameter_you've_added_in_self.params":
            self.controller.your_method_to_apply_this_param_change()
        #elif ...

    def ini_detector(self, controller=None):
        """Detector communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator/detector by controller
            (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """
        #raise NotImplemented  # TODO when writing your own plugin remove this line and modify the one below
        self.ini_detector_init(old_controller=controller,
                               new_controller=pco.Camera())

        ## TODO for your custom plugin
        # get the x_axis (you may want to to this also in the commit settings if x_axis may have changed
        #data_x_axis = self.controller.your_method_to_get_the_x_axis()  # if possible

        PixNbr = self.settings.child('PixNbr').value()
        PixSize = self.settings.child('PixSize').value()*1e3 #in mm

        data_x_axis = np.linspace(-int(PixNbr/2)*PixSize ,int(PixNbr/2-1)*PixSize,PixNbr)
        self.x_axis = Axis(data=data_x_axis, label='', units='', index=1)

        # get the y_axis (you may want to to this also in the commit settings if y_axis may have changed
        #data_y_axis = self.controller.your_method_to_get_the_y_axis()  # if possible

        data_y_axis = np.linspace(-int(PixNbr/2)*PixSize, int(PixNbr/2-1)*PixSize,PixNbr)
        self.y_axis = Axis(data=data_y_axis, label='', units='', index=0)

        ## TODO for your custom plugin. Initialize viewers pannel with the future type of data
        self.dte_signal_temp.emit(DataToExport('myplugin',
                                               data=[DataFromPlugins(name='Cam', data=[np.zeros((PixNbr,PixNbr))],
                                                                     dim='Data2D', labels=['dat0'],
                                                                     axes=[self.x_axis, self.y_axis]), ]))

        self.controller.configuration = {'exposure time': 0.01}


        info = "Whatever info you want to log"
        initialized = True
        return info, initialized

    def close(self):
        """Terminate the communication protocol"""

        self.controller.close()

    def grab_data(self, Naverage=1, **kwargs):
        """Start a grab from the detector

        Parameters
        ----------
        Naverage: int
            Number of hardware averaging (if hardware averaging is possible, self.hardware_averaging should be set to
            True in class preamble and you should code this implementation)
        kwargs: dict
            others optionals arguments
        """
        ## TODO for your custom plugin: you should choose EITHER the synchrone or the asynchrone version following
        PixNbr = self.settings.child('PixNbr').value()
        PixSize = self.settings.child('PixSize').value()*1e3 #in mm

        data_x_axis = np.linspace(-int(PixNbr/2)*PixSize ,int(PixNbr/2-1)*PixSize,PixNbr)
        self.x_axis = Axis(data=data_x_axis, label='', units='', index=1)

        # get the y_axis (you may want to to this also in the commit settings if y_axis may have changed
        #data_y_axis = self.controller.your_method_to_get_the_y_axis()  # if possible

        data_y_axis = np.linspace(-int(PixNbr/2)*PixSize, int(PixNbr/2-1)*PixSize,PixNbr)
        self.y_axis = Axis(data=data_y_axis, label='', units='', index=0)



        ##synchrone version (blocking function)
        self.controller.record()
        data_tot = self.controller.image()[0]
        self.dte_signal.emit(DataToExport('pcoCam',
                                          data=[DataFromPlugins(name='Cam', data=data_tot,
                                                                dim='Data2D', labels=['image'],
                                                                x_axis=self.x_axis,
                                                                y_axis=self.y_axis), ]))

        ##asynchrone version (non-blocking function with callback)
        #self.controller.your_method_to_start_a_grab_snap(self.callback)
        #########################################################

    def callback(self):
        """optional asynchrone method called when the detector has finished its acquisition of data"""
        data_tot = self.controller.your_method_to_get_data_from_buffer()
        self.dte_signal.emit(DataToExport('myplugin',
                                          data=[DataFromPlugins(name='Mock1', data=data_tot,
                                                                dim='Data2D', labels=['label1'],
                                                                x_axis=self.x_axis,
                                                                y_axis=self.y_axis), ]))
    def stop(self):
        """Stop the current grab hardware wise if necessary"""

        self.controller.stop()  # when writing your own plugin replace this line
        self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))
        ##############################
        return ''


if __name__ == '__main__':
    main(__file__)
