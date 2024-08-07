pip install easyocr
pip install streamlit


code = """
import streamlit as st
import easyocr
import cv2
import numpy as np
from datetime import datetime

# Dictionary of authorized plates with their current status
authorized_plates = {
    'ABC123': 'in',
    'XYZ789': 'out',
    'DEF456': 'in',
    'GHI012': 'in',
    'JKL345': 'out',
    'MNO678': 'in',
    'PQR901': 'out',
    'STU234': 'in',
    'VWX567': 'out',
    'YZA890': 'in',
}

def main():
    st.title("Vehicle Entry/Exit System")

    uploaded_file = st.file_uploader("Choose an image file...", type="jpg")

    if uploaded_file is not None:
        # Load the image
        img = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)

        # Initialize the EasyOCR reader
        reader = easyocr.Reader(['en'])

        # Read the text from the image
        results = reader.readtext(img)

        # Filter and format the results to find the number plate text
        number_plate_text = ""
        for (bbox, text, prob) in results:
            if prob > 0.5:
                number_plate_text += f"{text} "
        number_plate_text = number_plate_text.strip()

        st.image(img, caption='Uploaded Image', use_column_width=True)
        st.write(f"Detected Number Plate Text: {number_plate_text}")

        if number_plate_text in authorized_plates:
            st.write("The number plate is authorized.")
            action = st.selectbox("Select action:", ["None", "Entry", "Exit"])

            if action == "Entry":
                result = handle_entry(number_plate_text)
                st.write(result)
            elif action == "Exit":
                result = handle_exit(number_plate_text)
                st.write(result)
        else:
            st.write("The number plate is not authorized.")
            plate = st.text_input("Enter the new plate number:")
            if plate:
                status = st.selectbox("Select status:", ["None", "in", "out"])
                if status != "None":
                    authorized_plates[plate] = status
                    st.write(f"Plate {plate} with status '{status}' has been added.")

        st.write("Updated authorized plates:", authorized_plates)

def handle_entry(license_plate):
    current_time = datetime.now()
    if license_plate in authorized_plates:
        if authorized_plates[license_plate] == 'in':
            return "Entry Denied: Vehicle already inside."
        else:
            authorized_plates[license_plate] = 'in'
            return f"Entry Allowed: Vehicle entered at {current_time}."
    else:
        return "Entry Denied: Vehicle not authorized."

def handle_exit(license_plate):
    current_time = datetime.now()
    if license_plate in authorized_plates:
        if authorized_plates[license_plate] == 'in':
            authorized_plates[license_plate] = 'out'
            return f"Exit Recorded: Vehicle exited at {current_time}."
        else:
            return "No Entry Recorded: Vehicle not currently inside."
    else:
        return "Exit Denied: Vehicle not authorized."

if __name__ == "__main__":
    main()
"""

with open("app.py", "w") as file:
    file.write(code)

     



     


