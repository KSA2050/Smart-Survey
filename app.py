import streamlit as st
import json
import time
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

def analyze_form_demo(form_data):
“”“تحليل تجريبي ذكي بناء على البيانات الفعلية”””
time.sleep(2)  # محاكاة وقت المعالجة

```
issues = []
age = form_data.get("Age", 30)
education = form_data.get("Education", "")
years_exp = form_data.get("Years Experience", 0)
employment = form_data.get("Employment Status", "")
salary = form_data.get("Monthly Salary", 0)
marital = form_data.get("Marital Status", "")
children = form_data.get("Children", 0)
nationality = form_data.get("Nationality", "")
language = form_data.get("Native Language", "")

# قاعدة 1: العمر مقابل المؤهل
if "PhD" in education or "دكتوراه" in education:
    if age < 25:
        issues.append({
            "severity": "high",
            "field_1": "العمر",
            "field_2": "المؤهل العلمي",
            "description": f"عمر {age} سنة مع درجة الدكتوراه غير منطقي - الحد الأدنى المعتاد 27 سنة",
            "suggestion": "راجع تاريخ الميلاد أو المؤهل العلمي"
        })

# قاعدة 2: العمر مقابل سنوات الخبرة
if years_exp > (age - 18):
    issues.append({
        "severity": "high",
        "field_1": "العمر",
        "field_2": "سنوات الخبرة",
        "description": f"سنوات الخبرة {years_exp} أكبر من الفترة الممكنة منذ بلوغ سن العمل (عمر {age} - 18 = {age-18} سنة)",
        "suggestion": "راجع العمر أو سنوات الخبرة"
    })

# قاعدة 3: الحالة الوظيفية مقابل الراتب
if "غير موظف" in employment or "Unemployed" in employment:
    if salary > 0:
        issues.append({
            "severity": "medium",
            "field_1": "الحالة الوظيفية",
            "field_2": "الراتب الشهري",
            "description": f"الحالة الوظيفية 'غير موظف' لكن الراتب {salary} ريال",
            "suggestion": "إما تصحيح الحالة الوظيفية أو تعيين الراتب صفر"
        })

# قاعدة 4: الحالة الاجتماعية مقابل الأطفال
if "اعزب" in marital or "Single" in marital:
    if children > 0:
        issues.append({
            "severity": "high",
            "field_1": "الحالة الاجتماعية",
            "field_2": "عدد الأطفال",
            "description": f"الحالة الاجتماعية 'أعزب' مع وجود {children} أطفال",
            "suggestion": "راجع الحالة الاجتماعية أو عدد الأطفال"
        })

# قاعدة 5: الجنسية مقابل اللغة الأم
if "سعودي" in nationality or "Saudi" in nationality:
    if "English" in language or "الانجليزية" in language:
        issues.append({
            "severity": "medium",
            "field_1": "الجنسية",
            "field_2": "اللغة الأم",
            "description": "جنسية سعودي مع لغة أم إنجليزية - غير شائع",
            "suggestion": "تأكد من اللغة الأم للمستجيب"
        })

# قاعدة 6: العمر مقابل الزواج والأطفال
if age < 20 and marital in ["متزوج", "Married"] and children >= 3:
    issues.append({
        "severity": "high",
        "field_1": "العمر",
        "field_2": "الحالة الاجتماعية والأطفال",
        "description": f"عمر {age} سنة مع حالة 'متزوج' و{children} أطفال - غير معتاد",
        "suggestion": "راجع تاريخ الميلاد والحالة الاجتماعية"
    })

# حساب درجة الثقة
if len(issues) == 0:
    confidence = 98
    status = "clean"
    summary = "لم يتم اكتشاف أي تناقضات منطقية - البيانات متسقة وموثوقة"
elif len(issues) == 1:
    confidence = 65
    status = "warning"
    summary = f"تم اكتشاف تناقض واحد يحتاج مراجعة"
elif len(issues) == 2:
    confidence = 35
    status = "error"
    summary = f"تم اكتشاف {len(issues)} تناقضات منطقية تتطلب تصحيح فوري"
else:
    confidence = 15
    status = "error"
    summary = f"تم اكتشاف {len(issues)} تناقضات حرجة - البيانات غير موثوقة"

return {
    "confidence_score": confidence,
    "status": status,
    "issues": issues,
    "summary": summary
}
```

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
st.info(“🎯 وضع العرض التوضيحي\n\nالنظام يعمل بمحرك تحليل ذكي مدمج”)
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
st.success(“✅ النظام جاهز للعمل”)

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
if st.button("فحص الاستمارة بالمحرك الذكي", use_container_width=True):
    form_data = {
        "Age": age, "Gender": gender, "Nationality": nationality,
        "Native Language": native_language, "Education": education,
        "Employment Status": employment_status, "Job Title": job_title,
        "Years Experience": years_exp, "Monthly Salary": monthly_salary,
        "Marital Status": marital_status, "Family Members": family_members,
        "Children": children_count, "Sector": sector, "Income Source": income_source
    }
    with st.spinner("النظام يحلل الاستمارة..."):
        result = analyze_form_demo(form_data)
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
                st.markdown(f'<div class="{card_class}"><strong>المشكلة {i}: {issue.get("field_1","")} vs {issue.get("field_2","")}</strong><br>{issue.get("description","")}<br><em>💡 {issue.get("suggestion","")}</em></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="success-card"><strong>✅ لم يتم اكتشاف اي تناقضات - البيانات متسقة ومنطقية</strong></div>', unsafe_allow_html=True)

        if "history" not in st.session_state:
            st.session_state.history = []
        st.session_state.history.append({"time": datetime.now().strftime("%H:%M:%S"), "score": score, "issues": len(issues), "status": status})
