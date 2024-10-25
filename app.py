import streamlit as st
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os

# 環境変数の読み込み
load_dotenv()

def initialize_chat():
    """ChatAnthropic の初期化"""
    return ChatAnthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        model="claude-3-5-sonnet-20240620",
        temperature=0.7
    )

def main():
    st.title("Streamlit Test App")
    
    # テキスト入力
    user_input = st.text_input("何か入力してください：")
    
    # ボタン
    if st.button("送信"):
        if user_input:
            # AIチャットの初期化
            chat = initialize_chat()
            
            # 処理中の表示
            with st.spinner("処理中..."):
                try:
                    # AIへのリクエスト
                    response = chat.invoke(input=user_input)
                    
                    # 結果の表示
                    st.markdown("### 応答:")
                    st.write(response.content)
                    
                except Exception as e:
                    st.error(f"エラーが発生しました: {str(e)}")
        else:
            st.warning("テキストを入力してください")
    
    # サイドバーにも何か表示
    st.sidebar.title("設定")
    st.sidebar.write("これはテスト用のアプリです")

if __name__ == "__main__":
    main()