import os
import csv
from pathlib import Path
from data_loader import load_all_students, load_scoring_map
from what_if_analyzer import analyze_impact

def save_results_to_csv(student_id, results, current_scores):
    """Save what-if analysis results to CSV file."""
    Path("results").mkdir(exist_ok=True)
    filename = Path("results") / f"results_{student_id}.csv"

    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Current score summary
        writer.writerow(["=== Current Scores ==="])
        writer.writerow(["Subject", "Raw", "Scaled", "Module2 Difficulty"])
        for subject, scores in current_scores.items():
            writer.writerow([subject, scores["raw"], scores["scaled"], scores["module2_difficulty"]])
        
        writer.writerow([])
        writer.writerow(["=== Top Impactful Questions ==="])
        writer.writerow(["Question ID", "Subject", "Topic", "Unit", "Difficulty", "Score Improvement", "Time Spent (ms)"])
        for r in results:
            writer.writerow([
                r["question_id"],
                r["subject"],
                r["topic"],
                r["unit"],
                r["difficulty"],
                r["score_improvement"],
                r["time_spent"]
            ])
    print(f"✅ Results saved to {filename}")

def run_analysis(student_id, student_data, scoring_map):
    results, current_scores = analyze_impact(student_data, scoring_map, threshold=0.5)

    print(f"\n=== Current Scores for {student_id} ===")
    for subject, scores in current_scores.items():
        print(f"{subject}: Raw={scores['raw']}, Scaled={scores['scaled']}, Module2={scores['module2_difficulty']}")

    print("\n=== Top Impactful Questions ===")
    for r in results[:10]:
        print(f"[{r['subject']}] {r['topic']} ({r['difficulty']}): +{r['score_improvement']} points, Time={r['time_spent']}ms")

    save_results_to_csv(student_id, results, current_scores)

if __name__ == "__main__":
    scoring_map = load_scoring_map(
        "scoring_DSAT_v2.json" if os.getenv("USE_MONGO", "false").lower() != "true" else "sat_scoring"
    )

    if os.getenv("USE_MONGO", "false").lower() == "true":
        students = load_all_students("student_results")  # Mongo collection name
    else:
        students = load_all_students([
            "67f2aae2c084263d16dbe462user_attempt_v2.json",
            "66fece285a916f0bb5aea9c5user_attempt_v3.json"
        ])  # JSON files

    for student_id, student_data in students:
        run_analysis(student_id, student_data, scoring_map)
