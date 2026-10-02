from functools import wraps
from typing import List, Dict, Any, Callable

def track_calls(history: List[Dict[str, Any]]) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Determine the next sequential call number across the shared history
            call_number = len(history) + 1
            func_name = func.__name__
            
            try:
                result = func(*args, **kwargs)
                # Record successful call
                history.append({
                    "call_number": call_number,
                    "function": func_name,
                    "status": "success",
                    "error_type": None
                })
                return result
            except Exception as e:
                # Record failed call and re-raise original exception
                history.append({
                    "call_number": call_number,
                    "function": func_name,
                    "status": "error",
                    "error_type": type(e).__name__
                })
                raise
                
        return wrapper
    return decorator

# --- Utility Functions Implementation & Decoration ---

# Global or shared audit history list
history: List[Dict[str, Any]] = []

@track_calls(history)
def average_score(scores: List[Any]) -> float:
    if not isinstance(scores, list) or not scores:
        raise ValueError("scores must be a non-empty list.")
        
    for item in scores:
        if isinstance(item, bool) or not isinstance(item, (int, float)):
            raise TypeError("Scores must be finite integers or floats excluding Booleans.")
            
    return float(sum(scores) / len(scores))

@track_calls(history)
def format_run_name(prefix: str, *, number: int) -> str:
    if not isinstance(prefix, str) or not prefix.strip():
        raise ValueError("prefix must be a non-empty string.")
    if not isinstance(number, int) or isinstance(number, bool) or number < 0:
        raise ValueError("number must be a non-negative integer excluding Booleans.")
        
    return f"{prefix}_{number:02d}"

# Reset history for sample run
history.clear()

# 1. Successful average_score call
print(average_score([60, 80]))

# 2. Successful format_run_name call
print(format_run_name("eval", number=3))

# 3. Failing average_score call (empty list)
try:
    average_score([])
except ValueError as e:
    print(f"Caught expected error: {e}")

# Display audit trail history
import pprint
pprint.pprint(history)
