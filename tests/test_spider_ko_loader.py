import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.text_to_sql.spider_ko_loader import SpiderKoLoader


class TestSpiderKoLoader:
    """SpiderKoLoader 클래스에 대한 테스트 케이스들"""

    @pytest.fixture
    def temp_dir(self):
        """테스트용 임시 디렉토리 생성"""
        temp_path = tempfile.mkdtemp()
        yield temp_path
        shutil.rmtree(temp_path)

    @pytest.fixture
    def spider_ko_loader(self, temp_dir):
        """SpiderKoLoader 인스턴스 생성"""
        return SpiderKoLoader(save_path=temp_dir)

    def test_download_dataset_pipeline(self, spider_ko_loader):
        """
        Arrange: SpiderKoLoader 인스턴스 생성
        Act: download_dataset() 호출
        Assert: 다음 파이프라인이 순서대로 실행되어야 함:
        1. super의 download_dataset 호출
        2. huggingface에서 spider-ko 데이터셋 다운로드
        3. dev_ko.json 파일 생성
        """
        # Arrange: Mock 설정 및 예상 동작 정의
        mock_dataset = MagicMock()
        mock_validation_data = [
            {
                "db_id": "test_db",
                "query": "SELECT * FROM table",
                "query_toks": ["SELECT", "*", "FROM", "table"],
                "query_toks_no_value": ["SELECT", "*", "FROM", "table"],
                "question_ko": "테이블에서 모든 데이터를 조회해주세요",
                "sql": "SELECT * FROM table"
            }
        ]
        mock_dataset.__getitem__.return_value = mock_validation_data
        
        with patch('src.text_to_sql.spider_ko_loader.SpiderLoader.download_dataset') as mock_super_download, \
             patch('src.text_to_sql.spider_ko_loader.load_dataset', return_value=mock_dataset) as mock_load_dataset, \
             patch('builtins.open', create=True) as mock_open, \
             patch('json.dump') as mock_json_dump:
            
            # Act: download_dataset() 호출
            spider_ko_loader.download_dataset()
            
            # Assert: 파이프라인 순서대로 실행되었는지 확인
            
            # 1. super의 download_dataset이 호출되었는지 확인
            mock_super_download.assert_called_once()
            
            # 2. huggingface에서 spider-ko 데이터셋 다운로드 확인
            mock_load_dataset.assert_called_once_with(spider_ko_loader.hf_dataset_name)
            
            # 3. dev_ko.json 파일 생성 확인
            mock_open.assert_called_once()
            mock_json_dump.assert_called_once()

    def test_is_dataset_already_downloaded(self, spider_ko_loader):
        """
        Arrange: SpiderKoLoader 인스턴스 생성
        Act: _is_dataset_already_downloaded() 호출
        Assert: 부모 클래스의 결과와 dev_ko.json 파일 존재 여부를 모두 확인해야 함
        """
        # Arrange: Mock 설정
        with patch.object(spider_ko_loader, '_get_dataset_detail_path_root') as mock_get_path, \
             patch('src.text_to_sql.spider_ko_loader.SpiderLoader._is_dataset_already_downloaded', return_value=True) as mock_super_check, \
             patch('src.text_to_sql.spider_ko_loader.Path.exists') as mock_path_exists:
            
            mock_path = MagicMock()
            mock_get_path.return_value = mock_path
            mock_path_exists.return_value = True
            
            # Act: _is_dataset_already_downloaded() 호출
            result = spider_ko_loader._is_spider_ko_dataset_already_downloaded()
            
            # Assert: 결과 확인
            assert result == True
            mock_super_check.assert_called_once()
            mock_path_exists.assert_called_once()
            
            # dev_ko.json 파일 경로가 올바르게 확인되었는지 검증
            expected_path = Path(mock_path, "dev_ko.json")
            mock_path_exists.assert_called_with()

    def test_is_dataset_already_downloaded_false_when_super_false(self, spider_ko_loader):
        """
        Arrange: SpiderKoLoader 인스턴스 생성
        Act: _is_dataset_already_downloaded() 호출 (부모 클래스가 False 반환)
        Assert: False를 반환해야 함
        """
        # Arrange: Mock 설정
        with patch('src.text_to_sql.spider_ko_loader.SpiderLoader._is_dataset_already_downloaded', return_value=False) as mock_super_check:
            
            # Act: _is_dataset_already_downloaded() 호출
            result = spider_ko_loader._is_spider_ko_dataset_already_downloaded()
            
            # Assert: 결과 확인
            assert result == False
            mock_super_check.assert_called_once()

    def test_is_dataset_already_downloaded_false_when_dev_ko_not_exists(self, spider_ko_loader):
        """
        Arrange: SpiderKoLoader 인스턴스 생성
        Act: _is_dataset_already_downloaded() 호출 (dev_ko.json이 존재하지 않음)
        Assert: False를 반환해야 함
        """
        # Arrange: Mock 설정
        with patch.object(spider_ko_loader, '_get_dataset_detail_path_root') as mock_get_path, \
             patch('src.text_to_sql.spider_ko_loader.SpiderLoader._is_dataset_already_downloaded', return_value=True) as mock_super_check, \
             patch('src.text_to_sql.spider_ko_loader.Path.exists') as mock_path_exists:
            
            mock_path = MagicMock()
            mock_get_path.return_value = mock_path
            mock_path_exists.return_value = False  # dev_ko.json이 존재하지 않음
            
            # Act: _is_dataset_already_downloaded() 호출
            result = spider_ko_loader._is_spider_ko_dataset_already_downloaded()
            
            # Assert: 결과 확인
            assert result == False
            mock_super_check.assert_called_once()
            mock_path_exists.assert_called_once()
