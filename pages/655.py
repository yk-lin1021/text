from github import Github

# 用您的 GitHub 令牌替換這裡
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]

# 使用 GitHub 令牌初始化 PyGithub
g = Github(GITHUB_TOKEN)

try:
    # 嘗試獲取當前使用者資料
    user = g.get_user()
    print("Authenticated as:", user.login)  # 顯示 GitHub 用戶名稱
except Exception as e:
    print(f"Authentication failed: {e}")  # 如果認證失敗，顯示錯誤訊息
