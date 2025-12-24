import streamlit as st
import requests

st.title("AI Customer Support")
user_input = st.text_input("How can we help you?")

if st.button("Send"):
	try:
		response = requests.post(
			"http://localhost:5678/webhook/customer",
			json={"message": user_input}
		)
		response.raise_for_status()
		st.write(response.json().get("reply", "No reply received."))
	except Exception as e:
		st.error(f"Error: {e}")