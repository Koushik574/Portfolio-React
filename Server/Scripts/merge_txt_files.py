import os

input_folder = "../Text-Files"
output_file = os.path.join(input_folder, "rag_corpus.txt")

with open(output_file, "w", encoding="utf-8") as outfile:
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt") and filename != "rag_corpus.txt":
            file_path = os.path.join(input_folder, filename)
            with open(file_path, "r", encoding="utf-8") as infile:
                outfile.write(infile.read() + "\n")

print("All text files merged into rag_corpus.txt ✅")
