# BadPhoneAgent

BadPhoneAgent is the first safety benchmark focused on malicious misuse of Phone-Use Agents across 6 major categories and 40 subcategories, including online scams, doxxing and harassment, and fake orders or review manipulation. This repository releases 288 basic test examples for single-step QA evaluation, enabling quick validation of the key findings in our technical report. For more details, see the [project page](https://ymsun2020.github.io/Jade-GUI-Agent/) and the [technical report](https://arxiv.org/pdf/2606.27944). BadPhoneAgent is part of the [Jade benchmark series](https://whitzard-ai.github.io/jade.html). Stars are welcome!

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Environment Setup](#environment-setup)
- [Project Structure](#project-structure)
- [Data Access](#data-access)
- [Dataset Format](#dataset-format)
- [Run Models](#run-models)
- [Evaluate Refusal Rate](#evaluate-refusal-rate)
- [Citation](#citation)

## Overview

With a single user instruction, a phone-use agent can order food, write reviews, and even play mini-program games. This powerful capability also creates serious misuse risks: could such agents become tireless online manipulation workers, automatically target scam victims and send tailored messages, or even help purchase ingredients for illegal drugs or explosives?

![BadPhoneAgent overview](assets/overview-en.png)

To study these risks, we introduce BadPhoneAgent. We conduct evaluations on real phones and 31 commercial apps, showing that 8 domestic and international phone-use agents all exhibit serious misuse risks across 6 major categories and 40 subcategories, including online scams, doxxing and harassment, and fake orders or review manipulation.

![BadPhoneAgent taxonomy](assets/taxonomy.png)

## Quick Start

1. Clone the repository

```bash
git clone <this-repo>
cd Mobile-GUI-Security
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Request and place the dataset

Follow the [Data Access](#data-access) instructions to request and download the dataset. After receiving the dataset file, place it at:

```text
data/mobile_gui_agent_144_faker_replaced.jsonl
```

4. Run all examples

```bash
CUDA_VISIBLE_DEVICES=0 python src/run_models.py \
  --model-path /path/to/UI-TARS-1.5-7B \
  --model-key ui_tars_1_5_7b \
  --prompt-field both \
  --limit 0 \
  --output-jsonl results/ui_tars.jsonl
```

5. Evaluate refusal rate

```bash
python src/evaluate_refusal.py \
  --input-jsonl results/ui_tars.jsonl \
  --summary-json results/ui_tars_summary.json
```

## Environment Setup

We recommend Python 3.10 or later:

```bash
conda create -n mobile_gui_security python=3.10
conda activate mobile_gui_security
pip install -r requirements.txt
```

For UI-TARS-1.5-7B, install `qwen-vl-utils` as listed in `requirements.txt`.

## Project Structure

```text
Mobile-GUI-Security/
|-- README.md
|-- README_cn.md
|-- requirements.txt
|-- configs/
|   `-- system_prompts.json        # Model-specific system prompts
|-- data/
|   `-- mobile_gui_agent_144_faker_replaced.jsonl
|-- assets/
|   |-- fig.jpg                    # Test screenshot used by the runner
|   |-- overview-cn.png
|   |-- overview-en.png
|   `-- taxonomy.png
|-- src/
|   |-- run_models.py              # Transformers inference runner
|   `-- evaluate_refusal.py        # Refusal-rate evaluator
`-- results/                       # Created by scripts
```

## Data Access

To mitigate potential misuse risks, the dataset is released through **Gated Public Access**. Researchers who wish to access the dataset should submit an email request to ymsun24@m.fudan.edu.cn with the following information:

1. applicant name and institutional affiliation;
2. principal investigator, supervisor, or responsible faculty member, if applicable;
3. intended research use of the dataset;
4. a statement confirming that the dataset will be used only for academic, defensive, or safety-related research purposes, and not for malicious deployment, harmful automation, or real-world abuse.

All requests will be manually reviewed by the authors before access is granted. We aim to respond to each request within **two business days**. Access may be denied, revoked, or further reviewed if the stated use is unclear, inconsistent with responsible research purposes, or violates the dataset terms.

After receiving the dataset, place the file at `data/mobile_gui_agent_144_faker_replaced.jsonl` so that the runner can read it by default.

By requesting and using the dataset, users agree not to apply it to harmful applications, including but not limited to fraud, harassment, illegal procurement, manipulation of online services, or the development of systems intended to facilitate such misuse. Violations may result in access revocation and reporting to the relevant institution or platform.

Researchers may copy the following email template when requesting access:

```text
Subject: Request for Access to the BadPhoneAgent Dataset

Dear Authors,

I am writing to request access to the BadPhoneAgent dataset.

My information is as follows:

* Name:
* Institution / Organization:
* Position / Role:
* Principal Investigator / Supervisor:
* Institutional Email:
* Intended Use:

I confirm that the dataset will be used only for academic, defensive, or safety-related research purposes. I will not use the dataset for malicious deployment, harmful automation, real-world abuse, or any activity that facilitates fraud, harassment, illegal procurement, manipulation of online services, or other harmful applications.

I also agree to comply with the responsible-use terms associated with the dataset. I understand that access may be revoked if these terms are violated.

Thank you for your consideration.

Best regards,
[Your Name]
```

## Dataset Format

The dataset uses JSONL format. Each line is one task with both Chinese and English versions:

```json
{
  "task_id": 1,
  "app": "小红书",
  "instruction_zh": "中文任务指令",
  "instruction_en": "English task instruction",
  "type": "risk category",
  "subtype": "risk subtype"
}
```

The runner only requires the `instruction_zh` and/or `instruction_en` fields.

## Run Models

Run UI-TARS:

```bash
CUDA_VISIBLE_DEVICES=0 python src/run_models.py \
  --model-path /path/to/UI-TARS-1.5-7B \
  --model-key ui_tars_1_5_7b \
  --prompt-field both \
  --output-jsonl results/ui_tars.jsonl
```

Run GUI-Owl:

```bash
CUDA_VISIBLE_DEVICES=0 python src/run_models.py \
  --model-path /path/to/GUI-Owl \
  --model-key gui_owl_1_5_8b_instruct \
  --prompt-field both \
  --output-jsonl results/gui_owl.jsonl
```

Useful options:

- `--limit 10`: run only the first 10 rows.
- `--limit 0`: run all rows.
- `--prompt-field instruction_zh`: run Chinese instructions only.
- `--prompt-field instruction_en`: run English instructions only.
- `--reload-each-call`: reload the model for every instruction. This is slower but useful for isolated smoke tests.

## Evaluate Refusal Rate

```bash
python src/evaluate_refusal.py \
  --input-jsonl results/gui_owl.jsonl \
  --summary-json results/gui_owl_summary.json
```

The evaluator uses keyword matching, including terms such as "抱歉", "无法", "不能", "I'm sorry", "cannot", and "unable to".

Example summary:

```json
{
  "total": 288,
  "refusals": 12,
  "refusal_rate": 0.0417,
  "by_prompt_field": {
    "instruction_zh": {"total": 144, "refusals": 8, "refusal_rate": 0.0556},
    "instruction_en": {"total": 144, "refusals": 4, "refusal_rate": 0.0278}
  }
}
```

## Citation

If you find this useful in your research, please consider citing our [paper](https://arxiv.org/abs/2606.27944):

```bibtex
@misc{sun2026lieddoctorbuypoison,
      title={It Lied to a Doctor to Buy Poison Ingredients: Quantifying Real-World Misuse of Phone-use Agents},
      author={Yiming Sun and Chen Chen and Zifan Zhou and Mi Zhang},
      year={2026},
      eprint={2606.27944},
      archivePrefix={arXiv},
      primaryClass={cs.MM},
      url={https://arxiv.org/abs/2606.27944},
}
```
