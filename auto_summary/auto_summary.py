# encoding=utf-8
import jieba
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
import chardet

'''
    中文自动摘要
    实现步骤：
        分句；分词；去停用词；建立词袋矩阵（每个句子为一行，每个词为一列，算tf-idf）；
        PageRank算句子权重，取top N的（默认N=1）句子当作摘要；
        用法：get_abstract(unicode_str, 5) 
        输入:source.txt 输出:summary.txt
'''


# 中文分句
def cut_sentence(sentence):
    # 非unicode的转为unicode
    if not isinstance(sentence, unicode):
        content_type = chardet.detect(sentence)
        sentence = sentence.decode(content_type['encoding'])
    # 按句号感叹号问号分句
    delimiters = frozenset(u'。！？')
    buf = []
    for ch in sentence:  # 遍历每个字
        buf.append(ch)
        if delimiters.__contains__(ch):
            yield ''.join(buf)
            buf = []
    if buf:
        yield ''.join(buf)


# 加载自定义停用词库
def load_stopwords(path='stopwords.txt'):
    with open(path) as f:
        stopwords = filter(lambda x: x, map(lambda x: x.strip().decode('utf-8'), f.readlines()))  # 停用词库要utf-8编码
    stopwords.extend([' ', '\t', '\n'])
    return frozenset(stopwords)


# 用结巴分词
def cut_words(sentence):
    stopwords = load_stopwords()
    return filter(lambda x: not stopwords.__contains__(x), jieba.cut(sentence))


# textRank 算法提取摘要
def get_abstract(content, size=1):
    docs = list(cut_sentence(content))
    tfidf_model = TfidfVectorizer(tokenizer=jieba.cut, stop_words=load_stopwords())
    tfidf_matrix = tfidf_model.fit_transform(docs)
    normalized_matrix = TfidfTransformer().fit_transform(tfidf_matrix)
    similarity = nx.from_scipy_sparse_matrix(normalized_matrix * normalized_matrix.T)  # 建立tf-idf的词袋
    scores = nx.pagerank(similarity)  # 用pagerank算句子权重
    tops = sorted(scores.iteritems(), key=lambda x: x[1], reverse=True)
    size = min(size, len(docs))  # 权重由高到低的句子
    indices = map(lambda x: x[0], tops)[:size]
    indices.sort()  # 维持句子在原文章中的先后顺序，原算法没这一步的
    return map(lambda idx: docs[idx], indices)  # 返回的是个list


# 测试效果
def check_performance(source_file="source.txt", summary_file="summary.txt"):
    with open(source_file, "r") as fr:
        content = fr.readlines()
        content = "".join(content)
        summary = get_abstract(content, 1)  # 1句话概括这篇文章
    with open(summary_file, 'w') as fw:
        for sentence in summary:
            fw.write((sentence+'\n').encode('utf-8'))
            print sentence


if __name__ == '__main__':
    check_performance()
