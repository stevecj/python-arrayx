import array as pyarray

import arrayx


def test_has_all_pyarraay_typecodes_in_its_typecodes_seq():
    py_typecode_set = set(pyarray.typecodes)
    x_typecode_set = set(arrayx.typecodes)

    assert py_typecode_set.issubset(x_typecode_set)


def test_has_all_arrayx_fixedwidth_codes_in_its_typecodes_seq():
    x_typecode_set = set(arrayx.typecodes)

    assert {'c1', 'c2', 'c4', 'c8'}.issubset(x_typecode_set)
