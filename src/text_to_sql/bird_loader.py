import gdown
import zipfile
import tempfile
import os
from pathlib import Path
from typing import List

class BirdMiniDevLoader:

  def __init__(self, save_path: str):
    self.gdrive_id = "1UJyA6I6pTmmhYpwdn8iT9QKrcJqSQAcX"
    self.save_path = save_path

  def download_dataset(self):
      """
      Google Drive에서 Bird Mini Dev 데이터셋을 다운로드하고 압축을 해제합니다.
      
      Args:
          save_path (str): 데이터를 저장할 경로
          
      Author: Minseok kim
      """

      # save_path 디렉토리 생성
      Path(self.save_path).mkdir(parents=True, exist_ok=True)
      
      # 1. google drive에서 zip 파일 다운로드. 이 때 zip 파일은 temporary directory에 저장됨.
      with tempfile.TemporaryDirectory() as temp_dir:
          temp_zip_path = os.path.join(temp_dir, "bird_mini_dev.zip")
          gdown.download(f"https://drive.google.com/uc?id={self.gdrive_id}", temp_zip_path, quiet=False)
          
          # 2. zip 파일 압축 해제
          with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
              zip_ref.extractall(self.save_path)
      
      print(f"Bird Mini Dev dataset has been successfully downloaded to {self.save_path}.")


  def get_sqlite_database(self) -> Path:
    """
    Bird Mini Dev 데이터셋의 sqlite 데이터페이스 폴더를 반환합니다.
    """
    return Path(self.save_path, "data_minidev", "MINIDEV", "dev_database")


  def get_sqlite_json_files(self) -> List[Path]:
    """
    Bird Mini Dev 데이터셋의 sqlite 데이터페이스 폴더에서 테이블 정보가 담긴 json 파일을 반환합니다.
    """
    return {
      "table" : Path(self.save_path, "data_minidev", "MINIDEV", "dev_tables.json"),
      "gold_sql" : Path(self.save_path, "data_minidev", "MINIDEV", "mini_dev_sqlite_gold.json"),
      "dev" : Path(self.save_path, "data_minidev", "MINIDEV", "mini_dev_sqlite_dev.json"),
    }