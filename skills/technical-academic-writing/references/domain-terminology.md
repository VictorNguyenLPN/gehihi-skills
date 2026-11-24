# Canonical Domain Terminology (SE, NLP, IR, CV)

Keep canonical English technical terms intact when writing in Vietnamese unless an established, unambiguous Vietnamese term exists. Never invent literal translations for standard concepts.

## 1. Natural Language Processing (NLP)

| Term | Exact Technical Scope |
| :--- | :--- |
| `tokenization`, `subword fertility` | Splitting text into tokens; average tokens per word for a given tokenizer |
| `autoregressive decoding` | Sequential left-to-right generation conditioned on prior tokens |
| `KV-cache`, `attention sink` | Cached key/value states across decoding steps; initial tokens absorbing high attention mass |
| `perplexity (PPL)` | Exponential of average negative log-likelihood per token |
| `exposure bias` | Train-inference discrepancy between teacher forcing and autoregressive rollout |
| `SFT`, `RLHF`, `DPO` | Supervised fine-tuning; RL from human feedback; Direct Preference Optimization |
| `faithfulness` vs. `factuality` | **Faithfulness**: consistency with provided source context. **Factuality**: accuracy against world knowledge |
| `in-context learning (ICL)` | Conditioning on demonstrations in the prompt without parameter updates |

## 2. Information Retrieval (IR)

| Term | Exact Technical Scope |
| :--- | :--- |
| `lexical retrieval` (`BM25`, `TF-IDF`) | Exact term-overlap scoring over inverted indexes |
| `learned sparse retrieval` (`SPLADE`) | Neural term-weight expansion compatible with inverted indexes |
| `dense retrieval` (`bi-encoder` / `dual-encoder`) | Independent query/document encoding into fixed-size vectors scored via dot product or cosine |
| `late interaction` (`ColBERT`, `MaxSim`) | Multi-vector token-level representations aggregated via maximum similarity |
| `cross-encoder reranking` | Joint query-document attention over top-k candidates |
| `hard negative mining` | Selecting high-scoring non-relevant passages (in-batch, BM25, or cross-batch) |
| `ANN` (`HNSW`, `IVF-PQ`) | Approximate Nearest Neighbor search indexes trading recall for sub-linear latency and RAM |
| `RRF` | Reciprocal Rank Fusion for rank-based hybrid score aggregation |
| `nDCG@k`, `MRR@k`, `Recall@k`, `MAP` | Standard ranked retrieval metrics; always specify cutoff `k` and graded vs. binary relevance |

## 3. Computer Vision (CV)

| Term | Exact Technical Scope |
| :--- | :--- |
| `receptive field` | Spatial extent of input pixels influencing a feature activation |
| `FPN` (Feature Pyramid Network) | Multi-scale top-down + lateral feature aggregation |
| `IoU` / `GIoU`, `mAP` (`AP50`, `AP50:95`) | Intersection over Union; mean Average Precision across IoU thresholds |
| `semantic` vs. `instance` vs. `panoptic segmentation` | Per-pixel class vs. per-object mask vs. unified stuff+things segmentation |
| `NMS` (Non-Maximum Suppression) | Post-processing step filtering overlapping bounding box predictions |
| `inductive bias` | Architectural priors (e.g., translation equivariance and locality in CNNs vs. global self-attention in ViTs) |
| `patch embedding` | Linear projection of fixed-size image patches into transformer token sequences |

## 4. Software Engineering (SE)

| Term | Exact Technical Scope |
| :--- | :--- |
| `tail latency` (`p95`, `p99`) vs. `throughput` (`QPS`/`RPS`) | High-percentile response time vs. sustained request rate |
| `idempotency` | Property where repeated identical requests produce the same state as one execution |
| `backpressure` | Flow-control mechanism propagating consumer saturation upstream to producers |
| `concurrency` vs. `parallelism` | Overlapping task lifetimes vs. simultaneous physical execution |
| `race condition`, `lock contention`, `deadlock` | Timing-dependent state corruption; threads blocking on shared locks; circular wait |
| `invariant`, `precondition`, `postcondition` | Conditions guaranteed to hold across state transitions, on entry, and on exit |
| `zero-copy` | Transferring/slicing data (e.g., `memoryview`, `mmap`, Arrow) without intermediate buffer copies |

