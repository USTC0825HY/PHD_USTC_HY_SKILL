#!/usr/bin/env python3
"""Filter photos containing a reference person using OpenCV YuNet + SFace."""

from __future__ import annotations

import argparse
import csv
import os
import shutil
import sys
import urllib.request
from collections import Counter
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw


MODEL_URLS = {
    "face_detection_yunet_2023mar.onnx": "https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx",
    "face_recognition_sface_2021dec.onnx": "https://github.com/opencv/opencv_zoo/raw/main/models/face_recognition_sface/face_recognition_sface_2021dec.onnx",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Photo workspace root.")
    parser.add_argument("--reference", required=True, help="Reference image containing the target person.")
    parser.add_argument("--sources", nargs="*", help="Source directories relative to --root.")
    parser.add_argument("--output", default="person_matches", help="Output folder, relative to --root unless absolute.")
    parser.add_argument("--threshold", type=float, default=0.70, help="Similarity threshold copied as final matches.")
    parser.add_argument("--candidate-threshold", type=float, default=0.28, help="Lower score recorded as candidate only.")
    parser.add_argument("--models-dir", help="Model directory. Defaults to a local app cache outside the photo root.")
    parser.add_argument("--max-side", type=int, default=960, help="Maximum image side for scanning.")
    parser.add_argument("--ref-max-side", type=int, default=1600, help="Maximum reference image side.")
    parser.add_argument("--overwrite", action="store_true", help="Clear output directory before copying.")
    parser.add_argument("--limit", type=int, help="Process only the first N images.")
    return parser.parse_args()


def resolve_under_root(root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def default_models_dir() -> Path:
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / "photo-person-filter" / "models"
    return Path.home() / ".cache" / "photo-person-filter" / "models"


def ensure_models(models_dir: Path) -> tuple[Path, Path]:
    models_dir.mkdir(parents=True, exist_ok=True)
    for filename, url in MODEL_URLS.items():
        target = models_dir / filename
        if not target.exists():
            print(f"Downloading {filename}", file=sys.stderr)
            urllib.request.urlretrieve(url, target)
    return (
        models_dir / "face_detection_yunet_2023mar.onnx",
        models_dir / "face_recognition_sface_2021dec.onnx",
    )


def iter_jpgs(root: Path, sources: list[str] | None, output_dir: Path, models_dir: Path) -> list[Path]:
    if sources:
        files: list[Path] = []
        for source in sources:
            files.extend(sorted((root / source).rglob("*.[jJ][pP][gG]")))
        return files

    excluded = {output_dir.resolve(), models_dir.resolve()}
    generated_prefixes = ("person_matches", "target-person")
    files = []
    for path in sorted(root.rglob("*.[jJ][pP][gG]")):
        resolved_parent = path.parent.resolve()
        if any(resolved_parent == ex or ex in resolved_parent.parents for ex in excluded):
            continue
        if any(part.startswith(generated_prefixes) for part in path.relative_to(root).parts[:-1]):
            continue
        files.append(path)
    return files


def clear_output(output_dir: Path) -> None:
    if not output_dir.exists():
        return
    for path in sorted(output_dir.rglob("*"), reverse=True):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            path.rmdir()


def load_cv(path: Path, max_side: int) -> np.ndarray:
    data = np.fromfile(str(path), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("decode failed")
    height, width = image.shape[:2]
    scale = max_side / max(height, width)
    if scale < 1:
        image = cv2.resize(image, (int(width * scale), int(height * scale)), interpolation=cv2.INTER_AREA)
    return image


def detect_faces(detector: cv2.FaceDetectorYN, image: np.ndarray) -> np.ndarray | None:
    height, width = image.shape[:2]
    detector.setInputSize((width, height))
    _, faces = detector.detect(image)
    return faces


def best_match(
    recognizer: cv2.FaceRecognizerSF,
    detector: cv2.FaceDetectorYN,
    reference_feature: np.ndarray,
    image: np.ndarray,
) -> tuple[int, float | None, float | None, np.ndarray | None]:
    faces = detect_faces(detector, image)
    if faces is None or len(faces) == 0:
        return 0, None, None, None

    best_score = -1.0
    best_face_score = None
    best_face = None
    for face in faces:
        try:
            feature = recognizer.feature(recognizer.alignCrop(image, face))
            score = float(recognizer.match(reference_feature, feature, cv2.FaceRecognizerSF_FR_COSINE))
        except Exception:
            continue
        if score > best_score:
            best_score = score
            best_face_score = float(face[-1])
            best_face = face

    if best_score < 0:
        return len(faces), None, None, None
    return len(faces), best_score, best_face_score, best_face


def make_full_preview(items: list[tuple[Path, str, float]], preview_path: Path) -> None:
    tiles = []
    for path, rel, score in items:
        try:
            image = load_cv(path, 900)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil = Image.fromarray(image)
            pil.thumbnail((240, 180), Image.Resampling.LANCZOS)
            tile = Image.new("RGB", (240, 222), "white")
            tile.paste(pil, ((240 - pil.width) // 2, 0))
            draw = ImageDraw.Draw(tile)
            draw.text((6, 184), Path(rel).name[:28], fill=(0, 0, 0))
            draw.text((6, 203), f"{score:.3f}", fill=(170, 0, 0))
            tiles.append(tile)
        except Exception:
            continue
    save_sheet(tiles, preview_path, cols=5)


def make_face_preview(
    items: list[tuple[Path, str, float]],
    recognizer: cv2.FaceRecognizerSF,
    detector: cv2.FaceDetectorYN,
    reference_feature: np.ndarray,
    preview_path: Path,
) -> None:
    tiles = []
    for path, rel, _score in items:
        try:
            image = load_cv(path, 1200)
            _count, score, _face_score, face = best_match(recognizer, detector, reference_feature, image)
            if score is None or face is None:
                continue
            x, y, width, height = [int(round(v)) for v in face[:4]]
            pad = int(max(width, height) * 0.45)
            image_h, image_w = image.shape[:2]
            x0, y0 = max(0, x - pad), max(0, y - pad)
            x1, y1 = min(image_w, x + width + pad), min(image_h, y + height + pad)
            crop = cv2.cvtColor(image[y0:y1, x0:x1], cv2.COLOR_BGR2RGB)
            pil = Image.fromarray(crop)
            pil.thumbnail((160, 160), Image.Resampling.LANCZOS)
            tile = Image.new("RGB", (180, 210), "white")
            tile.paste(pil, ((180 - pil.width) // 2, 0))
            draw = ImageDraw.Draw(tile)
            draw.text((4, 164), Path(rel).name[:22], fill=(0, 0, 0))
            draw.text((4, 184), f"{score:.3f}", fill=(170, 0, 0))
            tiles.append(tile)
        except Exception:
            continue
    save_sheet(tiles, preview_path, cols=8)


def save_sheet(tiles: list[Image.Image], path: Path, cols: int) -> None:
    if not tiles:
        return
    width, height = tiles[0].size
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * width, rows * height), "white")
    for index, tile in enumerate(tiles):
        sheet.paste(tile, ((index % cols) * width, (index // cols) * height))
    sheet.save(path, quality=92)


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    reference = Path(args.reference).resolve()
    output_dir = resolve_under_root(root, args.output)
    models_dir = resolve_under_root(root, args.models_dir) if args.models_dir else default_models_dir()
    result_csv = root / f"{output_dir.name}_matching_results.csv"
    selected_csv = root / f"{output_dir.name}_selected.csv"
    issues_txt = root / f"{output_dir.name}_issues.txt"
    full_preview = root / f"{output_dir.name}_full_preview.jpg"
    face_preview = root / f"{output_dir.name}_face_preview.jpg"

    detection_model, recognition_model = ensure_models(models_dir)
    detector = cv2.FaceDetectorYN_create(str(detection_model), "", (320, 320), score_threshold=0.45, nms_threshold=0.3, top_k=5000)
    recognizer = cv2.FaceRecognizerSF_create(str(recognition_model), "")

    reference_image = load_cv(reference, args.ref_max_side)
    faces = detect_faces(detector, reference_image)
    if faces is None or len(faces) == 0:
        raise RuntimeError("reference face not detected")
    reference_face = max(faces, key=lambda face: face[2] * face[3])
    reference_feature = recognizer.feature(recognizer.alignCrop(reference_image, reference_face))

    if args.overwrite:
        clear_output(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    files = iter_jpgs(root, args.sources, output_dir, models_dir)
    if args.limit:
        files = files[: args.limit]

    issues: list[str] = []
    copied: list[tuple[Path, str, float]] = []
    rows: list[list[object]] = []

    with result_csv.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["file", "face_count", "best_similarity", "best_face_score", "result"])
        for index, path in enumerate(files, 1):
            rel = str(path.relative_to(root))
            try:
                image = load_cv(path, args.max_side)
                face_count, score, face_score, _face = best_match(recognizer, detector, reference_feature, image)
                if score is None:
                    result = "no_detectable_face" if face_count == 0 else "feature_failed"
                    row = [rel, face_count, "", "", result]
                elif score >= args.threshold:
                    result = "match"
                    dest = output_dir / rel
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(path, dest)
                    copied.append((path, rel, score))
                    row = [rel, face_count, round(score, 6), round(face_score or 0, 6), result]
                elif score >= args.candidate_threshold:
                    row = [rel, face_count, round(score, 6), round(face_score or 0, 6), "candidate_not_copied"]
                else:
                    row = [rel, face_count, round(score, 6), round(face_score or 0, 6), "no_match"]
            except Exception as exc:
                issues.append(f"{rel}\t{type(exc).__name__}: {exc}")
                row = [rel, "", "", "", f"failed:{type(exc).__name__}"]
            rows.append(row)
            writer.writerow(row)
            if index % 50 == 0:
                handle.flush()

    with selected_csv.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["file", "best_similarity"])
        for _path, rel, score in sorted(copied, key=lambda item: item[2], reverse=True):
            writer.writerow([rel, round(score, 6)])

    issues_txt.write_text("\r\n".join(issues) if issues else "None", encoding="utf-8-sig")
    copied_sorted = sorted(copied, key=lambda item: item[2], reverse=True)
    make_full_preview(copied_sorted, full_preview)
    make_face_preview(copied_sorted, recognizer, detector, reference_feature, face_preview)

    counts = Counter(row[-1] for row in rows)
    print(f"source_files={len(files)}")
    print(f"copied={len(copied)}")
    print(f"issues={len(issues)}")
    for label, count in counts.most_common():
        print(f"{label}={count}")
    print(f"output={output_dir}")
    print(f"results_csv={result_csv}")
    print(f"selected_csv={selected_csv}")
    print(f"full_preview={full_preview}")
    print(f"face_preview={face_preview}")
    print(f"issues_txt={issues_txt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
