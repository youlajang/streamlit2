import streamlit as st  # Web App
from PIL import Image  # Image Processing
from google.cloud import vision_v1
from openai import OpenAI
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
st.set_page_config(page_title="OCR web", layout="wide")

# title
st.title("Google Vision OCR and ChatGPT Comments")

# subtitle
st.markdown("## Extract `Text` from  `Images`")

st.markdown("")


def extract_text_from_image(image):
    # Instantiates a client
    client = vision_v1.ImageAnnotatorClient()

    # Perform OCR (Optical Character Recognition) on the image
    response = client.text_detection(image=image)

    # Process the response and extract the text
    text_annotations = response.text_annotations
    if text_annotations:
        return text_annotations[0].description
    else:
        return None  # Return None if no text found in the image


def main():
    # Allow the user to upload an image
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        # Read the image file
        content = uploaded_file.read()

        # Perform text extraction
        image = vision_v1.Image(content=content)
        extracted_text = extract_text_from_image(image)

        return extracted_text


def response(output_text):
    # Display the extracted text
    
    if output_text is not None:
        st.subheader("OCR Result:")
        st.write(output_text)
        messages = []

        # user_content=input("user : ")
        messages.append({"role": "system", "content": "당신은 초등학교 선생님입니다. 학생들의 일기에 공감하고 적당한 길이의 서로 다른 코멘트 3개를 작성해주세요."})
        messages.append({"role": "user", "content": f"{output_text}"})
        completion = client.chat.completions.create(model="gpt-3.5-turbo-1106", messages=messages)
        st.subheader("ChatGPT Comments:")
        st.write(completion.choices[0].message.content.strip())

    else:
        st.write("")

if __name__ == "__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"openocr-394310-95d8b763df38.json"
    client = OpenAI(api_key='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')
    output_text = main()
    response(output_text)
    