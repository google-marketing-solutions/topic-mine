# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from services.client_trends_service import ClientTrendsService
from services.google_trends_service import GoogleTrendsService
from utils.utils import Utils
from flask import Flask, request, jsonify
import logging
import os
import datetime

app = Flask(__name__)

# Logger config
logging.basicConfig()
logging.root.setLevel(logging.INFO)

# Helpers and config
config = Utils.load_config('config.json')

client_trends_service = ClientTrendsService(config)
google_trends_service = GoogleTrendsService(config)


@app.route("/test")
def test_endpoint():
    """
    This is a test endpoint that returns a JSON response with a "Hello world!" message.

    Returns:
        A JSON response with a success message.
    """
    return jsonify({"message": "Hello world!"}), 200


@app.route("/trends/client/generate")
def generate_client_trends_content():
    """
    Entry point for client trends generation.

    Calls the service entry point and starts the copy generation process associated with client trends.

    Returns:
        A JSON response with a success message and a 200 status code in case of success.
        A JSON response with an error message and a 500 status code in case of an exception.
    """
    try:
        start_date = request.json.get("end_date", (datetime.date.today() - datetime.timedelta(days=7)).strftime("%Y-%m-%d"))
        end_date = request.json.get("start_date", datetime.date.today().strftime("%Y-%m-%d"))
    except:
        end_date = datetime.date.today().strftime("%Y-%m-%d")
        start_date = (datetime.date.today() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")

    return client_trends_service.start(start_date, end_date)


@app.route("/trends/google/generate")
def generate_google_trends_content():
    """
    Entry point for client trends generation.

    Calls the service entry point and starts the copy generation process associated with client trends.

    Returns:
        A JSON response with a success message and a 200 status code in case of success.
        A JSON response with an error message and a 500 status code in case of an exception.
    """
    return google_trends_service.start()


if __name__ == "__main__":
    logging.info('Starting server')
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    logging.info('Server started')
