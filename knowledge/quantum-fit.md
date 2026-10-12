# Quantum Fit

## When classical is the correct answer

- Problem size fits exact enumeration or strong classical MIP/heuristics.
- No precise mathematical kernel.
- Encoding overhead or noise destroys any theoretical scaling benefit.
- End-to-end cost (queue + sampling + post-processing) exceeds classical.

## When a teaching or research PoC is reasonable

- The kernel is a known hard combinatorial or simulation problem.
- A strong classical baseline already exists and is fairly measured.
- The experiment has a clear stop condition and success metric.
- Only synthetic or public data is used.

## Hard rule

Never claim quantum advantage without a reproducible end-to-end comparator that includes data preparation, optimization loop, sampling, decoding, queue time, and cost.
