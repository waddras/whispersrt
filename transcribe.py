import sys
from faster_whisper import WhisperModel

if len(sys.argv) < 2:
    print("Usage: python3 transcribe.py input.mkv [output.srt]")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.rsplit(".", 1)[0] + ".srt"

model = WhisperModel("base", device="cpu", compute_type="int8")
segments, info = model.transcribe(input_file)

with open(output_file, "w") as f:
    for i, segment in enumerate(segments, 1):
        start_h = int(segment.start // 3600)
        start_m = int((segment.start % 3600) // 60)
        start_s = int(segment.start % 60)
        start_ms = int((segment.start % 1) * 1000)
        end_h = int(segment.end // 3600)
        end_m = int((segment.end % 3600) // 60)
        end_s = int(segment.end % 60)
        end_ms = int((segment.end % 1) * 1000)
        start_ts = f"{start_h:02d}:{start_m:02d}:{start_s:02d},{start_ms:03d}"
        end_ts = f"{end_h:02d}:{end_m:02d}:{end_s:02d},{end_ms:03d}"
        line = str(i) + "\n" + start_ts + " --> " + end_ts + "\n" + segment.text.strip() + "\n\n"
        f.write(line)

print(f"Done: {output_file}")
