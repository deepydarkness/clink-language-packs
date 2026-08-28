from cebdict import dictionary

entries = dictionary.get_entries()

with open("cebdict.txt", "w", encoding="utf-8") as f:
    for word in entries:
        f.write(word + "\n")

print(f"Exported {len(entries)} entries to cebdict.txt")
