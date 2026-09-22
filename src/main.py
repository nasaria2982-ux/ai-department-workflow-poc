import argparse, json, logging
from pathlib import Path
from .workflow import process_request

def main():
    p = argparse.ArgumentParser()
    p.add_argument("input_json", type=Path)
    p.add_argument("--output", type=Path, default=Path("output/result.json"))
    p.add_argument("--log", type=Path, default=Path("output/run.log"))
    args = p.parse_args()

    args.log.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(args.log, encoding="utf-8"), logging.StreamHandler()],
        force=True,
    )

    with args.input_json.open("r", encoding="utf-8") as f:
        data = json.load(f)

    result = process_request(data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    logging.info("完了 department=%s risk=%s human_review=%s", result.department, result.risk_level, result.human_review_required)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
