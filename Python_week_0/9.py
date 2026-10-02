from functools import wraps
from typing import List, Callable, Any

def validate_text_batch(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Determine whether 'texts' was passed as a positional or keyword argument.
        # By convention/interface, 'texts' is either the first positional argument or passed as kwarg 'texts'.
        texts = None
        if len(args) > 0:
            texts = args[0]
        elif "texts" in kwargs:
            texts = kwargs["texts"]
        else:
            raise TypeError("Missing required argument 'texts'.")
            
        # Require texts to be a list and every item to be a string; otherwise raise TypeError.
        if not isinstance(texts, list):
            raise TypeError("texts must be a list.")
            
        for item in texts:
            if not isinstance(item, str):
                raise TypeError("All items in texts must be strings.")
            # Reject strings empty after whitespace removal with ValueError.
            if not item.strip():
                raise ValueError("Strings cannot be empty after whitespace removal.")
                
        # Validate complete batch before executing the wrapped function
        return func(*args, **kwargs)
        
    return wrapper

@validate_text_batch
def text_lengths(texts: List[str], *, strip: bool = True) -> List[int]:
    if strip:
        return [len(t.strip()) for t in texts]
    else:
        return [len(t) for t in texts]

texts = ["   agent ", "ML", "data"]

# First call (default strip=True)
print(text_lengths(texts))

# Second call (strip=False)
print(text_lengths(texts=texts, strip=False))
