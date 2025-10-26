import re
import time
import pandas as pd
from datasketch import HyperLogLog

def load_ip_addresses(filename):
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    ips = []
    with open(filename, 'r', encoding='utf-8', errors='ignor') as f:
        for line in f:
            match = ip_pattern.search(line)
            if match:
                ips.append(match.group(0))
    return ips

def exact_count(ips):
    start = time.time()
    unique_ips = set(ips) 
    duration = time.time() - start
    return len(unique_ips), duration

def hll_count(ips, p=12):
    hll = HyperLogLog(p)
    start = time.time()
    for ip in ips:
        hll.update(ip.encode('utf-8'))
    duration = time.time() - start
    return hll.count(), duration

def compare_methods(log_file):
    print(f"Loading data from file: {log_file}.")
    ips = load_ip_addresses(log_file)               
    print(f"Loaded {len(ips)} rows.") 

    exact_result, exact_time = exact_count(ips)
    hll_result, hll_time = hll_count(ips)

    df = pd.DataFrame({
        "Metod": ["Exact Count", "HyperLogLog"],
        "Unique elements": [exact_result, hll_result],
        "Execution time (sec)": [round(exact_time, 4), round(hll_time, 4)]
    })

    print("\nComparison results:\n")
    print(df.to_string(index=False))

if __name__ == "__main__":
    log_file = "lms-stage-access.log"
    compare_methods(log_file)