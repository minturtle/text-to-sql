from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
import tempfile
import os
import zipfile
import gdown



class Loader(ABC):

  def __init__(self, save_path: str, gdrive_id: str, dataset_name: str):
    self.save_path = save_path
    self.gdrive_id = gdrive_id
    self.dataset_name = dataset_name


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
          temp_zip_path = os.path.join(temp_dir, f"{self.dataset_name}.zip")
          gdown.download(f"https://drive.google.com/uc?id={self.gdrive_id}", temp_zip_path, quiet=False)
          
          # 2. zip 파일 압축 해제
          with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
              zip_ref.extractall(self.save_path)
      
      print(f"{self.dataset_name} dataset has been successfully downloaded to {self.save_path}.")


  @abstractmethod
  def get_sqlite_database(self) -> Path:
    pass

  @abstractmethod
  def get_sqlite_json_files(self) -> List[Path]:
    pass

  @abstractmethod
  def _get_dataset_detail_path_root(self) -> Path:
    pass