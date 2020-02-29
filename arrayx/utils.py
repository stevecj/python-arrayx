import array as pyarray
from collections import namedtuple, OrderedDict as odict


def _is_int_typecode(typecode):
    try:
        ary = pyarray.array(typecode, (0,))
    except TypeError:
        # type does not accept integer values
        return False

    try:
        ary[0] = 0.1
        # Type accepts floating point values.
        return False
    except TypeError:
        pass

    return True


PY_ARRAY_INT_ITEMTYPE_SEQ = tuple(
    tc for tc in pyarray.typecodes if _is_int_typecode(tc))


# First 3 members are in sequence for the desired sort ordering.
_FixedWidthIntItemtypeBase = namedtuple(
    'FixedWidthIntItemtype', (
        'itemsize'
        ' signedness_prefix'
        ' py_array_itemtype_ord'
        ' py_array_typecode'
        ' fixedwidth_code'
        ' value_bounds'
        ))


class FixedWidthIntItemtype(_FixedWidthIntItemtypeBase):

    def __new__(cls, itemsize, signedness_prefix, py_array_typecode):
        py_array_itemtype_ord = PY_ARRAY_INT_ITEMTYPE_SEQ.index(
            py_array_typecode)
        fixedwidth_code = f'{signedness_prefix}{itemsize}'

        if signedness_prefix == 'u':
            valuebit_count = itemsize << 3
            maxval = (1 << valuebit_count) - 1
            value_bounds = IntBounds(0, maxval)
        else:
            valuebit_count = (itemsize << 3) - 1
            minval = -(1 << valuebit_count)
            value_bounds = IntBounds(minval, ~minval)

        return super().__new__(
            cls,
            itemsize,
            signedness_prefix,
            py_array_itemtype_ord,
            py_array_typecode,
            fixedwidth_code,
            value_bounds)


_IntBoundsTuple = namedtuple(
    'IntBounds',
    'minval, maxval')


class IntBounds(_IntBoundsTuple):
    def __new__(cls, minval, maxval):
        cls._validate_arg('minval', minval)
        cls._validate_arg('maxval', maxval)

        return super().__new__(cls, minval, maxval)

    def __contains__(self, other):
        cls = type(self)
        if not isinstance(other, cls):
            raise TypeError(
                f"'in <{cls.__name__}>' requires {cls.__name__} as left"
                f" operand, not {type(other).__name__}")
        return (
            self.minval <= other.minval
            and other.maxval <= self.maxval)

    @classmethod
    def _validate_arg(cls, name, val):
        if not isinstance(val, int):
            raise TypeError(
                f'The {name} argument must be an integer, not'
                f' {type(val).__name__}')


class ItemtypeResolver:
    def __init__(self):
        fw_itemtypes_by_code = odict()
        signed_typecodes_by_itemsize = odict()
        unsigned_typecodes_by_itemsize = odict()

        for pytc in PY_ARRAY_INT_ITEMTYPE_SEQ:
            fw_itemtype = FixedWidthIntItemtype(
                itemsize=pyarray.array(pytc).itemsize,
                signedness_prefix='u' if pytc.isupper() else 'i',
                py_array_typecode=pytc)
            if fw_itemtype.fixedwidth_code in fw_itemtypes_by_code:
                continue
            fw_itemtypes_by_code[fw_itemtype.fixedwidth_code] = fw_itemtype
            if fw_itemtype.signedness_prefix == 'i':
                signed_typecodes_by_itemsize[fw_itemtype.itemsize] = pytc
            if fw_itemtype.signedness_prefix == 'u':
                unsigned_typecodes_by_itemsize[fw_itemtype.itemsize] = pytc

        self._fw_itemtypes_by_code = fw_itemtypes_by_code
        self._signed_typecodes_by_itemsize = signed_typecodes_by_itemsize
        self._unsigned_typecodes_by_itemsize = unsigned_typecodes_by_itemsize

    def resolve_typecode(self, typespec):
        if typespec in pyarray.typecodes:
            return typespec

        fw_itemtype = self._fw_itemtypes_by_code.get(typespec)
        return fw_itemtype and fw_itemtype.py_array_typecode

    def resolve_signed_itemsize(self, itemsize):
        return self._signed_typecodes_by_itemsize.get(itemsize)

    def resolve_unsigned_itemsize(self, itemsize):
        return self._unsigned_typecodes_by_itemsize.get(itemsize)

    def resolve_int_valuebounds(self, bounds):
        print(' == ')
        for fw_itemtype in self._fw_itemtypes_by_code.values():
            print(bounds, fw_itemtype, bounds in fw_itemtype.value_bounds)
            if bounds in fw_itemtype.value_bounds:
                return fw_itemtype.py_array_typecode


itemtype_resolver = ItemtypeResolver()
