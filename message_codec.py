def _take_bits(bit_gen, n: int) -> str:
    bits = []
    for _ in range(n):
        bits.append(str(next(bit_gen)))
    return "".join(bits)


def message_to_bitstream(message: str) -> str:
    message_bytes = message.encode("utf-8")
    if len(message_bytes) > 0xFFFFFFFF:
        raise ValueError("Pesan terlalu panjang buat header 32-bit.")

    header_bits = format(len(message_bytes), "032b")
    message_bits = "".join(format(byte, "08b") for byte in message_bytes)
    return header_bits + message_bits


def bitstream_to_message(bit_gen) -> str:
    header_bits = _take_bits(bit_gen, 32)
    message_length_bytes = int(header_bits, 2)

    message_bit_count = message_length_bytes * 8
    message_bits = _take_bits(bit_gen, message_bit_count)

    message_bytes = bytes(
        int(message_bits[i:i + 8], 2) for i in range(0, len(message_bits), 8)
    )
    return message_bytes.decode("utf-8")
