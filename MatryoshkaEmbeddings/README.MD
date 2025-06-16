## Matryoshka Embeddings

To compare the benchmark results in percentages, I'll use the average query times (`avg_query_time_seconds`) for each dimension and calculate the percentage difference relative to the "full" dimension (0.08909 seconds) as the baseline. This will show how much faster or slower each dimension is compared to the full dimension.
 
### Calculations
- **Full (0.08909 seconds)**: Baseline (100%)
- **256 dimensions (0.05909 seconds)**:
  - Difference: 0.08909 - 0.05909 = 0.03 seconds
  - Percentage difference: (0.03 / 0.08909) × 100 ≈ 33.67%
  - Result: 256 dimensions is ~33.67% faster than full.
- **128 dimensions (0.05316 seconds)**:
  - Difference: 0.08909 - 0.05316 = 0.03593 seconds
  - Percentage difference: (0.03593 / 0.08909) × 100 ≈ 40.32%
  - Result: 128 dimensions is ~40.32% faster than full.
- **64 dimensions (0.05063 seconds)**:
  - Difference: 0.08909 - 0.05063 = 0.03846 seconds
  - Percentage difference: (0.03846 / 0.08909) × 100 ≈ 43.17%
  - Result: 64 dimensions is ~43.17% faster than full.
 
### Summary
- **256 dimensions**: ~33.67% faster than full
- **128 dimensions**: ~40.32% faster than full
- **64 dimensions**: ~43.17% faster than full
 
The percentage improvements show that reducing dimensions consistently decreases query time, with 64 dimensions being the fastest, offering a 43.17% reduction in average query time compared to the full dimension.
 