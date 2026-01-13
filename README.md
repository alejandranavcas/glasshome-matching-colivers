# glasshome-matching-colivers

## What is it

Matchmaking app to find your best fit for your neighbours, flatmates in a community living set up.

**Discover Yourself. Connect with Others.**
Unlock deeper insights about your personality, values, and preferences, and find your perfect community match.

## How to use repository

1. **Go to the desired folder you want to save the repository**

2. **Clone the repository**:

   ```bash
   git clone https://github.com/alejandranavcas/glasshome-matching-colivers.git
   cd glasshome-matching-colivers
   ```

3. **Create and activate virtual environment**:

   ```bash
   # Replace python3.10 with the full path if needed
    python3.10 -m venv .venv
   ```

   ```bash
   # Windows
   .venv\Scripts\activate

   # macOS/Linux
   source .venv/bin/activate
   ```

4. **Install dependencies**:

   If you only want to run the working app:

   ```bash
   # Install only app dependencies
   pip install -r app/requirements.txt
   ```

   Or, if you want to use also the experiments folder then:

   ```bash
   # Install all repository dependencies
   pip install -r requirements.txt
   ```

## Run the streamlit app

1. **Activate the virtual environment** (if not already active):

   ```bash
   # Windows
   .venv\Scripts\activate

   # macOS/Linux
   source .venv/bin/activate
   ```

2. **Navigate to the app folder and run Streamlit**:
   ```bash
   cd app
   streamlit run app.py
   ```

The app will open automatically in your default browser at `http://localhost:8501`. If it doesn't, manually navigate to that URL.
