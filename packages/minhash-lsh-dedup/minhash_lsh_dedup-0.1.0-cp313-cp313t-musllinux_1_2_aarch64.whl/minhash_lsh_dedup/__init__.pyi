from typing import List

def generate_dedup_lsh(
    text: str, n_minhash: int, n_gram: int, n_buckets: int, bucket_size: int
) -> List[str]: ...

class LSHDeduplicator:
    seen: List[str]
    def __init__(self) -> None: ...
    def is_rejected(self, hashes: str) -> bool: ...
