import os
import pytest
import pyansys


if 'PYANSYS_IGNORE_ANSYS' in os.environ:
    has_ansys = False
else:
    has_ansys = pyansys.has_ansys



@pytest.fixture(scope='module')
def mapdl():
    return pyansys.Mapdl(override=True)


@pytest.fixture(scope='function')
def cleared(mapdl):
    mapdl.finish()
    mapdl.clear()
    mapdl.prep7()
    yield


@pytest.mark.skipif(not has_ansys, reason="Requires ANSYS installed")
def test_e(mapdl, cleared):
    mapdl.et("", 183)
    n0 = mapdl.n("", 0, 0, 0)
    n1 = mapdl.n("", 1, 0, 0)
    n2 = mapdl.n("", 1, 1, 0)
    n3 = mapdl.n("", 0, 1, 1)
    n4 = mapdl.n("", 0, 1, -1)
    e0 = mapdl.e(n0, n1, n2, n3)
    assert e0 == 1
    e1 = mapdl.e(n0, n1, n2, n4)
    assert e1 == 2


@pytest.mark.skipif(not has_ansys, reason="Requires ANSYS installed")
def test_et(mapdl, cleared):
    n_plane183 = mapdl.et("", "PLANE183")
    assert n_plane183 == 1
    n_compare = int(mapdl.get_float("ETYP", 0, "NUM", "MAX"))
    assert n_plane183 == n_compare
    n_plane183 = mapdl.et(17, "PLANE183")
    assert n_plane183 == 17
