---
name: photo-person-filter
description: Find and copy photos that contain a specific person using a reference image. Use when the user asks to screen, filter, extract, or collect photos of one person from a local photo directory, especially JPG sports/event folders, and wants results saved into a separate folder with reviewable CSV and preview artifacts.
---

# Photo Person Filter

## Overview

Use this skill to find photos containing the same person as a reference image. The bundled script uses OpenCV YuNet for face detection and SFace for face embeddings, copies high-confidence matches to an output folder, and writes review artifacts.

Prefer this workflow when the person has visible faces in the target photos. It will not reliably detect back-only shots, fully occluded faces, or tiny distant faces.

## Workflow

1. Identify the workspace root, the reference image path, and the source photo directories.
2. Run `scripts/filter_person_photos.py` with explicit source directories whenever possible. This avoids rescanning generated output folders.
3. Use the default strict threshold `0.70` for team/sports/event albums where many similar people appear. Lower only if the user prioritizes recall and accepts more manual review.
4. Inspect the face preview image before calling the result final. The face preview shows the face actually matched by the model, which is more reliable than full-image thumbnails for group photos.
5. Report the final output folder, count, CSV, preview images, and any processing/copy issues.

## Script

Run from the photo workspace:

```powershell
python "C:\Users\Administrator\.codex\skills\photo-person-filter\scripts\filter_person_photos.py" `
  --root "D:\photos\football" `
  --reference "C:\path\to\reference.jpg" `
  --sources "event-a" "event-b" `
  --output "target-person-strict" `
  --threshold 0.70 `
  --overwrite
```

Important options:

- `--root`: Photo workspace root.
- `--reference`: Reference image containing the target person.
- `--sources`: One or more source directories relative to `--root`. If omitted, the script scans `--root` recursively and excludes common generated folders.
- `--output`: Output directory relative to `--root`, unless an absolute path is provided.
- `--threshold`: Similarity threshold copied as final matches. Use `0.70` for stricter results, `0.60` for broader review.
- `--candidate-threshold`: Lower threshold recorded as candidates in the CSV but not copied.
- `--models-dir`: Optional model cache. By default the script uses a local app cache outside the photo root so OpenCV does not need to read ONNX files from non-ASCII photo paths.
- `--overwrite`: Clear the output directory before copying. Use a fresh output folder if Windows reports locked files.
- `--limit`: Process only the first N files for smoke tests.

## Outputs

For output name `<output>`, the script creates:

- `<output>/`: copied match photos, preserving source subdirectories.
- `<output>_matching_results.csv`: all scanned photos with face count, best similarity, and result label.
- `<output>_selected.csv`: copied matches only.
- `<output>_full_preview.jpg`: contact sheet of copied match photos.
- `<output>_face_preview.jpg`: contact sheet of matched face crops.
- `<output>_issues.txt`: decode/copy errors, or `None`.

## Threshold Guidance

Use face preview, not just score, to decide whether the threshold is too loose.

- `>= 0.80`: very strict; may miss valid side-angle or group photos.
- `0.70`: recommended default for sports/team albums.
- `0.60`: broader, useful for candidate review.
- `0.363`: OpenCV SFace general threshold; too permissive for many team albums and should not be used as final without manual review.

If a first pass is too broad, rerun into a new output folder with a higher threshold. If a first pass misses obvious photos, rerun with a lower threshold and inspect `<output>_face_preview.jpg`.
