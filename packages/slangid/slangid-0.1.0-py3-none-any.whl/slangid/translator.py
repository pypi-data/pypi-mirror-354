import json
from pathlib import Path
from typing import Union, List

class Translator:
    def __init__(self):
        self.master_db = self._load_data()

    def _load_data(self) -> dict:
        data_dir = Path(__file__).parent / "data"
        combined = {}
        
        for file in ["singkatan_ke_baku.json", "daerah_ke_baku.json", "slang_ke_baku.json"]:
            with open(data_dir / file) as f:
                combined.update(json.load(f))
        return combined

    def translate(self, text: str) -> str:
        return " ".join([self.master_db.get(word.lower(), word) for word in text.split()])

class BatchTranslator(Translator):
    def translate_batch(self, texts: List[str]) -> List[str]:
        return [self.translate(text) for text in texts]