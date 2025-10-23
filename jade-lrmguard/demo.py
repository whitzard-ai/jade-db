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

# 生成JadeLRMGuard防护后的安全回答
response = JadeLRMGuard.decoding(
    model, 
    tokenizer, 
    prompt, 
    max_new_tokens=32768
)

# 查看回答
print(response)