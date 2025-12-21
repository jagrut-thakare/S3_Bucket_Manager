# S3 Browser & Uploader

A Streamlit-based web application to browse, upload, and download files from S3-compatible storage services (like AWS S3 or Shakti Cloud).

## Features

-   **File Browser**: Navigate through folders and files in your S3 buckets.
-   **Multi-Region Support**: Switch between `us-east-1` and `ap-south-1`.
-   **Upload**: Upload files directly to the current folder.
-   **Download**: Download individual files with customizable link expiration (up to 100 years).
-   **Download All**: Download the entire bucket as a ZIP file.

## Prerequisites

-   Python 3.8+
-   Conda (optional but recommended)

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd S3_Bucket_Manager
    ```

2.  **Create and activate a virtual environment (optional):**

    ```bash
    # Using conda
    conda create -n s3-browser python=3.12
    conda activate s3-browser
    
    # Or using venv
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  Create a `.env` file in the root directory:

    ```bash
    cp .env.template .env
    ```

2.  Edit `.env` and add your S3 credentials:

    ```env
    ACCESS_KEY_ID=your_access_key
    SECRET_ACCESS_KEY=your_secret_key
    # Optional: If using a custom S3 provider (like Shakti Cloud)
    ENDPOINT_URL=https://your-s3-endpoint-url
    ```

## Running the App

Run the following command to start the Streamlit application:

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`.

## Usage

1.  **Select Region**: Choose your region from the sidebar.
2.  **Select Bucket**: Choose a bucket from the list.
3.  **Browse**: Click folders to navigate. Use "Back" or "Home" to move up.
4.  **Upload**: Expand the "Upload File" section to upload a file to the directory you are currently viewing.
5.  **Download**: Click the "⬇️ Download" link next to a file. You can adjust the "Link Validity" in the sidebar to create links that last for a specific duration (up to 100 years).
