# ユースケース定義

## 主要な利用シナリオ

### UC1: PDF文書の読み込み
**アクター**: RAGアプリケーション開発者  
**前提条件**: PDFファイルが存在する  
**基本フロー**:
1. DoclingLoaderを初期化
2. load(pdf_path)を呼び出し
3. DoclingがPDFを解析
4. テキスト抽出・構造化
5. refinire-ragのDocument型に変換
6. List[Document]を返却

**成功条件**: 文書内容がDocument型で取得できる

### UC2: DOCX/XLSX文書の読み込み
**アクター**: RAGアプリケーション開発者  
**前提条件**: Office文書が存在する  
**基本フロー**:
1. DoclingLoaderを初期化
2. load(file_path)を呼び出し
3. Doclingが文書形式を自動判定
4. 内容を構造化して抽出
5. refinire-ragのDocument型に変換
6. List[Document]を返却

### UC3: Web上の文書の読み込み
**アクター**: RAGアプリケーション開発者  
**前提条件**: アクセス可能なURL  
**基本フロー**:
1. DoclingLoaderを初期化
2. load(url)を呼び出し
3. DoclingがWebから文書をダウンロード
4. 文書を解析・構造化
5. refinire-ragのDocument型に変換
6. List[Document]を返却

### UC4: 設定による出力形式の制御
**アクター**: RAGアプリケーション開発者  
**前提条件**: 特定の出力形式が必要  
**基本フロー**:
1. ConversionConfigを設定（markdown/text）
2. DoclingLoaderに設定を渡して初期化
3. load()を呼び出し
4. 指定された形式で変換
5. Document型で返却

### UC5: 大きな文書のチャンク化
**アクター**: RAGアプリケーション開発者  
**前提条件**: 長い文書を分割したい  
**基本フロー**:
1. ConversionConfigでchunk_sizeを設定
2. DoclingLoaderを初期化
3. load()を呼び出し
4. 文書をチャンクサイズで分割
5. 複数のDocument型で返却

## エラーシナリオ

### E1: ファイルが存在しない
- FileNotFoundErrorを発生
- 適切なエラーメッセージを提供

### E2: サポートされていないファイル形式
- UnsupportedFormatErrorを発生
- サポート形式の一覧を提示

### E3: ネットワークエラー（URL読み込み時）
- NetworkErrorを発生
- リトライ機能を提供

### E4: メモリ不足（大きなファイル）
- MemoryErrorを適切にハンドリング
- ストリーミング処理を検討