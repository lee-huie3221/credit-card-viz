# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ========== 页面配置 ==========
st.set_page_config(page_title="信用卡还款对比", layout="wide", page_icon="💳")

# ========== 隐藏Streamlit默认样式 ==========
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {
        background-color: #f7f7f8;
    }
    .stButton button {
        background-color: #000000;
        color: white;
        border-radius: 8px;
    }
    .stButton button:hover {
        background-color: #333333;
    }
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# ========== 字体设置 ==========
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'PingFang SC']
plt.rcParams['axes.unicode_minus'] = False

# ========== 标题区域 ==========
st.markdown('<h1 style="text-align:center; font-size:2.5rem; margin-bottom:0;">💳 信用卡还款策略</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#666666; font-size:1rem; margin-top:-10px;">最低还款 · 分期还款 · 全额还款</p>', unsafe_allow_html=True)
st.markdown("---")

# ========== 侧边栏 ==========
with st.sidebar:
    st.markdown("### ⚙️ 参数设置")
    st.markdown("---")
    
    amount = st.number_input("💰 消费金额", min_value=100, max_value=100000, value=5000, step=1000)
    months = st.selectbox("📅 分期期数", [3, 6, 9, 12, 18, 24], index=3)
    daily_rate = st.number_input("📉 最低还款日利率", min_value=0.01, max_value=0.10, value=0.05, step=0.01) / 100
    installment_rate = st.number_input("📊 分期月费率", min_value=0.1, max_value=2.0, value=0.7, step=0.1) / 100
    
    st.markdown("---")
    st.markdown("### 📌 对比选项")
    show_full = st.checkbox("全额还款", value=True)
    show_installment = st.checkbox("分期还款", value=True)
    show_min = st.checkbox("最低还款", value=True)

# ========== 计算函数 ==========
def calc_full(amount):
    return amount

def calc_installment(amount, months):
    return amount + amount * installment_rate * months

def calc_min_payment(amount, months):
    remaining = amount
    total_interest = 0
    daily = daily_rate
    for month in range(months):
        payment = remaining * 0.1
        interest = remaining * daily * 30
        total_interest += interest
        remaining = remaining - payment + interest
        if remaining <= 0:
            break
    return amount + total_interest

full_total = calc_full(amount)
inst_total = calc_installment(amount, months)
min_total = calc_min_payment(amount, months)

# ========== 结果卡片（简约风格） ==========
col1, col2, col3 = st.columns(3)

