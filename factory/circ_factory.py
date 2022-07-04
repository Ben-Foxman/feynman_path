import random, os
# generate files representing circuits to test
def generate_files(size, num_gates, p, outfile):
    with open(outfile, "w+") as f:
        f.write(f"{size}\n")
        f.writelines("#\n")

        for _ in range(num_gates):
            a = random.random()
            if a < p:
                gate = "h"
            elif p <= a < (1 + p)/2:
                gate = "cx"
            else:
                gate = "s"

            if gate != "cx":
                f.write(f"{gate} {random.randint(0, size - 1)}\n")
            else:
                l = list(range(size))
                random.shuffle(l)
                k = l[:2]
                f.write(f"{gate} {l[0]} {l[1]}\n")

for size in range(2, 25):
    for num_gates in range(5000, 10001, 10000):
        for p in [0, .05, .1, .15, .2, .25, .3]:
            generate_files(size, num_gates, p, os.path.dirname(__file__) + f"/../circuits/n={size}g={num_gates}p={p}")
