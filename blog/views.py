from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404

import sys
import numpy
import scipy as sp
import MeCab
from sklearn.feature_extraction.text import CountVectorizer

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    similar_posts = get_similar_posts(pky=pk)
    return render(request, 'blog/post_detail.html', {'post': post, 'posts':similar_posts})

def dist_raw(v1, v2):
    delta = v1-v2
    return sp.linalg.norm(delta.toarray())

def get_similar_posts(pky):
    wd = WordDividor()
    vectorizer = CountVectorizer(analyzer=wd.extract_words)

#   psts = []
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
#   psts.append(posts[0])
#   psts.append(posts[1])
#   psts.append(posts[2])

    samples = []
    for i in range(0, len(posts)):
        samples.append(posts[i].text)

    x_train = vectorizer.fit_transform(samples)
    num_samples, num_features = x_train.shape

    target_txt = Post.objects.get(pk=pky).text
    target_txt_vec = vectorizer.transform([target_txt])

    best_doc = None
    best_dist = float("inf")
    best_i = None

    samples_d = []
    results = []
    user_objs = []

    for i in range(0, num_samples):
        sample = samples[i]
        if sample==target_txt:
            continue
        post_vec = x_train.getrow(i)
        d = dist_raw(post_vec, target_txt_vec)
        user_objs.append(User_Posts(posts[i],d))

        if d<best_dist:
            best_dist = d
            best_i = i

    psts = []
#    psts.append(posts[i])

    sorted(user_objs, key=lambda u:u.dist, reverse=True)
    psts.append(user_objs[0].post)
    psts.append(user_objs[1].post)

    return psts
#####################################################
class User_Posts(object):
    def __init__(self, post, dist):
        self.post = post
        self.dist = dist
    def __repr__(self):
        return repr((self.post, self.dist))
#####################################################
class WordDividor:
    INDEX_CATEGORY = 0
    INDEX_ROOT_FORM = 6
    TARGET_CATEGORIES = ["名詞", " 動詞",  "形容詞", "副詞", "連体詞", "感動詞"]

    def __init__(self, dictionary="mecabrc"):
        self.dictionary = dictionary
        self.tagger = MeCab.Tagger(self.dictionary)

    def extract_words(self, text):
        if not text:
            return []

        words = []

        node = self.tagger.parseToNode(text)
        while node:
            features = node.feature.split(',')

            if features[self.INDEX_CATEGORY] in self.TARGET_CATEGORIES:
                if features[self.INDEX_ROOT_FORM] == "*":
                    words.append(node.surface)
                else:
                    # prefer root form
                    words.append(features[self.INDEX_ROOT_FORM])

            node = node.next

        return words
#####################################################
