
<h1 align="center">
  DocsGPT  🦖
</h1>

<p align="center">
  <strong>Open-Source Documentation Assistant</strong>
</p>

<p align="left">
  <strong>DocsGPT</strong> is a cutting-edge open-source solution that streamlines the process of finding information in project documentation. With its integration of the powerful <strong>GPT</strong> models, developers can easily ask questions about a project and receive accurate answers.
  
Say goodbye to time-consuming manual searches, and let <strong>DocsGPT</strong> help you quickly find the information you need. Try it out and see how it revolutionizes your project documentation experience. Contribute to its development and be a part of the future of AI-powered assistance.
</p>

<div align="center">

  <a href="https://discord.gg/n5BX8dh8rU">![example1](https://img.shields.io/github/stars/arc53/docsgpt?style=social)</a>
  <a href="https://discord.gg/n5BX8dh8rU">![example2](https://img.shields.io/github/forks/arc53/docsgpt?style=social)</a>
  <a href="https://discord.gg/n5BX8dh8rU">![example3](https://img.shields.io/github/license/arc53/docsgpt)</a>
  <a href="https://discord.gg/n5BX8dh8rU">![example3](https://img.shields.io/discord/1070046503302877216)</a>

</div>

## Flow of DocGPT

![Alt text](docsgpt.png?raw=true "Flow of DocGPT")

## Roadmap

You can find our [Roadmap](https://github.com/orgs/arc53/projects/2) here, please don't hesitate contributing or creating issues, it helps us make DocsGPT better!

## Screenshot
<img width="1440" alt="image" src="https://user-images.githubusercontent.com/15183589/216717215-adc6ea2d-5b35-4694-ac0d-e39a396025f4.png">

## [Live preview](https://docsgpt.arc53.com/)

## [Join Our Discord](https://discord.gg/n5BX8dh8rU)


## Project structure
application - flask app (main application)

extensions - chrome extension

scripts - script that creates similarity search index and store for other libraries 

## QuickStart
Please note: current vector database uses pandas Python documentation, thus responses will be related to it, if you want to use other docs please follow a guide below

1. Navigate to `/application` folder
2. Install dependencies
`pip install -r requirements.txt`
3. Prepare .env file
Copy .env_sample and create .env with your openai api token
4. Run the app
`python app.py`


[How to install the Chrome extension](https://github.com/arc53/docsgpt/wiki#launch-chrome-extension)


## [Guides](https://github.com/arc53/docsgpt/wiki)



## How to use any other documentation
How to train on other documentation
This AI can use any documentation, but first it needs to be prepared for similarity search.

Start by going to /scripts/ folder

If you open this file you will see that it uses RST files from the folder to create a docs.index and faiss_store.pkl.

It currently uses OPEN_AI to create vector store, so make sure your documentation is not too big. Pandas cost me around 3-4$

You can usually find documentation on github in docs/ folder for most open-source projects.

1. Find documentation in .rst and create a folder with it in your scripts directory
Name it inputs/ Put all your .rst files in there

If there are no .rst files just convert whatever you find to txt and feed it. (dont forget to change the extension in script)

2. Create .env file in scripts/ folder
And write your OpenAI API key inside OPENAI_API_KEY=<your-api-key>

3. Run scripts/ingest.py
python ingest.py

It will tell you how much it will cost

4. Move docs.index and faiss_store.pkl generated in scripts/ to application/ folder.
5. Run web app
Once you run it will use new context that is relevant to your documentation Make sure you select default in the dropdown in the UI

## Understanding Langchain

### What is langchain

It is used to build apps based on Large Language Models. Large Language Models (LLMs) are a core component of LangChain. LangChain is not a provider of LLMs, but rather provides a standard interface through which you can interact with a variety of LLMs.

### Flow of langchain:
  

![Alt text](understanding_langchain.png?raw=true "Flow of langchain")


### Why Prompt templates?

Normally when you use an LLM in an application, you are not sending user input directly to the LLM. Instead, you are probably taking user input and constructing a prompt, and then sending that to the LLM.

A prompt is the input to a language model. It is a string of text that is used to generate a response from the language model.

### What is chain

Using an LLM in isolation is fine for some simple applications, but many more complex ones require chaining LLMs - either with eachother or with other experts. LangChain provides a standard interface for Chains, as well as some common implementations of chains for easy use.

Example:

we can construct an LLMChain which takes user input, formats it with a PromptTemplate, and then passes the formatted response to an LLM.

From langchain.chains import LLMChain

chain=LLMChain(llm=llm,prompt=prompt)

### What is Tool?

A tools is a function that performs a specific duty. This can be things like: Google Search, Database lookup, Python REPL, other chains. The interface for a tool is currently a function that is expected to have a string as an input, with a string as an output.


