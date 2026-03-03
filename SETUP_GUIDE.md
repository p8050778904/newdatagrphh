# Setup Instructions for VS Code

To run this project locally on your machine and open it in VS Code, follow these steps:

## 1. Prerequisites
Ensure you have the following installed:
- **VS Code**: [Download here](https://code.visualstudio.com/)
- **Python (3.9+)**: [Download here](https://www.python.org/)
- **Node.js (v18+)**: [Download here](https://nodejs.org/)
- **MongoDB**: Since you already have MongoDB Compass, ensure the service is running.

## 2. VS Code Extensions
Open VS Code and install these recommended extensions:
- **Python** (by Microsoft)
- **ESLint** (for React/JS)
- **Prettier** (for code formatting)
- **Thunder Client** (optional, for testing APIs similar to Postman)

## 3. Backend Setup
1. Open a terminal in VS Code (`Ctrl + ` `) or `Terminal > New Terminal`.
2. Navigate to the backend folder: `cd backend`.
3. Create a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
4. Install dependencies:
   ```powershell
   pip install fastapi uvicorn motor openai python-dotenv httpx
   ```
5. Run the backend:
   ```powershell
   python -m uvicorn app.main:app --reload --port 8000
   ```

## 4. Frontend Setup
1. Open a **second** terminal window in VS Code.
2. Navigate to the frontend folder: `cd frontend`.
3. Install dependencies:
   ```powershell
   npm install
   ```
4. Run the frontend:
   ```powershell
   npm run dev
   ```

## 5. Environment Variables
Ensure your `backend/.env` file has the following:
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=newmcp_database
OPENAI_API_KEY=your_key_here
```
