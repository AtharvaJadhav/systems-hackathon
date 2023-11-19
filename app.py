from flask import Flask, render_template, request, jsonify, send_from_directory
import openai
import os
import csv
import PyPDF2
import pdfplumber
import pandas as pd
from werkzeug.utils import secure_filename
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
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

# Set the folder for saving uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'csv', 'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Document conversion functions
# (place the conversion functions from your second script here)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form['user_message']

    # Process the query using the conversational chain
    result = chain({"question": user_message, "chat_history": []})
    response = result['answer']

    return jsonify({'response': response})

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']

        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Process the file based on its extension
            if filename.lower().endswith('.pdf'):
                text = convert_pdf_to_txt(file_path)
            elif filename.lower().endswith('.csv'):
                text = convert_csv_to_txt(file_path)
            elif filename.lower().endswith(('.xlsx', '.xls')):
                text = convert_excel_to_txt(file_path)

            # Saving the converted text to a file (optional)
            output_filename = filename + '.txt'
            output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            with open(output_filepath, 'w', encoding='utf-8') as text_file:
                text_file.write(text)

            return send_from_directory(app.config['UPLOAD_FOLDER'], output_filename, as_attachment=True)

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
