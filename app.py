from flask import Flask, render_template, request, jsonify
import openai
import os
import constant
from flask_caching import Cache
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.vectorstores import Chroma

# Initialize Flask app
app = Flask(__name__)

# Configure OpenAI API key
os.environ["OPENAI_API_KEY"] = constant.APIKEY

# Configure and initialize Redis cache
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'  # Adjust if your Redis config differs
cache = Cache(app)

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
chat_histories = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form['user_message']
    user_id = request.form.get('user_id', 'default_user_id')

    # Compose a unique cache key based on the user message and user ID
    cache_key = f"user:{user_id}_message:{user_message}"
    cached_response = cache.get(cache_key)

    # If the response is cached, return it without calling the API
    if cached_response:
        return jsonify({'response': cached_response})

    # Get or initialize chat history for the user
    chat_history = chat_histories.get(user_id, [])

    # Process the query using the conversational chain
    result = chain({"question": user_message, "chat_history": chat_history})
    response = result['answer']

    # Update chat history and cache the response
    chat_history.append((user_message, response))
    chat_histories[user_id] = chat_history
    cache.set(cache_key, response, timeout=60*60)  # Cache for 1 hour

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
