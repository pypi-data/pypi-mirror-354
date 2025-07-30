import os
import json
from tc_estimator import compute_complexity
from tqdm import tqdm

def read_jsonl_and_estimate(filepath):
    results = []
    with open(filepath, 'r', encoding='utf-8') as json_file:
        for line in tqdm(json_file):
            entry = json.loads(line)
            code = entry['src']
            print(code)
            predicted = compute_complexity(code)
            print("prediction done")
            results.append({
                'predicted': predicted,
                'actual': entry.get('complexity'),
                'problem' : entry.get('problem')
            })
    return results

filepath = "python_data.jsonl"
results = read_jsonl_and_estimate(filepath)
for r in results:
    print(f"Problem: {r['problem']}, Predicted: {r['predicted']}, Acutal : {r['actual']}")
