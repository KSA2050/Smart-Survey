import streamlit as st
import time
from datetime import datetime
import pandas as pd

# OpenAI (AI Mode)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False


# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Smart Semantic Guardian | الحارس الدلالي",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------
# CSS
# ---------------------------
st.markdown(
    """
<style>
body {
    background: #f7fafc;
}
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
""",
    unsafe_allow_html=True,
)

# ---------------------------
# Session State init
# ---------------------------
if "total_forms" not in st.session_state:
    st.session_state.total_forms = 0
if "errors_found" not in st.session_state:
    st.session_state.errors_found = 0
if "clean_forms" not in st.session_state:
    st.session_state.clean_forms = 0
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------
# System Prompt (AI Mode)
# ---------------------------
SYSTEM_PROMPT = """You are a smart semantic validator for Arabic statistical survey forms.
Analyze the form data and detect logical/semantic contradictions between fields.

Look for contradictions like:
1. Age vs education level (e.g. age 19 with PhD)
2. Age vs years of experience (e.g. age 22 with 25 years experience)
3. Employment status vs salary (e.g. unemployed with salary 10000)
4. Marital status vs number of children (e.g. single with 4 children)
5. Nationality vs native language contradictions
6. Job title vs gender contradictions
7. Any other logical inconsistency

Always respond with JSON only in this exact format:
{
  "confidence_score": <number 0-100>,
  "status": "<clean or warning or error>",
  "issues": [
    {
      "severity": "<high or medium or low>",
      "field_1": "<field name in Arabic>",
      "field_2": "<field name in Arabic>",
      "description": "<description in Arabic>",
      "suggestion": "<correction suggestion in Arabic>"
    }
  ],
  "summary": "<short summary in Arabic>"
}

If no issues found, return empty issues array, status: clean, score: 95-100
"""

# ---------------------------
# Demo Engine (Fallback)
# ---------------------------
def analyze_form_demo(form_data: dict) -> dict:
    """تحليل تجريبي ذكي بناء على البيانات الفعلية"""
    time.sleep(1.1)  # محاكاة وقت المعالجة

    issues = []
    age = int(form_data.get("Age", 30))
    education = str(form_data.get("Education", ""))
    years_exp = int(form_data.get("Years Experience", 0))
    employment = str(form_data.get("Employment Status", ""))
    salary = int(form_data.get("Monthly Salary", 0))
    marital = str(form_data.get("Marital Status", ""))
    children = int(form_data.get("Children", 0))
    nationality = str(form_data.get("Nationality", ""))
    language = str(form_data.get("Native Language", ""))

    # قاعدة 1: العمر مقابل المؤهل
    if ("PhD" in education) or ("دكتوراه" in education):
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
    if ("غير موظف" in employment) or ("Unemployed" in employment):
        if salary > 0:
            issues.append({
                "severity": "medium",
                "field_1": "الحالة الوظيفية",
                "field_2": "الراتب الشهري",
                "description": f"الحالة الوظيفية 'غير موظف' لكن الراتب {salary} ريال",
                "suggestion": "إما تصحيح الحالة الوظيفية أو تعيين الراتب صفر"
            })

    # قاعدة 4: الحالة الاجتماعية مقابل الأطفال
    if ("اعزب" in marital) or ("أعزب" in marital) or ("Single" in marital):
        if children > 0:
            issues.append({
                "severity": "high",
                "field_1": "الحالة الاجتماعية",
                "field_2": "عدد الأطفال",
                "description": f"الحالة الاجتماعية 'أعزب' مع وجود {children} أطفال",
                "suggestion": "راجع الحالة الاجتماعية أو عدد الأطفال"
            })

    # قاعدة 5: الجنسية مقابل اللغة الأم
    if ("سعودي" in nationality) or ("Saudi" in nationality):
        if ("English" in language) or ("الانجليزية" in language) or ("الإنجليزية" in language):
            issues.append({
                "severity": "medium",
                "field_1": "الجنسية",
                "field_2": "اللغة الأم",
                "description": "جنسية سعودي مع لغة أم إنجليزية - غير شائع",
                "suggestion": "تأكد من اللغة الأم للمستجيب"
            })

    # قاعدة 6: العمر مقابل الزواج والأطفال
    if (age < 20) and (marital in ["متزوج", "Married"]) and (children >= 3):
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
        summary = "تم اكتشاف تناقض واحد يحتاج مراجعة"
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

