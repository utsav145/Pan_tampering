### Step 2: Create a Virtual Environment and Install Requirements

1. **Create a virtual environment**:
    ```bash
    python -m venv pan_env
    ```

2. **Activate the virtual environment**:
    - **On Windows**:
      ```bash
      pan_env\Scripts\activate
      ```
    - **On macOS/Linux**:
      ```bash
      source pan_env/bin/activate
      ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

### Step 3: Run the Streamlit Application

1. **Run the app**:
    ```bash
    streamlit run app.py
    ```

2. **Open the app in your browser** (usually at [http://localhost:8501](http://localhost:8501)).

## Project Structure

- `app.py`: The main Streamlit application that handles the user interface.
- `backend.py`: Contains database operations and image comparison functions.
- `requirements.txt`: Lists the dependencies required for the application.
- `README.md`: Documentation for the project.

## How to Use

1. **Store an Original Image**:
   - Enter a name to associate with the PAN card image.
   - Upload an image of the original PAN card and click "Store Original Image."
   - This stores the original image in the database for future comparison.

2. **Check for Tampering**:
   - Enter the same name associated with the original PAN card.
   - Upload an image of the PAN card to verify for tampering.
   - Choose a comparison method (SSIM or ORB) and click "Check for Tampering."
   - The app will display a message indicating whether tampering was detected.

## Requirements

- Python 3.7 or higher
- Streamlit
- OpenCV
- NumPy
- Scikit-Image
- Pillow

## Notes

- Adjust similarity thresholds in `backend.py` if needed for better tampering detection accuracy.

## License

This project is licensed under the MIT License.
