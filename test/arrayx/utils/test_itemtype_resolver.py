import array as pyarray

import pytest

from arrayx.utils import IntBounds, itemtype_resolver


@pytest.mark.parametrize(
    'typecode',
    argvalues=pyarray.typecodes)
def test_resolves_py_array_typecode_to_itself(typecode):
    assert itemtype_resolver.resolve_typecode(typecode) == typecode


def test_resolves_i1_to_b():
    assert itemtype_resolver.resolve_typecode('i1') == 'b'


def test_resolves_u2_to_H():
    assert itemtype_resolver.resolve_typecode('u2') == 'H'


@pytest.mark.parametrize(
    'fwcode',
    argvalues='i1 u1 i2 u2 i4 u4 i8 u8'.split())
def test_resolves_fixedwidth_int_code_to_pyarray_typecode(fwcode):
    assert itemtype_resolver.resolve_typecode(fwcode) in pyarray.typecodes


def test_resolves_signed_itemsize_1_to_pyarray_typecode_of_b():
    assert itemtype_resolver.resolve_signed_itemsize(1) == 'b'


def test_resolves_unsigned_itemsize_2_to_pyarray_typecode_of_H():
    assert itemtype_resolver.resolve_unsigned_itemsize(2) == 'H'


@pytest.mark.parametrize(
    'itemsize',
    argvalues=(1, 2, 4, 8))
def test_resolves_signed_itemsize_to_pyarray_typecode(itemsize):
    assert itemtype_resolver.resolve_signed_itemsize(itemsize) in pyarray.typecodes


@pytest.mark.parametrize(
    'itemsize',
    argvalues=(1, 2, 4, 8))
def test_resolves_unsigned_itemsize_to_pyarray_typecode(itemsize):
    assert itemtype_resolver.resolve_unsigned_itemsize(itemsize) in pyarray.typecodes


@pytest.mark.parametrize(
    'value_bounds_txt,expect_itemsize,expect_is_signed',
    argvalues=(
        (' 0x00 ,                      0x00', 1, True),
        (' 0x00 ,                      0x7f', 1, True),
        (' 0x00 ,                      0x80', 1, False),
        (' 0x00 ,                      0xff', 1, False),
        (' 0x00 ,                   0x01_00', 2, True),
        (' 0x00 ,                   0x7f_ff', 2, True),
        (' 0x00 ,                   0x80_00', 2, False),
        (' 0x00 ,                   0xff_ff', 2, False),
        (' 0x00 ,                0x01_ff_ff', 4, True),
        (' 0x00 ,             0x7f_ff_ff_ff', 4, True),
        (' 0x00 ,             0x80_00_00_00', 4, False),
        (' 0x00 ,             0xff_ff_ff_ff', 4, False),
        (' 0x00 ,          0x10_00_00_00_00', 8, True),
        (' 0x00 , 0x7f_ff_ff_ff_ff_ff_ff_ff', 8, True),
        (' 0x00 , 0x80_00_00_00_00_00_00_00', 8, False),
        (' 0x00 , 0xff_ff_ff_ff_ff_ff_ff_ff', 8, False),
        ('                      -0x01 , 0x00', 1, True),
        ('                      -0x80 , 0x00', 1, True),
        ('                      -0x81 , 0x00', 2, True),
        ('                  -0x_80_00 , 0x00', 2, True),
        ('                  -0x_80_01 , 0x00', 4, True),
        ('            -0x_80_00_00_00 , 0x00', 4, True),
        ('            -0x_80_00_00_01 , 0x00', 8, True),
        (' -0x80_00_00_00_00_00_00_00 , 0x00', 8, True),
        ))
def test_resolves_valuebounds_to_smallest_fitting_size_prefering_signed(
        value_bounds_txt, expect_itemsize, expect_is_signed):

    value_bounds = IntBounds(*eval(value_bounds_txt))

    typecode = itemtype_resolver.resolve_int_valuebounds(value_bounds)

    pyary = pyarray.array(typecode, (0,))
    try:
        pyary[0] = -1
        is_signed = True
    except OverflowError:
        is_signed = False

    assert (pyary.itemsize, is_signed) == (expect_itemsize, expect_is_signed)
