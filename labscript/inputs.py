#####################################################################
#                                                                   #
# /inputs.py                                                        #
#                                                                   #
# Copyright 2013, Monash University                                 #
#                                                                   #
# This file is part of the program labscript, in the labscript      #
# suite (see http://labscriptsuite.org), and is licensed under the  #
# Simplified BSD License. See the license.txt file in the root of   #
# the project for the full license.                                 #
#                                                                   #
#####################################################################

"""Classes for device channels that are inputs"""

from .base import Device
from .utils import set_passed_properties


class AnalogIn(Device):
    """Analog Input for use with all devices that have an analog input."""
    description = "Analog Input"

    @set_passed_properties(property_names={})
    def __init__(
        self, name, parent_device, connection, scale_factor=1.0, units="Volts", **kwargs
    ):
        """Instantiates an Analog Input.

        Args:
            name (str): python variable to assign this input to.
            parent_device (:obj:`IntermediateDevice`): Device input is connected to.
            scale_factor (float, optional): Factor to scale the recorded values by.
            units (str, optional): Units of the input.
            **kwargs: Keyword arguments passed to :func:`Device.__init__`.
        """
        self.acquisitions = []
        self.scale_factor = scale_factor
        self.units=units
        Device.__init__(self, name, parent_device, connection, **kwargs)

    def acquire(
        self, label, start_time, end_time, wait_label="", scale_factor=None, units=None
    ):
        """Command an acquisition for this input.

        Args:
            label (str): Unique label for the acquisition. Used to identify the saved trace.
            start_time (float): Time, in seconds, when the acquisition should start.
            end_time (float): Time, in seconds, when the acquisition should end.
            wait_label (str, optional): 
            scale_factor (float): Factor to scale the saved values by.
            units: Units of the input, consistent with the unit conversion class.

        Returns:
            float: Duration of the acquistion, equivalent to `end_time - start_time`.
        """
        if scale_factor is None:
            scale_factor = self.scale_factor
        if units is None:
            units = self.units
        self.acquisitions.append(
            {
                "start_time": start_time,
                "end_time": end_time,
                "label": label,
                "wait_label": wait_label,
                "scale_factor": scale_factor,
                "units": units,
            }
        )
        return end_time - start_time


class Counter(Device):
    """Counter Input for edge counting over timed gate windows."""
    description = "Counter Input"

    def __init__(self, name, parent_device, connection, edge_terminal, gate_terminal=None, sample_terminal=None, **kwargs):
        """Counter device

        Args:
            name (str): python variable to assign this device to.
            parent_device (:obj:`IntermediateDevice`): Device this counter is attached to. (e.g. NI_***)
            connection (str): Connection name on the parent device. (e.g. /NI_***/ctr0)
            edge_terminal (str): Terminal on the parent device for edge counting. (e.g. PFI0)
            gate_terminal (str): Terminal on the parent device for gate. High for enabled. (e.g. PFI1)
            sample_terminal (str): Terminal on the parent device for accepting ticks for sampling. High at tick. (e.g. PFI2)
            **kwargs: Passed to :func:`Device.__init__`.
        """
        self.acquisitions = []
        self.edge_terminal = edge_terminal
        self.gate_terminal = gate_terminal
        self.sample_terminal = sample_terminal
        Device.__init__(self, name, parent_device, connection, **kwargs)

    def acquire(self, label, max_sampling_rate=None, buffer_size=None, polling_interval=None):
        """Schedule a counter acquisition

        Args:
            label (str): Unique label for the acquisition.
            max_sampling_rate (float): Estimated maximum sampling rate in Hz. Only necessary in sampling mode.
            buffer_size (int): Length of buffer storing sampled data. Only necessary in sampling mode.
            polling_interval (float): Polling interval to read data from buffer in seconds. Only necessary in sampling mode.
        """

        self.acquisitions.append(
            {
                "label": label,
                "max_sampling_rate": max_sampling_rate,
                "buffer_size": buffer_size,
                "polling_interval": polling_interval,
            }
        )

        return
