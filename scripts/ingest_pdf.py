from pathlib import Path
from langchain.text_splitter import CharacterTextSplitter
import faiss
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import pickle
import dotenv

dotenv.load_dotenv()

"""
# Here we load in the data in the format that Notion exports it in.
ps = list(Path("seaborn").glob("**/*.rst"))
# parse all child directories

data = []
sources = []
for p in ps:
    with open(p, encoding="utf8") as f:
        data.append(f.read())
    sources.append(p)
"""
# pdf to text
import PyPDF2
pdfFileObj = open('PDP document for QA bot.pdf', 'rb')
pdfReader = PyPDF2.PdfReader(pdfFileObj)
num_pages = len(pdfReader.pages)
print(pdfReader.pages)
data = []
for page in range(0, num_pages):
    print('print', page)
    pageObj = pdfReader.pages[page]
    page_text = pageObj.extract_text()
    data.append(page_text)
pdfFileObj.close()
data = data[0:15]
# Here we split the documents, as needed, into smaller chunks.
# We do this due to the context limits of the LLMs.
text_splitter = CharacterTextSplitter(chunk_size=1500, separator="\n")
docs = []
metadatas = []
for i, d in enumerate(data):
    splits = text_splitter.split_text(d)
    docs.extend(splits)
    #metadatas.extend([{"source": sources[i]}] * len(splits))

metadatas = [{'source':"Developers’ portal for PDP"}]*len(docs)
# Here we create a vector store from the documents and save it to disk.
store = FAISS.from_texts(docs, OpenAIEmbeddings(), metadatas=metadatas)
faiss.write_index(store.index, "docs.index")
store.index = None
with open("faiss_store.pkl", "wb") as f:
    pickle.dump(store, f)