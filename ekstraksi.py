from message_codec import bitstream_to_message

def extract_message_from_images(sorted_paths: list[str]) -> str:
    bit_gen = extract_bits_from_images(sorted_paths)  # generator baca LSB dari PNG
    return bitstream_to_message(bit_gen)               # decode jadi plaintext
