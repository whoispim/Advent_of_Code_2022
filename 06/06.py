with open("input", "r") as f:
    datastream = f.readline().strip()

for i in range(len(datastream)-4):
    if len(set(datastream[i:i+4])) == 4:
        break

print(f"First start-of-packet-marker detected after parsing {i+4} characters.")
print(f"The marker: {datastream[i:i+4]}")

for i in range(len(datastream)-14):
    if len(set(datastream[i:i+14])) == 14:
        break

print(f"First start-of-message-marker detected after parsing {i+14} characters.")
print(f"The marker: {datastream[i:i+14]}")
