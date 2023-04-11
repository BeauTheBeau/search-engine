import os
import fuzzywuzzy
from fuzzywuzzy import fuzz
from indexer import index_files


def search_files(query, indexed_files):
    results = []
    for file in indexed_files:

        file_name = os.path.basename(file)

        if fuzzywuzzy.fuzz.ratio(query, file_name) > 70:
            results.append(file)
    return results


print("Indexing files...")
target_dir = os.path.dirname(os.path.abspath(__file__))
indexed_files, indexed_dirs = index_files(target_dir)

# Print results
print("> Done indexing files")
print(f"> {len(indexed_files)} files indexed and {len(indexed_dirs)} dirs indexed")

print()
print(f"Using FuzzyWuzzy {fuzzywuzzy.__version__}")

query = input("Enter a query: ")
results = search_files(query, indexed_files)

print("> Search complete")
print(f"> Found {len(results)} results")
print()

for result in results:
    print(f"> {result} ({os.path.getsize(result)} bytes)")
