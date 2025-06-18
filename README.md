# 🧮 24 Points O1 Training with Qwen2.5-0.5B

This project demonstrates how to fine-tune a compact language model, [Qwen2.5-0.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct), using the **O1-CoT (one-step chain-of-thought)** paradigm to solve the classic 24-point arithmetic game. Our training achieves **98.9% accuracy** while maintaining **single-step inference**, enabling efficient deployment on edge devices.

📄 **More details**: See our full report here:  
👉 [O1_Training_Report.pdf](https://github.com/HuYunhai-Alex/O1-24-Game/blob/main/O1_Training_Report.pdf)

---

## 🚀 Highlights

- 🔗 **O1-CoT Fine-tuning**: Embed one-step reasoning patterns in the prompt; no autoregressive CoT chains required.
- 🧠 **SFT**: Begin with instruction tuning, bootstrap new examples.
- 📉 **Efficiency**: Reduce latency by **35%** over baseline without increasing model size or inference length.
- 🔍 **Model**: Qwen2.5-0.5B (12-layer Transformer, 2048 hidden size, 16 heads)

---

## 🗃️ Dataset Format

Training samples follow an SFT-style JSONL format with inline reasoning:

```json
{
  "instruction": "Solve the 24 based on the given input and provide your reasoning.",
  "input": "[5, 9, 13, 3]",
  "output": "<think>
Combine 5 + 9 = 14
Combine 13 - 3 = 10
Combine (5+9)+(13-3) = 24
</think>
Final Solution:
((5+9)+(13-3)) = 24"
}
```

All examples contain:

instruction: fixed task prompt

input: 4 integer cards

output: <think>...</think> block and a final expression

## 📂 Repo Structure
```text
├── data/                     # Training/test data
├── train/                    # Training config(Llama-factory yaml)
├── gen_data/                 # generate CoT step by step data
├── O1_Training_Report.pdf    # report
└── README.md
```
