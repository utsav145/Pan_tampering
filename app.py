import sqlite3
import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import io

def create_database():
    conn = sqlite3.connect('pan_card_db.sqlite')
    c = conn.cursor()
    # Create table for storing images
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS pan_cards (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            image BLOB NOT NULL 
        )
    ''')
    conn.commit()
    conn.close()

def insert_image(name, image_path):
    with open(image_path, 'rb') as file:
        image_blob = file.read()
    conn = sqlite3.connect('pan_card_db.sqlite')
    c = conn.cursor()
    c.execute('INSERT INTO pan_cards (name, image) VALUES (?, ?)', (name, image_blob))
    conn.commit()
    conn.close()

def retrieve_image(name):
    conn = sqlite3.connect('pan_card_db.sqlite')
    c = conn.cursor()
    c.execute('SELECT image FROM pan_cards WHERE name = ?', (name,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def compare_images(original_blob, uploaded_image_path, method='ssim'):
    """
    Compare images using specified method: 'ssim' or 'orb'.
    Returns True if no tampering is detected, False otherwise.
    """
    # Decode the original image from blob and read the uploaded image
    original_image = cv2.imdecode(np.frombuffer(original_blob, np.uint8), cv2.IMREAD_COLOR)
    uploaded_image = cv2.imread(uploaded_image_path)

    if method == 'ssim':
        # Convert images to grayscale for SSIM
        original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        uploaded_gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)

        # Calculate the Structural Similarity Index (SSIM)
        score, _ = ssim(original_gray, uploaded_gray, full=True)
        print(f"SSIM score: {score}")
        return score > 0.95  # Threshold for similarity; adjust as needed

    elif method == 'orb':
        # Convert images to grayscale for ORB
        original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        uploaded_gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)

        # Initialize ORB detector
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(original_gray, None)
        kp2, des2 = orb.detectAndCompute(uploaded_gray, None)

        # Use BFMatcher to find matches
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)

        # Calculate match ratio based on the minimum keypoints in both images
        match_ratio = len(matches) / min(len(kp1), len(kp2))
        print(f"ORB match ratio: {match_ratio}")
        return match_ratio > 0.8  # Threshold for ORB similarity

    else:
        raise ValueError("Unsupported method. Use 'ssim' or 'orb'.")

def main():
    create_database()

    # Example: Insert an original image (uncomment to use)
    # insert_image('John Doe', 'path_to_original_image.jpg')

    # Example: Upload a new image to check
    uploaded_image_path = 'path_to_uploaded_image.jpg'  # Replace with the path to the uploaded image
    name_to_check = 'John Doe'  # The name to look up in the database

    # Retrieve the original image from the database
    original_blob = retrieve_image(name_to_check)
    if original_blob is None:
        print("No original image found for this name.")
        return

    # Choose the method: 'ssim' or 'orb'
    method = 'ssim'  # Change to 'orb' if you want to use ORB for tampering detection
    is_tampered = not compare_images(original_blob, uploaded_image_path, method=method)

    if is_tampered:
        print("Tampering detected!")
    else:
        print("No tampering detected.")

if __name__ == "__main__":
    main()