with col1:
    if show_full:
        st.markdown(f"""
        <div style="background:white; padding:1rem; border-radius:12px; text-align:center; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
            <p style="color:#2e7d32; font-weight:bold; margin:0;">全额还款</p>
            <p style="font-size:1.8rem; font-weight:bold; margin:0;">{full_total:,.0f}<span style="font-size:1rem;"> 元</span></p>
            <p style="color:#666; margin:0;">利息 0 元</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    if show_installment:
        st.markdown(f"""
        <div style="background:white; padding:1rem; border-radius:12px; text-align:center; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
            <p style="color:#ed6c02; font-weight:bold; margin:0;">分期还款</p>
            <p style="font-size:1.8rem; font-weight:bold; margin:0;">{inst_total:,.0f}<span style="font-size:1rem;"> 元</span></p>
            <p style="color:#666; margin:0;">利息 +{inst_total-amount:,.0f} 元</p>
        </div>
        """, unsafe_allow_html=True)

with col3:
    if show_min:
        st.markdown(f"""
        <div style="background:white; padding:1rem; border-radius:12px; text-align:center; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
            <p style="color:#d32f2f; font-weight:bold; margin:0;">最低还款</p>
            <p style="font-size:1.8rem; font-weight:bold; margin:0;">{min_total:,.0f}<span style="font-size:1rem;"> 元</span></p>
            <p style="color:#666; margin:0;">利息 +{min_total-amount:,.0f} 元</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ========== 柱状图（简约风格） ==========
st.markdown("### 📊 利息对比")

fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor('#f7f7f8')
ax.set_facecolor('#f7f7f8')

labels, values, colors = [], [], []
if show_full:
    labels.append("全额还款"); values.append(full_total); colors.append("#2e7d32")
if show_installment:
    labels.append("分期还款"); values.append(inst_total); colors.append("#ed6c02")
if show_min:
    labels.append("最低还款"); values.append(min_total); colors.append("#d32f2f")

bars = ax.bar(labels, values, color=colors, width=0.5, edgecolor='white', linewidth=1.5)
ax.set_ylabel("总还款金额 (元)", fontsize=11)
ax.set_title(f"消费 {amount:,} 元 · 分 {months} 期", fontsize=13, fontweight='normal', pad=15)
ax.axhline(y=amount, color='#999', linestyle='--', alpha=0.6, linewidth=1)
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
            f'{int(bar.get_height()):,}', ha='center', va='bottom', fontsize=10, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#ddd')
ax.spines['bottom'].set_color('#ddd')
ax.grid(axis='y', alpha=0.2, linestyle='--')
st.pyplot(fig)

# ========== 债务递减曲线 ==========
st.markdown("### 📉 债务变化")

fig2, ax2 = plt.subplots(figsize=(10, 4.5))
fig2.patch.set_facecolor('#f7f7f8')
ax2.set_facecolor('#f7f7f8')

x_months = list(range(months + 1))

if show_full:
    ax2.plot(x_months, [amount] + [0]*months, 'o-', label='全额还款', color='#2e7d32', linewidth=1.8, markersize=5)
if show_installment:
    monthly = amount / months
    inst_curve = [amount - monthly * i for i in range(months + 1)]
    ax2.plot(x_months, inst_curve, 's-', label='分期还款', color='#ed6c02', linewidth=1.8, markersize=5)
if show_min:
    remaining = amount
    min_curve = [remaining]
    for i in range(months):
        interest = remaining * daily_rate * 30
        remaining = remaining - remaining * 0.1 + interest
        if remaining < 0:
            remaining = 0
        min_curve.append(remaining)
    ax2.plot(x_months, min_curve, '^-', label='最低还款', color='#d32f2f', linewidth=1.8, markersize=5)

ax2.set_xlabel("月份", fontsize=11)
ax2.set_ylabel("剩余债务 (元)", fontsize=11)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color('#ddd')
ax2.spines['bottom'].set_color('#ddd')
ax2.grid(alpha=0.2, linestyle='--')
ax2.legend(loc='upper right', frameon=False)
st.pyplot(fig2)

# ========== 结论 ==========
st.markdown("---")
st.markdown(f"""
<div style="background:#e8f5e9; padding:0.8rem 1rem; border-radius:10px; margin-top:0.5rem;">
    <p style="margin:0; color:#2e7d32;">💡 <strong>结论</strong> · 全额还款利息为0；分期还款多付 {inst_total-amount:,.0f} 元；最低还款多付 {min_total-amount:,.0f} 元</p>
</div>
""", unsafe_allow_html=True)

# ========== 数据来源 ==========
with st.expander("📄 数据来源"):
    st.markdown("""
    - **工商银行**：日利率万分之五，按月复利 → [查看官网](https://www.icbc.com.cn/page/890517450792525824.html)
    - **农业银行**：日利率万分之五，按月复利，分期费率0.80% → [查看官网](https://www.abchina.com/cn/CreditCard/WealthManagement/Bill/)
    - **中国银行**：日利率万分之五，按月复利 → [查看官网](https://www.boc.cn/bcservice/bc3/bc31/201203/t20120331_1767028.html)
    - **建设银行**：日利率万分之五，按月复利，分期费率0.75% → [查看官网](https://creditcard1.ccb.com/chn/2022-08/29/article_2022082916344488399.shtml)
    - **交通银行**：日利率万分之五，按月复利，分期费率0.70% → [查看官网](https://creditcardapp.bankcomm.com/openapps/cms/1431733796531773.html)
    
    > 分期费率取平均值0.75%，数据来源于各银行官网公示的服务价目表
    """)