from pathlib import Path
from typing import List
from .loader import Loader


class BirdMiniDevLoader(Loader):

  def __init__(self, save_path: str):
    super().__init__(save_path, "1UJyA6I6pTmmhYpwdn8iT9QKrcJqSQAcX", "Bird Mini Dev")

  def get_sqlite_database(self) -> Path:
    """
    Bird Mini Dev 데이터셋의 sqlite 데이터페이스 폴더를 반환합니다.
    """
    return Path(self._get_dataset_detail_path_root(), "dev_database")


  def get_sqlite_json_files(self) -> List[Path]:
    """
    Bird Mini Dev 데이터셋의 sqlite 데이터페이스 폴더에서 테이블 정보가 담긴 json 파일을 반환합니다.
    """
    return {
      "table" : Path(self._get_dataset_detail_path_root(), "dev_tables.json"),
      "gold_sql" : Path(self._get_dataset_detail_path_root(), "mini_dev_sqlite_gold.json"),
      "dev" : Path(self._get_dataset_detail_path_root(), "mini_dev_sqlite_dev.json"),
    }


  def _get_dataset_detail_path_root(self) -> Path:
    return Path(self.save_path, "data_minidev", "MINIDEV")