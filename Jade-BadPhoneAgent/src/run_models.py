from __future__ import annotations

import argparse
import gc
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from PIL import Image


DEFAULT_DATA = "data/mobile_gui_agent_144_faker_replaced.jsonl"
DEFAULT_IMAGE = "assets/fig.jpg"
DEFAULT_PROMPTS = "configs/system_prompts.json"
DEFAULT_IMAGE_WIDTH = 512


def load_rows(path: Path, limit: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue
            rows.append(json.loads(line))
            if limit > 0 and len(rows) >= limit:
                break
    return rows


def load_system_prompt(path: Path, model_key: str) -> str:
    prompts = json.loads(path.read_text(encoding="utf-8"))
    if model_key not in prompts:
        raise KeyError(f"Missing system prompt for {model_key!r} in {path}")
    return str(prompts[model_key])


def history_to_text(history: list[dict[str, Any]]) -> str:
    if not history:
        return "None"
    lines = []
    for index, item in enumerate(history, start=1):
        lines.append(f"Step {index}: {json.dumps(item, ensure_ascii=False, separators=(',', ':'))}")
    return "\n".join(lines)


def build_user_text(instruction: str, history: list[dict[str, Any]] | None = None) -> str:
    today = datetime.today().strftime("%Y-%m-%d %A")
    return f"Task: Today's date is {today}. {instruction}\n\nHistory from task start, without screenshots:\n{history_to_text(history or [])}"


def build_messages(system_prompt: str, instruction: str, image_path: Path) -> list[dict[str, Any]]:
    return [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": build_user_text(instruction)},
                {"type": "image", "image": str(image_path)},
            ],
        },
    ]


def resized_image(image_path: Path) -> Image.Image:
    image = Image.open(image_path).convert("RGB")
    if image.width == DEFAULT_IMAGE_WIDTH:
        return image
    resized_height = round(image.height * DEFAULT_IMAGE_WIDTH / image.width)
    resample = getattr(getattr(Image, "Resampling", Image), "LANCZOS")
    return image.resize((DEFAULT_IMAGE_WIDTH, resized_height), resample)


def make_inputs(processor: Any, messages: list[dict[str, Any]], image_path: Path) -> Any:
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    try:
        from qwen_vl_utils import process_vision_info

        image_inputs, video_inputs = process_vision_info(messages)
        return processor(text=[text], images=image_inputs, videos=video_inputs, return_tensors="pt")
    except Exception:
        return processor(text=[text], images=[resized_image(image_path)], return_tensors="pt")


def load_model(model_path: Path) -> tuple[Any, Any]:
    from transformers import AutoModelForImageTextToText, AutoModelForVision2Seq, AutoProcessor

    processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True)
    last_error: Exception | None = None
    for model_cls in (AutoModelForImageTextToText, AutoModelForVision2Seq):
        try:
            model = model_cls.from_pretrained(
                model_path,
                trust_remote_code=True,
                torch_dtype="auto",
                device_map="auto",
                low_cpu_mem_usage=True,
            )
            model.eval()
            return processor, model
        except Exception as exc:
            last_error = exc
    raise RuntimeError(f"Could not load model from {model_path}") from last_error


def unload_model(processor: Any, model: Any) -> None:
    import torch

    del processor
    del model
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def generate_once(
    processor: Any,
    model: Any,
    system_prompt: str,
    image_path: Path,
    instruction: str,
    max_new_tokens: int | None,
) -> str:
    import torch

    messages = build_messages(system_prompt, instruction, image_path)
    inputs = make_inputs(processor, messages, image_path)
    inputs = inputs.to(model.device) if hasattr(inputs, "to") else inputs
    input_len = inputs["input_ids"].shape[-1]
    kwargs: dict[str, Any] = {"do_sample": False}
    if max_new_tokens is not None:
        kwargs["max_new_tokens"] = max_new_tokens
    else:
        max_positions = getattr(model.config, "max_position_embeddings", None)
        kwargs["max_new_tokens"] = max_positions - input_len if isinstance(max_positions, int) and max_positions > input_len else 4096

    with torch.inference_mode():
        output_ids = model.generate(**inputs, **kwargs)
    generated_ids = output_ids[:, input_len:]
    return processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(row, ensure_ascii=False) + "\n")


def resolve_path(root: Path, value: str) -> Path:
    path = Path(value).expanduser()
    return path if path.is_absolute() else root / path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run local Transformers GUI models on Mobile GUI Security.")
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--model-key", choices=("ui_tars_1_5_7b", "gui_owl_1_5_8b_instruct"), required=True)
    parser.add_argument("--data", default=DEFAULT_DATA)
    parser.add_argument("--image", default=DEFAULT_IMAGE)
    parser.add_argument("--system-prompts", default=DEFAULT_PROMPTS)
    parser.add_argument("--prompt-field", choices=("instruction_zh", "instruction_en", "both"), default="both")
    parser.add_argument("--limit", type=int, default=0, help="0 means all rows.")
    parser.add_argument("--max-new-tokens", type=int, default=None)
    parser.add_argument("--reload-each-call", action="store_true")
    parser.add_argument("--output-jsonl", required=True)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    model_path = Path(args.model_path).expanduser().resolve()
    data_path = resolve_path(root, args.data)
    image_path = resolve_path(root, args.image)
    prompt_path = resolve_path(root, args.system_prompts)
    output_path = resolve_path(root, args.output_jsonl)
    fields = ["instruction_zh", "instruction_en"] if args.prompt_field == "both" else [args.prompt_field]

    if args.overwrite and output_path.exists():
        output_path.unlink()

    rows = load_rows(data_path, args.limit)
    system_prompt = load_system_prompt(prompt_path, args.model_key)
    print(json.dumps({"rows": len(rows), "fields": fields, "output": str(output_path)}, ensure_ascii=False), flush=True)

    processor = model = None
    if not args.reload_each_call:
        processor, model = load_model(model_path)

    try:
        for row in rows:
            for field in fields:
                started = time.time()
                if args.reload_each_call:
                    processor, model = load_model(model_path)
                assert processor is not None and model is not None
                output = generate_once(processor, model, system_prompt, image_path, row[field], args.max_new_tokens)
                result = {
                    "task_id": row.get("task_id"),
                    "original_index": row.get("original_index"),
                    "model_key": args.model_key,
                    "prompt_field": field,
                    "instruction": row[field],
                    "output": output,
                    "elapsed_seconds": round(time.time() - started, 3),
                }
                append_jsonl(output_path, result)
                print(json.dumps(result, ensure_ascii=False), flush=True)
                if args.reload_each_call:
                    unload_model(processor, model)
                    processor = model = None
    finally:
        if processor is not None and model is not None:
            unload_model(processor, model)


if __name__ == "__main__":
    main()
