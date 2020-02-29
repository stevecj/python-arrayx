import array as pyarray

from .utils import IntBounds, itemtype_resolver


typecodes = tuple(pyarray.typecodes) + ('c1', 'c2', 'c4', 'c8')


NOT_SUPPLIED = object()


class Array(pyarray.array):

    def __new__(
            cls, itemtype_spec, initializer=NOT_SUPPLIED, is_signed=None,
            **kwargs):
        if isinstance(itemtype_spec, str):
            pyarray_tc = itemtype_resolver.resolve_typecode(itemtype_spec)
        elif isinstance(itemtype_spec, int):
            is_signed = True if is_signed is None else is_signed
            if is_signed:
                pyarray_tc = itemtype_resolver.resolve_signed_itemsize(
                    itemtype_spec)
            else:
                pyarray_tc = itemtype_resolver.resolve_unsigned_itemsize(
                    itemtype_spec)
        elif isinstance(itemtype_spec, IntBounds):
            pyarray_tc = itemtype_resolver.resolve_int_valuebounds(itemtype_spec)

        args = (initializer,) if initializer is not NOT_SUPPLIED else ()
        return super().__new__(cls, pyarray_tc, *args, **kwargs)
