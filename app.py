from flask import Flask, jsonify, request
from flask_cors import CORS
import openai
import os

openai.api_key = "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"

# openai.api_key = "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"
app = Flask(__name__)

CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

def generate_prompt(patient_text, choice):
    """Generate prompt based on user's choice."""
    choice = int(choice)
    if choice == 1:
        return f"Based on the following progress note and medications, please tell me what diagnosis the patient would have. Here is the progress note: {patient_text}"
    elif choice == 2:
        return f"Based on the following progress note, please provide ICD10 and CPT codes for this visit. Here is the patient's progress note: {patient_text}"
    elif choice == 3:
        return f"Based on the following progress note, please provide Medicare verbiage if the patient can benefit from physical therapy based on the patient's diagnoses. Here is the patient's progress note: {patient_text}"
    elif choice == 4:
        return f"Spell check the following progress note and notify me if there are any spelling errors. Here is the progress note: {patient_text}"
    elif choice == 5:
        return f"Based on the following progress note, create a care plan based on the patient's diagnosis. Here is the patient's progress note: {patient_text}"
    else:
        return "Invalid choice."

@app.route('/get-prompt', methods=['POST'])
def get_prompt():
    # Extract notes array and choice from POST data
    data = request.json
    notes_array = data['notes']
    selected_option = data['choice']

    compiled_responses = []

    # Loop through each note in the notes_array
    for idx, note in enumerate(notes_array):
        # Generate a prompt based on the choice
        prompt = generate_prompt(note['text'], selected_option)

        # Call OpenAI and get the response
        response_content = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]).choices[0].message.content

        # Append a note marker and the response
        compiled_responses.append(f"Note {idx + 1}:")
        compiled_responses.append(response_content)

    # Structure the response for the frontend
    response = {
        'processedNotes': compiled_responses
    }

    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)