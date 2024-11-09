import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

# Define the dropout prediction logic based on selected features
def predict_dropout(row):
    if row['absences'] > 20 or row['failures'] >= 3 or row['G3'] < 10:
        return 'yes'
    return 'no'

# Main function to handle Streamlit interface
def main():
    # Title for the app
    st.title('Student Dropout Prediction')

    # File upload
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    # If file is uploaded, process it
    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        data = pd.read_csv(uploaded_file)

        # Show the first few rows of the dataset
        st.write("Dataset Preview:")
        st.write(data.head())

        # Apply dropout prediction logic
        data['dropout'] = data.apply(predict_dropout, axis=1)

        # Display the updated dataset
        st.write("Updated Dataset with Dropout Predictions:")
        st.write(data)

        # Generate and display the dropout distribution plot
        st.write("Dropout Distribution:")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.countplot(x='dropout', data=data, ax=ax)
        st.pyplot(fig)

        # Optionally, save the updated dataset with dropout prediction
        if st.button('Download Updated Dataset'):
            data.to_csv('updated_student_data.csv', index=False)
            st.success("Dataset saved as 'updated_student_data.csv'.")

    # Single input prediction for dropout
    st.subheader("Predict Dropout for a Single Student")

    # Input fields for a single student's data
    absences = st.number_input("Absences", min_value=0, value=0)
    failures = st.number_input("Failures", min_value=0, value=0)
    G3 = st.number_input("Final Grade (G3)", min_value=0, value=0)

    # Button to predict dropout for the single student
    if st.button('Predict Dropout'):
        student_data = {
            'absences': absences,
            'failures': failures,
            'G3': G3
        }
        dropout_prediction = predict_dropout(student_data)
        st.write(f"Dropout Prediction: {dropout_prediction}")

# Run the Streamlit app
if __name__ == "__main__":
    main()
