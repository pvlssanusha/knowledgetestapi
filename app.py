from flask import Flask, request, jsonify
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Replace 'YOUR_COHERE_API_KEY' with your Cohere API key

# Initialize the Cohere Client with an API Key
api = os.getenv("GEMINI_API_KEY")
api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + api

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/', methods=['POST'])
def get_response():
    try:
        coursename = request.get_json().get('coursename')
        prerequisitelist=request.get_json().get('prerequisitelist')
        
            # Define the request payload
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": 
                            f'''
        Generate 8 easy, 6 medium and 6 hard level multiple choice questions on prereqiusites which have only 4 options the course {coursename} which has prerequisites : {prerequisitelist} .Generate questions only based on prerequisites ani ivvu. 
                    Give output strictly in the following JSON format:
                    {{
                        "quizName": "string",
                        "easy/medium/hard": [
                            {{
                                "question": "string",
                                "options": ["strings"],
                                "correctOption": "Number" // index of correct option
                            }}],
                        
                    }}
        '''
                        }
                    ]
                }
            ]
        }

        # Set the headers
        headers = {
            "Content-Type": "application/json"
        }

        # Make the API call
        response = requests.post(api_url, json=payload, headers=headers)

        if response.status_code == 200:
            # Parse and print the response JSON
            response_json = response.json()
            if (response_json["candidates"][0]["content"]["parts"][0]["text"][0]=="{"):
                return (response_json["candidates"][0]["content"]["parts"][0]["text"])
            else:
                if response_json["candidates"][0]["content"]["parts"][0]["text"][3:-3][0]=="J" or response_json["candidates"][0]["content"]["parts"][0]["text"][3:-3][0]=="j":
                    return (response_json["candidates"][0]["content"]["parts"][0]["text"][7:-3])
                else:
                    return (response_json["candidates"][0]["content"]["parts"][0]["text"][3:-3])

            # print(json.dumps(response_json, indent=2))
            # print(response_json)
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return json.dump(
            {
                "msg":"Error Assessing AI"
            }
            ) 

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
