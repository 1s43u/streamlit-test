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

def check_password():
    """パスワード認証機能"""
    def password_entered():
        """ユーザーが入力したパスワードをチェック"""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # セッションからパスワードを削除
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # 初回実行時、パスワード入力を表示
        st.text_input(
            "パスワードを入力してください", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # パスワードが間違っている場合、エラーメッセージとともに再入力を促す
        st.text_input(
            "パスワードを入力してください", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        st.error("😕 パスワードが違います")
        return False
    else:
        # パスワードが正しい場合
        return True

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
    # パスワード認証をメイン処理の前に実行
    if check_password():
        main()