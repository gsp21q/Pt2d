import streamlit as st
import subprocess
import tempfile
import os

# إعدادات الصفحة لتناسب الجوال والشاشات الداكنة
st.set_page_config(page_title="محول النصوص والتقارير", page_icon="📄", layout="centered")

st.title("📄 محول النصوص والمعادلات إلى Word")
st.markdown("اكتب تقريرك باستخدام النصوص العادية، أو **Markdown**، أو معادلات **LaTeX** (بين علامات `$` أو `$$`).")

# صندوق إدخال النص
input_text = st.text_area("أدخل النص هنا...", height=300, placeholder="مثال: لحساب الطاقة نستخدم المعادلة $E = mc^2$ ...")

# زر التحويل
if st.button("⚙️ تحويل إلى Word", use_container_width=True):
    if input_text.strip():
        with st.spinner("جاري معالجة النص والمعادلات..."):
            try:
                # إنشاء ملفات مؤقتة آمنة
                with tempfile.NamedTemporaryFile(delete=False, suffix=".md", mode="w", encoding="utf-8") as temp_in:
                    temp_in.write(input_text)
                    temp_in_path = temp_in.name
                
                temp_out_path = temp_in_path.replace(".md", ".docx")

                # تشغيل Pandoc مع دعم معادلات الرياضيات
                # tex_math_dollars يضمن تحويل الـ LaTeX إلى معادلات 
                # استبدل الجزء القديم بهذا:
try:
    # استخدام الصيغة الأبسط والأكثر استقراراً
    subprocess.run([
        "pandoc", 
        temp_in_path, 
        "-o", temp_out_path,
        "--from", "markdown",
        "--to", "docx"
    ], check=True)
except Exception as e:
    # محاولة ثانية بصيغة بديلة في حال فشل الأولى
    subprocess.run(f"pandoc {temp_in_path} -o {temp_out_path}", shell=True, check=True)


                # قراءة الملف الناتج للتحميل
                with open(temp_out_path, "rb") as file:
                    docx_data = file.read()

                st.success("✅ تم التحويل بنجاح!")
                st.download_button(
                    label="📥 تحميل ملف الـ Word",
                    data=docx_data,
                    file_name="Report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )

                # تنظيف الملفات المؤقتة
                os.remove(temp_in_path)
                os.remove(temp_out_path)

            except Exception as e:
                st.error(f"❌ حدث خطأ أثناء التحويل. تفاصيل: {e}")
    else:
        st.warning("⚠️ يرجى كتابة نص أولاً قبل التحويل.")
