from flask import Flask, request, jsonify
from test_sdk.test_dummy_workflow import generate_message
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve

app = Flask(__name__)


@app.route("/generate", methods=["POST"])
async def generate():
    try:
        data = request.get_json()
        query = data.get("query")

        if not query:
            return jsonify({"error": "Query is required"}), 400

        # Run the generate_message function
        print(query)
        result = await generate_message(query)

        return jsonify({"response": result})

    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Debug log
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    config = Config()
    config.bind = ["localhost:5001"]
    asyncio.run(serve(app, config))
