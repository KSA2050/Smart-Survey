import streamlit as st
import openai
import json
from datetime import datetime

st.set_page_config(
page_title=“Smart Guardian | الحارس الدلالي”,
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
.score-box {
    text-align: center;
    padding: 25px;
    border-radius: 15px;
    font-size: 3rem;
    font-weight: 900;
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
“confidence_score”: <number 0-100>,
“status”: “<clean or warning or error>”,
“issues”: [
{
“severity”: “<high or medium or low>”,
“field_1”: “<field name in Arabic>”,
“field_2”: “<field name in Arabic>”,
“description”: “<description in Arabic>”,
“suggestion”: “<correction suggestion in Arabic>”
}
],
“summary”: “<short summary in Arabic>”
}

If no issues found, return empty issues array, status: clean, score: 95-100”””

def analyze_form(api_key, form_data):
client = openai.OpenAI(api_key=api_key)
form_text = “\n”.join([f”- {k}: {v}” for k, v in form_data.items() if v])
user_message = f”Analyze this Arabic survey form for logical contradictions:\n\n{form_text}\n\nRespond with JSON only.”

```
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ],
    temperature=0.1,
    max_tokens=1000
)
raw = response.choices[0].message.content.strip()
raw = raw.replace("```json", "").replace("```", "").strip()
return json.loads(raw)
```

# Header

st.markdown(”””

<div class="main-header">
    <h1>الحارس الدلالي - Smart Semantic Guardian</h1>
    <p>نظام ذكي للتحقق من جودة البيانات الاحصائية لحظيا</p>
    <small>هكاثون الابتكار في البيانات | الهيئة العامة للاحصاء 2026</small>
</div>
""", unsafe_allow_html=True)

# Sidebar

with st.sidebar:
st.markdown(”## الاعدادات”)
api_key = st.text_input(“OpenAI API Key”, type=“password”, placeholder=“sk-…”)

```
st.markdown("---")
st.markdown("### احصائيات الجلسة")
if "total_forms" not in st.session_state:
    st.session_state.total_forms = 0
    st.session_state.errors_found = 0
    st.session_state.clean_forms = 0

col1, col2 = st.columns(2)
col1.metric("استمارات فحصت", st.session_state.total_forms)
col2.metric("اخطاء اكتشفت", st.session_state.errors_found)

st.markdown("---")
st.info("يقوم النظام بتحليل اجاباتك لحظيا باستخدام الذكاء الاصطناعي للكشف عن التناقضات المنطقية قبل حفظ البيانات.")
```

# Tabs

tab1, tab2, tab3 = st.tabs([“الاستمارة التفاعلية”, “اختبار سجلات جاهزة”, “لوحة التحكم”])

# Tab 1: Interactive Form

with tab1:
st.markdown(”### استمارة مسح سوق العمل”)
st.markdown(“ادخل البيانات وسيقوم النظام بفحصها لحظيا”)

```
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### البيانات الشخصية")
    name = st.text_input("الاسم", placeholder="ادخل الاسم...")
    age = st.number_input("العمر", min_value=10, max_value=100, value=30)
    gender = st.selectbox("الجنس", ["ذكر", "انثى"])
    nationality = st.selectbox("الجنسية", ["سعودي", "مصري", "اردني", "هندي", "باكستاني", "اخرى"])
    native_language = st.selectbox("اللغة الام", ["العربية", "الانجليزية", "الاردية", "الهندية", "اخرى"])

with col2:
    st.markdown("#### البيانات المهنية")
    education = st.selectbox("المؤهل العلمي", ["اقل من ثانوي", "ثانوي", "دبلوم", "بكالوريوس", "ماجستير", "دكتوراه"])
    employment_status = st.selectbox("الحالة الوظيفية", ["موظف حكومي", "موظف قطاع خاص", "اعمال حرة", "غير موظف", "طالب", "متقاعد"])
    job_title = st.text_input("المسمى الوظيفي", placeholder="مثال: مهندس، طبيب...")
    years_exp = st.number_input("سنوات الخبرة", min_value=0, max_value=50, value=5)
    monthly_salary = st.number_input("الراتب الشهري (ريال)", min_value=0, max_value=100000, value=0, step=500)

col3, col4 = st.columns(2)
with col3:
    st.markdown("#### الحالة الاجتماعية")
    marital_status = st.selectbox("الحالة الاجتماعية", ["اعزب", "متزوج", "مطلق", "ارمل"])
    family_members = st.number_input("عدد افراد الاسرة", min_value=1, max_value=20, value=1)
    children_count = st.number_input("عدد الاطفال", min_value=0, max_value=15, value=0)

with col4:
    st.markdown("#### بيانات اضافية")
    region = st.selectbox("المنطقة", ["الرياض", "مكة المكرمة", "المدينة المنورة", "الشرقية", "اخرى"])
    sector = st.selectbox("القطاع", ["حكومي", "خاص", "غير ربحي", "لا ينطبق"])
    income_source = st.selectbox("مصدر الدخل الرئيسي", ["راتب", "اعمال حرة", "استثمارات", "لا يوجد"])

st.markdown("---")

if st.button("فحص الاستمارة بالذكاء الاصطناعي", use_container_width=True):
    if not api_key:
        st.error("الرجاء ادخال OpenAI API Key في الشريط الجانبي")
    else:
        form_data = {
            "العمر": age, "الجنس": gender, "الجنسية": nationality,
            "اللغة الام": native_language, "المؤهل العلمي": education,
            "الحالة الوظيفية": employment_status, "المسمى الوظيفي": job_title,
            "سنوات الخبرة": years_exp, "الراتب الشهري": monthly_salary,
            "الحالة الاجتماعية": marital_status, "عدد افراد الاسرة": family_members,
            "عدد الاطفال": children_count, "القطاع": sector, "مصدر الدخل": income_source
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
                    st.markdown(f"""<div class="score-box" style="background:{color}22; border:3px solid {color}">
                        <div style="color:{color}">{score}</div>
                        <div style="font-size:1rem;color:#666">درجة الثقة</div>
                    </div>""", unsafe_allow_html=True)
                
                with col_s2:
                    st.markdown(f"""<div class="score-box" style="background:#ebf8ff;border:3px solid #3182ce">
                        <div style="color:#3182ce">{len(issues)}</div>
                        <div style="font-size:1rem;color:#666">مشكلة مكتشفة</div>
                    </div>""", unsafe_allow_html=True)
                
                with col_s3:
                    status_map = {"clean": ("نظيفة", "#38a169"), "warning": ("تحذير", "#d69e2e"), "error": ("اخطاء", "#e53e3e")}
                    s_text, s_color = status_map.get(status, ("غير محدد", "#666"))
                    st.markdown(f"""<div class="score-box" style="background:{s_color}22;border:3px solid {s_color}">
                        <div style="color:{s_color};font-size:2rem">{s_text}</div>
                        <div style="font-size:1rem;color:#666">الحالة</div>
                    </div>""", unsafe_allow_html=True)
                
                st.markdown(f"**الملخص:** {result.get('summary', '')}")
                
                if issues:
                    st.markdown("### المشكلات المكتشفة:")
                    for i, issue in enumerate(issues, 1):
                        severity = issue.get("severity", "medium")
                        card_class = "error-card" if severity == "high" else "warning-card"
                        icon = "عالي" if severity == "high" else "متوسط"
                        st.markdown(f"""<div class="{card_class}">
                            <strong>المشكلة {i} [{icon}]: {issue.get('field_1','')} vs {issue.get('field_2','')}</strong><br>
                            {issue.get('description','')}<br>
                            <em>الاقتراح: {issue.get('suggestion','')}</em>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.markdown("""<div class="success-card">
                        <strong>لم يتم اكتشاف اي تناقضات! البيانات متسقة ومنطقية.</strong>
                    </div>""", unsafe_allow_html=True)
                
                if "history" not in st.session_state:
                    st.session_state.history = []
                st.session_state.history.append({
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "score": score, "issues": len(issues), "status": status
                })
                
            except json.JSONDecodeError:
                st.error("خطا في تحليل رد النموذج. حاول مرة اخرى.")
            except Exception as e:
                st.error(f"خطا: {str(e)}")
```

# Tab 2: Test Records

with tab2:
st.markdown(”### اختبار سجلات من واقع العمل الميداني”)

```
test_records = [
    {"الاسم": "احمد محمد", "العمر": 19, "المؤهل العلمي": "دكتوراه",
     "المسمى الوظيفي": "طبيب متخصص", "سنوات الخبرة": 15,
     "الحالة الوظيفية": "موظف قطاع خاص", "الراتب الشهري": 25000,
     "الحالة الاجتماعية": "متزوج", "عدد الاطفال": 5,
     "الجنسية": "سعودي", "اللغة الام": "الانجليزية"},
    {"الاسم": "فاطمة علي", "العمر": 35, "المؤهل العلمي": "بكالوريوس",
     "المسمى الوظيفي": "سائق شاحنة", "سنوات الخبرة": 10,
     "الحالة الوظيفية": "غير موظف", "الراتب الشهري": 8000,
     "الحالة الاجتماعية": "اعزب", "عدد الاطفال": 4,
     "الجنسية": "سعودي", "اللغة الام": "العربية"},
    {"الاسم": "خالد السالم", "العمر": 45, "المؤهل العلمي": "بكالوريوس هندسة",
     "المسمى الوظيفي": "مهندس مدني", "سنوات الخبرة": 20,
     "الحالة الوظيفية": "موظف حكومي", "الراتب الشهري": 18000,
     "الحالة الاجتماعية": "متزوج", "عدد الاطفال": 3,
     "الجنسية": "سعودي", "اللغة الام": "العربية"}
]

labels = ["سجل 1: عمر 19 + دكتوراه + 15 سنة خبرة (اخطاء متعددة)",
          "سجل 2: غير موظف + راتب 8000 (تناقض)",
          "سجل 3: مهندس سليم (لا اخطاء)"]

selected_idx = st.selectbox("اختر سجلا للفحص:", range(len(labels)), format_func=lambda i: labels[i])
selected_record = test_records[selected_idx]

st.markdown("**بيانات السجل:**")
cols = st.columns(3)
for i, (k, v) in enumerate(selected_record.items()):
    cols[i % 3].info(f"**{k}:** {v}")

if st.button("فحص هذا السجل", use_container_width=True):
    if not api_key:
        st.error("الرجاء ادخال OpenAI API Key في الشريط الجانبي")
    else:
        with st.spinner("جاري التحليل..."):
            try:
                result = analyze_form(api_key, selected_record)
                st.session_state.total_forms += 1
                score = result.get("confidence_score", 0)
                issues = result.get("issues", [])
                
                color = "#38a169" if score >= 80 else "#d69e2e" if score >= 60 else "#e53e3e"
                st.markdown(f"""<div style="background:{color}22;border:3px solid {color};padding:20px;border-radius:15px;text-align:center;margin:20px 0">
                    <h2 style="color:{color}">درجة الثقة: {score}/100</h2>
                    <p>{result.get('summary','')}</p>
                </div>""", unsafe_allow_html=True)
                
                if issues:
                    st.session_state.errors_found += len(issues)
                    st.markdown(f"### تم اكتشاف {len(issues)} مشكلة:")
                    for issue in issues:
                        severity = issue.get("severity", "medium")
                        card_class = "error-card" if severity == "high" else "warning-card"
                        st.markdown(f"""<div class="{card_class}">
                            <strong>{issue.get('field_1','')} vs {issue.get('field_2','')}</strong><br>
                            {issue.get('description','')}<br>
                            <em>الاقتراح: {issue.get('suggestion','')}</em>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.success("لا توجد تناقضات في هذا السجل")
            except Exception as e:
                st.error(f"خطا: {str(e)}")
```

# Tab 3: Dashboard

with tab3:
st.markdown(”### لوحة متابعة جودة البيانات”)
col1, col2, col3, col4 = st.columns(4)
col1.metric(“اجمالي الاستمارات”, st.session_state.total_forms)
col2.metric(“اخطاء مكتشفة”, st.session_state.errors_found)
col3.metric(“استمارات نظيفة”, st.session_state.clean_forms)
error_rate = round((st.session_state.errors_found / max(st.session_state.total_forms, 1)) * 100, 1)
col4.metric(“معدل الخطا”, f”{error_rate}%”)

```
if "history" in st.session_state and st.session_state.history:
    import pandas as pd
    df = pd.DataFrame(st.session_state.history)
    df.columns = ["الوقت", "درجة الثقة", "المشاكل", "الحالة"]
    st.dataframe(df, use_container_width=True)
    st.line_chart(df["درجة الثقة"])
else:
    st.info("ابدا بفحص استمارات لعرض الاحصائيات هنا")

st.markdown("---")
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown("""<div style="background:#ebf8ff;padding:20px;border-radius:10px;text-align:center">
        <h3>توفير الوقت</h3><p>اكتشاف الاخطاء لحظيا بدلا من المعالجة اليدوية</p>
    </div>""", unsafe_allow_html=True)
with col_b:
    st.markdown("""<div style="background:#f0fff4;padding:20px;border-radius:10px;text-align:center">
        <h3>جودة البيانات</h3><p>ضمان دقة وموثوقية البيانات الاحصائية الوطنية</p>
    </div>""", unsafe_allow_html=True)
with col_c:
    st.markdown("""<div style="background:#fffbeb;padding:20px;border-radius:10px;text-align:center">
        <h3>ذكاء اصطناعي</h3><p>تجاوز القواعد الجامدة نحو الفهم الدلالي العميق</p>
    </div>""", unsafe_allow_html=True)
```

st.markdown(”—”)
st.markdown(”<div style='text-align:center;color:#999'>الحارس الدلالي | هكاثون الابتكار في البيانات | الهيئة العامة للاحصاء 2026</div>”, unsafe_allow_html=True)
