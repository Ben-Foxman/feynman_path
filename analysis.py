import numpy as np
from matplotlib import pyplot as plt 
import pandas as pd 

aggregate_data = pd.read_csv("output/results.txt").rename(columns=lambda x: x.replace(" ", ""))



combined_experiments = dict()
for experiment in aggregate_data.to_dict(orient="records"):
    label = (experiment["experiment"], experiment["error_type"], experiment["error_prob"])
    if label in combined_experiments:
       old_mean = combined_experiments[label]['mean_fidelity']

      
       combined_experiments[label]["mean_fidelity"] = (experiment["mean_fidelity"] * experiment["num_samples"] + combined_experiments[label]["mean_fidelity"] * combined_experiments[label]["num_samples"])\
        / (experiment["num_samples"] + combined_experiments[label]["num_samples"])

       combined_experiments[label]['std_dev_fidelity'] = np.sqrt(experiment["num_samples"] * (experiment["std_dev_fidelity"] ** 2 + (experiment["mean_fidelity"] - old_mean) ** 2)\
        + combined_experiments[label]["num_samples"] * (combined_experiments[label]["std_dev_fidelity"] ** 2 + (combined_experiments[label]["mean_fidelity"] - old_mean) ** 2))\
            / (experiment["num_samples"]+ combined_experiments[label]["num_samples"])

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
    for x in aggregate_data.columns:
        f.write(x + ",")
    f.write("\n")
    for k, v in combined_experiments.items():
        combined_experiments[k]["time per shot"] = combined_experiments[k]["time"]/combined_experiments[k]["num_samples"]
        for s in k:
            f.write(str(s) + ",")
        for t in v.values():
            f.write(str(t) + ",")
        f.write("\n")
    