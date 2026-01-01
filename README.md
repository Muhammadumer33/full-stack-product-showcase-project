# Full Stack Product Showcase Project

A full-stack product showcase application built with FastAPI (backend) and Next.js (frontend).

## Video Demo



https://github.com/user-attachments/assets/1218f03a-368f-497d-bb68-0e352e2b18fb


## 🚀 Features

- Product listing and management
- Image upload functionality
- RESTful API
- Modern, responsive UI
- Database integration

## 📁 Project Structure

```
full stack project/
├── backend/          # FastAPI backend
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── requirements.txt
│   └── uploads/     # Uploaded images
└── frontend/         # Next.js frontend
    ├── app/
    ├── components/
    ├── services/
    └── public/
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend
- **Next.js** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **React** - UI library

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

## ⚙️ Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the backend server:
```bash
uvicorn main:app --reload
```

The backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Run the development server:
```bash
npm run dev
# or
yarn dev
```

The frontend will run on `http://localhost:3000`

## 🔧 Configuration

### Backend Configuration
- Update database connection settings in `database.py`
- Configure CORS settings in `main.py` if needed

### Frontend Configuration
- Update API endpoint in `services/api.ts`
- Modify environment variables as needed

## 📝 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🚀 Deployment

### Backend Deployment
- Deploy to services like Heroku, Railway, or AWS
- Ensure environment variables are properly set
- Use production-grade database (PostgreSQL recommended)

### Frontend Deployment
- Deploy to Vercel, Netlify, or similar platforms
- Update API endpoint to production backend URL

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

Muhammad Umer

## 🙏 Acknowledgments

- FastAPI documentation
- Next.js documentation
- Community contributors
