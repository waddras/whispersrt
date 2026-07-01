import sys
import subprocess

if len(sys.argv) < 2:
    print("Usage: python3 translate_srt.py input.srt [--lines N] [--lang LANG]")
    sys.exit(1)

input_srt = sys.argv[1]
max_lines = 30
target_lang = "Arabic"

for i, arg in enumerate(sys.argv):
    if arg == "--lines" and i + 1 < len(sys.argv):
        max_lines = int(sys.argv[i + 1])
    if arg == "--lang" and i + 1 < len(sys.argv):
        target_lang = sys.argv[i + 1]

output_srt = input_srt.rsplit(".", 1)[0] + ".ar.srt"

with open(input_srt, "r") as f:
    content = f.read()

blocks = content.strip().split("\n\n")
blocks = blocks[:max_lines]

result = []
for block in blocks:
    lines = block.split("\n")
    if len(lines) >= 3:
        idx = lines[0]
        timestamp = lines[1]
        text = " ".join(lines[2:])
        print(f"Translating {idx}/{len(blocks)}: {text[:50]}...")
        proc = subprocess.run(
            ["ollama", "run", "translategemma:4b-it-q4_K_M",
             f"Translate the following text from English to {target_lang}: {text}"],
            capture_output=True, text=True, timeout=60
        )
        translated = proc.stdout.strip()
        result.append(idx + "\n" + timestamp + "\n" + translated + "\n")

with open(output_srt, "w") as f:
    f.write("\n".join(result))

print(f"Done: {output_srt}")
