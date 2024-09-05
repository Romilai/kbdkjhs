import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up the Google Sheets API
def setup_gspread():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    # Provide the path to your downloaded JSON file here
    creds = ServiceAccountCredentials.from_json_keyfile_name(r'eng-gate-434608-i0-ad7f3afc379a.json', scope)
    client = gspread.authorize(creds)
    return client

# Fetch the Google Sheet data
def fetch_sheet_data(sheet_url):
    client = setup_gspread()
    sheet = client.open_by_url(sheet_url).sheet1
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df

# Streamlit App
def main():
    st.title("Whistleblower Application Status")

    # Input field for application number
    application_number = st.text_input("Enter Application Number")

    if application_number:
        # Fetch data from Google Sheets
        sheet_url = "https://docs.google.com/spreadsheets/d/1A7o0eN1vNq5lbWGHNcTlLqmIJlWGOs7y6IonMiKdAFg/edit?usp=sharing"
        df = fetch_sheet_data(sheet_url)

        # Filter data based on the application number
        filtered_data = df[df['application-number'] == application_number]

        if not filtered_data.empty:
            # Select only the 'name-3' and 'status' columns
            filtered_data = filtered_data[['name-3', 'Status']]  # Ensure 'Status' is the correct column name in your sheet

            st.write("Application Details:")
            st.dataframe(filtered_data)
        else:
            st.write("No records found for the entered application number.")

if __name__ == "__main__":
    main()
