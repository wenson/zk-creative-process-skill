#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path


INVALID_NAME_CHARS = set('\\/:*?"<>|')


def fail(message: str) -> None:
    raise SystemExit(message)


def run(cmd, log_path: Path | None = None, allow_failure: bool = False) -> bool:
    if log_path:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("w", encoding="utf-8") as log:
            result = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, text=True)
    else:
        result = subprocess.run(cmd, text=True)
    if result.returncode != 0:
        if allow_failure:
            return False
        detail = f" See log: {log_path}" if log_path else ""
        fail(f"Command failed: {' '.join(map(str, cmd))}.{detail}")
    return True


def output_json(data) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def resolve_executable(explicit: str | None, name: str) -> str:
    if explicit:
        path = Path(explicit).expanduser()
        if not path.exists():
            fail(f"{name} not found: {path}")
        return str(path)
    found = shutil.which(name)
    if not found:
        flag = "--ffmpeg-path" if name == "ffmpeg" else "--ffprobe-path"
        fail(
            f"Required executable not found on PATH: {name}. "
            f"Install FFmpeg first. macOS: brew install ffmpeg. Windows: winget install Gyan.FFmpeg. "
            f"If it is already installed, pass {flag}."
        )
    return found


def assert_safe_name(value: str, field_name: str = "name") -> None:
    if not value.strip():
        fail(f"{field_name} cannot be empty.")
    if any(char in INVALID_NAME_CHARS for char in value):
        fail(f"{field_name} contains invalid filename characters: {value}")


def parse_fps(rate: str | None):
    if not rate or "/" not in rate:
        return None
    left, right = rate.split("/", 1)
    try:
        den = float(right)
        return None if den == 0 else round(float(left) / den, 4)
    except ValueError:
        return None


