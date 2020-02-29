import array as pyarray

import pytest

from arrayx import Array, IntBounds


@pytest.mark.parametrize('pyarray_typecode', argvalues=pyarray.typecodes)
def test_can_be_initialized_using_pyarray_typecode(pyarray_typecode):

    aryx = Array(pyarray_typecode)

    assert aryx.typecode == pyarray_typecode


@pytest.mark.parametrize(
    'fw_typecode,expected_itemsize',
    argvalues=(
        ('i1', 1),
        ('i2', 2),
        ('i4', 4),
        ('i8', 8),
        ))
def test_can_be_initialized_using_signed_fixedwidth_typecode(
        fw_typecode, expected_itemsize):

    aryx = Array(fw_typecode, (0,))

    assert aryx.itemsize == expected_itemsize
    aryx[0] = -1  # Should raise no exception.


@pytest.mark.parametrize(
    'fw_typecode,expected_itemsize',
    argvalues=(
        ('u1', 1),
        ('u2', 2),
        ('u4', 4),
        ('u8', 8),
        ))
def test_can_be_initialized_using_unsigned_fixedwidth_typecode(
        fw_typecode, expected_itemsize):

    aryx = Array(fw_typecode, (0,))

    assert aryx.itemsize == expected_itemsize
    with pytest.raises(OverflowError):
        aryx[0] = -1


@pytest.mark.parametrize('itemsize', (1, 2, 4, 8))
def test_can_be_initialized_with_itemsize_int_signed_by_default(itemsize):
    aryx = Array(itemsize, (0,))

    assert aryx.itemsize == itemsize
    aryx[0] = -1  # Should raise no exception.


@pytest.mark.parametrize('itemsize', (1, 2, 4, 8))
def test_can_be_initialized_with_itemsize_int_explicitly_signed(itemsize):
    aryx = Array(itemsize, is_signed=True, initializer=(0,))

    assert aryx.itemsize == itemsize
    aryx[0] = -1  # Should raise no exception.


@pytest.mark.parametrize('itemsize', (1, 2, 4, 8))
def test_can_be_initialized_with_itemsize_int_explicitly_unsigned(itemsize):
    aryx = Array(itemsize, is_signed=False, initializer=(0,))

    assert aryx.itemsize == itemsize
    with pytest.raises(OverflowError):
        aryx[0] = -1


# Byte and short types are not platform-dependent, so these tests should
# behave the same way on all Python platforms.
@pytest.mark.parametrize(
    'bounds_txt,expected_typecode',
    argvalues=(
        ('  -1,     10', 'b'),
        (' 100,    200', 'B'),
        ('-200,   -100', 'h'),
        (' 500, 40_000', 'H'),
        ))
def test_can_be_initialized_using_int_bounds(
        bounds_txt, expected_typecode):

    int_bounds = IntBounds(*eval(bounds_txt))

    aryx = aryx = Array(int_bounds)

    assert aryx.typecode == expected_typecode
