import sys
import time
import argparse
from faster_whisper import WhisperModel

parser = argparse.ArgumentParser(description="Transcribe audio/video to SRT")
parser.add_argument("input", help="Input audio/video file")
parser.add_argument("-o", "--output", help="Output SRT file (default: same as input with .srt)")
parser.add_argument("-m", "--model", default="large-v3-turbo", choices=["tiny", "base", "small", "medium", "large-v3", "large-v3-turbo"], help="Model size (default: large-v3-turbo)")
args = parser.parse_args()

input_file = args.input
output_file = args.output if args.output else input_file.rsplit(".", 1)[0] + ".srt"

print(f"[info] Input: {input_file}")
print(f"[info] Output: {output_file}")
print(f"[info] Model: {args.model}")
print(f"[info] Loading model...")

t0 = time.time()
model = WhisperModel(args.model, device="cpu", compute_type="int8")
print(f"[info] Model loaded in {time.time() - t0:.1f}s")

print(f"[info] Transcribing...")
t1 = time.time()
segments, info = model.transcribe(input_file)

print(f"[info] Language: {info.language} (prob: {info.language_probability:.2f})")
print(f"[info] Duration: {info.duration:.1f}s")
print()

count = 0
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
        count = i
        pct = min(100, segment.end / info.duration * 100)
        bar_len = 40
        filled = int(bar_len * pct / 100)
        bar = "#" * filled + "-" * (bar_len - filled)
        sys.stdout.write(f"\r[{bar}] {pct:5.1f}% | {i} segments | {segment.end:.1f}s/{info.duration:.1f}s")
        sys.stdout.flush()

elapsed = time.time() - t1
print()
print()
print(f"[info] Done: {count} segments written")
print(f"[info] Time: {elapsed:.1f}s ({info.duration / elapsed:.1f}x realtime)")
print(f"[info] Saved: {output_file}")
