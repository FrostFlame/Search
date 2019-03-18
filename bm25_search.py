import math

from binary_search import get_list_of_lexems, ArticleTerm, TermList
from crawl import Article
from preprocessing import WordsPorter


def count_idf(word):
    word_id = TermList.select(TermList.term_id).where(TermList.term_text == word)
    x = ArticleTerm.select().where(ArticleTerm.term_id == word_id).count()
    idf = math.log10((30 - x + 0.5) / (x + 0.5))
    return idf


def search(request):
    words = get_list_of_lexems(request)
    docs = []
    arts = Article.select(Article.id)
    for art in arts:
        docs.append(art.id)
    avgdl = 0
    for doc in docs:
        avgdl += WordsPorter.select().where(WordsPorter.article_id == doc).count()

    avgdl = avgdl / 30
    bm25_scores = {}
    for doc in docs:
        k = 1.2
        b = 0.75
        d = WordsPorter.select().where(WordsPorter.article_id == doc).count()
        bm25 = sum([e if e > 0 else 0 for e in [count_idf(word) *
                    WordsPorter.select().where((WordsPorter.term == word) & (WordsPorter.article_id == doc)).count() * (k + 1) /
                    (WordsPorter.select().where((WordsPorter.term == word) & (WordsPorter.article_id == doc)).count()
                     + k * (1 - b + b * d / avgdl)) for word in words]])
        bm25_scores[doc] = bm25

    sorted_bm25 = sorted(bm25_scores.items(), key=lambda kv: kv[1], reverse=True)
    for i in range(10):
        id = sorted_bm25[i][0]
        cos = sorted_bm25[i][1]
        a = Article.select(Article.url).where(Article.id == id)
        print(a[0].url + ' ' + str(cos))


if __name__ == '__main__':
    s = 'ведьмак от мира сериалов'
    print(s)
    search(s)
