import pandas as pd

data = {}
time = []
nodes = []
everything = []
t = None

file_name = input("File Name: ")
with open(file_name, "r") as file:
    everything = file.readlines()

names = False
time_marks = False
_line = []
for line in everything:
    if line.strip() == "#N":
        names = True
        continue

    if line.find("#C") != -1 and not time_marks:
        names = False
        time_marks = True
        nodes = "".join(nodes).strip().split(" ")

        data["t"] = []
        for node in nodes:
            data[node] = []

    if names:
        nodes.append(line.replace(r"'", "").replace("\n", ""))
    
    if time_marks:
        if line.find("#;") != -1:
            data["t"].append(t)
            for node, point in zip(nodes, _line):
                data[node].append(point)
            break
        if line.find("#C") != -1:
            if t != None:
                data["t"].append(t)
                for node, point in zip(nodes, _line):
                    data[node].append(point)

            _line = []
            t = float(line.split()[1])
        else:
            line = line.split()
            try:
                _line.extend(list(map(lambda x: float(x[0:x.find(":")]), line)))
            except:
                print(line)
                exit()

df = pd.DataFrame.from_dict(data)
df.to_csv("data.csv", index=False)
