"""
Define utilities to calculate the estimated mass of any passengers, their
baggage, and other cargo. The methodology is based on the GASP weight
equations, modified to output mass instead of weight.
"""

import numpy as np
import openmdao.api as om

from aviary.constants import GRAV_ENGLISH_LBM
from aviary.variable_info.functions import add_aviary_input, add_aviary_option, add_aviary_output
from aviary.variable_info.variables import Aircraft


class CargoContainerMass(om.ExplicitComponent):
    """Calculate the mass of cargo containers."""

    def initialize(self):
        add_aviary_option(self, Aircraft.CrewPayload.Design.NUM_PASSENGERS)

    def setup(self):
        add_aviary_input(self, Aircraft.CrewPayload.ULD_MASS_PER_PASSENGER)

        add_aviary_output(self, Aircraft.CrewPayload.CARGO_CONTAINER_MASS, units='lbm')

    def setup_partials(self):
        self.declare_partials(
            Aircraft.CrewPayload.CARGO_CONTAINER_MASS, Aircraft.CrewPayload.ULD_MASS_PER_PASSENGER
        )

    def compute(self, inputs, outputs):
        PAX = self.options[Aircraft.CrewPayload.Design.NUM_PASSENGERS]
        uld_per_pax = inputs[Aircraft.CrewPayload.ULD_MASS_PER_PASSENGER][0]
        uld_per_pax = uld_per_pax.real

        # weight of a single ULD (LD-3 type)
        unit_weight_cargo_handling = 165.0

        cargo_handling_wt = (int(PAX * uld_per_pax) + 1) * unit_weight_cargo_handling

        outputs[Aircraft.CrewPayload.CARGO_CONTAINER_MASS] = cargo_handling_wt / GRAV_ENGLISH_LBM
