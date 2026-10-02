def prepare_messages(payloads, min_length=3):
    # Validate min_length: must be a positive integer, explicitly excluding booleans
    if not isinstance(min_length, int) or isinstance(min_length, bool) or min_length <= 0:
        raise ValueError("min_length must be a positive integer excluding Booleans.")
        
    if not isinstance(payloads, list):
        return {"token_lists": [], "vocabulary": [], "rejected_indices": []}
        
    token_lists = []
    rejected_indices = []
    punctuations = ".,!?;:"
    
    for i, payload in enumerate(payloads):
        text = None
        if isinstance(payload, str):
            text = payload
        elif isinstance(payload, (bytes, bytearray)):
            try:
                text = payload.decode('utf-8')
            except (UnicodeDecodeError, AttributeError):
                rejected_indices.append(i)
                continue
        else:
            rejected_indices.append(i)
            continue
            
        # Lowercase, split, strip end punctuations, and filter using a list comprehension
        raw_words = text.lower().split()
        tokens = [
            word.strip(punctuations) 
            for word in raw_words 
            if len(word.strip(punctuations)) >= min_length
        ]
        token_lists.append(tokens)
        
    # Construct vocabulary using a set comprehension
    vocabulary = sorted({token for t_list in token_lists for token in t_list})
    
    return {
        "token_lists": token_lists,
        "vocabulary": vocabulary,
        "rejected_indices": rejected_indices
    }
payloads = [
    "   AI, helps TEAMS! ",
    b"Build reliable agents.",
    bytearray(b"AI helps."),
    None,
    b"\xff",
]

print(prepare_messages(payloads, min_length=3))