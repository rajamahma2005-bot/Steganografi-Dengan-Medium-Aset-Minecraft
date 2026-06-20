def get_image_capacity_bits(image_path:str) -> int:
  with Image.open(Image_path) as img:
    img = img.convert("RGB")
    widht, height = img.size
    return widht * height * 3

def check_total_capacity(sorted_paths: list[str], bitstream_length: str) -> None:
  total_capacity = sum(get_image_capacity_bits(p) for p in sorted_paths)
  if bitstream_length > total_capacity:
    raise ValueError(f"Kapasitas tidak cukup, butuh {bitstream_length} bit", f"tersedia {total_capacity} bit dari {len(sorted_paths)} PNG")
  print(f"[CAPACITY] OK -> butuh {bitstream_length} bit, tersedia {total_capacity} bit.")

# fungsi embed bitstream pesan ke semua PNG
def embed_bitstream_to_images(sorted_paths: list[str], bitstream: str) -> None:
    check_total_capacity(sorted_paths, len(bitstream))

    bit_index = 0
    total_bits = len(bitstream)

    for path in sorted_paths:
        if bit_index >= total_bits:
            break  # bitstream udah abis, sisa file gak usah disentuh

        with Image.open(path) as img:
            img = img.convert("RGB")
            pixels = img.load()
            width, height = img.size

            for x, y in itertools.product(range(width), range(height)):
                if bit_index >= total_bits:
                    break
                r, g, b = pixels[x, y]
                channels = [r, g, b]

                for c in range(3):
                    if bit_index >= total_bits:
                        break
                    bit = int(bitstream[bit_index])
                    channels[c] = (channels[c] & 0b11111110) | bit  # ganti LSB doang
                    bit_index += 1

                pixels[x, y] = tuple(channels)

            img.save(path)  # overwrite PNG asli jadi stego-image

        print(f"[EMBED] {path} -> selesai (bit_index sekarang: {bit_index})")

    print(f"[EMBED] Total bit tersisip: {bit_index}/{total_bits}")
