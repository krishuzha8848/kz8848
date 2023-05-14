import streamlit as st
import requests
import json

# Function to get ChatGPT response
def get_chatgpt_response(query, temperature=0.7):
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "92c9fe48c2msh475fe4af8df9dcdp1c3a1bjsnde496d9e53e0",
        "X-RapidAPI-Host": "openai80.p.rapidapi.com"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ],
        "temperature": temperature
    }

    response = requests.post('https://openai80.p.rapidapi.com/chat/completions',
                             headers=headers,
                             json=payload)

    try:
        response_json = json.loads(response.content)
        return response_json['choices'][0]['message']['content']
    except KeyError:
        return ''

# Function to generate images
def generate_image(prompt):
    # Define the API endpoint URL
    url = "https://openai80.p.rapidapi.com/images/generations"

    # Define the payload data
    payload = {
        "prompt": prompt,
        "n": 2,
        "size": "1024x1024"
    }

    # Define the headers
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "92c9fe48c2msh475fe4af8df9dcdp1c3a1bjsnde496d9e53e0",
        "X-RapidAPI-Host": "openai80.p.rapidapi.com"
    }

    # Make the POST request to the API
    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the response data
        data = response.json()

        # Display the generated images
        for i, image_data in enumerate(data["data"]):
            image_url = image_data["url"]
            st.image(image_url, use_column_width=True)
            st.markdown(f'[Download Image {i+1}]({image_url})')
    else:
        st.error("Request failed with status code: " + str(response.status_code))

# Set page title and favicon
st.set_page_config(page_title="Chat and Image Generator", page_icon=":speech_balloon:")

st.title("Nepal Made AI Chatbot")

# HTML and CSS styles
styles = """
<style>
.chat-container {
    max-width: 600px;
    margin: 20px auto;
    padding: 20px;
    background-color: #f2f2f2;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    font-family: Arial, sans-serif;
}
.user-message {
    background-color: #d6eaf8;
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 10px;
    font-size: 16px;
}
.bot-message {
    background-color: #f5f5f5;
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 10px;
    font-size: 16px;
}
</style>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css">
"""

st.markdown(styles, unsafe_allow_html=True)
query = st.text_input('Enter Your Question to Chat:')
prompt = st.text_input("Enter a prompt to generate Image")

if st.button("Send"):
    if query:
        chatgpt_response = get_chatgpt_response(query, temperature=0.7)
        # Display the chat response
        st.markdown(
            f'<div class="chat-container"><div class="user-message">You: {query}</div><div class="bot-message">KZ 8848: {chatgpt_response}</div></div>',
            unsafe_allow_html=True)
    if prompt:
        generate_image(prompt)
    elif not query and not prompt:
        st.warning("Please enter a query or prompt")