# ---------------------------
# AI Engine
# ---------------------------
def analyze_form_ai(api_key: str, form_data: dict) -> dict:
    if not OPENAI_AVAILABLE:
        raise RuntimeError("OpenAI library not available in this environment.")

    client = OpenAI(api_key=api_key)

    # Keep zeros; filter only None/empty string
    form_text = "\n".join([f"- {k}: {v}" for k, v in form_data.items() if v is not None and v != ""])
    user_message = (
        "Analyze this Arabic survey form for logical contradictions:\n\n"
        f"{form_text}\n\n"
        "Respond with JSON only."
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.1,
        max_tokens=900,
    )

    raw = (response.choices[0].message.content or "").strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    import json
    return json.loads(raw)

# ---------------------------
# Unified: AI then fallback to Demo
# ---------------------------
def analyze_form_with_fallback(api_key: str, form_data: dict):
    # no key -> demo
    if not api_key:
        return analyze_form_demo(form_data), "demo"

    try:
        result = analyze_form_ai(api_key, form_data)
        return result, "ai"
    except Exception as e:
        msg = str(e).lower()

        quota_signals = [
            "insufficient_quota",
            "exceeded your current quota",
            "billing",
            "payment",
            "error code: 429",
            "429",
        ]

        # Any quota/billing/429 -> demo
        if any(s in msg for s in quota_signals):
            return analyze_form_demo(form_data), "demo"

        # Any other error -> demo (حتى ما يوقف التطبيق)
        return analyze_form_demo(form_data), "demo"

