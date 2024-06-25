import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, stream_with_context
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from flask_cors import CORS
# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

def get_response(user_query, chat_history):
    template = """
    Listen to patient doctor conversation and give your opinion.
    Please always consider chat history:\n\n{chat_history}
    """

    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI()
    chain = prompt | llm | StrOutputParser()

    return chain.stream({
        "chat_history": chat_history,
        "user_question": user_query,
    })

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json()
    user_query = data.get("input")
    chat_history = data.get("chat_history", [])

    if not user_query:
        return jsonify({"error": "User input is required"}), 400

    try:
        response = get_response(user_query, chat_history)
        return app.response_class(stream_with_context(response), mimetype='text/event-stream')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

