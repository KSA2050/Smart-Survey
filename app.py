import streamlit as st
import openai
import json
from datetime import datetime

st.set_page_config(
page_title=“Smart Semantic Guardian”,
page_icon=“shield”,
layout=“wide”,
initial_sidebar_state=“expanded”
)

st.markdown(”””

<style>
.main-header {
    background: linear-gradient(135deg, #1a3a6b 0%, #0d6efd 100%);
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    color: white;
    margin-bottom: 30px;
}
.error-card {
    background: #fff5f5;
    border-right: 5px solid #e53e3e;
    padding: 15px 20px;
    border-radius: 10px;
    margin: 10px 0;
}
.warning-card {
    background: #fffbeb;
    border-right: 5px solid #d69e2e;
    padding: 15px 20px;
    border-radius: 10px;
    margin: 10px 0;
}
.success-card {
    background: #f0fff4;
    border-right: 5px solid #38a169;
    padding: 15px 20px;
    border-radius: 10px;
    margin: 10px 0;
}
</style>

“””, unsafe_allow_html=True)

SYSTEM_PROMPT = “”“You are a smart semantic validator for Arabic statistical survey forms.
Analyze the form data and detect logical/semantic contradictions between fields.

Look for contradictions like:

1. Age vs education level (e.g. age 19 with PhD)
1. Age vs years of experience (e.g. age 22 with 25 years experience)
1. Employment status vs salary (e.g. unemployed with salary 10000)
1. Marital status vs number of children (e.g. single with 4 children)
1. Nationality vs native language contradictions
1. Job title vs gender contradictions
1. Any other logical inconsistency

Always respond with JSON only in this exact format:
{
“confidence_score”: 85,
“status”: “clean”,
“issues”: [],
“summary”: “No issues found”
}

For issues use this format:
{
“confidence_score”: 20,
“status”: “error”,
“issues”: [
{
“severity”: “high”,
“field_1”: “field name”,
“field_2”: “field name”,
“description”: “description in Arabic”,
“suggestion”: “suggestion in Arabic”
}
],
“summary”: “summary in Arabic”
}”””

def analyze_form(api_key, form_data):
client = openai.OpenAI(api_key=api_key)
form_text = “\n”.join([f”- {k}: {v}” for k, v in form_data.items() if v])
user_message = “Analyze this survey form for logical contradictions and respond with JSON only:\n\n” + form_text
response = client.chat.completions.create(
model=“gpt-4o”,
messages=[
{“role”: “system”, “content”: SYSTEM_PROMPT},
{“role”: “user”, “content”: user_message}
],
temperature=0.1,
max_tokens=1000
)
raw = response.choices[0].message.content.strip()
raw = raw.replace(”`json", "").replace("`”, “”).strip()
return json.loads(raw)

st.markdown(”””

<div class="main-header">
    <h1>Smart Semantic Guardian</h1>
    <h2 style="color:#93c5fd">الحارس الدلالي</h2>
    <p>نظام ذكي للتحقق من جودة البيانات الاحصائية لحظيا</p>
    <small>هكاثون الابتكار في البيانات - الهيئة العامة للاحصاء 2026</small>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
st.markdown(”## الاعدادات”)
api_key = st.text_input(“OpenAI API Key”, type=“password”, placeholder=“sk-…”)
st.markdown(”—”)
st.markdown(”### احصائيات الجلسة”)
if “total_forms” not in st.session_state:
st.session_state.total_forms = 0
st.session_state.errors_found = 0
st.session_state.clean_forms = 0
col1, col2 = st.columns(2)
col1.metric(“استمارات”, st.session_state.total_forms)
col2.metric(“اخطاء”, st.session_state.errors_found)
st.markdown(”—”)
st.info(“يكتشف النظام التناقضات المنطقية في البيانات لحظيا باستخدام GPT-4o”)

tab1, tab2, tab3 = st.tabs([“الاستمارة التفاعلية”, “سجلات اختبار”, “لوحة التحكم”])

with tab1:
st.markdown(”### استمارة مسح سوق العمل”)
col1, col2 = st.columns(2)
with col1:
st.markdown(”#### البيانات الشخصية”)
age = st.number_input(“العمر”, min_value=10, max_value=100, value=30)
gender = st.selectbox(“الجنس”, [“ذكر”, “انثى”])
nationality = st.selectbox(“الجنسية”, [“سعودي”, “مصري”, “اردني”, “هندي”, “باكستاني”, “اخرى”])
native_language = st.selectbox(“اللغة الام”, [“العربية”, “الانجليزية”, “الاردية”, “الهندية”, “اخرى”])
with col2:
st.markdown(”#### البيانات المهنية”)
education = st.selectbox(“المؤهل العلمي”, [“اقل من ثانوي”, “ثانوي”, “دبلوم”, “بكالوريوس”, “ماجستير”, “دكتوراه”])
employment_status = st.selectbox(“الحالة الوظيفية”, [“موظف حكومي”, “موظف قطاع خاص”, “اعمال حرة”, “غير موظف”, “طالب”, “متقاعد”])
job_title = st.text_input(“المسمى الوظيفي”, placeholder=“مثال: مهندس، طبيب…”)
years_exp = st.number_input(“سنوات الخبرة”, min_value=0, max_value=50, value=5)
monthly_salary = st.number_input(“الراتب الشهري ريال”, min_value=0, max_value=100000, value=0, step=500)
col3, col4 = st.columns(2)
with col3:
st.markdown(”#### الحالة الاجتماعية”)
marital_status = st.selectbox(“الحالة الاجتماعية”, [“اعزب”, “متزوج”, “مطلق”, “ارمل”])
family_members = st.number_input(“عدد افراد الاسرة”, min_value=1, max_value=20, value=1)
children_count = st.number_input(“عدد الاطفال”, min_value=0, max_value=15, value=0)
with col4:
st.markdown(”#### بيانات اضافية”)
region = st.selectbox(“المنطقة”, [“الرياض”, “مكة المكرمة”, “المدينة المنورة”, “الشرقية”, “اخرى”])
sector = st.selectbox(“القطاع”, [“حكومي”, “خاص”, “غير ربحي”, “لا ينطبق”])
income_source = st.selectbox(“مصدر الدخل”, [“راتب”, “اعمال حرة”, “استثمارات”, “لا يوجد”])

```
st.markdown("---")
if st.button("فحص الاستمارة بالذكاء الاصطناعي", use_container_width=True):
    if not api_key:
        st.error("الرجاء ادخال OpenAI API Key في الشريط الجانبي")
    else:
        form_data = {
            "Age": age, "Gender": gender, "Nationality": nationality,
            "Native Language": native_language, "Education": education,
            "Employment Status": employment_status, "Job Title": job_title,
            "Years Experience": years_exp, "Monthly Salary": monthly_salary,
            "Marital Status": marital_status, "Family Members": family_members,
            "Children": children_count, "Sector": sector, "Income Source": income_source
        }
        with st.spinner("النظام يحلل الاستمارة..."):
            try:
                result = analyze_form(api_key, form_data)
                st.session_state.total_forms += 1
                score = result.get("confidence_score", 0)
                status = result.get("status", "error")
                issues = result.get("issues", [])
                if issues:
                    st.session_state.errors_found += len(issues)
                else:
                    st.session_state.clean_forms += 1

                st.markdown("---")
                st.markdown("## نتائج الفحص")
                col_s1, col_s2, col_s3 = st.columns(3)
                color = "#38a169" if score >= 80 else "#d69e2e" if score >= 60 else "#e53e3e"
                with col_s1:
                    st.markdown(f'<div style="background:{color}22;border:3px solid {color};padding:20px;border-radius:15px;text-align:center"><div style="color:{color};font-size:3rem;font-weight:900">{score}</div><div>درجة الثقة</div></div>', unsafe_allow_html=True)
                with col_s2:
                    st.markdown(f'<div style="background:#ebf8ff;border:3px solid #3182ce;padding:20px;border-radius:15px;text-align:center"><div style="color:#3182ce;font-size:3rem;font-weight:900">{len(issues)}</div><div>مشكلة مكتشفة</div></div>', unsafe_allow_html=True)
                with col_s3:
                    status_map = {"clean": ("نظيفة", "#38a169"), "warning": ("تحذير", "#d69e2e"), "error": ("اخطاء", "#e53e3e")}
                    s_text, s_color = status_map.get(status, ("غير محدد", "#666"))
                    st.markdown(f'<div style="background:{s_color}22;border:3px solid {s_color};padding:20px;border-radius:15px;text-align:center"><div style="color:{s_color};font-size:2rem;font-weight:900">{s_text}</div><div>الحالة</div></div>', unsafe_allow_html=True)

                st.markdown(f"**الملخص:** {result.get('summary', '')}")

                if issues:
                    st.markdown("### المشكلات المكتشفة:")
                    for i, issue in enumerate(issues, 1):
                        severity = issue.get("severity", "medium")
                        card_class = "error-card" if severity == "high" else "warning-card"
                        st.markdown(f'<div class="{card_class}"><strong>المشكلة {i}: {issue.get("field_1","")} vs {issue.get("field_2","")}</strong><br>{issue.get("description","")}<br><em>الاقتراح: {issue.get("suggestion","")}</em></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="success-card"><strong>لم يتم اكتشاف اي تناقضات - البيانات متسقة ومنطقية</strong></div>', unsafe_allow_html=True)

                if "history" not in st.session_state:
                    st.session_state.history = []
                st.session_state.history.append({"time": datetime.now().strftime("%H:%M:%S"), "score": score, "issues": len(issues), "status": status})
            except Exception as e:
                st.error(f"خطا: {str(e)}")
```

with tab2:
st.markdown(”### سجلات اختبار جاهزة”)
test_records = [
{“Age”: 19, “Education”: “PhD”, “Job Title”: “Specialist Doctor”, “Years Experience”: 15, “Employment Status”: “Private Sector”, “Salary”: 25000, “Marital Status”: “Married”, “Children”: 5, “Nationality”: “Saudi”, “Native Language”: “English”},
{“Age”: 35, “Education”: “Bachelor”, “Job Title”: “Truck Driver”, “Years Experience”: 10, “Employment Status”: “Unemployed”, “Salary”: 8000, “Marital Status”: “Single”, “Children”: 4, “Nationality”: “Saudi”, “Native Language”: “Arabic”},
{“Age”: 45, “Education”: “Engineering Bachelor”, “Job Title”: “Civil Engineer”, “Years Experience”: 20, “Employment Status”: “Government”, “Salary”: 18000, “Marital Status”: “Married”, “Children”: 3, “Nationality”: “Saudi”, “Native Language”: “Arabic”}
]
labels = [“سجل 1: عمر 19 + دكتوراه + 15 سنة خبرة (اخطاء متعددة)”, “سجل 2: غير موظف + راتب 8000 (تناقض)”, “سجل 3: مهندس سليم (لا اخطاء)”]
selected_idx = st.selectbox(“اختر سجلا:”, range(len(labels)), format_func=lambda i: labels[i])
selected_record = test_records[selected_idx]
cols = st.columns(3)
for i, (k, v) in enumerate(selected_record.items()):
cols[i % 3].info(f”**{k}:** {v}”)

```
if st.button("فحص هذا السجل", use_container_width=True):
    if not api_key:
        st.error("الرجاء ادخال OpenAI API Key")
    else:
        with st.spinner("جاري التحليل..."):
            try:
                result = analyze_form(api_key, selected_record)
                st.session_state.total_forms += 1
                score = result.get("confidence_score", 0)
                issues = result.get("issues", [])
                color = "#38a169" if score >= 80 else "#d69e2e" if score >= 60 else "#e53e3e"
                st.markdown(f'<div style="background:{color}22;border:3px solid {color};padding:20px;border-radius:15px;text-align:center;margin:20px 0"><h2 style="color:{color}">درجة الثقة: {score}/100</h2><p>{result.get("summary","")}</p></div>', unsafe_allow_html=True)
                if issues:
                    st.session_state.errors_found += len(issues)
                    st.markdown(f"### تم اكتشاف {len(issues)} مشكلة:")
                    for issue in issues:
                        severity = issue.get("severity", "medium")
                        card_class = "error-card" if severity == "high" else "warning-card"
                        st.markdown(f'<div class="{card_class}"><strong>{issue.get("field_1","")} vs {issue.get("field_2","")}</strong><br>{issue.get("description","")}<br><em>الاقتراح: {issue.get("suggestion","")}</em></div>', unsafe_allow_html=True)
                else:
                    st.success("لا توجد تناقضات في هذا السجل")
            except Exception as e:
                st.error(f"خطا: {str(e)}")
```

with tab3:
st.markdown(”### لوحة متابعة جودة البيانات”)
col1, col2, col3, col4 = st.columns(4)
col1.metric(“اجمالي الاستمارات”, st.session_state.total_forms)
col2.metric(“اخطاء مكتشفة”, st.session_state.errors_found)
col3.metric(“استمارات نظيفة”, st.session_state.clean_forms)
error_rate = round((st.session_state.errors_found / max(st.session_state.total_forms, 1)) * 100, 1)
col4.metric(“معدل الخطا”, f”{error_rate}%”)
if “history” in st.session_state and st.session_state.history:
import pandas as pd
df = pd.DataFrame(st.session_state.history)
st.dataframe(df, use_container_width=True)
st.line_chart(df[“score”])
else:
st.info(“ابدا بفحص استمارات لعرض الاحصائيات”)

st.markdown(”—”)
st.markdown(”<div style='text-align:center;color:#999;padding:10px'>Smart Semantic Guardian - GASTAT Hackathon 2026</div>”, unsafe_allow_html=True)
