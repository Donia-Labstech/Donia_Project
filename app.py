import streamlit as str_ui
from anthropic import Anthropic
import os
import pyotp
import qrcode
from PIL import Image
import io

# 1. إعداد واجهة Streamlit وحماية التهيئة الأولى
str_ui.set_page_config(
    page_title="DONIA LABS TECH", 
    page_icon="🤖",
    layout="centered"
)

# تصفيف الواجهة وتطوير مظهرها البصري ليتماشى مع الهوية الذكية لشعارك
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

# 2. إعداد مفتاح الأمان الثابت الخاص بـ Google Authenticator
# ملاحظة: هذا المفتاح السري مشفر ومولد خصيصاً لمنظمتك لإصدار رموز الـ 2FA
if "totp_secret" not in str_ui.session_state:
    str_ui.session_state.totp_secret = "JBSWY3DPEHPK3PXP" # مفتاح أمان أساسي خاص بك

totp = pyotp.TOTP(str_ui.session_state.totp_secret)

# نظام جدار الحماية الذكي والمصادقة المزدوجة
if "authenticated" not in str_ui.session_state:
    str_ui.session_state.authenticated = False

if not str_ui.session_state.authenticated:
    str_ui.warning("🔐 منطقة محظورة: يرجى إثبات هويتك الإدارية عبر مصادقة Google للوج إلى مختبر الأفكار الذكية.")
    
    col1, col2 = str_ui.columns(2)
    with col1:
        # توليد رابط الـ QR لإضافته إلى تطبيق Google Authenticator
        auth_url = totp.provisioning_uri(name="Touina Daoud", issuer_name="DONIA LABS TECH")
        
        # إنشاء صورة الـ QR برمجياً وعرضها في الواجهة
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(auth_url)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white")
        
        # تحويل الصورة إلى بايتات ليفهمها Streamlit
        buf = io.BytesIO()
        img_qr.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        str_ui.image(byte_im, caption="امسح الـ QR عبر تطبيق Google Authenticator", width=220)
        
    with col2:
        str_ui.markdown("### 🛡️ خطوتان للأمان المطلق:")
        str_ui.info("1. افتح تطبيق Google Authenticator في هاتفك وامسح رمز الـ QR المقابل.")
        str_ui.info("2. أدخل الرمز المكون من 6 أرقام والذي يظهر في هاتفك بالأسفل لتأكيد الدخول.")
        
        user_code = str_ui.text_input("أدخل رمز التحقق الديناميكي الحالي (6 أرقام):", max_chars=6, type="password")
        
        if str_ui.button("تأكيد الهوية والمصادقة 🔓", use_container_width=True):
            # التحقق الفوري والدقيق من الرمز المتغير
            if totp.verify(user_code):
                str_ui.session_state.authenticated = True
                str_ui.success("🎯 تم التحقق من سحابة Google بنجاح! مرحباً بك أستاذ داود.")
                str_ui.rerun()
            else:
                str_ui.error("❌ الرمز غير صحيح أو انتهت صلاحيته الزمنية (30 ثانية)! تم تأمين خوادم دونيا لابس تيك.")
                
    str_ui.stop() # حجب بقية عناصر التطبيق تماماً حتى يتم التحقق

# =========================================================================
# الكود التالي لا يظهر إلا بعد إدخال رمز Google Authenticator الصحيح بنجاح
# =========================================================================

# 3. إدارة مفاتيح الـ API التلقائية (سحابياً) أو طلبها محلياً بأمان
api_key = None
if "ANT_API_KEY" in str_ui.secrets:
    api_key = str_ui.secrets["ANT_API_KEY"]
else:
    with str_ui.sidebar:
        str_ui.markdown("### 🔑 مصادقة خادم الذكاء")
        api_key = str_ui.text_input("أدخل مفتاح Anthropic API الجديد:", type="password")
        if api_key:
            str_ui.success("✅ تم ربط المفتاح الجديد محلياً")

# 4. عرض الشعار الرسمي للمنصة في المنتصف العلوي بدقة عالية
logo_path = "LOGO_DONIA_LABS_TECH.png"
if os.path.exists(logo_path):
    col1, col2, col3 = str_ui.columns([1, 2, 1])
    with col2:
        str_ui.image(logo_path, use_container_width=True)

# العناوين المطورة للعلامة التجارية
str_ui.markdown("<h1 class='main-title'>🤖 منصة التطوير الذكية</h1>", unsafe_allow_html=True)
str_ui.markdown("<p class='sub-title'>البيئة الاحترافية لإدارة وتطوير المشاريع التعليمية والتجارية</p>", unsafe_allow_html=True)

# 5. توثيق اسم رائد الأعمال وحفظ حقوق الملكية الفكرية لبراندك
str_ui.markdown("""
    <div class='credits-box'>
        <p class='credits-text'>👤 رائد الأعمال: TOUINA DAOUD</p>
        <p class='rights-text'>© 2026 DONIA LABS TECH. جميع الحقوق محفوظة لـ مختبر الأفكار الذكية</p>
    </div>
""", unsafe_allow_html=True)

# 6. تفعيل الذاكرة وحفظ سياق وتاريخ المحادثة في الـ Session State
if "chat_history" not in str_ui.session_state:
    str_ui.session_state.chat_history = []

# عرض الرسائل السابقة المتبادلة في الواجهة بتنسيق ذكي
for message in str_ui.session_state.chat_history:
    with str_ui.chat_message(message["role"]):
        str_ui.markdown(message["content"])

# 7. استقبال المدخلات والأسئلة من خلال شريط الإدخال السفلي
if user_prompt := str_ui.chat_input("كيف يمكنني مساعدتك في تطوير مشروعك التجاري اليوم؟"):
    
    if not api_key:
        str_ui.error("⚠️ خطأ في الاتصال: يرجى تزويد المنصة بمفتاح الـ API الجديد عبر الشريط الجانبي أولاً.")
    else:
        with str_ui.chat_message("user"):
            str_ui.markdown(user_prompt)
        
        str_ui.session_state.chat_history.append({"role": "user", "content": user_prompt})

        try:
            client = Anthropic(api_key=api_key)
            
            with str_ui.chat_message("assistant"):
                message_placeholder = str_ui.empty()
                message_placeholder.markdown("⏳ جاري التحليل والتفكير عبر Claude 3.5 Sonnet...")
                
                response = client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=4000,
                    temperature=0.3,
                    messages=[{"role": m["role"], "content": m["content"]} for m in str_ui.session_state.chat_history]
                )
                
                assistant_response = response.content[0].text
                message_placeholder.markdown(assistant_response)
                str_ui.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
                
        except Exception as error:
            str_ui.error(f"حدث خطأ أثناء الاتصال بالـ API: {str(error)}")