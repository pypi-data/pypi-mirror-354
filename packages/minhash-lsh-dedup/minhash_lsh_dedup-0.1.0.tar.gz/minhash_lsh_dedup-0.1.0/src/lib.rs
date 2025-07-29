use ::std::fmt::Write;
use murmur3::murmur3_32;
use pyo3::prelude::*;
use std::io::Cursor;

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

fn mmh3(text: &String, seed: u32) -> i32 {
    let mut bytes_reader = Cursor::new(text.as_bytes());
    let hash_value_u32 = murmur3_32(&mut bytes_reader, seed).unwrap();
    hash_value_u32 as i32
}

fn get_minhash(tokens: &[String], seed: u32) -> i32 {
    if tokens.is_empty() {
        return i32::MAX;
    }
    tokens
        .iter()
        .map(|text| mmh3(text, seed))
        .min()
        .unwrap_or(i32::MAX)
}

#[pyfunction]
fn generate_dedup_lsh(
    text: String,
    n_minhash: i64,
    n_gram: i64,
    n_buckets: i64,
    bucket_size: i64,
) -> PyResult<Vec<String>> {
    let n_gram_tokenized: Vec<String> = n_gram_tokenize(&text, n_gram as usize);
    let fingerprints: Vec<i32>=(0..n_minhash as u32).map(|seed|get_minhash(&n_gram_tokenized, seed)).collect();

    let mut lshs: Vec<String> = Vec::with_capacity(n_buckets as usize);
    let n_buckets_usize: usize=n_buckets as usize;
    let bucket_size_usize: usize=bucket_size as usize;
    for bucket_idx in 0..n_buckets_usize {
        let start_fp_idx = bucket_idx * bucket_size_usize;
        let end_fp_idx = (bucket_idx + 1) * bucket_size_usize;

        let actual_slice_start = std::cmp::min(start_fp_idx, fingerprints.len());
        let actual_slice_end = std::cmp::min(end_fp_idx, fingerprints.len());

        let estimated_fp_len = (actual_slice_end - actual_slice_start) * 4;
        let mut concatenated_fp_parts = String::with_capacity(estimated_fp_len);

        if actual_slice_start < actual_slice_end {
            for &fp_val in &fingerprints[actual_slice_start..actual_slice_end] {
                let val_to_format = (fp_val as u32) & 0xFFFF;
                write!(&mut concatenated_fp_parts, "{:04x}", val_to_format).unwrap();
            }
        }

        lshs.push(format!("{}+{}", bucket_idx, concatenated_fp_parts));
    }
    Ok(lshs)
}

#[pyclass]
struct LSHDeduplicator {
    seen: Vec<String>,
}

#[pymethods]
impl LSHDeduplicator {
    #[new]
    fn new() -> Self {
        Self { seen: Vec::new() }
    }
    fn is_rejected(&mut self, hashes: Vec<String>) -> PyResult<bool> {
        let mut num_rejected: i64 = 0;
        for hash in hashes {
            if self.seen.contains(&hash) {
                num_rejected += 1;
            } else {
                self.seen.push(hash.to_string());
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
