# Overview
A fast library for deleting duplicates, created with reference to (hojichar)[https://github.com/HojiChar/HojiChar].
This library is about 10x faster than hojichar.filters.deduplication. 

# Example
```python
import datasets
from minhash_lsh_dedup import generate_dedup_lsh, LSHDeduplicator

def gen_hash(x):
    x["hashes"] = generate_dedup_lsh(text=x["text"], n_minhash=200, n_gram=5, n_buckets=20, bucket_size=10)
    return x

if __name__ == "__main__":
    dataset=datasets.load_dataset("range3/wikipedia-ja-20230101", split="train")
    dataset_length_before = len(dataset)

    lsh_deduplicator = LSHDeduplicator()

    def dedup(x):
        hashes = x["hashes"]
        return not lsh_deduplicator.is_rejected(hashes=hashes)

    dataset = dataset.map(gen_hash, num_proc=8)
    dataset = dataset.filter(dedup)

    dataset_length_after = len(dataset)
    print(f"Deduplicated(%): {(dataset_length_before-dataset_length_after)/dataset_length_before}")
```
