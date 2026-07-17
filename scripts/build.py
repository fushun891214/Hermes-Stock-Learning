#!/usr/bin/env python3
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LESSON_META = {
    1: {"minutes": "18 分鐘", "tag": "基礎觀念"},
    2: {"minutes": "16 分鐘", "tag": "開始準備"},
    3: {"minutes": "17 分鐘", "tag": "商品挑選"},
    4: {"minutes": "16 分鐘", "tag": "投入節奏"},
    5: {"minutes": "17 分鐘", "tag": "常見錯誤"},
    6: {"minutes": "16 分鐘", "tag": "持有節奏"},
    7: {"minutes": "16 分鐘", "tag": "賣出判斷"},
    8: {"minutes": "17 分鐘", "tag": "加碼判斷"},
    9: {"minutes": "16 分鐘", "tag": "投入節奏"},
    10: {"minutes": "16 分鐘", "tag": "投資紀錄"},
    11: {"minutes": "16 分鐘", "tag": "檢查節奏"},
    12: {"minutes": "16 分鐘", "tag": "資訊判讀"},
    13: {"minutes": "16 分鐘", "tag": "配息判讀"},
    14: {"minutes": "16 分鐘", "tag": "績效判讀"},
    15: {"minutes": "16 分鐘", "tag": "資訊判讀"},
    16: {"minutes": "16 分鐘", "tag": "商品比較"},
    17: {"minutes": "16 分鐘", "tag": "商品比較"},
    18: {"minutes": "17 分鐘", "tag": "分散觀念"},
    19: {"minutes": "16 分鐘", "tag": "資訊判讀"},
    20: {"minutes": "16 分鐘", "tag": "商品比較"},
    21: {"minutes": "16 分鐘", "tag": "買前確認"},
    22: {"minutes": "16 分鐘", "tag": "資金安排"},
    23: {"minutes": "16 分鐘", "tag": "下單準備"},
    24: {"minutes": "16 分鐘", "tag": "持有開始"},
    25: {"minutes": "16 分鐘", "tag": "後續投入"},
    26: {"minutes": "16 分鐘", "tag": "投入節奏"},
    27: {"minutes": "16 分鐘", "tag": "投入金額"},
    28: {"minutes": "16 分鐘", "tag": "節奏調整"},
}


def main() -> int:
    subprocess.run(["npm", "run", "build"], cwd=ROOT, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
