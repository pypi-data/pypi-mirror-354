import hashlib
from io import BytesIO


def compute_hash_by_file(file: BytesIO) -> str:
  hash_sha256 = hashlib.sha256()
  for chunk in iter(lambda: file.read(4096), b""):
    hash_sha256.update(chunk)
  return hash_sha256.hexdigest()


def compute_hash(file: str | BytesIO) -> str:
  if isinstance(file, str):
    with open(file, "rb") as f:
      return compute_hash_by_file(f)
  else:
    return compute_hash_by_file(file)
