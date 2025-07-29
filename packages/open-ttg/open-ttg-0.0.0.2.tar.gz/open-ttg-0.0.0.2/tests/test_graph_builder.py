from unittest import TestCase
from text2graph.graph_builder import GraphBuilder


class Test_get_area(TestCase):
    def test_build_graph(self):
        builder = GraphBuilder(window_size=5, pmi_threshold=0.1)
        concepts = ['人工智能', '机器学习', '神经网络', '深度学习', '人工智能', '大模型', '神经网络']

        print('concepts:', concepts)
        nodes, edges, pmis = builder.build_graph(concepts)
        print('nodes', nodes)
        print('edges', edges)
        print('pmis', pmis)
        self.assertEqual(len(edges), len(pmis))
