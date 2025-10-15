# JADE 7.0：面向智能体安全的MCP恶意server实例集合



推送文章：[https://mp.weixin.qq.com/s/9De_RR-jX-c04hhaBuhniQ](https://mp.weixin.qq.com/s/9De_RR-jX-c04hhaBuhniQ)

@ [复旦白泽智能](https://whitzard-ai.github.io/index.html)

我们在此发布 JADE-MCP —— 面向智能体安全的MCP恶意server实例集合。

## 数据集说明

随着OpenAI、Cursor等主流模型厂商和开发工具的相继支持，一个以Model Context Protocol（MCP）为核心的繁荣AI应用生态正迅速形成。以MCP.so平台为例，其收录的MCP Server数量已超过15,000个。然而，这个开放、繁荣的新生态，也为智能体的负责任部署带来了全新的安全隐患。

在此背景下，JADE 7.0 项目重点研究了 MCP 生态系统面临的两种关键投毒攻击：一是通过篡改工具描述实现的直接攻击，二是通过污染外部信息源发起的间接攻击。为了支撑这项研究，我们通过多源数据整合与人工筛选，构建了一个包含 6 大类、33 个子类的 MCP 恶意 server 实例集合。本开源仓库主要涉及隐私泄露风险大类的恶意 server 实例。

- **BenignServers**：良性server实例集合；
- **PrivacyLeakage**：隐私泄露风险大类的恶意server实例；
- **prompts_DP.py**：基于工具描述的直接投毒攻击的提示词模板；
- **prompts_MER.py**：基于外部资源的间接投毒攻击的提示词模板。




该数据集仅用于学术研究目的，如需合作或完整集合，欢迎联系：张谧老师 [mi_zhang@fudan.edu.cn](mailto:mi_zhang@fudan.edu.cn)

