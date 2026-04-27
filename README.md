# sentinel
An AI agent that helps evaluate your match for a job profile

## Setup Instructions

1. **Create a virtual environment using `uv`**
   ```bash
   uv venv
   ```

2. **Activate the virtual environment**
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```

3. **Install dependencies**
   ```bash
   uv pip install -r requirements.txt
   ```

4. **Set the Google API Key**
   You need a Google Gemini API key to run the agent.
   ```bash
   export GOOGLE_API_KEY="your-api-key-here"
   ```

5. **Run the agent**
   To test the agent script directly:
   ```bash
   python agent.py
   ```

   To start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
   You can then access the interactive API docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

   To run the Streamlit UI:
   ```bash
   streamlit run ui.py
   ```
   This will open a browser window with the user interface.
