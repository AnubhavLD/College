import math

def clean_training_records(records):
    cleaned = []
    rejected_indices = []
    
    if not isinstance(records, list):
        return {"cleaned": [], "rejected_indices": []}
    
    for i, record in enumerate(records):
        # 1. Validate that the record is a dictionary with required keys
        if not isinstance(record, dict) or "learner_id" not in record or "score" not in record:
            rejected_indices.append(i)
            continue
            
        learner_id = record.get("learner_id")
        score = record.get("score")
        
        # 2. Validate learner_id: must be a string and non-empty after stripping whitespace
        if not isinstance(learner_id, str):
            rejected_indices.append(i)
            continue
            
        trimmed_id = learner_id.strip()
        if not trimmed_id:
            rejected_indices.append(i)
            continue
            
        # 3. Validate score: reject booleans (bool is a subclass of int), None, and complex numbers
        if isinstance(score, bool) or score is None or isinstance(score, complex):
            rejected_indices.append(i)
            continue
            
        valid_score = None
        if isinstance(score, (int, float)):
            f_val = float(score)
            if not math.isfinite(f_val):
                rejected_indices.append(i)
                continue
            valid_score = f_val
        elif isinstance(score, str):
            try:
                f_val = float(score)
                if not math.isfinite(f_val):
                    rejected_indices.append(i)
                    continue
                valid_score = f_val
            except (ValueError, TypeError):
                rejected_indices.append(i)
                continue
        else:
            rejected_indices.append(i)
            continue
            
        # 4. Check score range (0 through 100 inclusive)
        if not (0 <= valid_score <= 100):
            rejected_indices.append(i)
            continue
            
        # 5. Determine eligibility (True if score >= 60)
        eligible = valid_score >= 60
        
        cleaned.append({
            "learner_id": trimmed_id,
            "score": valid_score,
            "eligible": eligible
        })
        
    return {
        "cleaned": cleaned,
        "rejected_indices": rejected_indices
    }
records = [
    {"learner_id": " L01 ", "score": "82.5"},
    {"learner_id": "L02", "score": 60},
    {"learner_id": "L03", "score": None},
    {"learner_id": "   ", "score": 75},
    {"learner_id": "L04", "score": True},
    {"learner_id": "L05", "score": 48.0},
    {"learner_id": "L06", "score": 105},
]

print(clean_training_records(records))