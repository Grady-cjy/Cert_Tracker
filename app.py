import streamlit as st
import json

# 页面基础设置
st.set_page_config(page_title="合规材料收集台", layout="centered")

# 加载配置文件的函数
def load_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("找不到 project_schema.json 文件，请检查路径。")
        return None

# 核心升级 1：使用 session_state 打造“记忆盒子”
# 只有在第一次打开网页时才去读 JSON，之后都读记忆盒子里的动态数据
if 'cert_data' not in st.session_state:
    st.session_state.cert_data = load_data('project_schema.json')

data = st.session_state.cert_data

if data:
    st.title(f"📁 {data['projectName']}")
    st.caption(f"最后更新时间: {data['lastUpdated']}")

    # 核心升级 2：进度条的计算现在基于记忆盒子里的动态数据
    total_items = sum(len(cat['items']) for cat in data['categories'])
    completed_items = sum(1 for cat in data['categories'] for item in cat['items'] if item['status'] == 'done')
    progress_pct = int((completed_items / total_items) * 100) if total_items > 0 else 0

    st.progress(progress_pct, text=f"总体进度: {progress_pct}% ({completed_items}/{total_items})")
    st.divider()

    # 渲染多页签
    tab_names = [cat['tabName'] for cat in data['categories']]
    tabs = st.tabs(tab_names)

    for i, tab in enumerate(tabs):
        with tab:
            for j, item in enumerate(data['categories'][i]['items']):
                
                # 确定当前复选框的状态
                is_checked = item['status'] == 'done'
                label = f"{item['name']} {'*(必填)*' if item['isRequired'] else ''}"
                
                # 渲染复选框，获取用户最新的点击动作
                new_checked = st.checkbox(label, value=is_checked, key=item['id'])
                
                # 核心升级 3：一旦发现用户点击了，立刻更新记忆盒子，并刷新网页重算进度
                if new_checked != is_checked:
                    # 更新状态字典
                    data['categories'][i]['items'][j]['status'] = 'done' if new_checked else 'pending'
                    # 强制刷新页面以更新顶部进度条
                    st.rerun()

    st.divider()
    st.info("💡 提示：目前的进度保存在你的浏览器临时记忆中。想要新增材料，只需修改 GitHub 上的 JSON 文件即可。")
