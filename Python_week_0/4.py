def audit_dataset_ids(train_ids, validation_ids):
    # Handle cases where inputs are not lists gracefully
    if not isinstance(train_ids, list):
        train_ids = []
    if not isinstance(validation_ids, list):
        validation_ids = []
        
    def process_ids(id_list):
        valid_items = []
        unique_seen = set()
        duplicates = set()
        invalid_indices = []
        
        for i, item in enumerate(id_list):
            # Do not convert non-strings; reject if not a string
            if not isinstance(item, str):
                invalid_indices.append(i)
                continue
                
            trimmed = item.strip()
            if not trimmed:
                invalid_indices.append(i)
                continue
                
            valid_items.append(trimmed)
            if trimmed in unique_seen:
                duplicates.add(trimmed)
            else:
                unique_seen.add(trimmed)
                
        return valid_items, sorted(list(duplicates)), invalid_indices
        
    train_valid, train_dups, invalid_train = process_ids(train_ids)
    val_valid, val_dups, invalid_val = process_ids(validation_ids)
    
    train_set = set(train_valid)
    val_set = set(val_valid)
    
    # Compute set relations and sort lexicographically
    overlap = sorted(list(train_set.intersection(val_set)))
    train_only = sorted(list(train_set - val_set))
    validation_only = sorted(list(val_set - train_set))
    
    return {
        "train_duplicates": train_dups,
        "validation_duplicates": val_dups,
        "overlap": overlap,
        "train_only": train_only,
        "validation_only": validation_only,
        "invalid_train_indices": invalid_train,
        "invalid_validation_indices": invalid_val,
        "snapshots": {
            "train": frozenset(train_set),
            "validation": frozenset(val_set),
        }
    }
train_ids = ["R3", "R1", " R2 ", "R1", None]
validation_ids = ["R2", "R4", "R4", " "]

print(audit_dataset_ids(train_ids, validation_ids))