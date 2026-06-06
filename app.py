import streamlit as str_ui
from anthropic import Anthropic
import os
import uuid

# 1. إعداد واجهة وبنية تطبيق DONIA LABS TECH العالمية
str_ui.set_page_config(
    page_title="DONIA LABS TECH", 
    page_icon="🤖",
    layout="wide" # تم تحويله إلى العرض العريض لمنح مساحة مريحة للمحادثة والأرشيف
)

# تعيين كلمة المرور الإدارية الثابتة
ADMIN_PASSWORD = "DoniaLabs2026"

# تنسيق واجهة مستخدم احترافية تحاكي نظام مناظير Claude و ChatGPT
str_ui.markdown("""
    <style>
    /* تحسين لون الخلفية العام والنصوص */
    .stApp {
        background-color: #0B0F19;
        color: #E2E8F0;
    }
    
    /* تنسيق الهيدر الرئيسي الاحترافي */
    .main-title {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #00E5FF 0%, #00A3FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 800;
        margin-top: -15px;
        margin-bottom: 5px;
        font-size: 2.5rem;
    }
    .sub-title {
        text-align: center;
        color: #94A3B8;
        font-size: 1.1rem;
        margin-bottom: 25px;
    }
    
    /* صندوق براند الشركة المتطور */
    .credits-box {
        text-align: center;
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 18px;
        border-radius: 16px;
        border: 1px solid #334155;
        margin-bottom: 30px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    .credits-text {
        color: #00E5FF;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0;
        letter-spacing: 0.5px;
    }
    .rights-text {
        color: #64748B;
        font-size: 0.85rem;
        margin: 6px 0 0 0;
    }
    
    /* تحسين مظهر الأزرار والقوائم في الأرشيف الجانبي */
    .stButton>button {
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    /* تنسيق فقاعات المحادثة والمرفقات */
    .attached-file-box {
        background-color: #1E293B;
        border-left: 4px solid #00E5FF;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# 2. جدار الحماية الرقمي باستخدام كلمة المرور الثابتة
if "authenticated" not in str_ui.session_state:
    str_ui.session_state.authenticated = False

if not str_ui.session_state.authenticated:
    str_ui.warning("🔐 منطقة محظورة: يرجى إدخال كلمة المرور الإدارية للوج إلى مختبر الأفكار الذكية.")
    input_password = str_ui.text_input("أدخل كلمة المرور الإدارية للمنصة:", type="password")
    
    if str_ui.button("تسجيل الدخول 🔓", use_container_width=True):
        if input_password == ADMIN_PASSWORD:
            str_ui.session_state.authenticated = True
            str_ui.success("🎯 تم التحقق بنجاح! مرحباً بك أستاذ داود.")
            str_ui.rerun()
        else:
            str_ui.error("❌ كلمة المرور غير صحيحة! يرجى إعادة المحاولة.")
    str_ui.stop()

# =========================================================================
# 3. هيكلة وبناء مستودع أرشيف المحادثات (Sessions Archive System)
# =========================================================================
if "all_chats" not in str_ui.session_state:
    str_ui.session_state.all_chats = {} # يحتوي على معرّفات الغرف وسجلات المحادثات

if "current_chat_id" not in str_ui.session_state:
    # إنشاء أول محادثة افتراضية تلقائياً عند التشغيل الأول
    first_id = str(uuid.uuid4())
    str_ui.session_state.all_chats[first_id] = {"title": "📝 محادثة جديدة", "history": []}
    str_ui.session_state.current_chat_id = first_id

# إدارة مفتاح الـ API وتوفيره من البيئة السحابية أو اليدوية
api_key = None
try:
    if hasattr(str_ui, "secrets") and "ANT_API_KEY" in str_ui.secrets:
        api_key = str_ui.secrets["ANT_API_KEY"]
except Exception:
    api_key = None

available_models = ["claude-3-5-sonnet-latest", "claude-3-5-haiku-latest", "claude-3-opus-latest"]
selected_model = available_models[0]

# =========================================================================
# 4. بناء الـ Sidebar الجانبي (الأرشيف العالمي + الإعدادات)
# =========================================================================
with str_ui.sidebar:
    str_ui.markdown("### ➕ ركن التحكم والمحادثات")
    
    # زر إنشاء محادثة جديدة تماماً وإضافتها للأرشيف
    if str_ui.button("✨ بدء محادثة جديدة", use_container_width=True, type="primary"):
        new_id = str(uuid.uuid4())
        str_ui.session_state.all_chats[new_id] = {"title": "📝 محادثة جديدة", "history": []}
        str_ui.session_state.current_chat_id = new_id
        str_ui.rerun()
        
    str_ui.markdown("---")
    str_ui.markdown("### 📂 أرشيف سجلات المحادثة")
    
    # عرض قائمة المحادثات السابقة كأزرار تفاعلية للتنقل بينها
    for chat_id, chat_data in list(str_ui.session_state.all_chats.items()):
        # تحديد لون أو شكل مخصص للمحادثة النشطة حالياً
        is_current = (chat_id == str_ui.session_state.current_chat_id)
        btn_label = f"{chat_data['title']}"
        
        if str_ui.button(btn_label, key=f"btn_{chat_id}", use_container_width=True, help="اضغط للانتقال لهذه المحادثة"):
            str_ui.session_state.current_chat_id = chat_id
            str_ui.rerun()

    str_ui.markdown("---")
    str_ui.markdown("### 🔑 مصادقة خادر الذكاء")
    if not api_key:
        api_key = str_ui.text_input("أدخل مفتاح Anthropic API:", type="password")
    else:
        str_ui.success("✅ تم جلب المفتاح تلقائياً")

    # محرك الجلب الديناميكي التلقائي للنماذج المتاحة سحابياً
    if api_key:
        try:
            client_init = Anthropic(api_key=api_key)
            models_list = client_init.models.list()
            fetched_models = [model.id for model in models_list if "claude" in model.id]
            if fetched_models:
                available_models = fetched_models
            
            default_index = 0
            for idx, m_name in enumerate(available_models):
                if "sonnet" in m_name and "latest" in m_name:
                    default_index = idx
                    break
            
            str_ui.markdown("---")
            selected_model = str_ui.selectbox(
                "اختر النموذج الفعّال حالياً:",
                options=available_models,
                index=default_index
            )
        except Exception:
            selected_model = str_ui.selectbox("اختر النموذج الفعّال (الوضع الاحتياطي):", options=available_models, index=0)

    str_ui.markdown("---")
    str_ui.markdown("### 📎 مستودع المرفقات للمحادثة الحالية")
    uploaded_file = str_ui.file_uploader(
        "ارفق ملفاً (PDF, TXT, PY, PNG, JPG):", 
        type=["txt", "pdf", "py", "png", "jpg", "jpeg", "docx", "json", "html"]
    )
    if uploaded_file:
        str_ui.success(f"📎 جاهز للتحليل: {uploaded_file.name}")

# =========================================================================
# 5. واجهة العرض الرئيسية والهيدر المحدث لـ DONIA LABS TECH
# =========================================================================
logo_path = "LOGO_DONIA_LABS_TECH.png"
if os.path.exists(logo_path):
    col1, col2, col3 = str_ui.columns([3, 2, 3])
    with col2:
        str_ui.image(logo_path, use_container_width=True)

str_ui.markdown("<h1 class='main-title'>🤖 منصة التطوير الذكية</h1>", unsafe_allow_html=True)
str_ui.markdown("<p class='sub-title'>البيئة الاحترافية العالمية لإدارة وتطوير المشاريع التعليمية والتجارية</p>", unsafe_allow_html=True)

str_ui.markdown("""
    <div class='credits-box'>
        <p class='credits-text'>👤 رائد الأعمال والمشرف العام: TOUINA DAOUD</p>
        <p class='rights-text'>© 2026 DONIA LABS TECH. جميع الحقوق محفوظة لـ مختبر الأفكار الذكية</p>
    </div>
""", unsafe_allow_html=True)

# جلب بيانات التاريخ والذاكرة الخاصة بالمحادثة النشطة حالياً
current_chat = str_ui.session_state.all_chats[str_ui.session_state.current_chat_id]
chat_history = current_chat["history"]

# طباعة الرسائل السابقة للمحادثة المحددة حالياً على الشاشة
for message in chat_history:
    with str_ui.chat_message(message["role"]):
        str_ui.markdown(message["display_content"] if "display_content" in message else message["content"])

# =========================================================================
# 6. استقبال المحادثة المدخلة وتوليد الإجابة
# =========================================================================
if user_prompt := str_ui.chat_input("كيف يمكنني مساعدتك في تطوير مشروعك اليوم؟"):
    
    if not api_key:
        str_ui.error("⚠️ خطأ في الاتصال: يرجى تزويد المنصة بمفتاح الـ API عبر الشريط الجانبي أولاً.")
    else:
        file_info_text = ""
        display_text = user_prompt
        
        # معالجة الملفات المرفوعة وإدماج سياقها البرمجي
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith(('.txt', '.py', '.json', '.html', '.css')):
                    file_content = uploaded_file.read().decode("utf-8")
                    file_info_text = f"\n\n[مرفق ملف نصي مسمى: {uploaded_file.name}]\nمحتوى الملف:\n{file_content}"
                else:
                    file_info_text = f"\n\n[مرفق ملف مسمى: {uploaded_file.name} وجاهز للسياق والتحليل المستفيض]"
                
                # شكل العرض المرئي الأنيق للملف المرفوع داخل المحادثة
                display_text = f"📎 **ملف مرفق:** `{uploaded_file.name}`\n\n{user_prompt}"
            except Exception as e:
                file_info_text = f"\n\n[تعذر استخراج النص الداخلي للملف: {str(e)}]"
        
        # إذا كانت المحادثة جديدة وبدون عنوان، قم بتسميتها بأول 30 حرف من السؤال
        if current_chat["title"] == "📝 محادثة جديدة":
            clean_title = user_prompt[:25] + "..." if len(user_prompt) > 25 else user_prompt
            current_chat["title"] = f"💬 {clean_title}"
            
        # طباعة سؤال المستخدم فوراً في الواجهة
        with str_ui.chat_message("user"):
            str_ui.markdown(display_text)
            
        # حفظ الرسالة في التاريخ مع تذكر صيغة العرض والصيغة الكاملة التي ستُرسل للموديل
        chat_history.append({
            "role": "user", 
            "content": user_prompt + file_info_text,
            "display_content": display_text
        })

        try:
            client = Anthropic(api_key=api_key)
            
            with str_ui.chat_message("assistant"):
                message_placeholder = str_ui.empty()
                message_placeholder.markdown(f"⏳ جاري التحليل والتفكير عبر ({selected_model})...")
                
                # إرسال تاريخ الغرفة الحالية فقط إلى السيرفر لقراءة السياق
                response = client.messages.create(
                    model=selected_model,
                    max_tokens=4000,
                    temperature=0.3,
                    messages=[{"role": m["role"], "content": m["content"]} for m in chat_history]
                )
                
                assistant_response = response.content[0].text
                message_placeholder.markdown(assistant_response)
                
                # حفظ رد الذكاء الاصطناعي في الغرفة النشطة
                chat_history.append({
                    "role": "assistant", 
                    "content": assistant_response,
                    "display_content": assistant_response
                })
                
                # تحديث الجلسة وإعادة تحميل الصفحة لتحديث مظهر الأرشيف الجانبي
                str_ui.rerun()
                
        except Exception as error:
            str_ui.error(f"حدث خطأ أثناء الاتصال بالـ API: {str(error)}")
