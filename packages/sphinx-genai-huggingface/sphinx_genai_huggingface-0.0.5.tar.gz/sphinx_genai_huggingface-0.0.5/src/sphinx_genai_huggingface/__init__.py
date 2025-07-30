from pathlib import Path

from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer
import sphinx_genai as core


# https://huggingface.co/Xenova/all-MiniLM-L6-v2
# https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
model_name = "sentence-transformers/all-MiniLM-L6-v2"
# model_name = "nomic-ai/nomic-embed-text-v1"
model = SentenceTransformer(model_name, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')


def init(app):
    static_dir = Path(__file__).parent / Path("static")
    core.init(app, static_dir)


def count_tokens(text):
    encoded_input = tokenizer(text, return_tensors='pt') # 'pt' for PyTorch tensors
    token_ids = encoded_input['input_ids']
    tokens = tokenizer.convert_ids_to_tokens(token_ids[0].tolist())
    return len(tokens)


def embed(text):
    response = model.encode([text])
    embedding = response[0].tolist()
    return embedding


def generate_document_retrieval_embeddings(app, doctree, docname):
    embeddings = core.generate_document_retrieval_embeddings(docname, doctree, model_name, embed, count_tokens)
    core.save(app.srcdir, docname, embeddings)


def merge(app, exception):
    core.merge(app.srcdir, app.outdir)


def setup(app):
    global functions
    global model_name
    global model
    app.connect("builder-inited", init)
    app.connect("doctree-resolved", generate_document_retrieval_embeddings)
    app.connect("build-finished", merge)
    return {
        "version": "0.0.5",
        "parallel_read_safe": True,
        "parallel_write_safe": True
    }
