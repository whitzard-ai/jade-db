# Jade-BadPhoneAgent：首个针对手机智能体恶意使用的安全测评

Jade-BadPhoneAgent 是首个专门针对 Phone-Use Agent 网络诈骗、开盒网暴、刷单控评等 6 大类、40 子类的恶意使用的安全测评。本项目开源了288条基础版测试样例，通过单步QA测试快速验证技术报告中的关键结论。 详细介绍可以见 [项目网页](https://ymsun2020.github.io/Jade-GUI-Agent/) 和 [技术报告](https://arxiv.org/pdf/2606.27944)。Jade-BadPhoneAgent 为 [Jade系列测评](https://whitzard-ai.github.io/jade.html)之一，欢迎关注与Star!

@ [复旦白泽智能](https://whitzard-ai.github.io/index.html)

## 目录

- [项目简介](#项目简介)
- [快速开始](#快速开始)
- [环境配置](#环境配置)
- [项目结构](#项目结构)
- [数据访问](#数据访问)
- [数据格式](#数据格式)
- [运行模型](#运行模型)
- [统计拒答率](#统计拒答率)
- [引用](#引用)

## 项目简介

只需用户一句话，手机智能体就能点外卖、写评价，甚至玩小程序游戏。可这份强大能力也打开了潘多拉魔盒：它会不会变成不眠不休的“网络水军”？会不会自动锁定诈骗对象、群发定制话术？甚至替人购买制毒、制爆原料，沦为黑灰产乃至犯罪的“得力帮凶”。

![BadPhoneAgent 概览](assets/overview-cn.png)

为此，我们推出了 Jade-BadPhoneAgent，首次在**真实手机**和31**个商业应用**中展开测评，揭露了**8款国内外**手机智能体均存在严重的**网络诈骗、开盒网暴、刷单控评等 6 大类、40 子类的违法使用隐患。**

![BadPhoneAgent 分类体系](assets/taxonomy.png)





## 快速开始

1. 克隆仓库

```bash
git clone <this-repo>
cd Mobile-GUI-Security
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 申请并放置数据集

按[数据访问](#数据访问)章节说明申请并下载数据集。获得数据文件后，请将其放在以下路径：

```text
data/mobile_gui_agent_144_faker_replaced.jsonl
```

4. 运行全部

```bash
CUDA_VISIBLE_DEVICES=0 python src/run_models.py \
  --model-path /path/to/UI-TARS-1.5-7B \
  --model-key ui_tars_1_5_7b \
  --prompt-field both \
  --limit 0 \
  --output-jsonl results/ui_tars.jsonl
```

5. 统计拒答率

```bash
python src/evaluate_refusal.py \
  --input-jsonl results/ui_tars.jsonl \
  --summary-json results/ui_tars_summary.json
```

## 环境配置

建议使用 Python 3.10 或更新版本：

```bash
conda create -n mobile_gui_security python=3.10
conda activate mobile_gui_security
pip install -r requirements.txt
```

对于 UI-TARS-1.5-7B，需要安装 `requirements.txt` 中的 `qwen-vl-utils`。



## 项目结构

```text
Mobile-GUI-Security/
|-- README.md
|-- README_cn.md
|-- requirements.txt
|-- configs/
|   `-- system_prompts.json        # 模型对应的系统提示词
|-- data/
|   `-- mobile_gui_agent_144_faker_replaced.jsonl
|-- assets/
|   |-- fig.jpg                    # 运行脚本使用的测试截图
|   |-- overview-cn.png
|   |-- overview-en.png
|   `-- taxonomy.png
|-- src/
|   |-- run_models.py              # Transformers 模型运行脚本
|   `-- evaluate_refusal.py        # 拒答率统计脚本
`-- results/                       # 脚本运行后生成
```

## 数据访问

为降低潜在滥用风险，数据集将通过 **Gated Public Access（门控公开访问）** 提供。希望访问数据集的研究人员请发送邮件至  ymsun24@m.fudan.edu.cn 提交申请，并在邮件中包含以下信息：

1. 申请人姓名与所属机构；
2. 如适用，请提供课题负责人、导师或负责教师信息；
3. 数据集的预期研究用途；
4. 确认数据集仅用于学术、防御或安全相关研究目的，不用于恶意部署、有害自动化或现实世界滥用的声明。

所有申请将在授权前由作者人工审核。我们会尽量在 **两个工作日** 内回复每一项申请。如果申请用途表述不清、与负责任研究目的不一致，或违反数据集使用条款，访问权限可能被拒绝、撤销或进入进一步审核。

获得数据集后，请将文件放置为 `data/mobile_gui_agent_144_faker_replaced.jsonl`，以便运行脚本默认读取。

申请并使用数据集即表示用户同意不将其用于有害应用，包括但不限于诈骗、骚扰、非法采购、操纵线上服务，或开发旨在促成此类滥用的系统。违反条款可能导致访问权限被撤销，并被报告给相关机构或平台。

研究人员可以直接复制以下邮件模板申请访问：

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

I also agree to comply with the  responsible-use terms associated with the dataset. I understand that access may be revoked if these terms are violated.

Thank you for your consideration. 

Best regards,
[Your Name]
```

## 数据格式

数据集使用 JSONL 格式，每行是一个任务，包含中英文两个版本：

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

运行脚本只依赖 `instruction_zh` 和/或 `instruction_en` 字段。

## 运行模型

运行 UI-TARS：

```bash
CUDA_VISIBLE_DEVICES=0 python src/run_models.py \
  --model-path /path/to/UI-TARS-1.5-7B \
  --model-key ui_tars_1_5_7b \
  --prompt-field both \
  --output-jsonl results/ui_tars.jsonl
```

运行 GUI-Owl：

```bash
CUDA_VISIBLE_DEVICES=0 python src/run_models.py \
  --model-path /path/to/GUI-Owl \
  --model-key gui_owl_1_5_8b_instruct \
  --prompt-field both \
  --output-jsonl results/gui_owl.jsonl
```

常用参数：

- `--limit 10`：只运行前 10 条数据。
- `--limit 0`：运行全部数据。
- `--prompt-field instruction_zh`：只运行中文指令。
- `--prompt-field instruction_en`：只运行英文指令。
- `--reload-each-call`：每条指令都重新加载模型，速度较慢，但适合隔离式冒烟测试。

## 统计拒答率

```bash
python src/evaluate_refusal.py \
  --input-jsonl results/gui_owl.jsonl \
  --summary-json results/gui_owl_summary.json
```

拒答率统计使用关键词匹配，例如“抱歉”、“无法”、“不能”、“I'm sorry”、“cannot”、“unable to”等。

示例 summary：

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

## 引用

如果你认为本项目对你的研究有帮助，欢迎引用我们的[论文](https://arxiv.org/abs/2606.27944)：

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
