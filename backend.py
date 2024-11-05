import sqlite3
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

# Database functions
def create_database():
    try:
     conn = sqlite3.connect('pan_card_db.sqlite')
     c = conn.cursor()
     c.execute(''' 
        CREATE TABLE IF NOT EXISTS pan_cards (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            image BLOB NOT NULL 
        )
     ''')
     conn.commit()
     conn.close()
        print("Database created successfully.")
    except Exception as e:
        print(f"Error creating database: {e}")

   

def insert_image(name, image_blob):
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

# Image comparison functions
def compare_images(original_blob, uploaded_image, method='ssim'):
    original_image = cv2.imdecode(np.frombuffer(original_blob, np.uint8), cv2.IMREAD_COLOR)
    uploaded_image = np.array(uploaded_image.convert("RGB"))
    uploaded_image = cv2.cvtColor(uploaded_image, cv2.COLOR_RGB2BGR)

    if method == 'ssim':
        original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        uploaded_gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)
        score, _ = ssim(original_gray, uploaded_gray, full=True)
        return score > 0.95  # Adjust threshold as needed

    elif method == 'orb':
        original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        uploaded_gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(original_gray, None)
        kp2, des2 = orb.detectAndCompute(uploaded_gray, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        match_ratio = len(matches) / min(len(kp1), len(kp2))
        return match_ratio > 0.8  # Adjust threshold as needed

    else:
        raise ValueError("Unsupported method. Use 'ssim' or 'orb'.")

