from src.text_to_sql import BirdMiniDevLoader


if __name__ == "__main__":
    bird_mini_dev_loader = BirdMiniDevLoader(save_path="data")
    bird_mini_dev_loader.download_dataset()
    print(bird_mini_dev_loader.get_sqlite_database())
    print(bird_mini_dev_loader.get_evaluation_files())
