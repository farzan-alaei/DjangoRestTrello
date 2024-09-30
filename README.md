# DjangoRestTrello

Hey there! Welcome to **DjangoRestTrello**, a project I built with lots of excitement and curiosity as part of the *
*Daneshkar Bootcamp**. The backend? Totally in my comfort zone with Django! But the frontend? Well, let's just say I
took on a bit of a challenge with **Svelte** to push myself beyond the usual.

## 🚀 What’s Inside?

- **Backend**: Powered by Django REST Framework, where I had the most fun! It's all about delivering a strong and
  scalable API for managing boards, lists, tasks, and more.
- **Frontend**: My first real dive into **Svelte**! It was a huge learning experience, and even though frontend isn’t my
  forte, I wanted to push myself and see how far I could go.
- **JWT Authentication**: Secure user login with token-based authentication.
- **Task Management**: You can create, update, and delete tasks, manage different lists—just like Trello, but with my
  twist!
- **(Optional) Real-time Updates**: Using WebSockets for real-time task updates if you enable them.

## 🛠 Tech Stack

- **Django REST Framework**: Backend API
- **Svelte**: Frontend framework for building the UI
- **SQLite**: Lightweight database (or switch to PostgreSQL easily!)
- **JWT**: For secure authentication
- **Docker & Docker Compose**: To easily run the project with one command, making setup a breeze!

## 💡 Why I Built This

To be honest, this project was a personal quest. I love backend development and feel super confident in it. But I wanted
to step out of my comfort zone and dive into frontend development—something that I’m not as experienced with. So, I
chose Svelte because it’s fast, modern, and... a bit intimidating at first! But hey, I’m always up for a good challenge.

This project taught me so much about full-stack development, and I’m really proud of how far I came. Even though the
frontend might not be perfect, it represents my determination to learn and improve.

## 🚀 How to Get it Running

### Using Docker Compose

If you have Docker installed, you can run the entire project using **Docker Compose**:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/farzan-alaei/DjangoRestTrello.git
   ```

2. **Run the project**:
   ```bash
   docker-compose up --build
   ```

That’s it! Docker will handle both the backend and frontend setup for you.

### Manual Setup (if you prefer)

## Backend Setup:

1. **Navigate to the backend directory and set up a virtual environment**:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the migrations and start the server**:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## Frontend Setup:

1. **Navigate to the frontend directory and install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Run the development server**:

### 🔮 What’s Next?

- Improving the frontend design (there’s always room for that!)
- Switching to PostgreSQL for better scalability
- Writing more tests to make sure everything is solid
