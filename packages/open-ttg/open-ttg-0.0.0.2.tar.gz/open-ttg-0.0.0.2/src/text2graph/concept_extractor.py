# concept_extractor.py

import math
from collections import Counter

import jieba.posseg as pseg


# ========== 功能性工具函数 ==========


def compute_cooccurrence(words, window_size=2):
    freq = Counter(words)
    cooc_pairs = []

    for offset in range(1, window_size):
        # 词列表和它自己位移offset后的列表打包
        pairs = zip(words, words[offset:])
        cooc_pairs.extend(pairs)

    cooc = Counter(cooc_pairs)
    total_windows = max(len(words) - window_size + 1, 1)
    return freq, cooc, total_windows


def compute_pmi(freq, cooc, total_windows):
    """
    计算所有词对的 PMI 值，不做阈值过滤。

    :param freq: 词频字典，freq[word]
    :param cooc: 共现频数字典，cooc[(w1, w2)]
    :param total_windows: 总窗口数，用于概率计算
    :return: dict，{(w1, w2): pmi_value}
    """
    pmi_dict = {}
    for (w1, w2), co_count in cooc.items():
        p_w1 = freq[w1] / total_windows
        p_w2 = freq[w2] / total_windows
        p_w1_w2 = co_count / total_windows
        # 避免对数零或负数
        pmi = math.log(p_w1_w2 / (p_w1 * p_w2) + 1e-12)
        pmi_dict[(w1, w2)] = pmi
    return pmi_dict


# ========== 概念抽取器类 ==========

class ConceptExtractor:
    def __init__(self, allowed_flags=None, stop_words=None, min_word_len=2):
        self.allowed_flags = allowed_flags or {'n', 'nz', 'vn', 'ns', 'nt'}
        self.stop_words = stop_words or {'的', '了', '是', '在', '和'}
        self.min_word_len = min_word_len

    def _filter_words(self, text):
        return [word for word, flag in pseg.cut(text)
                if flag in self.allowed_flags and len(word) >= self.min_word_len and word not in self.stop_words]

    def extract_by_pos(self, text):
        return self._filter_words(text)

    def extract_by_pmi(self, text, window_size=2, pmi_threshold=0.0):
        words = self._filter_words(text)
        freq, cooc, total_windows = compute_cooccurrence(words, window_size)
        pmi_dict = compute_pmi(freq, cooc, total_windows)

        # 过滤 PMI 阈值，获取满足条件的词对（合成的新概念）
        filtered_pairs = {pair for pair, pmi in pmi_dict.items() if pmi > pmi_threshold}

        # 把词和词对里拆分的单词都收集起来（不重复）
        all_terms = set(words)
        for w1, w2 in filtered_pairs:
            all_terms.add(w1 + w2)  # 合成词形式，可以换成其他拼接形式

        return list(all_terms)


def read_file(filepath):
    """
    读取文件全部内容，返回字符串
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("请在命令行输入要读取的文件路径，例如：")
        print("python concept_extractor.py example.txt")
        sys.exit(1)

    filepath = sys.argv[1]
    text = read_file(filepath)

    stopwords = {'的', '了', '是', '在', '和'}
    extractor = ConceptExtractor(stopwords=stopwords)
    concepts = extractor.extract_by_pos(text, min_word_len=2)
    print("词性过滤抽取:", concepts)

    # concepts = extractor.extract_by_pmi(text, min_word_len=2)
    # print("PMI合成抽取:", concepts)
