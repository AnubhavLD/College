def summarise_predictions(results):
    if not isinstance(results, list):
        return {
            "valid_count": 0,
            "correct_count": 0,
            "accuracy": None,
            "by_actual": {},
            "misclassified_ids": [],
            "rejected_indices": []
        }
        
    valid_count = 0
    correct_count = 0
    by_actual = {}
    misclassified_ids = []
    rejected_indices = []
    
    for i, record in enumerate(results):
        # 1. Validate that record is a dict and has all required keys
        if not isinstance(record, dict) or not all(k in record for k in ("id", "actual", "predicted")):
            rejected_indices.append(i)
            continue
            
        ticket_id = record.get("id")
        actual = record.get("actual")
        predicted = record.get("predicted")
        
        # 2. Validate that id, actual, and predicted are non-empty strings after trimming
        if not isinstance(ticket_id, str) or not ticket_id.strip():
            rejected_indices.append(i)
            continue
        if not isinstance(actual, str) or not actual.strip():
            rejected_indices.append(i)
            continue
        if not isinstance(predicted, str) or not predicted.strip():
            rejected_indices.append(i)
            continue
            
        # Normalize labels: trim whitespace and lowercase
        norm_actual = actual.strip().lower()
        norm_predicted = predicted.strip().lower()
        
        # Increment valid count
        valid_count += 1
        
        # Initialize category in by_actual if not present
        if norm_actual not in by_actual:
            by_actual[norm_actual] = {"total": 0, "correct": 0}
            
        by_actual[norm_actual]["total"] += 1
        
        # Check correctness
        if norm_actual == norm_predicted:
            correct_count += 1
            by_actual[norm_actual]["correct"] += 1
        else:
            misclassified_ids.append(ticket_id)
            
    # Compute accuracy rounded to 4 decimal places
    if valid_count == 0:
        accuracy = None
    else:
        accuracy = round(correct_count / valid_count, 4)
        
    return {
        "valid_count": valid_count,
        "correct_count": correct_count,
        "accuracy": accuracy,
        "by_actual": by_actual,
        "misclassified_ids": misclassified_ids,
        "rejected_indices": rejected_indices
    }
results = [
    {"id": "T1", "actual": "Billing", "predicted": " billing "},
    {"id": "T2", "actual": "Technical", "predicted": "billing"},
    {"id": "T3", "actual": "billing", "predicted": "billing"},
    {"id": "T4", "actual": "Account", "predicted": "ACCOUNT"},
    {"id": "T5", "actual": None, "predicted": "account"},
]

print(summarise_predictions(results))