def probe_video(ffprobe: str, video_path: Path):
    result = subprocess.run(
        [ffprobe, "-v", "error", "-print_format", "json", "-show_streams", "-show_format", str(video_path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        fail(f"ffprobe failed for {video_path}: {result.stderr.strip()}")
    probe = json.loads(result.stdout)
    video_stream = next((s for s in probe.get("streams", []) if s.get("codec_type") == "video"), None)
    if not video_stream:
        fail("No video stream found.")
    audio_stream = next((s for s in probe.get("streams", []) if s.get("codec_type") == "audio"), None)
    duration = video_stream.get("duration") or probe.get("format", {}).get("duration")
    if not duration or float(duration) <= 0:
        fail("Cannot determine video duration.")
    return probe, video_stream, audio_stream, float(duration)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def copy_product_brief(product_brief_path: str | None, output_path: Path, mixed: bool = False) -> None:
    if product_brief_path:
        source = Path(product_brief_path).expanduser().resolve()
        if not source.exists():
            fail(f"Product brief not found: {source}")
        shutil.copy2(source, output_path)
        return
    reference_word = "videos" if mixed else "video"
    mapping_word = "this shared reference direction" if mixed else "the reference hook"
    write_text(
        output_path,
        f"""# Product Brief

Fill this before asking AI to map the reference {reference_word} into your own product.

## Product Basics

- Product/game name: TODO
- Genre/category: TODO
- Target market and audience: TODO
- Platform and ad channel: TODO

## Core Gameplay

- Main loop: TODO
- First 30 seconds of real user experience: TODO
- Core interaction the ad can truthfully show: TODO
- Progression, upgrade, merge, battle, puzzle, building, collection, or other system: TODO

## Sellable Hooks

- Strongest fantasy or desire: TODO
- Visual assets already available: TODO
- Mechanics that can connect to {mapping_word}: TODO
- Emotional payoff after the hook: TODO

## Constraints

- Must show: TODO
- Must avoid: TODO
- Production constraints: TODO
- Compliance/platform constraints: TODO

## Mapping Goal

- Acquisition goal: TODO
- Creative angle to test: TODO
- Success metric: TODO

## Privacy Reminder

Do not include API keys, unreleased financial data, personal information, or private partner data in this file.
""",
    )


def make_contact_sheet(ffmpeg: str, selected_dir: Path, frame_count: int, output_path: Path, log_path: Path) -> None:
    rows = (frame_count + 3) // 4
    run(
        [
            ffmpeg,
            "-hide_banner",
            "-y",
            "-framerate",
            "1",
            "-i",
            str(selected_dir / "selected-%02d.jpg"),
            "-vf",
            f"tile=4x{rows}:padding=4:margin=2",
            "-frames:v",
            "1",
            str(output_path),
        ],
        log_path,
    )


def selected_frames(ffmpeg: str, video_path: Path, duration: float, frame_count: int, selected_dir: Path, work_dir: Path):
    selected_dir.mkdir(parents=True, exist_ok=True)
    frames = []
    start_time = 0.03
    end_time = max(start_time, duration - 0.35)
    for index in range(frame_count):
        ratio = 0 if frame_count == 1 else index / (frame_count - 1)
        timestamp = start_time + ((end_time - start_time) * ratio)
        frame_name = f"selected-{index + 1:02d}.jpg"
        run(
            [
                ffmpeg,
                "-hide_banner",
                "-y",
                "-ss",
                str(round(timestamp, 3)),
                "-i",
                str(video_path),
                "-frames:v",
                "1",
                "-q:v",
                "2",
                "-vf",
                "scale=360:-1",
                "-update",
                "1",
                str(selected_dir / frame_name),
            ],
            work_dir / f"ffmpeg-selected-{index + 1:02d}.log",
        )
        frames.append(
            {
                "index": index + 1,
                "timestamp_seconds": round(timestamp, 3),
                "work_file": frame_name,
                "contact_sheet_position": {"row": (index // 4) + 1, "column": (index % 4) + 1},
                "ai_instruction": f"Use contact sheet frame {index + 1} at approximately {round(timestamp, 2)}s.",
            }
        )
    return frames


def create_single(args) -> dict:
    assert_safe_name(args.name, "name")
    if args.copy and args.move:
        fail("Use either --copy or --move, not both. Copy is the default.")
    if args.storyboard_frames < 4 or args.storyboard_frames > 30:
        fail("storyboard-frames must be between 4 and 30.")

    ffmpeg = resolve_executable(args.ffmpeg_path, "ffmpeg")
    ffprobe = resolve_executable(args.ffprobe_path, "ffprobe")
    base_dir = Path(args.base_dir or "creative-materials").expanduser().resolve()
    base_dir.mkdir(parents=True, exist_ok=True)
    source_video = Path(args.video_path).expanduser().resolve()
    if not source_video.exists():
        fail(f"Video not found: {source_video}")

    extension = source_video.suffix or ".mp4"
    material_dir = base_dir / f"{datetime.now():%Y-%m-%d}-{args.slug}-{args.name}"
    if material_dir.exists():
        fail(f"Material folder already exists: {material_dir}")

    outputs_dir = material_dir / "outputs"
    system_dir = material_dir / "_system-review-系统复查资料"
    work_dir = material_dir / "keyframes-work"
    selected_dir = work_dir / "selected"
    outputs_dir.mkdir(parents=True)
    system_dir.mkdir(parents=True)

    dest_video = material_dir / f"original-{args.name}{extension}"
    if args.move:
        shutil.move(str(source_video), dest_video)
        video_action = "moved"
    else:
        shutil.copy2(source_video, dest_video)
        video_action = "copied"

    product_brief = material_dir / "product-brief-产品信息.md"
    copy_product_brief(args.product_brief_path, product_brief)

    probe, video_stream, audio_stream, duration = probe_video(ffprobe, dest_video)
    metadata_path = system_dir / "video_metadata.json"
    metadata_path.write_text(
        json.dumps(
            {
                "generated_at": datetime.now().isoformat(timespec="seconds"),
                "source_video_action": video_action,
                "material_folder": str(material_dir),
                "file": dest_video.name,
                "video": {
                    "codec": video_stream.get("codec_name"),
                    "width": video_stream.get("width"),
                    "height": video_stream.get("height"),
                    "r_frame_rate": video_stream.get("r_frame_rate"),
                    "fps": parse_fps(video_stream.get("r_frame_rate")),
                    "duration_seconds": round(duration, 3),
                    "nb_frames": video_stream.get("nb_frames"),
                },
                "audio": None
                if not audio_stream
                else {
                    "codec": audio_stream.get("codec_name"),
                    "duration_seconds": round(float(audio_stream["duration"]), 3)
                    if audio_stream.get("duration")
                    else None,
                },
                "format": {
                    "duration_seconds": round(float(probe.get("format", {}).get("duration", 0)), 3)
                    if probe.get("format", {}).get("duration")
                    else None,
                    "size_bytes": int(probe.get("format", {}).get("size", 0))
                    if probe.get("format", {}).get("size")
                    else None,
                    "bit_rate": probe.get("format", {}).get("bit_rate"),
                },
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    frames = selected_frames(ffmpeg, dest_video, duration, args.storyboard_frames, selected_dir, work_dir)
    final_sheet = material_dir / f"keyframes-reference-storyboard-contact-sheet-{args.name}.jpg"
    make_contact_sheet(ffmpeg, selected_dir, args.storyboard_frames, final_sheet, work_dir / "ffmpeg-final-sheet.log")

    frame_index = system_dir / "frame-index.json"
    frame_index.write_text(
        json.dumps(
            {
                "generated_at": datetime.now().isoformat(timespec="seconds"),
                "source_video": dest_video.name,
                "contact_sheet": final_sheet.name,
                "frame_count": args.storyboard_frames,
                "selection_method": "uniform timestamps across source duration",
                "frames": frames,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    brief = material_dir / "brief.md"
    reference_storyboard = outputs_dir / "reference-video-storyboard-原视频场景变化分镜.md"
    creative_directions = outputs_dir / "creative-script-directions-创意脚本方向.md"
    write_text(
        brief,
        f"""# {args.name} Reference Video Creative Task

## Source Video

- File: [{dest_video.name}]({dest_video.name})
- Video: {round(duration, 2)} seconds, {video_stream.get("width")}x{video_stream.get("height")}, {parse_fps(video_stream.get("r_frame_rate"))}fps.
- Metadata: [_system-review-系统复查资料/video_metadata.json](_system-review-系统复查资料/video_metadata.json)

## Generated Assets

- Keyframe contact sheet: [{final_sheet.name}]({final_sheet.name})
- Output folder: [outputs](outputs/)
- Product brief: [product-brief-产品信息.md](product-brief-产品信息.md)

## Product Context

Fill `product-brief-产品信息.md` before mapping the reference structure into your own product.

## AI Output Requirements

- Fill `outputs/reference-video-storyboard-原视频场景变化分镜.md`.
- Fill `outputs/creative-script-directions-创意脚本方向.md`.
- First produce a story-direction pool only.
- Do not create production storyboard or prompt folders until a direction is selected.
""",
    )
    write_text(
        reference_storyboard,
        f"""# Reference Video Storyboard

## Keyframe And Metadata

- Keyframe contact sheet: [{final_sheet.name}](../{final_sheet.name})
- Metadata: [video_metadata.json](../_system-review-系统复查资料/video_metadata.json)

## Scene Progression

| Order | Representative frame | Scene content | Information progress | Transferable structure |
| --- | --- | --- | --- | --- |
| 1 | TODO | TODO | TODO | TODO |

## Underlying Structure

TODO

## Transfer Notes

TODO

## Do Not Copy Directly

TODO
""",
    )
    write_text(
        creative_directions,
        """# Creative Script Directions

## Assumptions

TODO

## Direction Overview

| Direction | Core hook | User desire | What to test | Risk |
| --- | --- | --- | --- | --- |
| 1 | TODO | TODO | TODO | TODO |

## Direction 1

### Core Hypothesis

TODO
""",
    )

    ai_input_pack = system_dir / "ai-input-pack.md"
    manifest = system_dir / "run-manifest.json"
    write_text(
        ai_input_pack,
        f"""# AI Input Pack: {args.name}

## Files

- Brief: {brief}
- Reference storyboard: {reference_storyboard}
- Creative directions: {creative_directions}
- Product brief: {product_brief}
- Frame index: {frame_index}
- Metadata: {metadata_path}

## Rule

Use product-brief-产品信息.md for product mapping. If product information is missing, do not invent product facts; output the missing questions and keep product mapping marked as pending.
""",
    )
    manifest.write_text(
        json.dumps(
            {
                "generated_at": datetime.now().isoformat(timespec="seconds"),
                "mode": "single",
                "script": __file__,
                "material_folder": str(material_dir),
                "ai_input_pack": str(ai_input_pack),
                "brief": str(brief),
                "product_brief": str(product_brief),
                "outputs": [str(reference_storyboard), str(creative_directions)],
                "source_video_action": video_action,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    if not args.keep_work and work_dir.exists():
        shutil.rmtree(work_dir)

    return {
        "material_folder": str(material_dir),
        "ai_input_pack": str(ai_input_pack),
        "final_storyboard_sheet": str(final_sheet),
        "frame_index": str(frame_index),
        "brief": str(brief),
        "product_brief": str(product_brief),
        "reference_storyboard": str(reference_storyboard),
        "creative_directions": str(creative_directions),
        "manifest": str(manifest),
    }


def create_mix(args) -> dict:
    assert_safe_name(args.name, "name")
    if len(args.video_paths) < 2:
        fail("mix mode requires at least two videos.")
    if args.copy and args.move:
        fail("Use either --copy or --move, not both. Copy is the default.")
    if args.storyboard_frames < 4 or args.storyboard_frames > 30:
        fail("storyboard-frames must be between 4 and 30.")

    ffmpeg = resolve_executable(args.ffmpeg_path, "ffmpeg")
    ffprobe = resolve_executable(args.ffprobe_path, "ffprobe")
    base_dir = Path(args.base_dir or "creative-materials").expanduser().resolve()
    base_dir.mkdir(parents=True, exist_ok=True)
    material_dir = base_dir / f"{datetime.now():%Y-%m-%d}-{args.slug}-{args.name}"
    if material_dir.exists():
        fail(f"Material folder already exists: {material_dir}")

    outputs_dir = material_dir / "outputs"
    system_dir = material_dir / "_system-review-系统复查资料"
    work_dir = material_dir / "keyframes-work"
    outputs_dir.mkdir(parents=True)
    system_dir.mkdir(parents=True)
    work_dir.mkdir(parents=True)

    product_brief = material_dir / "product-brief-产品信息.md"
    copy_product_brief(args.product_brief_path, product_brief, mixed=True)

    metadata_items = []
    frame_items = []
    for index, raw_path in enumerate(args.video_paths, start=1):
        source = Path(raw_path).expanduser().resolve()
        if not source.exists():
            fail(f"Video not found: {source}")
        extension = source.suffix or ".mp4"
        dest_name = f"video-{index:02d}-{source.stem}{extension}"
        dest = material_dir / dest_name
        if args.move:
            shutil.move(str(source), dest)
        else:
            shutil.copy2(source, dest)

        _, video_stream, _, duration = probe_video(ffprobe, dest)
        metadata_items.append(
            {
                "index": index,
                "file": dest_name,
                "duration_seconds": round(duration, 3),
                "width": video_stream.get("width"),
                "height": video_stream.get("height"),
                "codec": video_stream.get("codec_name"),
            }
        )

        selected_dir = work_dir / f"selected-{index:02d}"
        frames = selected_frames(ffmpeg, dest, duration, args.storyboard_frames, selected_dir, work_dir)
        sheet = material_dir / f"keyframes-reference-storyboard-contact-sheet-{args.name}-video-{index:02d}.jpg"
        make_contact_sheet(ffmpeg, selected_dir, args.storyboard_frames, sheet, work_dir / f"ffmpeg-sheet-video-{index:02d}.log")
        frame_items.append(
            {
                "video_index": index,
                "video_file": dest_name,
                "contact_sheet": sheet.name,
                "frames": [{"index": item["index"], "timestamp_seconds": item["timestamp_seconds"]} for item in frames],
            }
        )

    metadata_path = system_dir / "video_metadata.json"
    frame_index = system_dir / "frame-index.json"
    manifest = system_dir / "run-manifest.json"
    ai_input_pack = system_dir / "ai-input-pack.md"
    brief = material_dir / "brief.md"
    shared_analysis = outputs_dir / "shared-analysis-同方向素材共性拆解.md"

    metadata_path.write_text(
        json.dumps(
            {"generated_at": datetime.now().isoformat(timespec="seconds"), "mode": "mix", "videos": metadata_items},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    frame_index.write_text(
        json.dumps(
            {
                "generated_at": datetime.now().isoformat(timespec="seconds"),
                "mode": "mix",
                "frame_count_per_video": args.storyboard_frames,
                "videos": frame_items,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    video_lines = "\n".join(
        f"- Video {item['index']}: {item['file']}, {item['duration_seconds']}s, {item['width']}x{item['height']}"
        for item in metadata_items
    )
    write_text(
        brief,
        f"""# {args.name} Mixed Reference Creative Task

## Source Videos

{video_lines}

## Generated Assets

- Per-video keyframe contact sheets are in the material root.
- System files are in `_system-review-系统复查资料/`.
- Shared analysis goes in `outputs/`.
- Product brief: [product-brief-产品信息.md](product-brief-产品信息.md)

## Shared Direction

TODO: describe the shared hook, theme, or creative direction.

## Product Mapping Context

Fill `product-brief-产品信息.md` before mapping this shared direction into your own product.
""",
    )
    write_text(
        shared_analysis,
        """# Shared Analysis

## Common Hook

TODO

## Differences Between Videos

TODO

## Transferable Structure

TODO

## Product Mapping

Use `../product-brief-产品信息.md`. If it still contains TODO or lacks product-specific information, list missing questions and mark product mapping as pending.

## Creative Direction Pool

TODO
""",
    )
    write_text(
        ai_input_pack,
        f"""# AI Input Pack: {args.name}

This is a same-direction multi-video batch.

## Files

- Brief: {brief}
- Shared analysis: {shared_analysis}
- Product brief: {product_brief}
- Frame index: {frame_index}
- Metadata: {metadata_path}

## Rule

Analyze these videos as one direction-level creative task. Do not split them into independent single-video folders.
Use product-brief-产品信息.md for product mapping. If product information is missing, do not invent product facts; output the missing questions and keep product mapping marked as pending.
""",
    )
    manifest.write_text(
        json.dumps(
            {
                "generated_at": datetime.now().isoformat(timespec="seconds"),
                "mode": "mix",
                "script": __file__,
                "material_folder": str(material_dir),
                "ai_input_pack": str(ai_input_pack),
                "brief": str(brief),
                "product_brief": str(product_brief),
                "outputs": [str(shared_analysis)],
                "video_count": len(metadata_items),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    if not args.keep_work and work_dir.exists():
        shutil.rmtree(work_dir)

    return {
        "material_folder": str(material_dir),
        "ai_input_pack": str(ai_input_pack),
        "brief": str(brief),
        "product_brief": str(product_brief),
        "shared_analysis": str(shared_analysis),
        "manifest": str(manifest),
        "temp_work_dir_kept": bool(args.keep_work),
    }


def check_material(args) -> dict:
    material = Path(args.material_dir).expanduser().resolve()
    if not material.exists():
        fail(f"MaterialDir not found: {material}")
    system_dir = material / "_system-review-系统复查资料"
    outputs_dir = material / "outputs"
    issues = []

    def issue(severity, code, message, path):
        issues.append({"severity": severity, "code": code, "message": message, "path": str(path)})

    for name in ["brief.md", "product-brief-产品信息.md"]:
        path = material / name
        if not path.is_file():
            issue("error", "missing_required_file", f"Missing required file: {name}", path)
    if not system_dir.is_dir():
        issue("error", "missing_system_dir", "Missing _system-review-系统复查资料 directory.", system_dir)
    for name in ["video_metadata.json", "run-manifest.json", "frame-index.json", "ai-input-pack.md"]:
        path = system_dir / name
        if not path.is_file():
            issue("error", "missing_system_file", f"Missing system file: {name}", path)
    if not list(material.glob("keyframes-reference-storyboard-contact-sheet-*.jpg")):
        issue("error", "missing_contact_sheet", "Missing keyframes contact sheet.", material)
    if not list(material.glob("original-*")) and not list(material.glob("video-*")):
        issue("error", "missing_reference_video", "Missing reference video. Expected original-* for single or video-* for mix.", material)
    single_outputs = [
        outputs_dir / "reference-video-storyboard-原视频场景变化分镜.md",
        outputs_dir / "creative-script-directions-创意脚本方向.md",
    ]
    has_single = all(path.is_file() for path in single_outputs)
    has_mix = bool(list(outputs_dir.glob("shared-analysis-*.md")))
    if not outputs_dir.is_dir():
        issue("error", "missing_outputs_dir", "Missing outputs directory.", outputs_dir)
    elif not has_single and not has_mix:
        issue("error", "missing_output_file", "Missing output files. Expected single outputs or shared-analysis-*.md for mix.", outputs_dir)
    for path in material.rglob("*.md"):
        if system_dir in path.parents:
            continue
        if "TODO" in path.read_text(encoding="utf-8"):
            issue("warning", "placeholder_text", "Markdown file still contains placeholder text.", path)
    errors = sum(1 for item in issues if item["severity"] == "error")
    warnings = sum(1 for item in issues if item["severity"] == "warning")
    return {
        "material_folder": str(material),
        "checked_at": datetime.now().isoformat(timespec="seconds"),
        "status": "failed" if errors or (args.strict and warnings) else "passed",
        "errors": errors,
        "warnings": warnings,
        "issues": issues,
    }


def command_check_environment(args) -> int:
    checks = []

    def add(name, passed, detail, fix=""):
        checks.append({"name": name, "passed": passed, "detail": detail, "fix": fix})

    add("Python version", sys.version_info >= (3, 10), f"Detected Python {sys.version.split()[0]}. Python 3.10+ is recommended.")
    ffmpeg = shutil.which("ffmpeg") if not args.ffmpeg_path else str(Path(args.ffmpeg_path).expanduser())
    ffprobe = shutil.which("ffprobe") if not args.ffprobe_path else str(Path(args.ffprobe_path).expanduser())
    add("ffmpeg available", bool(ffmpeg and Path(ffmpeg).exists()), f"Found: {ffmpeg}" if ffmpeg else "ffmpeg was not found.", "macOS: brew install ffmpeg.")
    add("ffprobe available", bool(ffprobe and Path(ffprobe).exists()), f"Found: {ffprobe}" if ffprobe else "ffprobe was not found.", "ffprobe ships with FFmpeg.")
    test_dir = Path(args.test_dir).expanduser().resolve() if args.test_dir else Path(tempfile.mkdtemp(prefix="zk-env-check-"))
    remove_test_dir = args.test_dir is None
    try:
        test_dir.mkdir(parents=True, exist_ok=True)
        test_file = test_dir / "utf8 path test-中文.txt"
        test_file.write_text("utf8-ok", encoding="utf-8")
        add("filesystem write/read", test_file.read_text(encoding="utf-8") == "utf8-ok", f"Created and read: {test_file}")
    except Exception as exc:
        add("filesystem write/read", False, str(exc), "Choose a writable base directory.")
    finally:
        if remove_test_dir and test_dir.exists():
            shutil.rmtree(test_dir, ignore_errors=True)

    print("# Environment Check\n")
    failed = [item for item in checks if not item["passed"]]
    for item in checks:
        status = "OK" if item["passed"] else "FAIL"
        print(f"[{status}] {item['name']}: {item['detail']}")
        if not item["passed"] and item["fix"]:
            print(f"  Fix: {item['fix']}")
    print()
    if failed:
        print(f"{len(failed)} check(s) failed.")
        return 1
    print("All required checks passed.")
    return 0


def command_install_skill(args) -> int:
    script_parent = Path(__file__).resolve().parent
    repo_or_skill_root = script_parent.parent
    source = repo_or_skill_root if (repo_or_skill_root / "SKILL.md").is_file() else repo_or_skill_root / "skills" / "zk-creative-process"
    if not source.is_dir():
        fail(f"Skill source not found: {source}")
    destination_root = Path(args.codex_skills_dir or Path.home() / ".codex" / "skills").expanduser().resolve()
    destination_root.mkdir(parents=True, exist_ok=True)
    destination = destination_root / "zk-creative-process"
    if destination.exists() and source.resolve() == destination.resolve():
        print(f"Skill is already installed at: {destination}")
        return 0
    if destination.exists():
        if args.backup:
            backup = destination.with_name(f"{destination.name}.backup-{datetime.now():%Y%m%d-%H%M%S}")
            shutil.move(str(destination), backup)
            print(f"Existing skill backed up to: {backup}")
        elif args.force:
            shutil.rmtree(destination)
        else:
            fail(f"Skill already exists: {destination}. Rerun with --backup or --force.")
    shutil.copytree(source, destination)
    for sh_file in (destination / "scripts").glob("*.sh"):
        sh_file.chmod(sh_file.stat().st_mode | 0o755)
    print(f"Installed zk-creative-process skill to: {destination}")
    print(f"Bundled scripts copied to: {destination / 'scripts'}")
    print("Restart Codex or start a new session if the skill does not appear immediately.")
    return 0


def command_process_single(args) -> int:
    result = create_single(args)
    check_args = argparse.Namespace(material_dir=result["material_folder"], strict=args.strict_check)
    check = check_material(check_args)
    result.update({"check_status": check["status"], "check_errors": check["errors"], "check_warnings": check["warnings"]})
    result["next_step"] = "AI reads _system-review-系统复查资料/ai-input-pack.md, product-brief-产品信息.md, and the keyframe contact sheet, then replaces the output skeleton documents. If product brief is incomplete, product mapping stays pending."
    output_json(result)
    return 1 if check["status"] == "failed" else 0


def command_process_mix(args) -> int:
    result = create_mix(args)
    output_json(result)
    return 0


def command_check_material(args) -> int:
    result = check_material(args)
    if args.json:
        output_json(result)
    else:
        print(f"Material check: {result['status']}")
        print(f"Errors: {result['errors']}")
        print(f"Warnings: {result['warnings']}")
        for item in result["issues"]:
            print(f"[{item['severity']}] {item['code']}: {item['message']} {item['path']}")
    return 1 if result["status"] == "failed" else 0


def command_test_install(args) -> int:
    tmp_root = Path(args.work_dir).expanduser().resolve() if args.work_dir else Path(tempfile.mkdtemp(prefix="zk-test-install-"))
    remove_tmp_root = not args.keep_output
    output_dir = tmp_root / "creative-materials"
    output_dir.mkdir(parents=True, exist_ok=True)
    ffmpeg = resolve_executable(args.ffmpeg_path, "ffmpeg")
    ffprobe = resolve_executable(args.ffprobe_path, "ffprobe")
    sample = next(Path(".").glob("shower.*"), None)
    if sample:
        video_path = sample.resolve()
        print(f"Using local sample video: {video_path}")
    else:
        video_path = tmp_root / "generated-test-video.mp4"
        run(
            [
                ffmpeg,
                "-hide_banner",
                "-y",
                "-f",
                "lavfi",
                "-i",
                "testsrc=size=720x1280:rate=30",
                "-t",
                "3",
                "-pix_fmt",
                "yuv420p",
                str(video_path),
            ],
            tmp_root / "ffmpeg-generate.log",
        )
        print(f"Generated synthetic test video: {video_path}")
    create_args = argparse.Namespace(
        video_path=str(video_path),
        slug="test-install",
        name="test-install-测试安装",
        base_dir=str(output_dir),
        ffmpeg_path=ffmpeg,
        ffprobe_path=ffprobe,
        product_brief_path=None,
        copy=True,
        move=False,
        keep_work=False,
        storyboard_frames=6,
        strict_check=False,
    )
    result = create_single(create_args)
    check = check_material(argparse.Namespace(material_dir=result["material_folder"], strict=False))
    if check["status"] == "failed":
        output_json(check)
        return 1
    print(f"Test install passed. Material folder: {result['material_folder']}")
    if remove_tmp_root:
        shutil.rmtree(tmp_root)
        print("Removed test output. Use --keep-output to inspect generated files.")
    else:
        print(f"Kept test output at: {tmp_root}")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(description="ZK creative process native helper")
    sub = parser.add_subparsers(dest="command", required=True)

    env = sub.add_parser("check-environment")
    env.add_argument("--ffmpeg-path")
    env.add_argument("--ffprobe-path")
    env.add_argument("--test-dir")
    env.set_defaults(func=command_check_environment)

    install = sub.add_parser("install-skill")
    install.add_argument("--codex-skills-dir")
    install.add_argument("--force", action="store_true")
    install.add_argument("--backup", action="store_true")
    install.set_defaults(func=command_install_skill)

    single = sub.add_parser("process-reference-video-phase1")
    single.add_argument("--video-path", required=True)
    single.add_argument("--slug", required=True)
    single.add_argument("--name", required=True)
    single.add_argument("--base-dir")
    single.add_argument("--ffmpeg-path")
    single.add_argument("--ffprobe-path")
    single.add_argument("--product-brief-path")
    single.add_argument("--copy", action="store_true")
    single.add_argument("--move", action="store_true")
    single.add_argument("--keep-work", action="store_true")
    single.add_argument("--storyboard-frames", type=int, default=12)
    single.add_argument("--strict-check", action="store_true")
    single.set_defaults(func=command_process_single)

    mix = sub.add_parser("process-reference-videos-mix")
    mix.add_argument("--video-paths", nargs="+", required=True)
    mix.add_argument("--slug", required=True)
    mix.add_argument("--name", required=True)
    mix.add_argument("--base-dir")
    mix.add_argument("--ffmpeg-path")
    mix.add_argument("--ffprobe-path")
    mix.add_argument("--product-brief-path")
    mix.add_argument("--copy", action="store_true")
    mix.add_argument("--move", action="store_true")
    mix.add_argument("--keep-work", action="store_true")
    mix.add_argument("--storyboard-frames", type=int, default=8)
    mix.set_defaults(func=command_process_mix)

    check = sub.add_parser("check-creative-material")
    check.add_argument("--material-dir", required=True)
    check.add_argument("--strict", action="store_true")
    check.add_argument("--json", action="store_true")
    check.set_defaults(func=command_check_material)

    test_install = sub.add_parser("test-install")
    test_install.add_argument("--ffmpeg-path")
    test_install.add_argument("--ffprobe-path")
    test_install.add_argument("--work-dir")
    test_install.add_argument("--keep-output", action="store_true")
    test_install.set_defaults(func=command_test_install)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
