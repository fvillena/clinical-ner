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
import json
import os
import torch

class MyEncoder(json.JSONEncoder):
    def default(self, obj): # pylint: disable=E0202
        if isinstance(obj, flair.data.Label):
            return str(obj)
        else:
            return super(MyEncoder, self).default(obj)

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

available_gpu = torch.cuda.is_available()
if available_gpu:
    print(f"GPU is available: {torch.cuda.get_device_name(0)}")
    flair.device = torch.device('cuda')
else:
    flair.device = torch.device('cpu')

def load_model(model_location):
    if os.path.exists(model_location):
        return flair.models.SequenceTagger.load(model_location)
    else:
        return None

diseases_model = load_model('diseases-best.pt')
body_parts_model = load_model('body_parts-best.pt')
abbreviations_model = load_model('abbreviations-best.pt')
neoplasm_morphologies_model = load_model('neoplasm_morphologies-best.pt')
neoplasm_topographies_model = load_model('neoplasm_topographies-best.pt')
medications_model = load_model('medications-best.pt')

app = Flask(__name__)
app.json_encoder = MyEncoder
@app.route('/index.xhtml')
def index_html():
    return current_app.send_static_file('index.xhtml')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

if diseases_model != None:
    class Diseases(Resource):
        @cross_origin()
        def post(self):
            content = request.get_json()
            result = clinicalner.annotate_text_as_dict(content["text"],diseases_model)
            return jsonify(result)
    api.add_resource(Diseases, '/diseases')

if body_parts_model != None:
    class BodyParts(Resource):
        @cross_origin()
        def post(self):
            content = request.get_json()
            result = clinicalner.annotate_text_as_dict(content["text"],body_parts_model)
            return jsonify(result)
    api.add_resource(BodyParts, '/body_parts')

if abbreviations_model != None:
    class Abbreviations(Resource):
        @cross_origin()
        def post(self):
            content = request.get_json()
            result = clinicalner.annotate_text_as_dict(content["text"],abbreviations_model)
            return jsonify(result)
    api.add_resource(Abbreviations, '/abbreviations')

if neoplasm_morphologies_model != None:
    class NeoplasmMorphologies(Resource):
        @cross_origin()
        def post(self):
            content = request.get_json()
            if "texts" in content:
                result = clinicalner.annotate_texts_as_dict(content["texts"],neoplasm_morphologies_model)
            else:
                result = clinicalner.annotate_text_as_dict(content["text"],neoplasm_morphologies_model)
            return jsonify(result)
    api.add_resource(NeoplasmMorphologies, '/neoplasm_morphologies')

if medications_model != None:
    class Medications(Resource):
        @cross_origin()
        def post(self):
            content = request.get_json()
            if "texts" in content:
                result = clinicalner.annotate_texts_as_dict(content["texts"],medications_model)
            else:
                result = clinicalner.annotate_text_as_dict(content["text"],medications_model)
            return jsonify(result)
    api.add_resource(Medications, '/medications')

if neoplasm_topographies_model != None:
    class NeoplasmTopographies(Resource):
        @cross_origin()
        def post(self):
            content = request.get_json()
            if "texts" in content:
                result = clinicalner.annotate_texts_as_dict(content["texts"],neoplasm_topographies_model)
            else:
                result = clinicalner.annotate_text_as_dict(content["text"],neoplasm_topographies_model)
            return jsonify(result)
    api.add_resource(NeoplasmTopographies, '/neoplasm_topographies')

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5555)
