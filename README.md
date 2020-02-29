# python-arrayx
An enhancement to Python's array class with instantiation conveniences

Note that this is not yet a distribution package and is not yet versioned.

If you want to use this code today, you must simply copy the code into your
project.

## Requirements
Python 3.x

##Overview
The `array.array` class in the Python standard linrary has a single means
of specifying the size and signedness of the items it will contain which
is to supply a single-characer `typecode` string.  Each typecode
corresponds to a C-language data type, and many of those types have
different sizes depending on the platform. As a result, it can be difficult
to create an array of integer items with a specific platform-independent
size.

The `arrayx.Array` class is a subclass of `array.array` that supports the
initialization using any of the same typecodes that `array.array` accepts
but can also have its item properties specified by any of the following
methods.

### Fixed-Width Integer Typecode
A 2-letter typecode of "i1", "u1" "i2", "u2", "i4", "u4", "i8", or "u8".
The first letter indicates whether item values are signed or not ("i" for
signed integer or "u" for unsigned integer) and the number is the
item size in bytes.

### Integer Size and Optional Signedness
An integer value for the integer-type item size (signed by default) and an
optional `is_signed` argument to specify signed or unsigned.

### Minimum and Maximum Value Bounds via IntBounds Instance
An instance of `arrayx.IntBounds` may be given to indicate integer items
with the smallest itemsize that can represent any value from its
`minval` through (and including) its `maxval`. If either the signed or
unsigned type of that size qualifies, then the signed type is used.
If only the signed type of that size qualifies, then that is used.

## Examples
```
# Unsigned short (2-byte) items. Same as `array.array('H')`.
arrayx.Array('H')

# Float-type items. Same as `array.array('f')`.
arrayx.Array('f')

# Signed 4-byte integer items (typecode 'i' or 'l' depending on platform)
arrayx.Array('i4')

# Unsigned 8-byte integer items.
arrayx.Array(8, is_signed=False)

# Signed 2-byte integer items. Either of the following.
arrayx.Array(arrayx.IntBounds(0, 120)
arrayx.Array(arrayx.IntBounds(-1, 200)

# Unsigned 1-byte integer items.
arrayx.Array(arrayx.IntBounds(0, 200)
```

## Future
In the future, this library will also provide efficient enhanced
initialization of array contents such as specifying a size and value with
which to initially fill the items.
