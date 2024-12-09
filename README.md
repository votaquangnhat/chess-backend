# Chess Backend

This is the backend of the chess application for Intro2AI course at SoICT. The application is in this website https://chess-fe-lac.vercel.app/

## Features
- Real-time communication with the frontend using **Socket.IO**.
- Implements these AI algorithms for chess:
  - Minimax
  - Alpha-Beta Pruning
  - Monte Carlo Tree Search (MCTS)
  - MCTS with Neural Network.
- Handles game state and resets.
- Configurable delay for AI moves for better observation.

---

## Requirements

- Python 3.8+
- Node.js and npm
- Pip
---

## Installation
In order to run the application on local machine, you can follow these instructions

1. Clone this repository:
```bash
   git clone https://github.com/<votaquangnhat>/chess-backend.git
```

2. Clone the repository for front-end:
```bash
   git clone https://github.com/<votaquangnhat>/chess-fe.git
```
3. Install all the requirements for back-end:
```bash
   cd chess-backend
   python -m venv venv
   venv\Scripts\activate # for Window
   source venv/bin/activate # for MacOS/Linux
   pip install -r requirements.txt
```

4. Set up front-end
```bash
   cd ../chess-fe
   npm install
```

5. Run back-end and front-end:
```bash
   cd ../chess-backend
   python app.py
   cd ../chess-fe
   npm run dev
```
The application is in http://localhost:5173/

