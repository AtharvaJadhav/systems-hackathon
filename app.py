from flask import Flask, render_template, request, jsonify
import openai
import os
import sys
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma


import constant



# Initialize Flask app
app = Flask(__name__)

# Configure OpenAI API key
os.environ["OPENAI_API_KEY"] = constant.APIKEY

# Initialize the index and chain
vectorstore = Chroma(embedding_function=OpenAIEmbeddings())
index = VectorStoreIndexWrapper(vectorstore=vectorstore)
loader = DirectoryLoader("data/")
index = VectorstoreIndexCreator().from_loaders([loader])
chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)

# In-memory store for chat history (for demonstration purposes)
# Note: For a production environment, consider using a more persistent storage system
chat_histories = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form['user_message']
    #user_id = request.form['user_id']  # Assuming user_id is passed from the client

    # Get or initialize chat history for the user
    #chat_history = chat_histories.get(user_id, [])
    chat_history = []

    # Process the query using the conversational chain
    result = chain({"question": user_message, "chat_history": chat_history})
    response = result['answer']

    # Update chat history
    #chat_history.append((user_message, response))
    #chat_histories[user_id] = chat_history

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
