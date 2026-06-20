# fungsi mengubah pesan menjadi bitstream
def message_to_bitstream(message: str) -> str:
    message_bytes = message.encode("utf-8")
    if len(message_bytes) > 0xFFFFFFFF:
        raise ValueError("Pesan terlalu panjang buat header 32-bit.")

    header_bits = format(len(message_bytes), "032b")
    message_bits = "".join(format(byte, "08b") for byte in message_bytes)
    return header_bits + message_bits

# fungsi ekstraksi pesan dari stegoimage
def extract_message_from_images(sorted_paths: list[str]) -> str:
    bit_gen = extract_bits_from_images(sorted_paths)

    header_bits = "".join(str(next(bit_gen)) for _ in range(32))
    message_length_bytes = int(header_bits, 2)

    message_bit_count = message_length_bytes * 8
    message_bits = "".join(str(next(bit_gen)) for _ in range(message_bit_count))

    message_bytes = bytes(
        int(message_bits[i:i + 8], 2) for i in range(0, len(message_bits), 8)
    )
    return message_bytes.decode("utf-8")
