"""Deterministically copy prompt/solution pairs from the detailed dataset."""

import json
from pathlib import Path


def main():
    directory = Path(__file__).resolve().parent
    source = directory / "contextual_prior_500_details.json"
    destination = directory / "contextual_prior_500_simple.json"
    data = json.loads(source.read_text(encoding="utf-8"))
    examples = data["examples"]
    if not isinstance(examples, list) or len(examples) != 500:
        raise ValueError("Expected exactly 500 detailed examples.")

    pairs = []
    for index, example in enumerate(examples):
        if example["simple_index"] != index:
            raise ValueError(f"Example {index} has an inconsistent simple_index.")
        if not isinstance(example["prompt"], str) or not example["prompt"].strip():
            raise ValueError(f"Example {index} needs a nonempty prompt.")
        if example["solution"] is not None:
            raise ValueError(f"Example {index} has a solution; this dataset has no known probability targets.")
        pairs.append({"prompt": example["prompt"], "solution": example["solution"]})

    destination.write_text(
        json.dumps(pairs, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(f"Exported {len(pairs)} pairs to {destination.name}")


if __name__ == "__main__":
    main()
