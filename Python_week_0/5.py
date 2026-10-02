def update_annotation_queue(queue, incoming, completed, priority=None, batch_size=3):
    # Validate batch_size: must be a non-negative integer excluding Booleans
    if not isinstance(batch_size, int) or isinstance(batch_size, bool) or batch_size < 0:
        raise ValueError("batch_size must be a non-negative integer excluding Booleans.")
        
    # Safely copy inputs to ensure original lists remain completely unchanged
    q = list(queue) if isinstance(queue, list) else []
    inc = list(incoming) if isinstance(incoming, list) else []
    comp = set(completed) if isinstance(completed, list) else set()
    
    # Combine queue and incoming IDs, retaining only the first occurrence of each ID
    seen = set()
    combined = []
    for item in q + inc:
        if item not in seen:
            seen.add(item)
            combined.append(item)  # List method 1: append
            
    # Remove all IDs appearing in completed
    remaining = []
    for item in combined:
        if item not in comp:
            remaining.append(item)
            
    # If priority is present in the remaining queue, move it to the front
    if priority is not None and priority in remaining:
        remaining.remove(priority)  # List method 2: remove
        remaining.insert(0, priority)  # List method 3: insert
        
    # Slicing for the next batch
    next_batch = remaining[:batch_size]
    
    # Indexing for the final item when available (None if empty)
    last_item = remaining[-1] if remaining else None
    
    # Range for numbered positions starting at 1
    positions = [(i + 1, remaining[i]) for i in range(len(remaining))]
    
    return {
        "queue": remaining,
        "next_batch": next_batch,
        "last_item": last_item,
        "positions": positions
    }
queue = ["D3", "D1", "D3", "D2"]
incoming = ["D4", "D2", "D5"]
completed = ["D1", "D9"]

print(update_annotation_queue(queue, incoming, completed, priority="D5", batch_size=3))