from copy import deepcopy
from score_calculator import calculate_raw_and_scaled

def analyze_impact(student_data, scoring_map, threshold=0.5):
    """
    Perform what-if analysis for each incorrect question.
    """
    current_scores = calculate_raw_and_scaled(student_data, scoring_map, threshold)

    results = []
    for i, q in enumerate(student_data):
        if q["correct"] == 1:
            continue  # skip already correct

        # Simulate changing this question to correct
        temp_data = deepcopy(student_data)
        temp_data[i]["correct"] = 1

        new_scores = calculate_raw_and_scaled(temp_data, scoring_map, threshold)

        for subject in current_scores:
            score_diff = new_scores[subject]["scaled"] - current_scores[subject]["scaled"]
            if score_diff > 0 and q["subject"]["name"] == subject:
                results.append({
                    "question_id": q.get("question_id", f"Q{i+1}"),
                    "subject": subject,
                    "topic": q["topic"]["name"],
                    "unit": q["unit"]["name"],
                    "difficulty": q.get("compleixty", "N/A"),
                    "score_improvement": score_diff,
                    "time_spent": q["time_spent"]
                })

    # Sort by score improvement, then lowest time spent
    results.sort(key=lambda x: (-x["score_improvement"], x["time_spent"]))
    return results, current_scores
