from flask import Flask
from flask import request, current_app
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from flask import jsonify
from waitress import serve
import flair.embeddings
import gensim.models
import re
import numpy as np
import torch
import clinicalner

class W2vWordEmbeddings(flair.embeddings.TokenEmbeddings):
    def __init__(self, embeddings):
        self.name = embeddings
        self.static_embeddings = False
        self.precomputed_word_embeddings = (
            gensim.models.KeyedVectors.load_word2vec_format(
                embeddings, binary=False, limit=100000
            )
        )
        self.__embedding_length = self.precomputed_word_embeddings.vector_size
        super().__init__()

    @property
    def embedding_length(self):
        return self.__embedding_length

    def _add_embeddings_internal(self, sentences):
        for _, sentence in enumerate(sentences):
            for token, _ in zip(sentence.tokens, range(len(sentence.tokens))):
                token = token
                if token.text in self.precomputed_word_embeddings:
                    word_embedding = self.precomputed_word_embeddings[token.text]
                elif token.text.lower() in self.precomputed_word_embeddings:
                    word_embedding = self.precomputed_word_embeddings[
                        token.text.lower()
                    ]
                elif (
                    re.sub(r"\d", "#", token.text.lower())
                    in self.precomputed_word_embeddings
                ):
                    word_embedding = self.precomputed_word_embeddings[
                        re.sub(r"\d", "#", token.text.lower())
                    ]
                elif (
                    re.sub(r"\d", "0", token.text.lower())
                    in self.precomputed_word_embeddings
                ):
                    word_embedding = self.precomputed_word_embeddings[
                        re.sub(r"\d", "0", token.text.lower())
                    ]
                else:
                    word_embedding = np.zeros(self.embedding_length, dtype="float")
                word_embedding = torch.FloatTensor(word_embedding) # pylint: disable=no-member
                token.set_embedding(self.name, word_embedding)
        return sentences

model = flair.models.SequenceTagger.load('diseases-best.pt')

app = Flask(__name__)
@app.route('/')
def index_html():
    return current_app.send_static_file('index.xhtml')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

class ClinicalNer(Resource):
    @cross_origin()
    def post(self):
        content = request.get_json()
        result = clinicalner.annotate_text_as_dict(content["text"],model)
        return jsonify(result)
api.add_resource(ClinicalNer, '/endpoint')

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5555)