import pickle
import dotenv
from flask import Flask, request, render_template
# os.environ["LANGCHAIN_HANDLER"] = "langchain"
import faiss
from langchain import OpenAI
from langchain.chains import VectorDBQAWithSourcesChain
from langchain.prompts import PromptTemplate

# Redirect PosixPath to WindowsPath on Windows
import platform
if platform.system() == "Windows":
    import pathlib
    temp = pathlib.PosixPath
    pathlib.PosixPath = pathlib.WindowsPath

# loading the .env file
dotenv.load_dotenv()


with open("combine_prompt.txt", "r") as f:
    template = f.read()



app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/answer", methods=["POST"])
def api_answer():
    data = request.get_json()
    print(data)
    question = data["question"]
    api_key = data["api_key"]
    # check if the vectorstore is set
    if data['active_docs'] !='Choose documentation':
        vectorstore = "vectorstores/" + data["active_docs"]

    else:
        vectorstore = ""
    print(vectorstore)

    # loading the index and the store and the prompt template
    index = faiss.read_index(f"{vectorstore}docs.index")

    with open(f"{vectorstore}faiss_store.pkl", "rb") as f:
        store = pickle.load(f)

    store.index = index
    # create a prompt template
    c_prompt = PromptTemplate(input_variables=["summaries", "question"], template=template)
    # create a chain with the prompt template and the store
    chain = VectorDBQAWithSourcesChain.from_llm(llm=OpenAI(openai_api_key=api_key, temperature=0), vectorstore=store,
                                                combine_prompt=c_prompt)
    # fetch the answer
    loop= True
    result = None
    # setting up loop to avoid rate error by openai
    while loop:
        try:
            result = chain({"question": question})
            print('Result: ', result)
            loop=False
        except:
            print('OPEN AI RATE ERROR')
    print('Sources: ', result['sources'])

    # some formatting for the frontend
    result['answer'] = result['answer'].replace("\\n", "<br>")
    result['answer'] = result['answer'].replace("SOURCES:", "")
    # mock result
    # result = {
    #     "answer": "The answer is 42",
    #     "sources": ["https://en.wikipedia.org/wiki/42_(number)", "https://en.wikipedia.org/wiki/42_(number)"]
    # }

    print('Answer: ', result['answer'])
    return result


# handling CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


if __name__ == "__main__":
    app.run(debug=True)
