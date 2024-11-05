import streamlit as st
from PIL import Image
import backend  # Import the backend module

# Initialize database
backend.create_database()

# Sidebar for storing original PAN card image
st.sidebar.header("Store an Original PAN Card Image")
name = st.sidebar.text_input("Enter name associated with PAN card")
original_image = st.sidebar.file_uploader("Upload original PAN card image", type=['jpg', 'jpeg', 'png'])

if st.sidebar.button("Store Original Image"):
    if name and original_image:
        image_blob = original_image.read()
        backend.insert_image(name, image_blob)
        st.sidebar.success(f"Stored original image for {name}")
    else:
        st.sidebar.warning("Please enter a name and upload an image.")

# Main section for checking tampering
st.header("Check for Tampering")
uploaded_name = st.text_input("Enter name associated with stored PAN card")
uploaded_image = st.file_uploader("Upload image to check for tampering", type=['jpg', 'jpeg', 'png'])
method = st.selectbox("Choose comparison method", ['ssim', 'orb'])

if st.button("Check for Tampering"):
    if uploaded_name and uploaded_image:
        original_blob = backend.retrieve_image(uploaded_name)
        if original_blob is None:
            st.error("No original image found for this name.")
        else:
            uploaded_img = Image.open(uploaded_image)
            is_tampered = not backend.compare_images(original_blob, uploaded_img, method=method)
            if is_tampered:
                st.error("Tampering detected!")
            else:
                st.success("No tampering detected.")
    else:
        st.warning("Please enter a name and upload an image.")
