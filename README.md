# PAN Card Tampering Detection App

This Streamlit app allows users to detect tampering in PAN card images by comparing an uploaded image with a stored original image in the database. It uses two methods for tampering detection: Structural Similarity Index (SSIM) and ORB (Oriented FAST and Rotated BRIEF) feature matching.

## Features

- **Store Original Image**: Save an original PAN card image in the database associated with a unique name.
- **Check for Tampering**: Upload a PAN card image to verify if it has been tampered with by comparing it to the stored original image.
- **Comparison Methods**:
  - **SSIM**: Uses structural similarity to assess tampering.
  - **ORB**: Uses keypoints and feature matching to check for tampering.

## Setup Instructions

### Prerequisites

Ensure you have Python installed. It's recommended to use a virtual environment.

### Step 1: Clone the Repository

Clone or download this project to your local machine.

```bash
git clone <repository-url>
cd <repository-directory>

