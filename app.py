import streamlit as str_ui
from anthropic import Anthropic
import os

# 1. إعداد واجهة وبنية تطبيق DONIA LABS TECH
str_ui.set_page_config(
    page_title="DONIA LABS TECH", 
    page_icon="🤖",
    layout="centered"
)

# تعيين كلمة المرور الإدارية الثابتة
ADMIN_PASSWORD = "DoniaLabs2026"

# تنسيق الهوية البصرية الذكية لمختبركم الاحترافي
str_ui.markdown("""
    <style>
    .main-title {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #00E5FF;
        text-align: center;
        font-weight: 700;
        margin-top: -10px;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        color: #A0AEC0;
        font-size: 1.1rem;
        margin-bottom: 20px;
    }
    .credits-box {
        text-align: center;
        background-color: #1A202C;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #2D3748;
        margin-bottom: 35px;
    }
    .credits-text {
        color: #00E5FF;
        font-size: 1.05rem;
        font-weight: 600;
        margin: 0;
    }
    .rights-text {
        color: #718096;
        font-size: 0.85rem;
        margin: 8px 0 0 0;
    }
    </style>
""", unsafe_allow_html=True)

# جدار الحماية الرقمي باستخدام كلمة المرور الثابتة
if "authenticated" not in str_ui.session_state:
    str_ui.session_state.authenticated = False

if not str_ui.session_state.authenticated:
    str_ui.warning("🔐 منطقة محظورة: يرجى إدخال كلمة المرور الإدارية للوج إلى مختبر الأفكار الذكية.")
    
    input_password = str_ui.text_input("أدخل كلمة المرور الإدارية للمنصة:", type="password")
    
    if str_ui.button("تسجيل الدخول 🔓", use_container_width=True):
        if input_password == ADMIN_PASSWORD:
            str_ui.session_state.authenticated = True
            str_ui.success("🎯 تم التحقق بنجاح! مرحباً بك.")
            str_ui.rerun()
        else:
            str_ui.error("❌ كلمة المرور غير صحيحة! يرجى إعادة المحاولة.")
            
    str_ui.stop()

# =========================================================================
# جدار الحماية وإدارة الـ API Key وجلب النماذج ديناميكياً
# =========================================================================

api_key = None
available_models = ["claude-3-5-sonnet-latest", "claude-3-5-haiku-latest", "claude-3-opus-latest"] # قائمة احتياطية افتراضية
selected_model = available_models[0]

try:
    if hasattr(str_ui, "secrets") and "ANT_API_KEY" in str_ui.secrets:
        api_key = str_ui.secrets["ANT_API_KEY"]
except Exception:
    api_key = None

with str_ui.sidebar:
    str_ui.markdown("### 🔑 مصادقة خادم الذكاء")
    if not api_key:
        api_key = str_ui.text_input("أدخل مفتاح Anthropic API الخاص بك لتشغيل المحرك:", type="password")
        if api_key:
            str_ui.success("✅ تم ربط المفتاح بنجاح!")
    else:
        str_ui.success("✅ تم جلب المفتاح تلقائياً من الإعدادات السحابية")
        
    # محرك الجلب الديناميكي التلقائي للنماذج المتاحة من شركة Anthropic
    if api_key:
        try:
            client_init = Anthropic(api_key=api_key)
            # الاتصال بالخادم الأصلي لقراءة قائمة النماذج الفعّالة الحالية
            models_list = client_init.models.list()
            # استخراج المعرفات (IDs) الخاصة بالنماذج فقط وتصفيتها
            fetched_models = [model.id for model in models_list if "claude" in model.id]
            
            if fetched_models:
                available_models = fetched_models
                
            str_ui.markdown("---")
            str_ui.markdown("### 🤖 محرك المعالجة الذكي")
            
            # تحديد الخيار الافتراضي الأنسب من القائمة المجلوبة تلقائياً
            default_index = 0
            for idx, m_name in enumerate(available_models):
                if "sonnet" in m_name and "latest" in m_name:
                    default_index = idx
                    break
                    
            selected_model = str_ui.selectbox(
                "اختر النموذج الفعّال حالياً سحابياً:",
                options=available_models,
                index=default_index,
                help="هذه القائمة تتحدث ديناميكياً فور إطلاق Anthropic لأي نموذج جديد."
            )
        except Exception as e:
            # في حال وجود مشكلة شبكة أو قيود حساب، يعتمد النظام القائمة الاحتياطية بأمان
            selected_model = str_ui.selectbox("اختر النموذج الفعّال حالياً (الوضع الاحتياطي):", options=available_models, index=0)

    str_ui.markdown("---")
    str_ui.markdown("### 📂 مستودع الملفات والمرفقات")
    uploaded_file = str_ui.file_uploader(
        "اختر ملفاً لإرفاقه بالمحادثة (PDF, TXT, PY, PNG, JPG):", 
        type=["txt", "pdf", "py", "png", "jpg", "jpeg", "docx", "json", "html"]
    )
    if uploaded_file:
        str_ui.success(f"📎 تم تحميل الملف: {uploaded_file.name} بنجاح وجاهز للتحليل.")

