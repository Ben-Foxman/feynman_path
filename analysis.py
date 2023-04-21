import numpy as np
from matplotlib import pyplot as plt 
import pandas as pd 

aggregate_data = pd.read_csv("output/results.txt").rename(columns=lambda x: x.replace(" ", ""))



combined_experiments = dict()
for experiment in aggregate_data.to_dict(orient="records"):
    label = (experiment["experiment"], experiment["error_type"], experiment["error_prob"])
    if label in combined_experiments:
       n1 = experiment["num_samples"]
       sd1 = experiment["std_dev_fidelity"] 
       mean1 = experiment["mean_fidelity"]
       n2 = combined_experiments[label]["num_samples"]
       sd2 = combined_experiments[label]["std_dev_fidelity"]
       mean2 = combined_experiments[label]["mean_fidelity"]
       
       meanc = (experiment["mean_fidelity"] * experiment["num_samples"] + combined_experiments[label]["mean_fidelity"] * combined_experiments[label]["num_samples"])\
        / (experiment["num_samples"] + combined_experiments[label]["num_samples"])
       q1 = (mean1 - meanc) ** 2
       q2 = (mean2 - meanc) ** 2
    
       combined_experiments[label]['std_dev_fidelity'] = np.sqrt(((n1 - 1) * (sd1 + q1) +(n2 - 1) * (sd2 + q2)) / (n1 + n2 - 1))
       combined_experiments[label]["mean_fidelity"] = meanc
       combined_experiments[label]["num_samples"] += experiment["num_samples"]
       combined_experiments[label]['time'] += experiment["time"]
    else: 
        combined_experiments[label] = dict()
        combined_experiments[label]["mean_fidelity"] = experiment["mean_fidelity"]
        combined_experiments[label]['std_dev_fidelity'] = experiment["std_dev_fidelity"]
        combined_experiments[label]["num_samples"] = experiment["num_samples"]
        combined_experiments[label]['time'] = experiment["time"]

combined_experiments = dict(sorted(combined_experiments.items(), key=lambda x: x[0]))

with open("curated_results.txt", "w") as f:
    f.write("experiment, error_type, error_prob, mean_fidelity, std_dev_fidelity, num_samples\n")
    for k, v in combined_experiments.items():
        combined_experiments[k]["time per shot"] = combined_experiments[k]["time"]/combined_experiments[k]["num_samples"]
        for s in k:
            f.write(str(s).replace(" ", "") + ", ")
        for u, t in v.items():
            if u not in ["time", "time per shot"]:
                f.write(str(round(t, 2)) + ", ")
        f.write("\n")
    