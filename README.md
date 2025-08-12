# SAT What-If Analysis

This project analyzes SAT (Digital SAT - DSAT) diagnostic test results to determine **which specific questions would contribute the most to a student's score improvement** if answered correctly.  
It uses the SAT section-adaptive scoring model and a "what-if" simulation.

---

## **Features**
- Works in **File Mode** (default) without requiring any database.
- Optional **Mongo Mode**: store and read results/scoring from MongoDB.
- Handles multiple students and generates CSV reports for each.
- Ranks questions by potential score improvement, breaking ties by lowest time spent.

---

## **Project Structure**
```
sat_whatif/
├── data_loader.py          # Loads data from JSON files or MongoDB
├── score_calculator.py     # Calculates raw & scaled scores
├── what_if_analyzer.py     # Runs what-if simulation
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── scoring_DSAT_v2.json    # SAT scoring model
├── 67f2aae2c084263d16dbe462user_attempt_v2.json # Student 1 results
├── 66fece285a916f0bb5aea9c5user_attempt_v3.json # Student 2 results
└── results/                # Generated CSV reports
```

---

## **1. Setup**

### Prerequisites
- Python 3.9+
- `pip` package manager

---

## **2. Installation**
Clone this repo and install dependencies:
```bash
pip install -r requirements.txt
```

---

## **3. Running in File Mode (default, no MongoDB)**
Simply run:
```bash
python main.py
```

**Output:**
- Console: current scores + top impactful questions.
- CSV: saved in `results/` folder for each student.

---

## **4. Running in Mongo Mode (optional)**

### 4.1 Start MongoDB
You can install MongoDB locally or run via Docker:
```bash
docker run -d --name mongo-sat -p 27017:27017 mongo:latest
```

### 4.2 Import JSON files into MongoDB
Using `mongoimport`:
```bash
mongoimport --db sat_analysis --collection student_results --file 67f2aae2c084263d16dbe462user_attempt_v2.json --jsonArray
mongoimport --db sat_analysis --collection student_results --file 66fece285a916f0bb5aea9c5user_attempt_v3.json --jsonArray
mongoimport --db sat_analysis --collection sat_scoring --file scoring_DSAT_v2.json --jsonArray
```

OR use the included Python helper:
```bash
python import_to_mongo.py
```

### 4.3 Run in Mongo Mode
Set environment variables and run:
```bash
# macOS/Linux
export USE_MONGO=true
export MONGO_URI="mongodb://localhost:27017"
export MONGO_DB="sat_analysis"
python main.py

# Windows PowerShell
$env:USE_MONGO="true"
$env:MONGO_URI="mongodb://localhost:27017"
$env:MONGO_DB="sat_analysis"
python main.py
```

---

## **5. Output Format**
CSV files are saved to `results/` and include:
- **Current Scores** (raw, scaled, module difficulty)
- **Top Impactful Questions**:
  - Question ID
  - Subject
  - Topic
  - Unit
  - Difficulty
  - Score Improvement
  - Time Spent (ms)

---

## **6. Configuration**
- Module 2 difficulty threshold is set at **50%** correct in Module 1.  
  Change `threshold=0.5` in `main.py` or `what_if_analyzer.py` to adjust.

---

## **7. Example**
Example output in console:
```
=== Current Scores for student_v2 ===
Math: Raw=45, Scaled=780, Module2=hard
Reading and Writing: Raw=41, Scaled=750, Module2=hard

=== Top Impactful Questions ===
[Math] Geometry (medium): +10 points, Time=45000ms
[Math] Algebra (easy): +10 points, Time=20000ms
...
```

---

## **8. License**
MIT License – free to use, modify, and distribute.
