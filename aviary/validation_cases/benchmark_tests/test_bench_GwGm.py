from copy import deepcopy
import unittest

from openmdao.utils.assert_utils import assert_near_equal
from openmdao.utils.testing_utils import require_pyoptsparse, use_tempdirs
from openmdao.core.problem import _clear_problem_names

from aviary.interface.default_phase_info.two_dof import phase_info
from aviary.interface.methods_for_level1 import setup_and_run_aviary
from aviary.variable_info.variables import Aircraft, Mission, Dynamic
from aviary.variable_info.enums import AnalysisScheme, Verbosity


@use_tempdirs
class ProblemPhaseTestCase(unittest.TestCase):

    def setUp(self):
        _clear_problem_names()  # need to reset these to simulate separate runs

    @require_pyoptsparse(optimizer="IPOPT")
    def test_bench_GwGm(self):
        local_phase_info = deepcopy(phase_info)
        prob = setup_and_run_aviary('models/test_aircraft/aircraft_for_bench_GwGm.csv',
                                    local_phase_info, optimizer='IPOPT', verbosity=Verbosity.QUIET)

        rtol = 0.01

        # There are no truth values for these.
        assert_near_equal(prob.get_val(Mission.Design.GROSS_MASS, units='lbm'),
                          174039., tolerance=rtol)

        assert_near_equal(prob.get_val(Aircraft.Design.OPERATING_MASS, units='lbm'),
                          95509, tolerance=rtol)

        assert_near_equal(prob.get_val(Mission.Summary.TOTAL_FUEL_MASS, units='lbm'),
                          42529., tolerance=rtol)

        assert_near_equal(prob.get_val(Mission.Landing.GROUND_DISTANCE, units='ft'),
                          2634.8, tolerance=rtol)

        assert_near_equal(prob.get_val(Mission.Summary.RANGE, units='NM'),
                          3675.0, tolerance=rtol)

        assert_near_equal(prob.get_val(Mission.Landing.TOUCHDOWN_MASS, units='lbm'),
                          136823.47, tolerance=rtol)

    @require_pyoptsparse(optimizer="SNOPT")
    def test_bench_GwGm_SNOPT(self):
        local_phase_info = deepcopy(phase_info)
        prob = setup_and_run_aviary('models/test_aircraft/aircraft_for_bench_GwGm.csv',
                                    local_phase_info, optimizer='SNOPT', verbosity=Verbosity.QUIET)

        rtol = 0.01

        # There are no truth values for these.
        assert_near_equal(prob.get_val(Mission.Design.GROSS_MASS, units='lbm'),
                          174039., tolerance=rtol)

        assert_near_equal(prob.get_val(Aircraft.Design.OPERATING_MASS, units='lbm'),
                          95509, tolerance=rtol)

        assert_near_equal(prob.get_val(Mission.Summary.TOTAL_FUEL_MASS, units='lbm'),
                          42529., tolerance=rtol)

        assert_near_equal(prob.get_val(Mission.Landing.GROUND_DISTANCE, units='ft'),
                          2634.8, tolerance=rtol)

        assert_near_equal(prob.get_val(Mission.Summary.RANGE, units='NM'),
                          3675.0, tolerance=rtol)

        assert_near_equal(prob.get_val(Mission.Landing.TOUCHDOWN_MASS, units='lbm'),
                          136823.47, tolerance=rtol)

    @require_pyoptsparse(optimizer="SNOPT")
    def test_bench_GwGm_SNOPT_lbm_s(self):
        local_phase_info = deepcopy(phase_info)
        prob = setup_and_run_aviary('models/test_aircraft/aircraft_for_bench_GwGm_lbm_s.csv',
                                    local_phase_info, optimizer='SNOPT', verbosity=Verbosity.QUIET)

        rtol = 0.01

        # There are no truth values for these.
        assert_near_equal(prob.get_val(Mission.Design.GROSS_MASS, units='lbm'),
                          174039., tolerance=rtol)

        assert_near_equal(prob.get_val(Aircraft.Design.OPERATING_MASS, units='lbm'),
                          95509, tolerance=rtol)

        assert_near_equal(prob.get_val(Mission.Summary.TOTAL_FUEL_MASS, units='lbm'),
                          42529., tolerance=rtol)

        assert_near_equal(prob.get_val(Mission.Landing.GROUND_DISTANCE, units='ft'),
                          2634.8, tolerance=rtol)

        assert_near_equal(prob.get_val(Mission.Summary.RANGE, units='NM'),
                          3675.0, tolerance=rtol)

        assert_near_equal(prob.get_val(Mission.Landing.TOUCHDOWN_MASS, units='lbm'),
                          136823.47, tolerance=rtol)

    @require_pyoptsparse(optimizer="IPOPT")
    def test_bench_GwGm_shooting(self):
        local_phase_info = deepcopy(phase_info)
        prob = setup_and_run_aviary('models/test_aircraft/aircraft_for_bench_GwGm.csv',
                                    local_phase_info, optimizer='IPOPT', run_driver=False,
                                    analysis_scheme=AnalysisScheme.SHOOTING, verbosity=Verbosity.QUIET)

        rtol = 0.01

        assert_near_equal(prob.get_val(Mission.Design.RESERVE_FUEL, units='lbm'),
                          4998, tolerance=rtol)

        assert_near_equal(prob.get_val(Mission.Design.GROSS_MASS, units='lbm'),
                          174039., tolerance=rtol)

        assert_near_equal(prob.get_val(Aircraft.Design.OPERATING_MASS, units='lbm'),
                          95509, tolerance=rtol)

        assert_near_equal(prob.get_val(Mission.Summary.TOTAL_FUEL_MASS, units='lbm'),
                          43574., tolerance=rtol)

        assert_near_equal(prob.get_val(Mission.Landing.GROUND_DISTANCE, units='ft'),
                          2634.8, tolerance=rtol)

        assert_near_equal(prob.get_val(Mission.Summary.RANGE, units='NM'),
                          3774.3, tolerance=rtol)

        assert_near_equal(prob.get_val(Mission.Landing.TOUCHDOWN_MASS, units='lbm'),
                          136823.47, tolerance=rtol)

        assert_near_equal(prob.get_val('traj.cruise_' + Dynamic.Mission.DISTANCE + '_final',
                                       units='nmi'), 3668.3, tolerance=rtol)


if __name__ == '__main__':
    # unittest.main()
    test = ProblemPhaseTestCase()
    test.test_bench_GwGm_SNOPT_lbm_s()
    test.test_bench_GwGm_shooting()
