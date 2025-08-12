def determine_module2_difficulty(module1_correct, module1_total, threshold=0.5):
    """
    Decide if Module 2 is 'hard' or 'easy' based on Module 1 performance.
    """
    return 'hard' if (module1_correct / module1_total) >= threshold else 'easy'

def calculate_raw_and_scaled(student_data, scoring_map, threshold=0.5):
    """
    Calculate raw and scaled scores for Math & Reading/Writing.
    """
    subjects = {}
    for subject in ["Math", "Reading and Writing"]:
        subj_data = [q for q in student_data if q["subject"]["name"] == subject]
        module1 = [q for q in subj_data if q["section"].lower() == "static"]
        module2 = [q for q in subj_data if q["section"].lower() != "static"]

        module1_correct = sum(q["correct"] for q in module1)
        module1_total = len(module1)
        module2_difficulty = determine_module2_difficulty(module1_correct, module1_total, threshold)

        raw_score = sum(q["correct"] for q in subj_data)
        scaled = lookup_scaled_score(raw_score, module2_difficulty, scoring_map[subject])

        subjects[subject] = {
            "raw": raw_score,
            "scaled": scaled,
            "module1_correct": module1_correct,
            "module1_total": module1_total,
            "module2_difficulty": module2_difficulty
        }
    return subjects

def lookup_scaled_score(raw_score, difficulty, score_map):
    """
    Find scaled score from scoring map given raw score & difficulty.
    """
    for entry in score_map:
        if entry["raw"] == raw_score:
            return entry[difficulty]
    return 0
