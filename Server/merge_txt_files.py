# merge_txt_files.py

files_to_be_merged = [
    "./Text-Files/github_data.txt",
    "./Text-Files/linkedin_data.txt",
    "./Text-Files/coding_certifications.txt"
]

with open("./Text-Files/rag_corpus.txt", "w", encoding="utf-8") as outfile:
    for filename in files_to_be_merged:
        with open(filename, "r", encoding="utf-8") as infile:
            content = infile.read().strip()
            outfile.write(content + "\n\n---\n\n")

print("✅ All files merged into rag_corpus.txt")
