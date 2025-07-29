"""
特許PDF構造化ライブラリの使用例
"""

from patent_extractor import PatentExtractor
import json
import os

def basic_usage():
    """基本的な使用例"""
    # エクストラクタのインスタンス化
    extractor = PatentExtractor(
        api_key="YOUR_API_KEY"  # APIキーを指定
    )
    
    # 特許PDFの処理
    result = extractor.process_patent_pdf("example_patent.pdf")
    
    # 結果を表示
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 結果をファイルに保存
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

def with_custom_schema():
    """カスタムJSONスキーマを使用した例"""
    # カスタムスキーマの定義
    custom_schema = {
        "title": "SimplePatentSchema",
        "type": "object",
        "required": ["publicationIdentifier", "title", "abstract", "claims"],
        "properties": {
            "publicationIdentifier": {"type": "string"},
            "title": {"type": "string"},
            "abstract": {"type": "string"},
            "claims": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "claimNumber": {"type": "integer"},
                        "text": {"type": "string"}
                    }
                }
            }
        }
    }
    
    # エクストラクタのインスタンス化（カスタムスキーマを指定）
    extractor = PatentExtractor(
        model_name="gemini-1.5-pro",
        api_key="YOUR_API_KEY",
        json_schema=custom_schema
    )
    
    # 特許PDFの処理
    result = extractor.process_patent_pdf("example_patent.pdf")
    
    # 結果を保存
    with open("custom_schema_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

def with_custom_prompt():
    """カスタムプロンプトを使用した例"""
    # カスタムプロンプトを指定
    custom_prompt = """
    この特許PDFから次の情報を抽出し、提供されたスキーマに従ってJSON形式で構造化してください：
    1. 特許の基本情報（公開番号、出願日、公開日、発明の名称）
    2. 発明者と出願人の詳細情報
    3. 請求項（すべての請求項と依存関係）
    4. 要約と発明の技術分野
    図面や表の詳細な説明は省略してかまいません。
    """
    
    # エクストラクタのインスタンス化（カスタムプロンプトを指定）
    extractor = PatentExtractor(
        model_name="gpt-4o",
        api_key="YOUR_OPENAI_API_KEY",
        user_prompt=custom_prompt
    )
    
    # 特許PDFの処理
    result = extractor.process_patent_pdf("example_patent.pdf")
    
    # 結果を保存
    with open("custom_prompt_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

def with_custom_generation_params():
    """カスタムの生成パラメータを使用した例"""
    # エクストラクタのインスタンス化（temperatureとmax_tokensを指定）
    extractor = PatentExtractor(
        model_name="claude-3-opus-20240229",
        api_key="YOUR_ANTHROPIC_API_KEY",
        temperature=0.3,  # より多様な出力を生成（デフォルトは0.1）
        max_tokens=8192   # より長い出力を許可（デフォルトは4096）
    )
    
    # 特許PDFの処理
    result = extractor.process_patent_pdf("complex_patent.pdf")
    
    # 結果を保存
    with open("custom_params_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

def using_environment_variables():
    """環境変数を使用した例"""
    # 環境変数を設定
    os.environ["GOOGLE_API_KEY"] = "your-gemini-api-key"
    os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
    os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-api-key"
    
    # Gemini（環境変数からAPIキーを取得）
    gemini_extractor = PatentExtractor(
        model_name="gemini-1.5-pro", 
        temperature=0.05,  # 非常に確定的な出力のために低いtemperature
        max_tokens=4096
    )
    gemini_result = gemini_extractor.process_patent_pdf("example_patent.pdf")
    
    # OpenAI（環境変数からAPIキーを取得）
    openai_extractor = PatentExtractor(
        model_name="gpt-4o",
        temperature=0.2,   # より創造的な出力
        max_tokens=8192
    )
    openai_result = openai_extractor.process_patent_pdf("example_patent.pdf")
    
    # Anthropic（環境変数からAPIキーを取得）
    claude_extractor = PatentExtractor(
        model_name="claude-3-opus-20240229",
        temperature=0.1,
        max_tokens=10000  # 非常に長い出力を許可
    )
    claude_result = claude_extractor.process_patent_pdf("example_patent.pdf")
    
    # 結果を比較
    results = {
        "gemini": gemini_result,
        "openai": openai_result,
        "claude": claude_result
    }
    
    with open("model_comparison.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

def batch_processing():
    """バッチ処理の例"""
    # エクストラクタのインスタンス化（最大トークン数を増やして詳細な抽出を可能に）
    extractor = PatentExtractor(
        api_key="YOUR_API_KEY",
        temperature=0.1,
        max_tokens=8192
    )
    
    # 処理対象のPDFリスト
    pdf_files = [
        "patent1.pdf",
        "patent2.pdf",
        "patent3.pdf"
    ]
    
    # 各PDFを処理
    results = {}
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file}...")
        results[pdf_file] = extractor.process_patent_pdf(pdf_file)
    
    # 結果をまとめて保存
    with open("batch_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # 使用例を実行するには、コメントを解除してAPIキーを設定してください
    # basic_usage()
    # with_custom_schema()
    # with_custom_prompt()
    # with_custom_generation_params()
    # using_environment_variables()
    # batch_processing()
    
    print("使用例の実行には、対応するコードのコメントを解除し、APIキーを設定してください。")
"""
特許PDF構造化ライブラリの使用例
"""

from patent_extractor import PatentExtractor
import json
import os

def basic_usage():
    """基本的な使用例"""
    # エクストラクタのインスタンス化
    extractor = PatentExtractor(
        api_key="YOUR_API_KEY"  # APIキーを指定
    )
    
    # 特許PDFの処理
    result = extractor.process_patent_pdf("example_patent.pdf")
    
    # 結果を表示
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 結果をファイルに保存
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

def with_custom_schema():
    """カスタムJSONスキーマを使用した例"""
    # カスタムスキーマの定義
    custom_schema = {
        "title": "SimplePatentSchema",
        "type": "object",
        "required": ["publicationIdentifier", "title", "abstract", "claims"],
        "properties": {
            "publicationIdentifier": {"type": "string"},
            "title": {"type": "string"},
            "abstract": {"type": "string"},
            "claims": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "claimNumber": {"type": "integer"},
                        "text": {"type": "string"}
                    }
                }
            }
        }
    }
    
    # エクストラクタのインスタンス化（カスタムスキーマを指定）
    extractor = PatentExtractor(
        model_name="gemini-1.5-pro",
        api_key="YOUR_API_KEY",
        json_schema=custom_schema
    )
    
    # 特許PDFの処理
    result = extractor.process_patent_pdf("example_patent.pdf")
    
    # 結果を保存
    with open("custom_schema_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

def with_custom_prompt():
    """カスタムプロンプトを使用した例"""
    # カスタムプロンプトを指定
    custom_prompt = """
    この特許PDFから次の情報を抽出し、提供されたスキーマに従ってJSON形式で構造化してください：
    1. 特許の基本情報（公開番号、出願日、公開日、発明の名称）
    2. 発明者と出願人の詳細情報
    3. 請求項（すべての請求項と依存関係）
    4. 要約と発明の技術分野
    図面や表の詳細な説明は省略してかまいません。
    """
    
    # エクストラクタのインスタンス化（カスタムプロンプトを指定）
    extractor = PatentExtractor(
        model_name="gpt-4o",
        api_key="YOUR_OPENAI_API_KEY",
        user_prompt=custom_prompt
    )
    
    # 特許PDFの処理
    result = extractor.process_patent_pdf("example_patent.pdf")
    
    # 結果を保存
    with open("custom_prompt_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

def using_environment_variables():
    """環境変数を使用した例"""
    # 環境変数を設定
    os.environ["GOOGLE_API_KEY"] = "your-gemini-api-key"
    os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
    os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-api-key"
    
    # Gemini（環境変数からAPIキーを取得）
    gemini_extractor = PatentExtractor(model_name="gemini-1.5-pro")
    gemini_result = gemini_extractor.process_patent_pdf("example_patent.pdf")
    
    # OpenAI（環境変数からAPIキーを取得）
    openai_extractor = PatentExtractor(model_name="gpt-4o")
    openai_result = openai_extractor.process_patent_pdf("example_patent.pdf")
    
    # Anthropic（環境変数からAPIキーを取得）
    claude_extractor = PatentExtractor(model_name="claude-3-opus-20240229")
    claude_result = claude_extractor.process_patent_pdf("example_patent.pdf")
    
    # 結果を比較
    results = {
        "gemini": gemini_result,
        "openai": openai_result,
        "claude": claude_result
    }
    
    with open("model_comparison.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

def batch_processing():
    """バッチ処理の例"""
    # エクストラクタのインスタンス化
    extractor = PatentExtractor(api_key="YOUR_API_KEY")
    
    # 処理対象のPDFリスト
    pdf_files = [
        "patent1.pdf",
        "patent2.pdf",
        "patent3.pdf"
    ]
    
    # 各PDFを処理
    results = {}
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file}...")
        results[pdf_file] = extractor.process_patent_pdf(pdf_file)
    
    # 結果をまとめて保存
    with open("batch_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # 使用例を実行するには、コメントを解除してAPIキーを設定してください
    # basic_usage()
    # with_custom_schema()
    # with_custom_prompt()
    # using_environment_variables()
    # batch_processing()
    
    print("使用例の実行には、対応するコードのコメントを解除し、APIキーを設定してください。")
