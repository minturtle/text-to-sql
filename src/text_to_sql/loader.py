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
      save_path_obj = Path(self.save_path)
      save_path_obj.mkdir(parents=True, exist_ok=True)
      
      # 이미 데이터가 존재하는지 확인
      if self._is_dataset_already_downloaded():
          print(f"{self.dataset_name} dataset already exists at {self.save_path}. Skipping download.")
          return
      
      # 1. google drive에서 zip 파일 다운로드. 이 때 zip 파일은 temporary directory에 저장됨.
      with tempfile.TemporaryDirectory() as temp_dir:
          temp_zip_name = f"{self.dataset_name.replace(' ', '_')}.zip"
          temp_zip_path = os.path.join(temp_dir, temp_zip_name)
          gdown.download(f"https://drive.google.com/uc?id={self.gdrive_id}", temp_zip_path, quiet=False)
          
          # 2. zip 파일 압축 해제
          with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
              zip_ref.extractall(self.save_path)
      
      print(f"{self.dataset_name} dataset has been successfully downloaded to {self.save_path}.")

  def _is_dataset_already_downloaded(self) -> bool:
      """
      데이터셋이 이미 다운로드되었는지 확인합니다.
      
      Returns:
          bool: 데이터셋이 이미 존재하면 True, 그렇지 않으면 False
      """
      # 실제 데이터셋 디렉토리가 존재하고 비어있지 않으면 다운로드된 것으로 간주
      dataset_path = self._get_dataset_detail_path_root()
      return dataset_path.exists() and any(dataset_path.iterdir())

  @abstractmethod
  def get_sqlite_database(self) -> Path:
    pass

  @abstractmethod
  def get_sqlite_json_files(self) -> List[Path]:
    pass

  @abstractmethod
  def _get_dataset_detail_path_root(self) -> Path:
    pass