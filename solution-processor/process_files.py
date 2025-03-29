import json
import os
import re
import sys
from zipfile import ZipFile


def process_data(repo_path):
    metadata = []
    with ZipFile(os.path.join(repo_path, "solutions.zip"), "w") as solution_zip:
        for dirpath, dirnames, filenames in os.walk(repo_path):
            for filename in filenames:
                if filename.endswith(".md") and "sol" not in filename:
                    filepath = os.path.join(dirpath, filename)
                    with open(filepath, encoding="utf-8") as file:
                        content = file.read()
                    if ":::solution" not in content:
                        continue
                    metadata.append({"dirpath": dirpath.replace(repo_path, ""), "filename": filename})
                    solution_filename = filepath.replace(".md", ".sol.md")
                    with open(solution_filename, "w", encoding="utf-8") as file:
                        file.write(content)
                    solution_zip.write(
                        solution_filename, f"{dirpath.replace(repo_path, "")}/{solution_filename.split("/")[-1]}"
                    )
                    result = re.sub(r":::solution.*?:::", "", content, flags=re.DOTALL)
                    # with open(filepath, "w", encoding="utf-8") as file:
                    #     file.write(result)
        json_str = json.dumps(metadata, indent=4, ensure_ascii=False)
        solution_zip.writestr("metadata.json", json_str)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("You must set a repo path as the parameter")
    else:
        process_data(sys.argv[1])
