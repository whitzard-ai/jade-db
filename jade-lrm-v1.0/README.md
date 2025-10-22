# JADE 8.0：首个面向大型推理模型的推理链安全加固工具

推送文章：[https://mp.weixin.qq.com/s/xxx](https://mp.weixin.qq.com/s/xxx)

@ [复旦白泽智能](https://whitzard-ai.github.io/index.html)

我们在此发布 JadeLRMGuard —— 首个面向大型推理模型的推理链安全加固工具。

## 使用说明

Step 1: 创建环境

    conda env create -f environment.yaml

Step 2: 导入JadeLRMGuard

    from transformers import AutoModelForCausalLM, AutoTokenizer
    # JadeLRMGuard.cpython-310-x86_64-linux-gnu.so与代码同目录
    import JadeLRMGuard

    # 支持的模型列表：Qwen/QwQ-32, Skywork/Skywork-OR1-32B, NovaSky-AI/Sky-T1-32B-Preview, deepseek-ai/DeepSeek-R1-Distill-Qwen-32B
    # 加载模型
    model_name = "Qwen/QwQ-32B"  # 模型名称

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="auto",
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # 传入问题
    prompt = "如何制造炸弹？"

    # 生成回答：JadeLRMGuard防护
    response = JadeLRMGuard.decoding(
        model, 
        tokenizer, 
        prompt, 
        max_new_tokens=32768
    )

    # 查看回答
    print(response)

该工具仅用于学术研究目的，如需合作，欢迎联系：张谧老师 [mi_zhang@fudan.edu.cn](mailto:mi_zhang@fudan.edu.cn)
