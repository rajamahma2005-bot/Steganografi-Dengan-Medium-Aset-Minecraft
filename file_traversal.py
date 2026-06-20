# fungsi DFS Folder & Counter jumlah PNG
def dfs_find_png(root_path: str) -> list[str]:
  found_paths: list[str] = []
  counter = 0

  def _dfs(current_dir: str) -> None:
    nonlocal counter
    try:
      entries = list(os.scandir(current_dir))
    except (PermissionError, FileNotFoundError):
      return

    for entry in entries:
      if entry.is_dir(follow_symlinks=False):
        _dfs(entry.path)
      elif entry.is_file() and entry.name.lower().endswith(".png"):
        counter += 1
        found_paths.append(entry.path)

  _dfs(root_path)
  print(f"Total PNG ditemukan: {counter}")
  return found_paths

# fungsi sortir array pathways
def sort_png_paths(png_paths: list[str]) -> list[str]:
  return sorted(png_paths, key=lambda p: (os.path.basename(p).lower(), p.lower()))

# fungsi tulis ulang sorted paths & path txt file
def write_sorted_path(sorted_path: list[str], output_txt_path: str) -> str:
  abs_paths = [os.path.abspath(p) for p in sorted_path]

  with open(output_txt_path, "w", encoding="utf-8") as f:
    for path in abs_paths:
      f.write(path + "\n")

  print(f"[TXT] {len(abs_paths)} path PNG ditulis ke : {output_txt_path}")
  return output_txt_path

# fungsi baca list PNG yang sudah sorted dari file txt
def read_path_list(txt_path: str) -> list[str]:
  with open(txt_path, "r", encoding="utf-8") as f:
    return [line.strip() for line in f if line.strip()]
