import streamlit as st
import json

# 页面基础设置
st.set_page_config(page_title="合规材料收集台", layout="centered")

# 1. 加载配置文件的函数
def load_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("找不到 project_schema.json 文件，请检查路径。")
        return None

data = load_data('project_schema.json')

if data:
    st.title(f"📁 {data['projectName']}")
    st.caption(f"最后更新时间: {data['lastUpdated']}")

    # 2. 计算并渲染进度条
    total_items = sum(len(cat['items']) for cat in data['categories'])
    completed_items = sum(1 for cat in data['categories'] for item in cat['items'] if item['status'] == 'done')
    progress_pct = int((completed_items / total_items) * 100) if total_items > 0 else 0

    st.progress(progress_pct, text=f"总体进度: {progress_pct}% ({completed_items}/{total_items})")
    st.divider()

    # 3. 渲染多页签 (Tabs)
    tab_names = [cat['tabName'] for cat in data['categories']]
    tabs = st.tabs(tab_names)

    for i, tab in enumerate(tabs):
        with tab:
            for item in data['categories'][i]['items']:
                # 渲染复选框
                is_checked = item['status'] == 'done'
                label = f"{item['name']} {'*(必填)*' if item['isRequired'] else ''}"
                
                # 用户点击复选框时的界面反馈
                st.checkbox(label, value=is_checked, key=item['id'])

    st.divider()
    st.info("💡 提示：在实际应用中，你可以将状态写入本地数据库或导出报告。")