# 4. بناء واجهة العرض والشعارات للعلامة التجارية
logo_path = "LOGO_DONIA_LABS_TECH.png"
if os.path.exists(logo_path):
    col1, col2, col3 = str_ui.columns([1, 2, 1])
    with col2:
        str_ui.image(logo_path, use_container_width=True)

str_ui.markdown("<h1 class='main-title'>🤖 منصة التطوير الذكية</h1>", unsafe_allow_html=True)
str_ui.markdown("<p class='sub-title'>البيئة الاحترافية لإدارة وتطوير المشاريع التعليمية والتجارية</p>", unsafe_allow_html=True)

str_ui.markdown("""
    <div class='credits-box'>
        <p class='credits-text'>👤 رائد الأعمال: TOUINA DAOUD</p>
        <p class='rights-text'>© 2026 DONIA LABS TECH. جميع الحقوق محفوظة لـ مختبر الأفكار الذكية</p>
    </div>
""", unsafe_allow_html=True)

# 5. إدارة الذاكرة ومحرك الشات الحواري لـ Claude 3.5 Sonnet
if "chat_history" not in str_ui.session_state:
    str_ui.session_state.chat_history = []

for message in str_ui.session_state.chat_history:
    with str_ui.chat_message(message["role"]):
        str_ui.markdown(message["content"])

if user_prompt := str_ui.chat_input("كيف يمكنني مساعدتك في تطوير مشروعك اليوم؟"):
    
    if not api_key:
        str_ui.error("⚠️ خطأ في الاتصال: يرجى تزويد المنصة بمفتاح الـ API عبر الشريط الجانبي أولاً لتفعيل محرك العمل.")
    else:
        full_prompt = user_prompt
        file_info_text = ""
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith(('.txt', '.py', '.json', '.html', '.css')):
                    file_content = uploaded_file.read().decode("utf-8")
                    file_info_text = f"\n\n[مرفق ملف نصي مسمى: {uploaded_file.name}]\nمحتوى الملف:\n{file_content}"
                else:
                    file_info_text = f"\n\n[مرفق ملف مسمى: {uploaded_file.name} وجاهز للسياق والتحليل]"
            except Exception as e:
                file_info_text = f"\n\n[تعذر استخراج النص الداخلي للملف: {str(e)}]"
        
        with str_ui.chat_message("user"):
            if uploaded_file:
                str_ui.markdown(f"📎 *{uploaded_file.name}* \n\n {user_prompt}")
            else:
                str_ui.markdown(user_prompt)
        
        str_ui.session_state.chat_history.append({"role": "user", "content": user_prompt + file_info_text})

        try:
            client = Anthropic(api_key=api_key)
            
            with str_ui.chat_message("assistant"):
                message_placeholder = str_ui.empty()
                message_placeholder.markdown(f"⏳ جاري التحليل والتفكير عبر المحرك الديناميكي ({selected_model})...")
                
                # استدعاء النموذج الذي تم اختياره تلقائياً أو يدوياً من القائمة الديناميكية المجلوبة
                response = client.messages.create(
                    model=selected_model,
                    max_tokens=4000,
                    temperature=0.3,
                    messages=[{"role": m["role"], "content": m["content"]} for m in str_ui.session_state.chat_history]
                )
                
                assistant_response = response.content[0].text
                message_placeholder.markdown(assistant_response)
                str_ui.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
                
        except Exception as error:
            str_ui.error(f"حدث خطأ أثناء الاتصال بالـ API: {str(error)}")
