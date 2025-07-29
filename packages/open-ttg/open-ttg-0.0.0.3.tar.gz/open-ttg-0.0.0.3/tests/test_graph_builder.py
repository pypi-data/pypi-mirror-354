from unittest import TestCase
from text2graph.graph_builder import GraphBuilder


class Test_GraphBuilder(TestCase):
    def test_build_graph(self):
        builder = GraphBuilder(window_size=5, pmi_threshold=0.1)
        concepts = ['人工智能', '机器学习', '神经网络', '深度学习', '人工智能', '大模型', '神经网络']

        nodes, edges, pmis = builder.build_graph(concepts)
        self.assertEqual(nodes, ['人工智能', '机器学习', '神经网络', '深度学习', '大模型'])
        self.assertEqual(edges, [('人工智能', '机器学习'), ('机器学习', '神经网络'), ('深度学习', '神经网络'),
                                 ('人工智能', '深度学习'), ('人工智能', '大模型'), ('大模型', '神经网络'),
                                 ('人工智能', '神经网络'), ('机器学习', '深度学习'), ('大模型', '深度学习'),
                                 ('大模型', '机器学习')])
        self.assertEqual(pmis, [1.098612288668443, 0.40546510810883113, 1.098612288668443, 1.098612288668443,
                                0.40546510810883113, 1.098612288668443, 0.8109302162167733, 1.098612288668443,
                                1.098612288668443, 1.098612288668443])

    def test_build_graph_from_text(self):
        builder = GraphBuilder(window_size=5, pmi_threshold=0.1)
        concepts = ['人工智能', '机器学习', '神经网络', '深度学习', '人工智能', '大模型', '神经网络']
        text = '\n'.join(concepts)

        data = builder.build_graph_from_text(text)
        print("nodes, edges, pmis", data)
        self.assertEqual(data['nodes'], ['人工智能', '机器', '神经网络', '深度', '模型'])
        self.assertEqual(data['edges'],
                         [('人工智能', '机器'), ('机器', '神经网络'), ('深度', '神经网络'), ('人工智能', '深度'),
                          ('人工智能', '模型'), ('模型', '神经网络'), ('人工智能', '神经网络'), ('机器', '深度'),
                          ('模型', '深度'), ('机器', '模型')])
        self.assertEqual(data['pmis'], [1.098612288668443, 0.40546510810883113, 1.098612288668443, 1.098612288668443,
                                        0.40546510810883113, 1.098612288668443, 0.8109302162167733, 1.098612288668443,
                                        1.098612288668443, 1.098612288668443])
