import os

# Configuration
input_file = r"C:\Solutions\figma user story trial\input_folder\gib_mobile\onboarding_figma_api_json.txt"   # Replace with your file path
output_folder = "split_files_15k_onboarding"
lines_per_file = 8500

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Split file
with open(input_file, "r", encoding="utf-8") as f:
    count = 0
    file_number = 1
    output_file = None

    for line in f:
        if count % lines_per_file == 0:
            if output_file:
                output_file.close()
            output_file_path = os.path.join(output_folder, f"part_{file_number}.txt")
            output_file = open(output_file_path, "w", encoding="utf-8")
            file_number += 1
        output_file.write(line)
        count += 1

    if output_file:
        output_file.close()

print(f"File split into {file_number - 1} files in folder '{output_folder}'")
