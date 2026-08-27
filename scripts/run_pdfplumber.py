from pathlib import Path

from toolcommons.adapters import get_adapter
from toolcommons.engine import run


ROOT = Path(__file__).resolve().parents[1]
TASK_PATH = ROOT / "tasks" / "pdf-quarterly-sales.json"
TASK_ID = "community.pdf.digital-table.quarterly-sales.v1"


if __name__ == "__main__":
    path = run(ROOT, TASK_ID, get_adapter("pdfplumber"))
    print(path.relative_to(ROOT))