# ---------------------------
# Header
# ---------------------------
st.markdown(
    """
<div class="main-header">
    <h1>Smart Semantic Guardian</h1>
    <h2 style="color:#93c5fd">الحارس الدلالي</h2>
    <p>نظام ذكي للتحقق من جودة البيانات الاحصائية لحظيا</p>
    <small>هكاثون الابتكار في البيانات - الهيئة العامة للاحصاء 2026</small>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------
# Sidebar (API Key optional)
# ---------------------------
with st.sidebar:
    st.markdown("## الإعدادات")

    # Prefer secrets if exists
    secret_key = ""
    try:
        secret_key = st.secrets.get("OPENAI_API_KEY", "")
    except Exception:
        secret_key = ""

    api_key_input = st.text_input("OpenAI API Key (اختياري)", type="password", placeholder="sk-...")

    api_key = api_key_input.strip() if api_key_input else (secret_key.strip() if secret_key else "")

    st.markdown("---")
    st.markdown("### وضع التشغيل الحالي")
    if api_key and OPENAI_AVAILABLE:
        st.success("🟢 AI متاح (إذا كان الرصيد مفعّل)")
        st.caption("إذا انتهى الرصيد سيتم التحويل تلقائياً إلى Demo.")
    else:
        st.info("🟡 Demo فقط (لا يوجد مفتاح أو مكتبة OpenAI غير متوفرة)")

    st.markdown("---")
    st.markdown("### احصائيات الجلسة")
    col1, col2 = st.columns(2)
    col1.metric("استمارات", st.session_state.total_forms)
    col2.metric("اخطاء", st.session_state.errors_found)

    st.markdown("---")
    st.caption("✅ التطبيق يعمل حتى بدون رصيد عبر Fallback تلقائي.")

# ---------------------------
# Tabs
# ---------------------------
tab1, tab2, tab3 = st.tabs(["الاستمارة التفاعلية", "سجلات اختبار", "لوحة التحكم"])

# ===========================
# Tab 1: Interactive Form
# ===========================
with tab1:
    st.markdown("### استمارة مسح سوق العمل")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### البيانات الشخصية")
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
        monthly_salary = st.number_input("الراتب الشهري ريال", min_value=0, max_value=100000, value=0, step=500)

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
        income_source = st.selectbox("مصدر الدخل", ["راتب", "اعمال حرة", "استثمارات", "لا يوجد"])

    st.markdown("---")

    if st.button("فحص الاستمارة (AI مع Fallback)", use_container_width=True):
        form_data = {
            "Age": age,
            "Gender": gender,
            "Nationality": nationality,
            "Native Language": native_language,
            "Education": education,
            "Employment Status": employment_status,
            "Job Title": job_title,
            "Years Experience": years_exp,
            "Monthly Salary": monthly_salary,
            "Marital Status": marital_status,
            "Family Members": family_members,
            "Children": children_count,
            "Sector": sector,
            "Income Source": income_source,
        }

        with st.spinner("النظام يحلل الاستمارة..."):
            result, mode = analyze_form_with_fallback(api_key, form_data)

        # mode banner
        if mode == "ai":
            st.success("✅ تم التحليل بواسطة الذكاء الاصطناعي (AI).")
        else:
            st.warning("⚠️ تم التحويل تلقائياً إلى وضع العرض التوضيحي (Demo) بسبب عدم توفر رصيد/فوترة أو تعذر الاتصال.")

        st.session_state.total_forms += 1

        score = int(result.get("confidence_score", 0))
        status = result.get("status", "error")
        issues = result.get("issues", [])

        if issues:
            st.session_state.errors_found += len(issues)
        else:
            st.session_state.clean_forms += 1

        st.session_state.history.append(
            {
                "time": datetime.now().strftime("%H:%M:%S"),
                "score": score,
                "issues": len(issues),
                "status": status,
                "mode": mode,
            }
        )

        st.markdown("---")
        st.markdown("## نتائج الفحص")

        col_s1, col_s2, col_s3 = st.columns(3)
        color = "#38a169" if score >= 80 else "#d69e2e" if score >= 60 else "#e53e3e"

        with col_s1:
            st.markdown(
                f'<div class="score-box" style="background:{color}22;border:3px solid {color}">'
                f'<div style="color:{color}">{score}</div>'
                f'<div style="font-size:1rem;color:#666">درجة الثقة</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        with col_s2:
            st.markdown(
                f'<div class="score-box" style="background:#ebf8ff;border:3px solid #3182ce">'
                f'<div style="color:#3182ce">{len(issues)}</div>'
                f'<div style="font-size:1rem;color:#666">مشكلة مكتشفة</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        with col_s3:
            status_map = {"clean": ("نظيفة", "#38a169"), "warning": ("تحذير", "#d69e2e"), "error": ("اخطاء", "#e53e3e")}
            s_text, s_color = status_map.get(status, ("غير محدد", "#666"))
            st.markdown(
                f'<div class="score-box" style="background:{s_color}22;border:3px solid {s_color}">'
                f'<div style="color:{s_color};font-size:2rem">{s_text}</div>'
                f'<div style="font-size:1rem;color:#666">الحالة</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown(f"**الملخص:** {result.get('summary','')}")

        if issues:
            st.markdown("### المشكلات المكتشفة:")
            for i, issue in enumerate(issues, 1):
                severity = issue.get("severity", "medium")
                card_class = "error-card" if severity == "high" else "warning-card"
                st.markdown(
                    f'<div class="{card_class}">'
                    f'<strong>المشكلة {i}: {issue.get("field_1","")} vs {issue.get("field_2","")}</strong><br>'
                    f'{issue.get("description","")}<br>'
                    f'<em>💡 {issue.get("suggestion","")}</em>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                '<div class="success-card"><strong>✅ لم يتم اكتشاف أي تناقضات - البيانات متسقة ومنطقية</strong></div>',
                unsafe_allow_html=True,
            )

# ===========================
# Tab 2: Test Records
# ===========================
with tab2:
    st.markdown("### سجلات اختبار جاهزة")

    test_records = [
        {
            "Age": 19, "Education": "دكتوراه", "Job Title": "طبيب متخصص", "Years Experience": 15,
            "Employment Status": "موظف قطاع خاص", "Monthly Salary": 25000, "Marital Status": "متزوج",
            "Children": 5, "Nationality": "سعودي", "Native Language": "الانجليزية", "Gender": "ذكر"
        },
        {
            "Age": 35, "Education": "بكالوريوس", "Job Title": "سائق شاحنة", "Years Experience": 10,
            "Employment Status": "غير موظف", "Monthly Salary": 8000, "Marital Status": "اعزب",
            "Children": 4, "Nationality": "سعودي", "Native Language": "العربية", "Gender": "انثى"
        },
        {
            "Age": 45, "Education": "بكالوريوس هندسة", "Job Title": "مهندس مدني", "Years Experience": 20,
            "Employment Status": "موظف حكومي", "Monthly Salary": 18000, "Marital Status": "متزوج",
            "Children": 3, "Nationality": "سعودي", "Native Language": "العربية", "Gender": "ذكر"
        }
    ]

    labels = [
        "🔴 سجل 1: عمر 19 + دكتوراه + 15 سنة خبرة (اخطاء متعددة)",
        "🟡 سجل 2: غير موظف + راتب 8000 (تناقض)",
        "🟢 سجل 3: مهندس سليم (لا اخطاء)"
    ]

    selected_idx = st.selectbox("اختر سجلا:", range(len(labels)), format_func=lambda i: labels[i])
    selected_record = test_records[selected_idx]

    st.markdown("**📄 بيانات السجل:**")
    cols = st.columns(3)
    for i, (k, v) in enumerate(selected_record.items()):
        cols[i % 3].info(f"**{k}:** {v}")

    if st.button("🔍 فحص هذا السجل (AI مع Fallback)", use_container_width=True):
        with st.spinner("🤖 جاري التحليل..."):
            result, mode = analyze_form_with_fallback(api_key, selected_record)

        if mode == "ai":
            st.success("✅ تم التحليل بواسطة الذكاء الاصطناعي (AI).")
        else:
            st.warning("⚠️ تم التحويل تلقائياً إلى Demo بسبب عدم توفر رصيد/فوترة أو تعذر الاتصال.")

        st.session_state.total_forms += 1

        score = int(result.get("confidence_score", 0))
        issues = result.get("issues", [])

        if issues:
            st.session_state.errors_found += len(issues)
        else:
            st.session_state.clean_forms += 1

        st.session_state.history.append(
            {
                "time": datetime.now().strftime("%H:%M:%S"),
                "score": score,
                "issues": len(issues),
                "status": result.get("status", "clean"),
                "mode": mode,
            }
        )

        color = "#38a169" if score >= 80 else "#d69e2e" if score >= 60 else "#e53e3e"
        st.markdown(
            f'<div style="background:{color}22;border:3px solid {color};padding:20px;border-radius:15px;text-align:center;margin:20px 0">'
            f'<h2 style="color:{color}">درجة الثقة: {score}/100</h2>'
            f'<p>{result.get("summary","")}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

        if issues:
            st.markdown(f"### ⚠️ تم اكتشاف {len(issues)} مشكلة:")
            for issue in issues:
                severity = issue.get("severity", "medium")
                card_class = "error-card" if severity == "high" else "warning-card"
                st.markdown(
                    f'<div class="{card_class}"><strong>{issue.get("field_1","")} ↔ {issue.get("field_2","")}</strong><br>'
                    f'📌 {issue.get("description","")}<br><em>💡 {issue.get("suggestion","")}</em></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.success("✅ لا توجد تناقضات في هذا السجل")

# ===========================
# Tab 3: Dashboard
# ===========================
with tab3:
    st.markdown("### 📈 لوحة متابعة جودة البيانات")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📋 اجمالي الاستمارات", st.session_state.total_forms)
    col2.metric("🔴 اخطاء مكتشفة", st.session_state.errors_found)
    col3.metric("✅ استمارات نظيفة", st.session_state.clean_forms)
    error_rate = round((st.session_state.errors_found / max(st.session_state.total_forms, 1)) * 100, 1)
    col4.metric("📊 معدل الخطا", f"{error_rate}%")

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, use_container_width=True)
        if "score" in df.columns:
            st.line_chart(df["score"])
    else:
        st.info("ابدأ بفحص استمارات لعرض الاحصائيات")

st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#999;padding:10px'>🛡️ الحارس الدلالي - Smart Semantic Guardian | هكاثون الابتكار في البيانات 2026</div>",
    unsafe_allow_html=True,
)
