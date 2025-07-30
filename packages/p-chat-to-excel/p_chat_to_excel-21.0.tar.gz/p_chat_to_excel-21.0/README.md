# Chat-to-Excel 智能表格分析工具

通过大模型（如通义千问）自动解析Excel文本数据，支持检索增强生成（RAG）、智能分析、结果保存与Prompt配置本地保存，支持 PDF 知识库构建和智能问答生成。

---

## 📌 近期更新

### **Prompt配置持久化** 🔄
- **自动保存**：每次通过`info_collect()`设置的prompt参数，将自动保存至本地`prompt_tomb`目录
- **按名称隔离**：通过`name`参数创建不同实例角色，调取本地相应的prompt参数，实现多组独立配置共存
- **断点续用**：重启程序时自动加载同名实例的历史配置，无需重复输入参数
- **灵活管理**：通过例如`info_collect(param='prompt')`或`prompt`属性可单独修改特定参数，保留其他配置不变
- **细粒度控制**：支持通过chat(temperature=0.7)单独调整任意参数，保持其他配置不变。支持temperature、top_p、frequency_penalty
- **PDF 知识库构建**：通过P_RAGKnowledgeBase将本地pdf文件转为向量数据库
- **检索增强生成（RAG）**：内置P_RAGRetriever实现从知识库中找出与用户问题最相关信息的组件
- **根据知识库的智能问答**：chat(kb,top_k)实现外挂知识库的智能问答
- **自主设置并发量**：chat(max_workers)实现调整并发量以应对Open AI客户端请求超限

---

## 🚀 主要功能

### 1. 大模型交互
- 支持各类大模型（默认qwen-plus）
- 多线程并发处理（自动适配CPU核心数）

### 2. 灵活分析模式
- **全量分析**：处理完整数据集
- **抽样调试**：通过`data_sample()`抽取小样本测试Prompt效果
- **单/多字段**：支持单列独立分析或多列联合分析

### 3、检索增强生成（RAG）
- **PDF知识库构建**：支持通过PDF文档构建领域知识库
- **语义检索增强**：基于FAISS向量数据库实现毫秒级语义检索
- **上下文感知**：自动将相关文档片段注入大模型上下文
- **混合推理**：结合企业知识库与通用模型能力进行决策

### 3. 结果输出
- 自动插入分析结果列
- 保留原始数据结构
- 支持xlsx格式导出

---

## 使用示例（外挂数据库版，若不需要数据库，则无视第一步和obj.chat方法中的kb参数）

### 根据本地pdf搭建向量数据库
kb = P_RAGKnowledgeBase()，embedding_model_name默认为all-MiniLM-L6-v2，也可修改。默认chunk_size=500,chunk_overlap=50。
kb.build_from_pdf(r"pdf_file_path")  # 替换为你的PDF路径

### 初始化助理
name = 'name'
API_KEY = 'your_api_key'
BASE_URL = 'your_base_url'
obj = P_chat_to_excel(name,API_KEY,BASE_URL)

### 导入数据
obj.excel_info(path = r'excel_file_path',column=['COLUMN1','COLUMN2']) # 替换为你的excel路径和目标字段名

### 抽取小样本测试
obj.data_sample(10) # 抽取10条

### 配置prompt等相关信息
obj.info_collect()

### 针对样本数据智能问答并本地保存结果至excel
obj.chat(sample = True,temperature=0.2,top_p=0.7,kb=kb,top_k=3)

### 根据在样本上的输出效果修改prompt
obj.prompt = '''string''' # 替换为prompt的改善版本

### 若结果尚可，则保留原本配置，跑全量数据
obj.chat(sample = False,temperature=0.2,top_p=0.7,kb=kb,top_k=3)