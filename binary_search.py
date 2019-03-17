import string
import uuid
from functools import reduce

from nltk.corpus import stopwords
from peewee import *

from crawl import Article
from porter import Stemmer
from preprocessing import WordsPorter

db = PostgresqlDatabase('Articles', user='postgres', password='postgres', host='localhost', port=5432)


class TermList(Model):
    term_id = UUIDField(primary_key=True)
    term_text = CharField(unique=True)

    class Meta:
        database = db
        db_table = 'term_list'


class ArticleTerm(Model):
    article_id = ForeignKeyField(Article, to_field='id', db_column='article_id')
    term_id = ForeignKeyField(TermList, to_field='term_id', db_column='term_id')
    tf_idf = FloatField(db_column='tf-idf')

    class Meta:
        database = db
        primary_key = CompositeKey('article_id', 'term_id')
        db_table = 'article_term'


def create_tables():
    TermList.create_table()
    ArticleTerm.create_table()

    words = WordsPorter.select()
    set_of_pairs = set()
    dic_of_words = {}
    for word in words:
        if (word.term, word.article_id) not in set_of_pairs:
            set_of_pairs.add((word.term, word.article_id))
            if word.term not in dic_of_words.keys():
                dic_of_words[word.term] = uuid.uuid4()
                term_list = TermList(term_id=dic_of_words[word.term], term_text=word.term)
                term_list.save(force_insert=True)
            article_term = ArticleTerm(article_id=word.article_id, term_id=dic_of_words[word.term])
            article_term.save(force_insert=True)


def get_list_of_lexems(text):
    text = ' '.join([e.lower() for e in text.split(' ')])
    punctuation = string.punctuation + "«»—•’"

    porter = Stemmer()
    stop = stopwords.words('russian')
    for p in punctuation:
        text = text.replace(p, "")
    text = [word for word in text.split() if word not in stop]
    porter_words = [porter.stem(word) for word in text]
    return porter_words


def binary_search(request):
    words = get_list_of_lexems(request)
    words_dict = {}
    for word in words:
        words_dict[word] = ArticleTerm.select(ArticleTerm.article_id).join(TermList).distinct().where(
            TermList.term_text == word).count()
    for word in words:
        if words_dict[word] == 0:
            del words_dict[word]
    sorted_dict = [(k, words_dict[k]) for k in sorted(words_dict, key=words_dict.get)]
    sorted_dict_with_articles = {}
    for word in sorted_dict:
        sorted_dict_with_articles[word[0]] = [a.article_id for a in ArticleTerm.select(ArticleTerm.article_id).join(
            TermList).distinct().where(TermList.term_text == word[0])]
    result = reduce(get_intersection, sorted_dict_with_articles.values())
    for a in result:
        x = Article.select(Article.url).where(Article.id == a.id)
        print(x[0].url)


def get_intersection(a, b):
    result = []
    for elem1 in a:
        for elem2 in b:
            if elem1 == elem2:
                result.append(elem1)
    return result


if __name__ == '__main__':
    s = 'ведьмак от мира сериалов'
    print(s)
    binary_search(s)
    # ArticleTerm.create_table()
    # create_tables()