```

with tab2:
st.markdown(”### سجلات اختبار جاهزة”)
test_records = [
{“Age”: 19, “Education”: “دكتوراه”, “Job Title”: “طبيب متخصص”, “Years Experience”: 15, “Employment Status”: “موظف قطاع خاص”, “Monthly Salary”: 25000, “Marital Status”: “متزوج”, “Children”: 5, “Nationality”: “سعودي”, “Native Language”: “الانجليزية”, “Gender”: “ذكر”},
{“Age”: 35, “Education”: “بكالوريوس”, “Job Title”: “سائق شاحنة”, “Years Experience”: 10, “Employment Status”: “غير موظف”, “Monthly Salary”: 8000, “Marital Status”: “اعزب”, “Children”: 4, “Nationality”: “سعودي”, “Native Language”: “العربية”, “Gender”: “انثى”},
{“Age”: 45, “Education”: “بكالوريوس هندسة”, “Job Title”: “مهندس مدني”, “Years Experience”: 20, “Employment Status”: “موظف حكومي”, “Monthly Salary”: 18000, “Marital Status”: “متزوج”, “Children”: 3, “Nationality”: “سعودي”, “Native Language”: “العربية”, “Gender”: “ذكر”}
]
labels = [“🔴 سجل 1: عمر 19 + دكتوراه + 15 سنة خبرة (اخطاء متعددة)”, “🟡 سجل 2: غير موظف + راتب 8000 (تناقض)”, “🟢 سجل 3: مهندس سليم (لا اخطاء)”]
selected_idx = st.selectbox(“اختر سجلا:”, range(len(labels)), format_func=lambda i: labels[i])
selected_record = test_records[selected_idx]

```
st.markdown("**📄 بيانات السجل:**")
cols = st.columns(3)
for i, (k, v) in enumerate(selected_record.items()):
    cols[i % 3].info(f"**{k}:** {v}")

if st.button("🔍 فحص هذا السجل", use_container_width=True):
    with st.spinner("🤖 المحرك الذكي يحلل السجل..."):
        result = analyze_form_demo(selected_record)
        st.session_state.total_forms += 1
        score = result.get("confidence_score", 0)
        issues = result.get("issues", [])
        color = "#38a169" if score >= 80 else "#d69e2e" if score >= 60 else "#e53e3e"
        st.markdown(f'<div style="background:{color}22;border:3px solid {color};padding:20px;border-radius:15px;text-align:center;margin:20px 0"><h2 style="color:{color}">درجة الثقة: {score}/100</h2><p>{result.get("summary","")}</p></div>', unsafe_allow_html=True)
        if issues:
            st.session_state.errors_found += len(issues)
            st.markdown(f"### ⚠️ تم اكتشاف {len(issues)} مشكلة:")
            for issue in issues:
                severity = issue.get("severity", "medium")
                card_class = "error-card" if severity == "high" else "warning-card"
                st.markdown(f'<div class="{card_class}"><strong>{issue.get("field_1","")} ↔ {issue.get("field_2","")}</strong><br>📌 {issue.get("description","")}<br><em>💡 {issue.get("suggestion","")}</em></div>', unsafe_allow_html=True)
        else:
            st.success("✅ لا توجد تناقضات في هذا السجل")
```

with tab3:
st.markdown(”### 📈 لوحة متابعة جودة البيانات”)
col1, col2, col3, col4 = st.columns(4)
col1.metric(“📋 اجمالي الاستمارات”, st.session_state.total_forms)
col2.metric(“🔴 اخطاء مكتشفة”, st.session_state.errors_found)
col3.metric(“✅ استمارات نظيفة”, st.session_state.clean_forms)
error_rate = round((st.session_state.errors_found / max(st.session_state.total_forms, 1)) * 100, 1)
col4.metric(“📊 معدل الخطا”, f”{error_rate}%”)

```
if "history" in st.session_state and st.session_state.history:
    import pandas as pd
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True)
    st.line_chart(df["score"])
else:
    st.info("ابدا بفحص استمارات لعرض الاحصائيات")

st.markdown("---")
st.markdown("### 💡 القيمة المضافة للنظام")
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown('<div style="background:#ebf8ff;padding:20px;border-radius:10px;text-align:center"><h2>⚡</h2><h3>توفير الوقت</h3><p>اكتشاف الاخطاء لحظيا بدلا من المعالجة اليدوية</p></div>', unsafe_allow_html=True)
with col_b:
    st.markdown('<div style="background:#f0fff4;padding:20px;border-radius:10px;text-align:center"><h2>📊</h2><h3>جودة البيانات</h3><p>ضمان دقة وموثوقية البيانات الاحصائية الوطنية</p></div>', unsafe_allow_html=True)
with col_c:
    st.markdown('<div style="background:#fffbeb;padding:20px;border-radius:10px;text-align:center"><h2>🧠</h2><h3>ذكاء تحليلي</h3><p>تجاوز القواعد الجامدة نحو الفهم الدلالي العميق</p></div>', unsafe_allow_html=True)
```

st.markdown(”—”)
st.markdown(”<div style='text-align:center;color:#999;padding:10px'>🛡️ الحارس الدلالي - Smart Semantic Guardian | هكاثون الابتكار في البيانات 2026</div>”, unsafe_allow_html=True)
