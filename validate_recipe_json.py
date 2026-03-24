#!/usr/bin/env python3
"""Strict JSON validator for Lemonade recipe files.

Usage:
  python validate_recipe_json.py <file1.json> [file2.json ...]
"""

from __future__ import annotations

import json
import pathlib
import sys
from typing import Any

ALLOWED_KEYS = {
    "checkpoint",
    "checkpoints",
    "model_name",
    "id",
    "image_defaults",
    "labels",
    "recipe",
    "recipe_options",
    "size",
}


def _is_string_map(value: Any) -> bool:
    return isinstance(value, dict) and all(isinstance(k, str) and isinstance(v, str) for k, v in value.items())


def validate_recipe(data: Any, path: pathlib.Path) -> list[str]:
    errors: list[str] = []

    if not isinstance(data, dict):
        return [f"{path}: top-level JSON value must be an object"]

    unknown = sorted(k for k in data.keys() if k not in ALLOWED_KEYS)
    if unknown:
        errors.append(f"{path}: unknown top-level keys: {', '.join(unknown)}")

    model_name = data.get("model_name")
    model_id = data.get("id")
    if not isinstance(model_name, str) and not isinstance(model_id, str):
        errors.append(f"{path}: requires 'model_name' (string) or 'id' (string)")

    if not isinstance(data.get("recipe"), str):
        errors.append(f"{path}: 'recipe' must be a string")

    has_checkpoint = isinstance(data.get("checkpoint"), str)
    has_checkpoints = _is_string_map(data.get("checkpoints"))
    if not (has_checkpoint or has_checkpoints):
        errors.append(f"{path}: requires 'checkpoint' (string) or 'checkpoints' (object<string,string>)")

    if "labels" in data and not (
        isinstance(data["labels"], list) and all(isinstance(x, str) for x in data["labels"])
    ):
        errors.append(f"{path}: 'labels' must be an array of strings")

    if "recipe_options" in data and not isinstance(data["recipe_options"], dict):
        errors.append(f"{path}: 'recipe_options' must be an object")

    if "image_defaults" in data and not isinstance(data["image_defaults"], dict):
        errors.append(f"{path}: 'image_defaults' must be an object")

    if "size" in data and not isinstance(data["size"], (str, int, float)):
        errors.append(f"{path}: 'size' must be a string or number")

    return errors


def load_json_strict(path: pathlib.Path) -> tuple[Any | None, str | None]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, f"{path}: failed to read file: {exc}"

    try:
        return json.loads(text), None
    except json.JSONDecodeError as exc:
        return None, (
            f"{path}: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        )


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: python test/validate_recipe_json.py <file1.json> [file2.json ...]", file=sys.stderr)
        return 2

    all_errors: list[str] = []
    for arg in argv[1:]:
        path = pathlib.Path(arg)
        data, parse_error = load_json_strict(path)
        if parse_error is not None:
            all_errors.append(parse_error)
            continue
        all_errors.extend(validate_recipe(data, path))

    if all_errors:
        print("Recipe validation failed:")
        for err in all_errors:
            print(f"  - {err}")
        return 1

    print("Recipe validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
