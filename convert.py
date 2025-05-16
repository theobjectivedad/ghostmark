print("{")
with open("invis.txt", "r") as f:
    for line in f.readlines():
        line = line.strip()
        if not line:
            continue

        parts = line.split(" ")
        code = parts[0].replace("U+", "\\u").lower()
        name = parts[1:]

        print(f"'{code}': '{' '.join(name)}',")

print("}")
