def summarise_tool_calls(records):
    if not isinstance(records, list):
        return {
            "unique_calls": 0,
            "by_tool": {},
            "failed_call_ids": [],
            "tool_ranking": []
        }
        
    # 1. Retain only the last occurrence of each call_id (overwriting entire earlier record)
    latest_records_map = {}
    for record in records:
        if isinstance(record, dict) and "call_id" in record:
            call_id = record["call_id"]
            # Store a shallow/deep copy to prevent mutating the original record
            latest_records_map[call_id] = dict(record)
            
    unique_calls = len(latest_records_map)
    
    # 2. Aggregate metrics per tool from the final unique records
    tool_stats = {}
    failed_call_ids = []
    
    for call_id, rec in latest_records_map.items():
        tool = rec.get("tool")
        status = rec.get("status")
        duration = rec.get("duration_ms", 0)
        
        if tool not in tool_stats:
            tool_stats[tool] = {
                "calls": 0,
                "successes": 0,
                "failures": 0,
                "total_duration_ms": 0
            }
            
        tool_stats[tool]["calls"] += 1
        tool_stats[tool]["total_duration_ms"] += duration
        
        if status == "ok":
            tool_stats[tool]["successes"] += 1
        elif status == "error":
            tool_stats[tool]["failures"] += 1
            failed_call_ids.append(call_id)
            
    # Sort failed call IDs lexicographically
    failed_call_ids.sort()
    
    # 3. Use a dictionary comprehension for constructing/formatting tool statistics if needed, 
    # or sorting tool names by ranking rules:
    # Rank by descending failure count, then descending total calls, then ascending tool name.
    sorted_tools = sorted(
        tool_stats.keys(),
        key=lambda t: (-tool_stats[t]["failures"], -tool_stats[t]["calls"], t)
    )
    
    # Example usage of dictionary comprehension as required by constraints:
    # Re-ordering/structuring the by_tool dictionary to match sorted rank order
    by_tool = {t: tool_stats[t] for t in sorted_tools}
    
    return {
        "unique_calls": unique_calls,
        "by_tool": by_tool,
        "failed_call_ids": failed_call_ids,
        "tool_ranking": sorted_tools
    }
records = [
    {"call_id": "C1", "tool": "search", "status": "error", "duration_ms": 120},
    {"call_id": "C2", "tool": "calculator", "status": "ok", "duration_ms": 10},
    {"call_id": "C1", "tool": "search", "status": "ok", "duration_ms": 80},
    {"call_id": "C3", "tool": "search", "status": "error", "duration_ms": 40},
    {"call_id": "C4", "tool": "retriever", "status": "error", "duration_ms": 50},
]

print(summarise_tool_calls(records))
