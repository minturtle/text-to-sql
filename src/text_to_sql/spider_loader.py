from pathlib import Path
from typing import List
from .loader import Loader



class SpiderLoader(Loader):

  def __init__(self, save_path: str):
    super().__init__(save_path, "1403EGqzIDoHMdQF4c9Bkyl7dZLZ5Wt6J", "Spider")

  def get_sqlite_database(self) -> Path:
    return Path(self._get_dataset_detail_path_root(), "database")

  def get_sqlite_json_files(self) -> List[Path]:
    return {
      "table" : Path(self._get_dataset_detail_path_root(), "tables.json"),
      "gold_sql" : Path(self._get_dataset_detail_path_root(), "dev_gold.json"),
      "dev" : Path(self._get_dataset_detail_path_root(), "dev.json"),
    }

  def _get_dataset_detail_path_root(self) -> Path:
    return Path(self.save_path, "spider_data")
