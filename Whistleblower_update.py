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
    return df, sheet


# Update the Status column based on application number
def update_status(sheet, application_number, new_status):
    records = sheet.get_all_records()
    df = pd.DataFrame(records)

    # Find the row number to update
    row_to_update = df.index[df['application-number'] == application_number].tolist()

    if row_to_update:
        row_number = row_to_update[0] + 2  # Adding 2 because gspread is 1-indexed and there is a header row
        sheet.update_cell(row_number, df.columns.get_loc('Status') + 1, new_status)
        return True
    else:
        return False


# Streamlit App
def main():
    st.title("Update Application Status")

    # Input fields for application number and new status
    application_number = st.text_input("Enter Application Number")
    new_status = st.text_input("Enter New Status")

    if st.button("Update Status"):
        if application_number and new_status:
            # Fetch data and Google Sheet object
            sheet_url = "https://docs.google.com/spreadsheets/d/1A7o0eN1vNq5lbWGHNcTlLqmIJlWGOs7y6IonMiKdAFg/edit?usp=sharing"
            df, sheet = fetch_sheet_data(sheet_url)

            # Update the status in the Google Sheet
            success = update_status(sheet, application_number, new_status)

            if success:
                st.success(f"Status updated successfully for application number {application_number}.")
            else:
                st.error(f"Application number {application_number} not found.")
        else:
            st.warning("Please enter both application number and new status.")


if __name__ == "__main__":
    main()
