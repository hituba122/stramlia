import streamlit as st
import requests

def get_user_data(username, api_key):
    """ Fetch user data using TikTok API with provided username """
    url = f"https://api.tikapi.io/public/check?username={username}"
    headers = {'X-API-KEY': api_key}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data['userInfo']['user']['id']
        else:
            return f"Failed to fetch ID for {username}, status code: {response.status_code}"
    except requests.RequestException as e:
        return f"Request failed for {username}: {str(e)}"

def main():
    st.title("TikTok User ID Fetcher")

    # User inputs for usernames and API key
    raw_usernames = st.text_area("Enter TikTok usernames here (one per line):", height=300)
    api_key = st.text_input("Enter your API Key:", type="password")

    if st.button("Fetch User IDs"):
        if raw_usernames and api_key:
            usernames = raw_usernames.splitlines()
            user_ids = []
            errors = []

            # Process each username
            for username in usernames:
                user_id = get_user_data(username.strip(), api_key)
                if "Failed" in user_id or "Request failed" in user_id:
                    errors.append(user_id)
                else:
                    user_ids.append(user_id)
            
            # Output user IDs in a copiable code block
            if user_ids:
                st.subheader("Fetched User IDs:")
                st.code("\n".join(user_ids), language="text")
            
            st.success(f"Number of usernames processed: {len(usernames)}")
            st.success(f"Number of IDs fetched: {len(user_ids)}")
            
            # Output errors in a copiable code block
            if errors:
                st.error("Errors encountered:")
                st.code("\n".join(errors), language="text")
        else:
            st.warning("Please enter usernames and an API key.")

if __name__ == "__main__":
    main()
