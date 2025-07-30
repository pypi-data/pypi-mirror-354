# bitpacking

[Bit-packing](https://www.cs.cornell.edu/courses/cs3410/2024fa/notes/bitpack.html) and unpacking integer fields.

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bitpacking?style=flat-square)
![PyPI](https://img.shields.io/pypi/v/bitpacking?style=flat-square)
<!-- ![PyPI - Downloads](https://img.shields.io/pypi/dm/bitpacking?style=flat-square) -->
<!--![Commits since latest release](https://img.shields.io/github/commits-since/nieswand/bitpacking/latest?include_prereleases&style=flat-square) -->

## Installation
bitpacking is available on pypi:
```bash
pip install bitpacking
```

## Example
Basic usage example (can be found in [examples/pack_unpack.py](examples/pack_unpack.py)):

```python
from bitpacking import bitpack, bitunpack

ints = [
    1, 2, 0, 0,
    3, 0, 0, 0,
    0, 0, 0, 0,
    4, 0, 0, 0,
    0, 0, 0, 0,
    0, 5, 0, 6,
]

chunks = list(bitpack(fields=ints, field_width=3, chunk_width=64))
print(f"Bit-packed chunks: {chunks}")

fields = list(bitunpack(chunks=chunks, chunk_width=64, field_width=3))
print(f"Unpacked fields: {fields}")
```

Output:

```python
Bit-packed chunks: [9223372311732695057, 194]
Unpacked fields: [1, 2, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

Notice that the `fields` list has more entries than the initial `ints` list.
This is because the leading zeros in the last chunk (`194`) are unpacked into
"empty" fields.