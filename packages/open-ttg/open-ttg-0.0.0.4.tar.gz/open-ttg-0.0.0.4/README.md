# Text2Graph
🌐 Languages: [中文](./README.zh.md)

---

## 📚 Table of Contents

* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)

  * [Build from Concept List](#build-from-concept-list)
  * [Build from Text](#build-from-text)
* [Output Format](#output-format)
* [Testing](#testing)

---

## 🚀 Features

* Build graphs from concept lists or raw text
* Customizable sliding window size and PMI threshold
* Returns graph data with nodes, edges, and PMI scores

---

## 🔧 Installation

```bash
pip install -e .
```

---

## 🧠 Usage

### Build from Concept List

```python
from text2graph.graph_builder import GraphBuilder

builder = GraphBuilder(window_size=5, pmi_threshold=0.1)
concepts = ['人工智能', '机器学习', '神经网络', '深度学习', '人工智能', '大模型', '神经网络']

nodes, edges, pmis = builder.build_graph(concepts)
```

### Build from Text

```python
from text2graph.graph_builder import GraphBuilder

builder = GraphBuilder(window_size=5, pmi_threshold=0.1)
text = '\n'.join(['人工智能', '机器学习', '神经网络', '深度学习', '人工智能', '大模型', '神经网络'])

data = builder.build_graph_from_text(text)
nodes = data['nodes']
edges = data['edges']
pmis = data['pmis']
```

---

## 📦 Output Format

* `nodes`: List of unique concepts
* `edges`: List of tuples (concept1, concept2)
* `pmis`: List of PMI scores corresponding to each edge

---

## ✅ Testing

```bash
python -m unittest
```

---


# For Developers
## setup docker env
```text
docker build -t text2graph -f docker/Dockerfile .
docker run -it --rm --name text2graph -v .\:/code text2graph bash
```