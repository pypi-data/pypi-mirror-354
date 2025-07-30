from typing import Iterable, Iterator


def bitpack(
    fields: Iterable[int],
    field_width: int,
    chunk_width: int,
) -> Iterator[int]:
    """Bit-pack integer fields into fixed-width chunks.

    Each entry in `fields` is treated as occupying `field_width` bits (including
    leading zeros). Fields are packed into chunks each holding `chunk_width`
    bits.

    Args:
        fields (Iterable[int]): The integer fields to pack.
        field_width (int): Number of bits per input field.
        chunk_width (int): Number of bits per output chunk.

    Returns:
        Iterator[int]: Iterator that generates bit-packed integer chunks, each
            up to `chunk_width` bits in size.

    Raises:
        ValueError: If `field_width` or `chunk_width` is not greater than 0.
        OverflowError: If the bit width of any field exceeds `field_width`.
    """
    if not field_width > 0:
        raise ValueError(
            f"'field_width' must be > 0 (got {field_width}).")
    if not chunk_width > 0:
        raise ValueError(
            f"'chunk_width' must be > 0 (got {chunk_width}).")

    field_mask = (1 << field_width) - 1
    chunk_mask = (1 << chunk_width) - 1

    stream = 0 # bits currently being processed
    size = 0 # bit size of `stream`
    for i, field in enumerate(fields):
        if field.bit_length() > field_width:
            raise OverflowError(
                f"Bit width of {field} ({field.bit_length()}) exceeds"
                f" 'field_width' ({field_width}).")

        field &= field_mask # clean up leading ones of negative field fields
        stream |= field << size
        size += field_width
        steps = int(size // chunk_width)
        for _ in range(steps):
            yield stream & chunk_mask
            stream >>= chunk_width
            size -= chunk_width
        if i == len(fields) - 1 and size:
            yield stream


def bitunpack(
    chunks: Iterable[int],
    chunk_width: int,
    field_width: int,
) -> Iterator[int]:
    """Unpack bit-packed chunks into integer fields.

    Each entry in `chunks` is treated as occupying `chunk_width` bits (including
    leading zeros). Chunks are unpacked into integer fields each representing
    `field_width` bits of the packed data.

    Args:
        chunks (Iterable[int]): The bit-packed chunks to unpack.
        chunk_width (int): Number of bits per input chunk.
        field_width (int): Number of bits per output field.

    Returns:
        Iterator[int]: Iterator that generates unpacked integer fields,
            each up to `field_width` bits in size.

    Raises:
        ValueError: If `field_width` or `chunk_width` is not greater than 0.
        OverflowError: If the bit width of any chunk exceeds `chunk_width`.
    """
    return bitpack(
        fields=chunks,
        field_width=chunk_width,
        chunk_width=field_width,
    )
