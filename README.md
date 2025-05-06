ECS635U Final Year Project: Portfolio Optimization Web Tool

This project implements Portfolio Optimization using the PyPortfolioOpt (Black-Litterman) model and Monte-Carlo Simulations. It leverages financial price data retrieved from yfinance. The app is structured with a backend (Python) and frontend (React).

Prerequisites:
- Python version: 3.13.3 or newer
- npm version: 9.2.0 or newer

Important, Port Availability:
- Frontend server (React): Port 5173
- Backend server (Python): Port 5000

Installation Steps

1. Install Backend Dependencies

Ensure you're in root folder portfolio-opt/

```bash
portfolio-opt> 
```
```bash
pip install -e .
```

2. Start Backend Server

Change directory to portfolio/src/backend

```bash
cd src/backend 
```
Run backend server 

```bash
python server.py
```

3. Install Frontend Dependencies

Open a new terminal window and change directory to the frontend folder:
```bash
cd frontend
```
Install frontend dependencies using npm:
```bash
npm install
```
4. Start Frontend Development Server

Run the development server
```bash
npm run dev
```
