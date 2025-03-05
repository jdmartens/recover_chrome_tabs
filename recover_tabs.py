import os
import re

# Define the path to Chrome's session files
CHROME_SESSION_PATH_MAC = os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/Sessions/")  # macOS
ALT_SESSION_PATH = os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/Sessions_save") # backup

session_path = ALT_SESSION_PATH

# get all session files
session_files = [f for f in os.listdir(session_path) if f.startswith("Session") or f.startswith("Tabs")]

if not session_files:
    print("❌ No session files found.")
    exit(1)

# List all session files
session_files = [f for f in os.listdir(session_path) if f.startswith("Session") or f.startswith("Tabs")]

if not session_files:
    print("❌ No session files found.")
    exit(1)

# Regular expression to match valid URLs (avoiding corrupted data)
url_pattern = re.compile(rb'(https?://[a-zA-Z0-9./?=&_%+-]+)')

# Process each session file individually
for file in session_files:
    file_path = os.path.join(session_path, file)
    output_file = f"recovered_{file}.txt"

    print(f"🔍 Scanning {file_path} for URLs...")

    extracted_urls = set()

    try:
        with open(file_path, "rb") as f:
            content = f.read()

            # Extract URLs using regex
            urls = url_pattern.findall(content)
            extracted_urls.update(url.decode('utf-8', errors='ignore') for url in urls)

    except Exception as e:
        print(f"⚠️ Error reading {file}: {e}")
        continue

    # Save the extracted URLs to a separate file per session file
    if extracted_urls:
        with open(output_file, "w") as f:
            for url in sorted(extracted_urls):
                f.write(url + "\n")

        print(f"✅ Extracted {len(extracted_urls)} URLs from {file}. Saved to {output_file}")
    else:
        print(f"❌ No readable URLs found in {file}.")

print("🎉 Extraction complete!")

