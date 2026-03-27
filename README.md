# GitHub Cloud Connector

A robust backend REST API built with Python and FastAPI. This connector securely authenticates users via the OAuth 2.0 flow to interact with their GitHub repositories, manage issues, and create pull requests.

## Tech Stack

* **Backend:** Python 3.10+
* **Framework:** FastAPI
* **HTTP Client:** HTTPX (Async)
* **Validation:** Pydantic
* **Security:** OAuth 2.0 (Authorization Code Flow) & HTTPBearer

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd github-connector
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Register your OAuth Application:**
   * Go to **GitHub Settings** -> **Developer settings** -> **OAuth Apps** -> **New OAuth App**.
   * Set the **Authorization callback URL** exactly to: `http://127.0.0.1:8000/auth/callback`
   * Generate a **Client Secret**.

5. **Environment Variables:**
   Create a `.env` file in the root directory and add your OAuth credentials:
   ```env
   GITHUB_CLIENT_ID=your_client_id_here
   GITHUB_CLIENT_SECRET=your_client_secret_here
   ```

## How to Run the Project

Start the ASGI server using Uvicorn:
```bash
uvicorn app.main:app --reload
```
The API will be live at http://127.0.0.1:8000.

## 📡 API Endpoints

Explore and test all endpoints interactively via the Swagger UI at http://127.0.0.1:8000/docs.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/auth/login` | Redirects the user to GitHub to grant repository access. |
| **GET** | `/auth/callback` | Catches the OAuth callback and exchanges the code for an Access Token. |
| **GET** | `/github/repos/{username}` | Fetches a list of repositories for a given user. |
| **POST** | `/github/repos/{username}/{repo_name}/issues` | Creates a new issue in the specified repository. |
| **GET** | `/github/repos/{username}/{repo_name}/issues` | Lists all issues for the specified repository. |
| **POST** | `/github/repos/{username}/{repo_name}/pulls` | *(Bonus)* Creates a new pull request in the specified repository. |
