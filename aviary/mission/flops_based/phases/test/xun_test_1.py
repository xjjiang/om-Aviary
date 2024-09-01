import openmdao.api as om
from openmdao.utils.assert_utils import assert_near_equal

from aviary.interface.methods_for_level2 import AviaryGroup
from aviary.subsystems.premission import CorePreMission
from aviary.variable_info.variables import Aircraft

from aviary.utils.test_utils.default_subsystems import get_default_premission_subsystems
from aviary.subsystems.propulsion.utils import build_engine_deck
from aviary.utils.process_input_decks import create_vehicle
from aviary.utils.preprocessors import preprocess_propulsion
from aviary.variable_info.variable_meta_data import _MetaData as BaseMetaData

import warnings
import unittest


class XunGASPOverrideTestCase(unittest.TestCase):
    def setUp(self):
        aviary_inputs, initial_guesses = create_vehicle(
            'models/test_aircraft/xun_aircraft_for_bench_GwGm.csv')
        aviary_inputs.set_val(Aircraft.Engine.SCALED_SLS_THRUST, val=28690, units="lbf")
        aviary_inputs.set_val(Aircraft.Fuselage.WETTED_AREA, val=4000, units="ft**2")

        engines = build_engine_deck(aviary_inputs)

        core_subsystems = get_default_premission_subsystems('GASP', engines)
        preprocess_propulsion(aviary_inputs, engines)

        #self.aviary_inputs = aviary_inputs

        prob = om.Problem()

        aviary_options = aviary_inputs
        subsystems = core_subsystems

        prob.model = AviaryGroup(aviary_options=aviary_options,
                                 aviary_metadata=BaseMetaData)
        prob.model.add_subsystem(
            'pre_mission',
            CorePreMission(aviary_options=aviary_options,
                           subsystems=subsystems),
            promotes_inputs=['aircraft:*', 'mission:*'],
            promotes_outputs=['aircraft:*', 'mission:*']
        )

        with warnings.catch_warnings():

            warnings.simplefilter("ignore", om.PromotionWarning)

            prob.setup()

        self.prob = prob

    def test_case1(self):
        prob = self.prob

        prob.run_model()

        x = prob[Aircraft.Fuselage.WETTED_AREA]
        print(f"WETTED_AREA = {x}")


if __name__ == '__main__':
    #unittest.main()
    thisClass = XunGASPOverrideTestCase()
    thisClass.setUp()
    # this run override:
    #   aircraft:engine:scale_factor
    #   aircraft:fuselage:wetted_area
    # and run Newton
    thisClass.test_case1()
