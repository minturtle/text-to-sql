from pathlib import Path
from typing import List
import json
from .spider_loader import SpiderLoader
from datasets import load_dataset
from mecab import MeCab

class SpiderKoLoader(SpiderLoader):
    """Spider Korean 데이터셋을 위한 로더"""

    def __init__(self, save_path: str):
        super().__init__(save_path)
        self.hf_dataset_name = "huggingface-KREW/spider-ko"
        self.tokenizer = MeCab()  # Mecab 한국어 토크나이저 초기화

    def get_sqlite_json_files(self):
        """
        Spider Korean 데이터셋의 JSON 파일들을 반환합니다.
        기존 Spider 파일들에 dev를 dev_ko.json으로 수정합니다.
        """
        base_files = super().get_sqlite_json_files()
        base_files["dev"] = Path(self._get_dataset_detail_path_root(), "dev_ko.json")
        return base_files

    def download_dataset(self):
        """
        Spider 데이터셋을 다운로드하고, 한국어 데이터셋을 추가로 처리합니다.
        """
        # 1. super의 download_dataset 호출
        super().download_dataset()
        
        # 2. huggingface로부터 spider-ko 데이터셋 다운로드
        dataset = load_dataset(self.hf_dataset_name)
        
        # 3. 2의 데이터셋을 기반으로 dev_ko.json 생성
        content = []

        for item in dataset["validation"]:
            # 한국어 질문을 토큰화
            question_ko = item["question_ko"]
            question_toks_ko = self.tokenizer.morphs(question_ko)  # Mecab 형태소 단위로 토큰화
            
            content.append({
                "db_id": item["db_id"],
                "query": item["query"],
                "query_toks": item["query_toks"],
                "query_toks_no_value": item["query_toks_no_value"],
                "question": question_ko,
                "question_toks": question_toks_ko,
                "sql": item["sql"],
            })

        with open(Path(self._get_dataset_detail_path_root(), "dev_ko.json"), "w") as f:
            json.dump(content, f)

    def _is_dataset_already_downloaded(self) -> bool:
        """
        Spider Korean 데이터셋이 이미 다운로드되었는지 확인합니다.
        """
        return super()._is_dataset_already_downloaded() and Path(self._get_dataset_detail_path_root(), "dev_ko.json").exists()