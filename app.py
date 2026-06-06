# ============================================================
# DONIA LABS TECH - منصة التطوير الذكية | النسخة 2.0
# المطور: TOUINA DAOUD | © 2026 DONIA LABS TECH
# ============================================================

import streamlit as str_ui
from anthropic import Anthropic
import os
import base64
import json
import datetime

# ============================================================
# 1. إعداد الصفحة والهوية البصرية
# ============================================================
str_ui.set_page_config(
    page_title="DONIA LABS TECH",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

ADMIN_PASSWORD = "DoniaLabs2026"

# ============================================================
# 2. CSS الشامل للهوية البصرية الاحترافية
# ============================================================
str_ui.markdown("""
<style>
/* ===== استيراد الخطوط ===== */
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap');

/* ===== الخلفية العامة ===== */
.stApp {
    background: linear-gradient(135deg, #0A0E1A 0%, #0D1117 50%, #0A0E1A 100%);
    font-family: 'Tajawal', 'Segoe UI', sans-serif;
}

/* ===== إخفاء عناصر Streamlit الافتراضية ===== */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ===== الشريط الجانبي ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1117 0%, #161B27 100%);
    border-right: 1px solid #1E2D40;
}
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #00E5FF;
    font-family: 'Tajawal', sans-serif;
    font-size: 0.95rem;
    border-bottom: 1px solid #1E2D40;
    padding-bottom: 8px;
}

/* ===== العنوان الرئيسي ===== */
.main-header {
    background: linear-gradient(135deg, #0D1117 0%, #161B27 100%);
    border: 1px solid #1E3A5F;
    border-radius: 20px;
    padding: 25px 30px;
    margin-bottom: 25px;
    text-align: center;
    box-shadow: 0 0 40px rgba(0, 229, 255, 0.08);
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, #00E5FF, #0080FF, #00E5FF, transparent);
}
.main-title {
    font-family: 'Tajawal', sans-serif;
    color: #00E5FF;
    font-size: 2.2rem;
    font-weight: 900;
    margin: 0 0 8px 0;
    text-shadow: 0 0 30px rgba(0, 229, 255, 0.4);
    letter-spacing: 1px;
}
.sub-title {
    color: #8892A4;
    font-size: 1rem;
    margin: 0 0 15px 0;
    font-family: 'Tajawal', sans-serif;
}
.credits-box {
    display: inline-block;
    background: rgba(0, 229, 255, 0.06);
    border: 1px solid rgba(0, 229, 255, 0.2);
    border-radius: 10px;
    padding: 8px 20px;
}
.credits-text {
    color: #00E5FF;
    font-size: 0.95rem;
    font-weight: 700;
    margin: 0;
    font-family: 'Tajawal', sans-serif;
}
.rights-text {
    color: #4A5568;
    font-size: 0.78rem;
    margin: 4px 0 0 0;
    font-family: 'Tajawal', sans-serif;
}

/* ===== بطاقات الإحصائيات ===== */
.stat-card {
    background: linear-gradient(135deg, #0D1117, #161B27);
    border: 1px solid #1E2D40;
    border-radius: 12px;
    padding: 12px 15px;
    text-align: center;
    margin-bottom: 8px;
    transition: border-color 0.3s;
}
.stat-card:hover { border-color: #00E5FF; }
.stat-number {
    color: #00E5FF;
    font-size: 1.6rem;
    font-weight: 900;
    margin: 0;
    font-family: 'Tajawal', sans-serif;
}
.stat-label {
    color: #4A5568;
    font-size: 0.75rem;
    margin: 2px 0 0 0;
    font-family: 'Tajawal', sans-serif;
}

/* ===== رسائل الشات ===== */
[data-testid="stChatMessage"] {
    background: rgba(13, 17, 23, 0.8) !important;
    border: 1px solid #1E2D40 !important;
    border-radius: 16px !important;
    margin-bottom: 12px !important;
    padding: 16px !important;
    backdrop-filter: blur(10px);
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    border-color: rgba(0, 229, 255, 0.25) !important;
    background: rgba(0, 229, 255, 0.04) !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    border-color: rgba(0, 128, 255, 0.25) !important;
    background: rgba(0, 128, 255, 0.04) !important;
}

/* ===== حقل الإدخال ===== */
[data-testid="stChatInput"] {
    background: #0D1117 !important;
    border: 2px solid #1E3A5F !important;
    border-radius: 16px !important;
    color: #E2E8F0 !important;
    font-family: 'Tajawal', sans-serif !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #00E5FF !important;
    box-shadow: 0 0 20px rgba(0, 229, 255, 0.15) !important;
}

/* ===== الأزرار ===== */
.stButton > button {
    background: linear-gradient(135deg, #00E5FF, #0080FF) !important;
    color: #0A0E1A !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-family: 'Tajawal', sans-serif !important;
    transition: all 0.3s !important;
    padding: 8px 16px !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(0, 229, 255, 0.35) !important;
}

/* ===== شريط تقدم الـ Streaming ===== */
.streaming-indicator {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: #00E5FF;
    font-size: 0.85rem;
    font-family: 'Tajawal', sans-serif;
    padding: 6px 12px;
    background: rgba(0, 229, 255, 0.08);
    border-radius: 20px;
    border: 1px solid rgba(0, 229, 255, 0.2);
    margin-bottom: 10px;
}
.dot-pulse {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #00E5FF;
    animation: pulse 1.2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.3; transform: scale(0.7); }
}

/* ===== System Prompt Box ===== */
.stTextArea textarea {
    background: #0D1117 !important;
    border: 1px solid #1E3A5F !important;
    border-radius: 10px !important;
    color: #E2E8F0 !important;
    font-family: 'Tajawal', sans-serif !important;
    font-size: 0.88rem !important;
}
.stTextArea textarea:focus {
    border-color: #00E5FF !important;
    box-shadow: 0 0 15px rgba(0, 229, 255, 0.1) !important;
}

/* ===== Selectbox & Slider ===== */
[data-testid="stSelectbox"] > div > div {
    background: #0D1117 !important;
    border: 1px solid #1E3A5F !important;
    border-radius: 10px !important;
    color: #E2E8F0 !important;
}
.stSlider [data-baseweb="slider"] {
    padding: 5px 0;
}

/* ===== تنبيهات ===== */
.stAlert {
    border-radius: 12px !important;
    font-family: 'Tajawal', sans-serif !important;
}

/* ===== شاشة تسجيل الدخول ===== */
.login-container {
    max-width: 420px;
    margin: 80px auto;
    background: linear-gradient(135deg, #0D1117, #161B27);
    border: 1px solid #1E3A5F;
    border-radius: 24px;
    padding: 40px;
    text-align: center;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}
.login-icon {
    font-size: 3.5rem;
    margin-bottom: 15px;
}
.login-title {
    color: #00E5FF;
    font-size: 1.6rem;
    font-weight: 900;
    font-family: 'Tajawal', sans-serif;
    margin-bottom: 8px;
}
.login-subtitle {
    color: #4A5568;
    font-size: 0.9rem;
    font-family: 'Tajawal', sans-serif;
    margin-bottom: 25px;
}

/* ===== شريط الأدوات ===== */
.toolbar {
    display: flex;
    gap: 10px;
    align-items: center;
    padding: 10px 0;
    margin-bottom: 15px;
    border-bottom: 1px solid #1E2D40;
}

/* ===== بطاقة الملف المرفق ===== */
.file-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0, 229, 255, 0.1);
    border: 1px solid rgba(0, 229, 255, 0.3);
    border-radius: 8px;
    padding: 4px 10px;
    font-size: 0.82rem;
    color: #00E5FF;
    font-family: 'Tajawal', sans-serif;
    margin-bottom: 8px;
}

/* ===== Divider ===== */
hr {
    border: none !important;
    border-top: 1px solid #1E2D40 !important;
    margin: 15px 0 !important;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. شاشة تسجيل الدخول المحسّنة
# ============================================================
if "authenticated" not in str_ui.session_state:
    str_ui.session_state.authenticated = False

if not str_ui.session_state.authenticated:
    # تصميم شاشة الدخول المركزية
    col_l, col_c, col_r = str_ui.columns([1, 1.5, 1])
    with col_c:
        str_ui.markdown("""
        <div class='login-container'>
            <div class='login-icon'>🔐</div>
            <div class='login-title'>DONIA LABS TECH</div>
            <div class='login-subtitle'>مختبر الأفكار الذكية — منطقة محمية</div>
        </div>
        """, unsafe_allow_html=True)

        str_ui.markdown("##### أدخل كلمة المرور الإدارية:")
        input_password = str_ui.text_input(
            "كلمة المرور",
            type="password",
            placeholder="••••••••••••",
            label_visibility="collapsed"
        )

        col_btn1, col_btn2 = str_ui.columns([3, 1])
        with col_btn1:
            login_btn = str_ui.button("🔓 دخول إلى المنصة", use_container_width=True)
        with col_btn2:
            if str_ui.button("
