use ::std::fmt::Write;
use murmur3::murmur3_32;
use pyo3::prelude::*;
use std::io::Cursor;
use std::collections::HashSet;

fn n_gram_tokenize(text: &String, n: usize) -> Vec<String> {
    let chars: Vec<char> = text.chars().collect();
    if chars.len() < n {
        if text.is_empty() && n == 0 {
            return Vec::new();
        }
        if text.is_empty() {
            return Vec::new();
        }
        return vec![text.to_string()];
    }

    let tokenized: Vec<String>=chars.windows(n).map(|window|window.iter().collect()).collect();
    tokenized
}

fn mmh3(text: &String, seed: u32) -> u32 {
    let mut bytes_reader = Cursor::new(text.as_bytes());
    let hash_value = murmur3_32(&mut bytes_reader, seed).unwrap();
    hash_value
}

fn get_minhash(tokens: &[String], seed: u32) -> u32 {
    if tokens.is_empty() {
        return u32::MAX;
    }
    tokens
        .iter()
        .map(|text| mmh3(text, seed))
        .min()
        .unwrap_or(u32::MAX)
}

#[pyfunction]
fn generate_dedup_lsh(
    text: String,
    n_minhash: i32,
    n_gram: i32,
    n_buckets: i32,
    bucket_size: i32,
) -> PyResult<Vec<String>> {
    let n_gram_tokenized: Vec<String> = n_gram_tokenize(&text, n_gram as usize);
    let fingerprints: Vec<u32>=(0..n_minhash as u32).map(|seed|get_minhash(&n_gram_tokenized, seed)).collect();

    let n_buckets_usize: usize=n_buckets as usize;
    let bucket_size_usize: usize=bucket_size as usize;
    let mut lshs: Vec<String> = Vec::with_capacity(n_buckets_usize);
    for bucket_idx in 0..n_buckets_usize {
        let start_fp_idx = bucket_idx * bucket_size_usize;
        let end_fp_idx = (bucket_idx + 1) * bucket_size_usize;

        let actual_slice_start = std::cmp::min(start_fp_idx, fingerprints.len());
        let actual_slice_end = std::cmp::min(end_fp_idx, fingerprints.len());

        let estimated_fp_len = (actual_slice_end - actual_slice_start) * 4;
        let mut concatenated_fp_parts = String::with_capacity(estimated_fp_len);

        if actual_slice_start < actual_slice_end {
            for &fp_val in &fingerprints[actual_slice_start..actual_slice_end] {
                let val_to_format = fp_val & 0xFFFF;
                write!(&mut concatenated_fp_parts, "{:04x}", val_to_format).unwrap();
            }
        }

        lshs.push(format!("{}+{}", bucket_idx, concatenated_fp_parts));
    }
    Ok(lshs)
}

#[pyclass]
struct LSHDeduplicator {
    seen: HashSet<String>,
}

#[pymethods]
impl LSHDeduplicator {
    #[new]
    fn new() -> Self {
        Self { seen: HashSet::new() }
    }
    fn is_rejected(&mut self, hashes: Vec<String>) -> PyResult<bool> {
        let mut num_rejected: i64 = 0;
        for hash in hashes {
            if self.seen.contains(&hash) {
                num_rejected += 1;
            } else {
                self.seen.insert(hash);
            }
        }
        Ok(num_rejected > 0)
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn minhash_lsh_dedup(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_dedup_lsh, m)?)?;
    m.add_class::<LSHDeduplicator>()?;
    Ok(())
}
