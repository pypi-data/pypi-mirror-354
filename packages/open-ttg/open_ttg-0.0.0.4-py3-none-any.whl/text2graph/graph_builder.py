import json
from collections import Counter, defaultdict
import math

from text2graph.concept_extractor import ConceptExtractor


def save_graph(filename, nodes, edges, pmis):
    data = {'nodes': nodes, 'edges': edges, 'pmis': pmis}
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_graph(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        nodes = data.get('nodes', [])
        edges = data.get('edges', [])
        pmis = data.get('pmis', [])
        return nodes, edges, pmis


class GraphBuilder:
    def __init__(self, window_size=2, pmi_threshold=0.0):
        self.window_size = window_size
        self.pmi_threshold = pmi_threshold

    def build_graph_from_text(self, text, directed=False):
        extractor = ConceptExtractor()
        concepts = extractor.extract_by_pos(text)

        nodes, edges, pmis = self.build_graph(concepts, directed=directed)

        return {
            'nodes': nodes,
            'edges': edges,
            'pmis': pmis
        }

    def build_graph(self, word_list, directed=False):
        print('Building graph...')
        print('window size: ', self.window_size)
        print('pmi threshold: ', self.pmi_threshold)
        freq, cooc, total_windows = self.compute_cooccurrence(word_list, self.window_size)
        pmi_dict = self.compute_pmi(freq, cooc, total_windows, symmetric=not directed)

        nodes = list(freq.keys())
        edges = []
        pmi = []

        for (w1, w2), pmi_val in pmi_dict.items():
            if pmi_val >= self.pmi_threshold and w1 != w2:
                edges.append((w1, w2))
                pmi.append(pmi_val)

        return list(nodes), edges, pmi

    @staticmethod
    def compute_cooccurrence(nodes, window_size=2):
        freq = Counter(nodes)
        cooc_pairs = []

        for offset in range(1, window_size):
            pairs = zip(nodes, nodes[offset:])
            cooc_pairs.extend(pairs)

        cooc = Counter(cooc_pairs)
        total_windows = max(len(nodes) - window_size + 1, 1)
        return freq, cooc, total_windows

    @staticmethod
    def compute_pmi(freq, cooc, total_windows, symmetric=False):
        """
        计算 PMI 值，可选对称处理（无向边）。

        :param freq: 词频 dict
        :param cooc: 共现频 dict（可能有向）
        :param total_windows: 总窗口数
        :param symmetric: 是否合并方向
        :return: dict，{(w1, w2): pmi}
        """
        if symmetric:
            merged_cooc = defaultdict(int)
            for (w1, w2), count in cooc.items():
                key = tuple(sorted((w1, w2)))
                merged_cooc[key] += count
            cooc = merged_cooc  # 用合并后的覆盖原 cooc

        pmi_dict = {}
        for (w1, w2), co_count in cooc.items():
            p_w1 = freq[w1] / total_windows
            p_w2 = freq[w2] / total_windows
            p_w1_w2 = co_count / total_windows
            pmi = math.log(p_w1_w2 / (p_w1 * p_w2) + 1e-12)
            pmi_dict[(w1, w2)] = pmi

        return pmi_dict


if __name__ == "__main__":
    builder = GraphBuilder(window_size=5, pmi_threshold=0.1)
    concepts = ['人工智能', '机器学习', '神经网络', '深度学习', '人工智能', '大模型', '神经网络']

    print('concepts:', concepts)
    nodes, edges, pmis = builder.build_graph(concepts)
    print('nodes', nodes)
    print('edges', edges)
    print('pmis', pmis)
