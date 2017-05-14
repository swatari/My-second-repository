import MeCab
from sklearn.feature_extraction.text import CountVectorizer

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

if __name__ == '__main__':
    data = [
        '水戸市千波 40歳男性',
        '水戸市堀町 30歳男性黒いズボン',
        '水戸市千波 60歳男性',
        '水戸市千波 40歳男性黒いズボン'
    ]

    wd = WordDividor()
    cv = CountVectorizer(analyzer=wd.extract_words)

    counts = cv.fit_transform(data)
    print(cv.get_feature_names())
    print(counts.toarray().transpose())

