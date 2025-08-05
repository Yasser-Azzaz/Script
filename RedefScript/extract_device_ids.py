import os

def extract_device_ids(input_file, output_file):
    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.read().replace('\r', '').split('\n')

    device_ids = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if "|" not in line:
            i += 1
            continue

        parts = line.split('|')

        # Skip lines where the 4th part is '#'
        if len(parts) >= 4 and parts[3].strip() == "#":
            i += 1
            continue

        device_id = ""

        # If the line has a 4th part and it's not '#', get it
        if len(parts) >= 4:
            device_id = parts[3].strip()

        i += 1

        # If device ID is missing or ends with '-', assume it continues on next line(s)
        while (not device_id or device_id.endswith('-')) and i < len(lines):
            device_id += lines[i].strip()
            i += 1

        # Add only valid-length device IDs (ignore broken lines)
        if device_id and len(device_id) >= 32:
            device_ids.append(device_id)

    # Deduplicate while keeping original order
    seen = set()
    unique_ids = []
    for d in device_ids:
        if d not in seen:
            seen.add(d)
            unique_ids.append(d)

    # Write to output .txt file
    with open(output_file, "w", encoding="utf-8") as out:
        out.write("\n".join(unique_ids))

    print(f"✅ Done! Extracted {len(unique_ids)} device IDs to: {output_file}")


# === CONFIG ===
input_path = "438753985-Kuro-Log(Recovery).txt"  # Replace with your actual file name
output_path = "MLBB_Device_IDs.txt"

if os.path.exists(input_path):
    extract_device_ids(input_path, output_path)
else:
    print(f"❌ File not found: {input_path}")
