import streamlit as st
import pandas as pd

# アプリのタイトル
st.title("🌾 Oryzae 商品開発一元管理システム")

# 1. 設定：歩留まりと販売予定数
st.sidebar.header("全体設定")
yield_rate = st.sidebar.slider("工場歩留まり率 (%)", 50, 100, 80) / 100
target_quantity = st.sidebar.number_input("販売予定数量 (袋/個)", min_value=1, value=1000)

# 2. 原材料マスター（本来はスプシやDBから読み込みますが、一旦サンプル）
raw_materials = {
    "オートミール": 0.25,
    "SWEET (甘味料)": 0.45,
    "米油": 0.85,
    "醤油麹": 0.60
}

st.header("📋 レシピ入力・原価計算")

# 入力フォーム
if 'ingredients' not in st.session_state:
    st.session_state.ingredients = []

col1, col2 = st.columns(2)
with col1:
    selected_material = st.selectbox("原材料を選択", list(raw_materials.keys()))
with col2:
    amount = st.number_input("配合量 (g/1個あたり)", min_value=0.0)

if st.button("材料を追加"):
    st.session_state.ingredients.append({
        "材料名": selected_material,
        "単価(円/g)": raw_materials[selected_material],
        "配合量(g)": amount
    })

# 3. 計算と表示
if st.session_state.ingredients:
    df = pd.DataFrame(st.session_state.ingredients)
    
    # 原価計算（歩留まり考慮）
    df["理論原価(円)"] = df["単価(円/g)"] * df["配合量(g)"]
    df["実質原価(円)"] = df["理論原価(円)"] / yield_rate
    
    # 発注量計算（kg単位）
    df["必要発注量(kg)"] = (df["配合量(g)"] / yield_rate * target_quantity) / 1000
    
    st.table(df)
    
    total_cost = df["実質原価(円)"].sum()
    st.metric("1袋あたりの最終原価", f"{total_cost:.2f} 円")
    
    st.header("📦 工場への発注指示")
    order_sheet = df[["材料名", "必要発注量(kg)"]]
    st.dataframe(order_sheet)

    if st.button("このレシピを保存・試作依頼へ"):
        st.success("データベースに保存されました（タブは増えません！）")
