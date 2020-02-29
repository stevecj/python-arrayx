import pytest

from arrayx.utils import FixedWidthIntItemtype


@pytest.mark.parametrize(
    'itemsize,signedness_prefix,py_array_itemtype,expected_fw_code', 
    argvalues=(
        (2, 'i', 'h', 'i2'),
        (4, 'u', 'i', 'u4'),
        (8, 'u', 'Q', 'u8'),
        ))
def test_has_fixedwidth_code_derived_from_signedness_and_itemsize(
        itemsize, signedness_prefix, py_array_itemtype, expected_fw_code):
    fw_itemtype = FixedWidthIntItemtype(
        itemsize, signedness_prefix, py_array_itemtype)
    assert fw_itemtype.fixedwidth_code == expected_fw_code


def test_sorts_by_itemsize_signed_before_unsigned_py_typecode_ord():
    fw_itemtypes_seq = (
        FixedWidthIntItemtype(1, 'i', 'b'),  # Signed byte
        FixedWidthIntItemtype(1, 'u', 'B'),  # Unigned byte
        FixedWidthIntItemtype(2, 'i', 'h'),  # Signed short
        FixedWidthIntItemtype(2, 'i', 'H'),  # Unigned byte
        FixedWidthIntItemtype(2, 'i', 'i'),  # Signed int (2-byte)
        FixedWidthIntItemtype(4, 'i', 'l'),  # Signed long (4-byte)
        FixedWidthIntItemtype(8, 'i', 'q'),  # Signed big (8-byte)
        )

    reversed_seq = reversed(fw_itemtypes_seq)
    sorted_seq = tuple(sorted(reversed_seq))
    assert sorted_seq == fw_itemtypes_seq
