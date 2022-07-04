import os
## FIRST RUN THE RANDOM CIRCUITS ##

# for size in range(2, 12):
#     for num_gates in range(5000, 10001, 10000):
#         for p in [0, .05, .1, .15, .2, .25, .3]:
#             print(f"n={size}g={num_gates}p={p}")
#             os.system(f"./chp.out n={size}g={num_gates}p={p}")
#             os.system(f"./fp.out n={size}g={num_gates}p={p}")


## PRINT RESULTS ##
import csv, re

f = open("out.csv", "r")
file_read = csv.reader(f)

res = dict()
res["0"] = []
res["0.05"] = []
res["0.1"] = []
res["0.15"] = []
res["0.3"] = []
res["0.2"] = []
res["0.25"] = []

for p in file_read:
    if p[0] == 'fp':
        q = re.findall("[0-9\.]+", p[1])
        res[q[2]].append([int(q[0]), float(p[2])])

from matplotlib import pyplot as plt

for a in res:
    plt.plot([x[0] for x in res[a]], [x[1] for x in res[a]], label=res)

plt.savefig("fpplots.png")
