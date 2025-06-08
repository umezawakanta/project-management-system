# 案件管理システム

PythonとDjangoを使用した案件管理システム

## 機能
- プロジェクト管理
- タスク管理
- ユーザー管理

## セットアップ

1. 仮想環境を有効化
```bash
source venv/bin/activate
依存関係をインストール
pip install -r requirements.txt
マイグレーションを実行
python manage.py makemigrations
python manage.py migrate
スーパーユーザーを作成
python manage.py createsuperuser
開発サーバーを起動
python manage.py runserver
