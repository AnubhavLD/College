import copy
from typing import Dict, Any, Optional

def build_experiment_config(
    base: Dict[str, Any], 
    *, 
    run_name: str, 
    parameter_updates: Optional[Dict[str, Any]] = None, 
    **metadata: Any
) -> Dict[str, Any]:
    # 1. Validate run_name: must be a non-empty string after trimming
    if not isinstance(run_name, str) or not run_name.strip():
        raise ValueError("run_name must be a non-empty string after trimming.")
        
    # 2. Validate parameter_updates: must be a dictionary or None
    if parameter_updates is not None and not isinstance(parameter_updates, dict):
        raise TypeError("parameter_updates must be a dictionary or None.")
        
    # 3. Create a deep independent copy of the base dictionary to prevent side effects
    config = copy.deepcopy(base)
    
    # Add trimmed run_name at the top level
    config["run_name"] = run_name.strip()
    
    # 4. Apply parameter_updates only to keys already present in base["parameters"]
    if parameter_updates:
        if "parameters" not in config or not isinstance(config["parameters"], dict):
            config["parameters"] = {}
            
        for key, value in parameter_updates.items():
            if key not in config["parameters"]:
                raise KeyError(f"Unknown parameter '{key}' not present in base configuration.")
            config["parameters"][key] = value
            
    # 5. Merge captured metadata into the copied metadata dictionary
    if "metadata" not in config or not isinstance(config["metadata"], dict):
        config["metadata"] = {}
        
    for k, v in metadata.items():
        config["metadata"][k] = v
        
    return config
base = {
    "model": "ticket_classifier",
    "parameters": {"threshold": 0.5, "max_tokens": 128},
    "metadata": {"owner": "platform", "stage": "baseline"},
}

result = build_experiment_config(
    base,
    run_name="trial_02",
    parameter_updates={"threshold": 0.7},
    owner="nlp_team",
    seed=42,
)

import pprint
pprint.pprint(result)