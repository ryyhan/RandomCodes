import streamlit as st
from groq import Groq

# Initialize the Groq client
client = Groq(api_key=API_KEY)

# Streamlit app
def main():
    st.title("LLM Speed Test")

    # Get user input
    system_message = st.text_area("System Message", value="You are Batman. Respond like him")
    user_message = st.text_area("User Message", value="Hello, 'sup!")

    # Create completion parameters
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": user_message})

    model = st.selectbox("Model", ["llama3-70b-8192"])
    temperature = st.slider("Temperature", 0.0, 1.0, 0.5, 0.1)
    max_tokens = st.number_input("Max Tokens", min_value=1, value=1024)
    top_p = st.number_input("Top P", min_value=0.0, max_value=1.0, value=1.0)

    # Generate completion when the button is clicked
    if st.button("Generate Completion"):
        with st.spinner("Generating completion..."):
            chat_completion = client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                stop=None,
                stream=False,
            )
            result = chat_completion.choices[0].message.content
            st.success(result)

if __name__ == "__main__":
    main()