import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.text_to_sql.spider_loader import SpiderLoader


class TestSpiderLoader:
    """SpiderLoader 클래스에 대한 테스트 케이스들"""

    @pytest.fixture
    def temp_dir(self):
        """테스트용 임시 디렉토리 생성"""
        temp_path = tempfile.mkdtemp()
        yield temp_path
        shutil.rmtree(temp_path)

    @pytest.fixture
    def spider_loader(self, temp_dir):
        """SpiderLoader 인스턴스 생성"""
        return SpiderLoader(save_path=temp_dir)


    class TestDownloadDataset:
        """데이터셋 다운로드 테스트"""

        @patch('src.text_to_sql.loader.gdown.download')
        @patch('src.text_to_sql.loader.zipfile.ZipFile')
        def test_download_dataset_success(self, mock_zipfile, mock_gdown, spider_loader):
            """
            Given: 정상적인 네트워크 환경과 Google Drive 파일
            When: download_dataset()을 호출할 때
            Then: 데이터셋이 성공적으로 다운로드되고 압축 해제되어야 함
            """
            # Arrange: Mock 설정 및 예상 동작 정의
            mock_gdown.return_value = "temp_spider.zip"
            mock_zip_instance = MagicMock()
            mock_zipfile.return_value.__enter__.return_value = mock_zip_instance
            
            # Act: download_dataset() 호출
            spider_loader.download_dataset()
            
            # Assert: 다운로드 및 압축 해제 성공 확인
            # gdown.download이 올바른 URL과 경로로 호출되었는지 확인
            expected_url = f"https://drive.google.com/uc?id={spider_loader.gdrive_id}"
            mock_gdown.assert_called_once()
            call_args = mock_gdown.call_args
            assert call_args[0][0] == expected_url
            assert call_args[0][1].endswith("Spider.zip")
            assert call_args[1]["quiet"] == False
            
            # zipfile.ZipFile이 올바른 경로로 호출되었는지 확인
            mock_zipfile.assert_called_once()
            zip_call_args = mock_zipfile.call_args[0]
            assert zip_call_args[0].endswith("Spider.zip")
            assert zip_call_args[1] == 'r'
            
            # extractall(압축 해제)이 올바른 경로로 호출되었는지 확인
            mock_zip_instance.extractall.assert_called_once_with(spider_loader.save_path)

        @patch('src.text_to_sql.loader.gdown.download')
        @patch('src.text_to_sql.loader.zipfile.ZipFile')
        def test_download_dir_already_exists(self, mock_zipfile, mock_gdown, spider_loader):
            """
            Given: 저장 디렉토리에 이미 데이터셋이 존재하는 상태
            When: download_dataset()을 호출할 때
            Then: 데이터셋이 다운로드되지 않아야 함
            """
            # Arrange: _get_dataset_detail_path_root가 존재하는 디렉토리를 반환하도록 Mock
            mock_dataset_path = MagicMock()
            mock_dataset_path.exists.return_value = True
            mock_dataset_path.iterdir.return_value = ['existing_file.txt']  # 디렉토리가 비어있지 않다고 가정
            
            with patch.object(spider_loader, '_get_dataset_detail_path_root', return_value=mock_dataset_path):
                # Act: download_dataset() 호출
                spider_loader.download_dataset()
                
                # Assert: 다운로드 관련 메서드들이 호출되지 않았는지 확인
                mock_gdown.assert_not_called()
                mock_zipfile.assert_not_called()


    class TestGetSqliteDatabase:
        """SQLite 데이터베이스 경로 반환 테스트"""

        def test_get_sqlite_database_returns_correct_path(self, spider_loader):
            """
            Given: SpiderLoader 인스턴스
            When: get_sqlite_database()을 호출할 때
            Then: 올바른 SQLite 데이터베이스 경로를 반환해야 함
            """
            # Arrange: SpiderLoader 인스턴스 준비
            # Act: get_sqlite_database() 호출
            result = spider_loader.get_sqlite_database()
            
            # Assert: 올바른 경로 반환 확인
            expected_path = Path(spider_loader.save_path, "spider_data", "database")
            assert result == expected_path


    class TestGetSqliteJsonFiles:
        """SQLite JSON 파일들 반환 테스트"""

        def test_get_sqlite_json_files_contains_required_keys(self, spider_loader):
            """
            Given: SpiderLoader 인스턴스
            When: get_sqlite_json_files()을 호출할 때
            Then: 필수 키들(table, gold_sql, dev)이 포함되고 올바르게 할당되어야 함
            """
            # Arrange: SpiderLoader 인스턴스 준비
            
            # Act: get_sqlite_json_files() 호출
            result = spider_loader.get_sqlite_json_files()
            
            # Assert: 필수 키들 존재 확인
            assert "table" in result
            assert "gold_sql" in result
            assert "dev" in result
            
            # Assert: 각 키에 올바른 파일명이 할당되었는지 확인
            assert result["table"].name == "tables.json"
            assert result["gold_sql"].name == "dev_gold.json"
            assert result["dev"].name == "dev.json"
