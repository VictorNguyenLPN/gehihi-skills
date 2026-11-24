# Banned AI Lexicon & Structural Slop

Delete or rewrite every pattern below unless quoting a third-party source verbatim.

## 1. Banned English Words & Phrases

| Banned Word / Phrase | Why It Fails | Direct Replacement |
| :--- | :--- | :--- |
| `delve into`, `explore the intricacies` | Ornate filler verb | `analyze`, `evaluate`, `measure`, `inspect` |
| `tapestry`, `realm`, `landscape` | Vague metaphor | `domain`, `benchmark suite`, `ecosystem`, or name the concrete field |
| `testament to`, `underscore`, `pivotal`, `crucial`, `paramount` | Inflated emphasis without evidence | State the exact causal effect or quantitative impact |
| `paradigm shift`, `game-changer`, `revolutionize` | Marketing hype | Describe the specific algorithmic or architectural change |
| `seamless`, `seamlessly`, `effortless` | Unfalsifiable claim | State integration interface, latency overhead, or zero-copy mechanism |
| `foster`, `garner`, `leverage` (as filler for "use") | Corporate/AI cliché | `use`, `apply`, `enable`, `increase` |
| `meticulous`, `comprehensive`, `holistic` | Empty qualifier | State exact coverage (e.g., `tested across 6 benchmarks`) |
| `robust` (unqualified) | Meaningless unless perturbation is named | Specify: `robust to 20% label noise`, `invariant under rotation` |

## 2. Banned English Structural Patterns

- **Em-Dashes (`U+2014`)**: Replace with commas, colons, parentheses, or separate sentences.
- **Negative Parallelisms**: *"It is not merely X; it is Y."* / *"Not only does it solve A, it also unlocks B."* -> State `Y` or `A and B` directly.
- **Throat-Clearing Openers**: *"In recent years, the rapid advancement of..."*, *"In today's fast-paced world..."*, *"As Large Language Models continue to evolve..."* -> Start with the concrete problem statement or gap.
- **Participial Tails**: *"...thereby paving the way for future research."*, *"...highlighting the importance of..."*, *"...underscoring the potential of..."* -> Delete the tail or state the concrete next constraint.
- **Sycophancy / Meta-Commentary**: *"Certainly! Here is..."*, *"Great question!"*, *"In conclusion, we have shown that..."* -> Omit entirely.

## 3. Banned Vietnamese Filler & Translationese

| Mẫu câu sáo rỗng | Thay thế chuẩn xác |
| :--- | :--- |
| *"Trong bối cảnh hiện nay / sự phát triển vượt bậc của..."* | Đi thẳng vào bài toán hoặc giới hạn kỹ thuật cụ thể |
| *"Không thể phủ nhận rằng..."*, *"Một thực tế là..."* | Xóa bỏ; nêu trực tiếp mệnh đề kèm dẫn chứng |
| *"Đóng vai trò vô cùng quan trọng / then chốt..."* | Nêu chính xác cơ chế tác động hoặc đóng góp định lượng |
| *"Một bức tranh toàn cảnh..."*, *"Cánh cửa mới cho..."* | Dùng thuật ngữ cụ thể (`survey`, `benchmark`, `direction`) |
| *"Không chỉ dừng lại ở X mà còn Y"* (lạm dụng đối xứng) | Liệt kê thẳng `X` và `Y` |
| *"Tóm lại, có thể thấy rằng..."* | Trình bày kết luận định lượng hoặc xóa bỏ nếu lặp ý |

## 4. Before / After Examples

- **Slop**: *"In recent years, dense retrieval has garnered significant attention, underscoring its pivotal role in modern IR landscapes by seamlessly capturing semantic nuances."*
- **Edited**: *"Dense bi-encoder retrieval maps queries and documents into a shared embedding space, improving `Recall@100` over BM25 on out-of-domain semantic queries at the cost of higher memory footprint and ANN index latency."*

- **Slop (VI)**: *"Việc áp dụng cơ chế này đóng vai trò vô cùng quan trọng, không chỉ giúp tối ưu hiệu năng mà còn mang lại sự ổn định vượt trội cho hệ thống."*
- **Edited (VI)**: *"Batching các tensor query giúp giảm tail latency `p99` từ `42 ms` xuống `11 ms` và loại bỏ GPU-CPU sync overhead trong vòng lặp inference."*

