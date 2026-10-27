"""Export prompt/solution pairs without changing text, targets, or ordering."""

import json
import math
from pathlib import Path


def main():
    directory = Path(__file__).resolve().parent
    source = directory / "framing_consistency_1000_details.json"
    destination = directory / "framing_consistency_1000_simple.json"
    examples = json.loads(source.read_text(encoding="utf-8"))["examples"]
    if not isinstance(examples, list) or len(examples) != 1000:
        raise ValueError("Expected exactly 1,000 detailed examples.")

    pairs = []
    conceptual_count = 0
    for index, example in enumerate(examples):
        if example["simple_index"] != index:
            raise ValueError(f"Example {index} has an inconsistent simple_index.")
        if not isinstance(example["prompt"], str) or not example["prompt"].strip():
            raise ValueError(f"Example {index} needs a nonempty prompt.")
        solution = example["solution"]
        if example["case_type"] == "conceptual":
            if solution is not None:
                raise ValueError(f"Conceptual example {index} must have a null solution.")
            conceptual_count += 1
        elif example["case_type"] == "numeric_control":
            if type(solution) not in (int, float) or not math.isfinite(solution) or not 0 <= solution <= 1:
                raise ValueError(f"Numeric example {index} needs a finite probability solution.")
        else:
            raise ValueError(f"Example {index} has an unknown case_type.")
        pairs.append({"prompt": example["prompt"], "solution": solution})

    if conceptual_count != 800:
        raise ValueError("Expected 800 conceptual examples and 200 numeric controls.")
    destination.write_text(
        json.dumps(pairs, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(f"Exported {len(pairs)} pairs to {destination.name}")


if __name__ == "__main__":
    main()
