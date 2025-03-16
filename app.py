import os
import json
import openai
from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv  # Load .env file

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def make_query_wacky(query):
    """
    Uses OpenAI to turn the search query into a ridiculous, funny, and rhyming version.
    """
    prompt = (
        f"Take the search query '{query}' and make it hilarious, absurd, and rhyme. "
        f"For example, 'How to do calculus' -> 'How to wrestle a walrus'. "
        f"Keep it really stupid,really funny, really weird, and really absurd and slightly related but make sure the new search rhymes with what the user said. The goal is to make the stuff as stupid and funny and possible. Return only the new query. ONLY THE NEW QUERY.  "
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a generator of absurd, rhyming search queries."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,
    )
    return response.choices[0].message.content.strip()

def generate_misspelled_steps(funny_query):
    """
    Uses OpenAI to generate 5 funny, misspelled steps on how to do the new search query.
    """
    prompt = (
        f"Generate exactly 5 funny, absurd, and badly misspelled steps for how to '{funny_query}'. "
        f"Each step should be ridiculous, exaggerated, and full of humorous typos. "
        f"Return ONLY a valid JSON array formatted like this:\n"
        f"[{{\"step\": \"Misspelled funny step\"}}]"
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You generate funny, badly misspelled instructions for ridiculous tasks."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,
    )

    json_response = response.choices[0].message.content.strip()
    
    try:
        steps = json.loads(json_response)
        if not isinstance(steps, list):  # Ensure it's a list
            raise ValueError("Invalid API response format")
    except Exception as e:
        print("Error parsing JSON:", e)
        steps = [{"step": "Errrorr! Cant think, brane ded."}]
    
    return steps

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    original_query = request.form.get('query', '').strip()
    if not original_query:
        return render_template('index.html', error="Please enter a search query.")
    
    # Generate a rhyming, wacky search query
    funny_query = make_query_wacky(original_query)
    
    # Generate misspelled funny steps
    steps = generate_misspelled_steps(funny_query)
    
    return render_template('results.html', original_query=original_query, funny_query=funny_query, steps=steps)

if __name__ == '__main__':
    app.run(debug=True)
