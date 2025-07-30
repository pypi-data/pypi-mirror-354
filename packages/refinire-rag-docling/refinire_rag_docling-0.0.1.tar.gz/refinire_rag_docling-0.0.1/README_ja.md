# Refinire-RAG Docling プラグイン

refinire-rag用の強力な文書処理プラグインです。IBM Doclingライブラリを活用して、PDF、DOCX、XLSX、HTML、画像など様々な文書形式を読み込み・処理できます。

## 特徴

🗂️ **多形式対応**: PDF、DOCX、XLSX、HTML、PNG、JPG、JPEG  
📑 **高度なPDF処理**: ページレイアウト解析、読み順序、表構造、コード、数式  
🧬 **統一された出力**: 全形式で一貫した文書表現  
↪️ **柔軟な出力**: Markdown、プレーンテキスト、JSON出力形式  
🔒 **ローカル処理**: 外部API呼び出しなしの安全な文書処理  
🔍 **OCR対応**: スキャン文書と画像用の内蔵OCR  
⚡ **バッチ処理**: 複数文書の効率的な処理  
🧩 **チャンク分割**: RAGアプリケーション用の自動テキスト分割

## インストール

```bash
# リポジトリをクローン
git clone <repository-url>
cd refinire-rag-docling

# uvでインストール（推奨）
uv add refinire-rag-docling

# または pipでインストール
pip install refinire-rag-docling
```

## クイックスタート

### 基本的な使用方法

```python
from refinire_rag_docling import DoclingLoader

# デフォルト設定でローダーを作成
loader = DoclingLoader()

# 単一文書を読み込み
documents = loader.load("path/to/document.pdf")

# 処理されたコンテンツにアクセス
for doc in documents:
    print(doc["content"])
    print(doc["metadata"])
```

### カスタム設定

```python
from refinire_rag_docling import DoclingLoader, ConversionConfig, ExportFormat

# 処理オプションを設定
config = ConversionConfig(
    export_format=ExportFormat.MARKDOWN,
    chunk_size=1024,
    ocr_enabled=True,
    table_structure=True
)

loader = DoclingLoader(config)
documents = loader.load("document.pdf")
```

### ファクトリーメソッド

```python
# Markdown出力用の簡単セットアップ
loader = DoclingLoader.create_with_markdown_output(chunk_size=512)

# テキスト出力用の簡単セットアップ
loader = DoclingLoader.create_with_text_output(chunk_size=2048)
```

### バッチ処理

```python
file_paths = ["doc1.pdf", "doc2.docx", "doc3.xlsx"]
documents = loader.load_batch(file_paths)

print(f"{len(documents)}個の文書を処理しました")
```

## 対応形式

| 形式 | 拡張子 | 機能 |
|------|--------|------|
| PDF | `.pdf` | レイアウト解析、OCR、表抽出 |
| Word | `.docx` | テキスト、書式、メタデータ |
| Excel | `.xlsx` | スプレッドシートデータ、複数シート |
| HTML | `.html` | Webコンテンツ、構造 |
| 画像 | `.png`, `.jpg`, `.jpeg` | OCRテキスト抽出 |

## 設定オプション

### ConversionConfig

```python
config = ConversionConfig(
    export_format=ExportFormat.MARKDOWN,  # MARKDOWN、TEXT、JSON
    chunk_size=512,                       # 100-4096文字
    ocr_enabled=True,                     # 画像のOCRを有効化
    table_structure=True,                 # 表構造を保持
    options={}                            # 追加オプション
)
```

### 出力形式

- **MARKDOWN**: 書式、表、構造を含むリッチテキスト
- **TEXT**: プレーンテキストのみ
- **JSON**: メタデータ付き構造化データ

## 文書構造

処理された各文書は以下の辞書を返します：

```python
{
    "content": "抽出されたテキストコンテンツ...",
    "metadata": {
        "source": "/path/to/file",
        "format": "pdf",
        "file_size": 1024,
        "page_count": 5,
        "processing_time": 2.3
    },
    "chunks": ["chunk1", "chunk2", ...],  # チャンク分割が有効な場合
}
```

## 開発

### 開発環境のセットアップ

```bash
# クローンとセットアップ
git clone <repository-url>
cd refinire-rag-docling

# 依存関係をインストール
uv add --dev pytest pytest-cov

# テスト実行
pytest tests/ -v

# カバレッジ付きで実行
pytest tests/ --cov=src --cov-report=term-missing
```

### プロジェクト構造

```
refinire-rag-docling/
├── src/
│   └── refinire_rag_docling/
│       ├── __init__.py
│       ├── loader.py          # メインDoclingLoaderクラス
│       ├── models.py          # データモデルと型
│       └── services.py        # 文書処理ロジック
├── tests/
│   ├── unit/                  # ユニットテスト
│   └── e2e/                   # 統合テスト
├── examples/                  # 使用例
├── docs/                      # ドキュメント
└── pyproject.toml
```

### テスト実行

```bash
# 全テスト
pytest tests/

# ユニットテストのみ
pytest tests/unit/

# カバレッジ付き
pytest tests/ --cov=src --cov-report=html
```

## エラーハンドリング

プラグインには包括的なエラーハンドリングが含まれています：

```python
from refinire_rag_docling import (
    DoclingLoaderError,
    FileFormatNotSupportedError,
    DocumentProcessingError,
    ConfigurationError
)

try:
    documents = loader.load("document.pdf")
except FileFormatNotSupportedError:
    print("サポートされていないファイル形式")
except DocumentProcessingError as e:
    print(f"処理に失敗しました: {e}")
```

## パフォーマンスのヒント

1. **バッチ処理**: 複数ファイルには `load_batch()` を使用
2. **チャンクサイズ**: RAGシステムに合わせてチャンクサイズを最適化
3. **OCR設定**: テキストベース文書ではOCRを無効化
4. **形式選択**: 適切な出力形式を選択

## コントリビューション

1. リポジトリをフォーク
2. フィーチャーブランチを作成
3. 新機能にテストを追加
4. 全テストが通ることを確認
5. プルリクエストを送信

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています - 詳細はLICENSEファイルをご覧ください。

## 依存関係

- [Docling](https://github.com/docling-project/docling): 文書処理エンジン
- Python 3.10+

## 謝辞

- DoclingライブラリのIBM DS4SDチーム
- refinire-ragエコシステム

## サポート

- 📖 [ドキュメント](./docs/)
- 🐛 [イシュートラッカー](https://github.com/your-repo/issues)
- 💬 [ディスカッション](https://github.com/your-repo/discussions)