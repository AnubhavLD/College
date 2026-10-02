import math

def aggregate_scores(*batches, top_n=3):
    # 1. Validate top_n: must be a non-negative integer excluding Booleans
    if not isinstance(top_n, int) or isinstance(top_n, bool) or top_n < 0:
        raise ValueError("top_n must be a non-negative integer excluding Booleans.")
        
    valid_records = []
    rejected_positions = []
    
    for batch_idx, batch in enumerate(batches):
        # A positional batch that is neither a list nor a tuple raises TypeError
        if not isinstance(batch, (list, tuple)):
            raise TypeError(f"Batch at index {batch_idx} must be a list or tuple.")
            
        for item_idx, score in enumerate(batch):
            # Reject Booleans, None, complex numbers, non-numeric types, and numeric strings
            if isinstance(score, bool) or score is None or isinstance(score, complex):
                rejected_positions.append((batch_idx, item_idx))
                continue
                
            # Accept only int or float types (numeric strings are invalid and excluded)
            if not isinstance(score, (int, float)):
                rejected_positions.append((batch_idx, item_idx))
                continue
                
            # Check finiteness and range [0, 100]
            try:
                f_score = float(score)
            except (ValueError, TypeError):
                rejected_positions.append((batch_idx, item_idx))
                continue
                
            if not math.isfinite(f_score) or not (0 <= f_score <= 100):
                rejected_positions.append((batch_idx, item_idx))
                continue
                
            valid_records.append((f_score, batch_idx, item_idx))
            
    valid_count = len(valid_records)
    
    if valid_count == 0:
        mean = None
        top_scores = []
    else:
        # Use a generator expression in an aggregate calculation (sum)
        total_sum = sum(score for score, _, _ in valid_records)
        mean = round(total_sum / valid_count, 2)
        
        # Rank by descending score, then lower batch index, then lower item index
        # Since valid_records stores (score, batch_idx, item_idx), sorting descending on score 
        # requires negative score or reverse sorting carefully.
        # Let's sort: primary key = -score (descending), secondary = batch_idx (ascending), tertiary = item_idx (ascending)
        sorted_records = sorted(valid_records, key=lambda x: (-x[0], x[1], x[2]))
        
        # Take up to top_n entries and format as (batch_index, item_index, score)
        top_scores = [(b_idx, i_idx, sc) for sc, b_idx, i_idx in sorted_records[:top_n]]
        
    return {
        "valid_count": valid_count,
        "mean": mean,
        "top_scores": top_scores,
        "rejected_positions": rejected_positions
    }
batch_a = [80, 90, None]
batch_b = (90, 70, True)
batch_c = []

print(aggregate_scores(batch_a, batch_b, batch_c, top_n=3))