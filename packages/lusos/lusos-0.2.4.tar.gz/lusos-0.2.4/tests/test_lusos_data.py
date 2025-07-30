import pandas as pd
import pytest
from numpy.testing import assert_array_equal

import lusos


@pytest.mark.unittest
def test_ef_low_netherlands():
    """
    Test the emission factors for the low part of the Netherlands.
    """
    ef = lusos.data.ef_low_netherlands()
    assert isinstance(ef, pd.DataFrame)
    assert ef.index.name == "layer"
    assert_array_equal(ef.columns, ["co2_uit", "ch4_uit", "n2o_uit", "co2_in"])
    assert_array_equal(
        ef.index,
        [
            "panden_peat",
            "overig_groen_peat",
            "percelen_peat",
            "openbare_ruimte_peat",
            "grote_wateren_peat",
            "erven_peat",
            "overig_peat",
            "sloten_peat",
            "stedelijk_groen_peat",
            "panden_moerig",
            "overig_groen_moerig",
            "percelen_moerig",
            "openbare_ruimte_moerig",
            "grote_wateren_moerig",
            "erven_moerig",
            "overig_moerig",
            "sloten_moerig",
            "stedelijk_groen_moerig",
            "panden_buried",
            "overig_groen_buried",
            "percelen_buried",
            "openbare_ruimte_buried",
            "grote_wateren_buried",
            "erven_buried",
            "overig_buried",
            "sloten_buried",
            "stedelijk_groen_buried",
            "panden_other",
            "overig_groen_other",
            "percelen_other",
            "openbare_ruimte_other",
            "grote_wateren_other",
            "erven_other",
            "overig_other",
            "sloten_other",
            "stedelijk_groen_other",
        ],
    )
    assert_array_equal(
        ef.values,
        [
            [1.025, 0.0, 0.0, 0.0],
            [1.025, 0.0, 0.0, 0.0],
            [1.025, 0.0, 0.0, 0.0],
            [1.025, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [1.025, 0.0, 0.0, 0.0],
            [1.025, 0.0, 0.0, 0.0],
            [0.0, 0.0518, 0.0, 0.0],
            [1.025, 0.0, 0.0, 0.0],
            [1.236, 0.0, 0.0, 0.0],
            [1.236, 0.0, 0.0, 0.0],
            [1.236, 0.0, 0.0, 0.0],
            [1.236, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [1.236, 0.0, 0.0, 0.0],
            [1.236, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [1.236, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
        ],
    )


@pytest.mark.unittest
def test_ef_high_netherlands():
    """
    Test the emission factors for the high part of the Netherlands.
    """
    ef = lusos.data.ef_high_netherlands()
    assert isinstance(ef, pd.DataFrame)
    assert ef.index.name == "layer"
    assert_array_equal(ef.columns, ["co2_uit", "ch4_uit", "n2o_uit", "co2_in"])
    assert_array_equal(
        ef.index,
        [
            "panden_peat",
            "overig_groen_peat",
            "percelen_peat",
            "openbare_ruimte_peat",
            "grote_wateren_peat",
            "erven_peat",
            "overig_peat",
            "sloten_peat",
            "stedelijk_groen_peat",
            "panden_moerig",
            "overig_groen_moerig",
            "percelen_moerig",
            "openbare_ruimte_moerig",
            "grote_wateren_moerig",
            "erven_moerig",
            "overig_moerig",
            "sloten_moerig",
            "stedelijk_groen_moerig",
            "panden_buried",
            "overig_groen_buried",
            "percelen_buried",
            "openbare_ruimte_buried",
            "grote_wateren_buried",
            "erven_buried",
            "overig_buried",
            "sloten_buried",
            "stedelijk_groen_buried",
            "panden_other",
            "overig_groen_other",
            "percelen_other",
            "openbare_ruimte_other",
            "grote_wateren_other",
            "erven_other",
            "overig_other",
            "sloten_other",
            "stedelijk_groen_other",
        ],
    )
    assert_array_equal(
        ef.values,
        [
            [2.57, 0.0, 0.0, 0.0],
            [2.57, 0.0, 0.0, 0.0],
            [2.57, 0.0, 0.0, 0.0],
            [2.57, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [2.57, 0.0, 0.0, 0.0],
            [2.57, 0.0, 0.0, 0.0],
            [0.0, 0.052, 0.0, 0.0],
            [2.57, 0.0, 0.0, 0.0],
            [1.3, 0.0, 0.0, 0.0],
            [1.3, 0.0, 0.0, 0.0],
            [1.3, 0.0, 0.0, 0.0],
            [1.3, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [1.3, 0.0, 0.0, 0.0],
            [1.3, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [1.3, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
        ],
    )
