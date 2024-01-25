import json
import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000"  # Замените на ваш URL


def sign_in():
    st.subheader("Sign In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign In"):
        response = requests.post(f"{API_BASE_URL}/auth/sign-in", json={"username": username, "password": password})
        if response.status_code == 200:
            st.success("Sign in successful!")
            st.json(response.json())
            return response.json().get("user_info")
        else:
            st.error("Sign in failed.")
            st.text(response.text)
            return None


def sign_up():
    st.subheader("Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        response = requests.post(f"{API_BASE_URL}/auth/sign-up", json={"username": username, "password": password})
        if response.status_code == 200:
            st.success("User registration successful!")
            st.json(response.json())
            return response.json().get("user_info")
        else:
            st.error("User registration failed.")
            st.text(response.text)
            return None


def get_user_balance():
    st.subheader("Get User Balance")
    response = requests.get(f"{API_BASE_URL}/billing/points")
    if response.status_code == 200:
        st.success(f"User balance: {response.json()} points")
    else:
        st.error("Failed to retrieve user balance.")
        st.text(response.text)


def deduct_credits():
    st.subheader("Deduct Credits")
    points = st.number_input("Points to deduct", min_value=1, step=1)
    reason = st.text_input("Deduction reason")
    if st.button("Deduct Credits"):
        response = requests.post(f"{API_BASE_URL}/billing/deduct", json={"points": points, "reason": reason})
        if response.status_code == 200:
            st.success("Credits deducted successfully.")
            st.json(response.json())
        else:
            st.error("Failed to deduct credits.")
            st.text(response.text)


def get_billing_history():
    st.subheader("Get Billing History")
    response = requests.get(f"{API_BASE_URL}/billing/history")
    if response.status_code == 200:
        st.success("Billing history retrieved successfully.")
        st.json(response.json())
    else:
        st.error("Failed to retrieve billing history.")
        st.text(response.text)


def make_prediction():
    st.subheader("Make Prediction")
    model_name = st.text_input("Model Name")
    input_data = st.text_area("Input Data (JSON format)")
    if st.button("Make Prediction"):
        try:
            input_data = json.loads(input_data)
            response = requests.post(f"{API_BASE_URL}/predictor/predict/{model_name}", json={"input_data": input_data})
            if response.status_code == 200:
                st.success("Prediction task created successfully.")
                st.json(response.json())
            else:
                st.error("Failed to create prediction task.")
                st.text(response.text)
        except json.JSONDecodeError as e:
            st.error(f"Error parsing input data: {e}")


def get_prediction_result():
    st.subheader("Get Prediction Result")
    prediction_task_id = st.number_input("Prediction Task ID", min_value=1, step=1)
    if st.button("Get Prediction Result"):
        response = requests.get(f"{API_BASE_URL}/predictor/prediction/{prediction_task_id}")
        if response.status_code == 200:
            st.success("Prediction result retrieved successfully.")
            st.json(response.json())
        else:
            st.error("Failed to retrieve prediction result.")
            st.text(response.text)


def main():
    st.title("ML Service Web UI")

    action = st.radio("Choose an action:", ["Sign Up", "Sign In"])

    if action == "Sign Up":
        sign_up()
    elif action == "Sign In":
        user_info = sign_in()
        if user_info:
            get_user_balance()
            deduct_credits()
            get_billing_history()
            make_prediction()
            get_prediction_result()


if __name__ == "__main__":
    main()
