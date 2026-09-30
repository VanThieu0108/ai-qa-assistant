import os

import pandas as pd
import streamlit as st

from llm_helper import generate_test_cases, generate_bug_report
from test_runner import run_login_test

st.set_page_config(
    page_title="NVT_AI QA Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');

:root {
    --ink: #0F172A; --muted: #64748B; --line: #E2E8F0; --bg: #F4F6FB;
    --primary: #4F46E5; --primary-soft: #EEF2FF; --cyan: #06B6D4;
    --pass: #10B981; --pass-soft: #D1FAE5; --pass-ink: #047857;
    --fail: #EF4444; --fail-soft: #FEE2E2; --fail-ink: #B91C1C;
    --shadow: 0 1px 2px rgba(15,23,42,.04), 0 8px 24px rgba(15,23,42,.06);
}
html, body, .stApp, button, input, textarea, [class*="st-"] {
    font-family: 'Be Vietnam Pro', system-ui, sans-serif;
}
.stApp { background: var(--bg); }
.block-container { max-width: 1200px; padding-top: 1.5rem; padding-bottom: 4rem; }
header[data-testid="stHeader"] { background: transparent; }
footer, #MainMenu { visibility: hidden; }
h1, h2, h3, h4 { color: var(--ink); letter-spacing: -.01em; }

/* Hero */
.hero {
    position: relative; overflow: hidden; color: #fff;
    border-radius: 24px; padding: 2.6rem 2.6rem 2.2rem; margin-bottom: 1.25rem;
    background:
        radial-gradient(600px 240px at 90% -10%, rgba(6,182,212,.55), transparent 70%),
        radial-gradient(500px 260px at 0% 110%, rgba(129,140,248,.5), transparent 70%),
        linear-gradient(135deg, #1E1B4B 0%, #3730A3 55%, #4F46E5 100%);
    box-shadow: 0 20px 40px rgba(55,48,163,.25);
}
.hero::after {
    content: ""; position: absolute; inset: 0; pointer-events: none;
    background-image: radial-gradient(rgba(255,255,255,.14) 1px, transparent 1px);
    background-size: 22px 22px;
    mask-image: linear-gradient(120deg, transparent 30%, #000 100%);
    -webkit-mask-image: linear-gradient(120deg, transparent 30%, #000 100%);
}
.hero h1 { position: relative; z-index: 1; color: #fff; font-size: 2.3rem; font-weight: 800; line-height: 1.2; margin: 0 0 .6rem; padding: 0; max-width: 640px; }
.hero p { position: relative; z-index: 1; color: #C7D2FE; font-size: 1.05rem; margin: 0; max-width: 560px; }

/* Stepper */
.steps { display: grid; grid-template-columns: repeat(4, 1fr); gap: .75rem; margin-bottom: 1.5rem; }
.st-step { background: #fff; border: 1px solid var(--line); border-radius: 16px; padding: .9rem 1rem; display: flex; gap: .75rem; align-items: center; box-shadow: var(--shadow); }
.st-step .n { flex: 0 0 32px; height: 32px; border-radius: 10px; background: #F1F5F9; color: var(--muted); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: .9rem; }
.st-step b { display: block; color: var(--ink); font-size: .92rem; }
.st-step small { color: var(--muted); font-size: .78rem; }
.st-step.done .n { background: var(--pass-soft); color: var(--pass-ink); }
.st-step.next { border-color: #C7D2FE; }
.st-step.next .n { background: var(--primary); color: #fff; }
@media (max-width: 900px) { .steps { grid-template-columns: repeat(2, 1fr); } }

/* Tabs dạng viên thuốc */
.stTabs [data-baseweb="tab-list"] { gap: .25rem; background: #fff; padding: .35rem; border-radius: 14px; width: fit-content; border: 1px solid var(--line); box-shadow: var(--shadow); }
.stTabs [data-baseweb="tab"] { height: 42px; padding: 0 1.2rem; border-radius: 10px; color: var(--muted); font-weight: 500; }
.stTabs [aria-selected="true"] { background: var(--primary); color: #fff !important; font-weight: 600; }
.stTabs [aria-selected="true"] p { color: #fff !important; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.5rem; }

/* Thẻ */
[class*="st-key-card_"], [class*="st-key-box_"] {
    background: #fff; border: 1px solid var(--line); border-radius: 20px;
    padding: 1.5rem; box-shadow: var(--shadow);
}
.st-key-card_pass { border-top: 4px solid var(--pass); }
.st-key-card_fail { border-top: 4px solid var(--fail); }
.tag { display: inline-block; padding: .18rem .7rem; border-radius: 999px; font-size: .78rem; font-weight: 600; margin-bottom: .7rem; }
.tag.pass { background: var(--pass-soft); color: var(--pass-ink); }
.tag.fail { background: var(--fail-soft); color: var(--fail-ink); }
.card-title { font-size: 1.15rem; font-weight: 700; color: var(--ink); margin: 0 0 .3rem; }
.card-desc { color: var(--muted); font-size: .92rem; margin: 0 0 .9rem; }
.creds { background: #F8FAFC; border: 1px dashed #CBD5E1; border-radius: 10px; padding: .55rem .8rem; color: var(--ink); font-size: .84rem; margin-bottom: .5rem; font-family: ui-monospace, Menlo, Consolas, monospace; }

/* Số liệu */
.stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: .75rem; margin-bottom: 1.25rem; }
.stat { background: #fff; border: 1px solid var(--line); border-radius: 16px; padding: 1rem 1.2rem; box-shadow: var(--shadow); }
.stat .v { font-size: 1.9rem; font-weight: 800; color: var(--ink); line-height: 1.1; }
.stat .l { color: var(--muted); font-size: .85rem; margin-top: .15rem; }
.stat.pass .v { color: var(--pass-ink); }
.stat.fail .v { color: var(--fail-ink); }

/* Banner kết quả */
.banner { display: flex; gap: .9rem; align-items: center; border-radius: 16px; padding: 1rem 1.25rem; margin: 1.25rem 0 1rem; }
.banner .ic { flex: 0 0 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; color: #fff; }
.banner b { display: block; font-size: 1.02rem; }
.banner span { font-size: .88rem; opacity: .85; }
.banner.pass { background: var(--pass-soft); color: var(--pass-ink); }
.banner.pass .ic { background: var(--pass); }
.banner.fail { background: var(--fail-soft); color: var(--fail-ink); }
.banner.fail .ic { background: var(--fail); }
.box-title { font-weight: 700; color: var(--ink); font-size: 1.02rem; margin: 0 0 .8rem; }

/* Nút */
.stButton > button, .stDownloadButton > button {
    border-radius: 12px; font-weight: 600; padding: .6rem 1.3rem;
    border: 1px solid var(--line); background: #fff; color: var(--ink);
    transition: transform .08s ease, box-shadow .15s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover { border-color: var(--primary); color: var(--primary); }
.stButton > button:active { transform: scale(.98); }
.stButton > button[kind="primary"] { background: linear-gradient(135deg, #4F46E5, #6366F1); border: none; color: #fff; box-shadow: 0 6px 16px rgba(79,70,229,.35); }
.stButton > button[kind="primary"]:hover { color: #fff; box-shadow: 0 8px 20px rgba(79,70,229,.45); }
.st-key-card_pass .stButton > button { background: var(--pass); border: none; color: #fff; }
.st-key-card_fail .stButton > button { background: var(--fail); border: none; color: #fff; }
.st-key-card_pass .stButton > button p, .st-key-card_fail .stButton > button p { color: #fff; }

/* Ô nhập, bảng */
.stTextArea textarea { border-radius: 14px; border: 1px solid var(--line); background: #fff; padding: .9rem 1rem; font-size: .98rem; }
.stTextArea textarea:focus { border-color: var(--primary); box-shadow: 0 0 0 4px var(--primary-soft); }
.stTextArea label p { font-weight: 600; color: var(--ink); }
[data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 16px; overflow: hidden; box-shadow: var(--shadow); }
[data-testid="stExpander"] { background: #fff; border: 1px solid var(--line); border-radius: 14px; }
[data-testid="stImage"] img { border-radius: 12px; border: 1px solid var(--line); }

/* Thanh bên tối */
[data-testid="stSidebar"] { background: #0F172A; }
[data-testid="stSidebar"] * { color: #CBD5E1; }
[data-testid="stSidebar"] h3 { color: #fff; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.1); }
[data-testid="stSidebar"] code { background: rgba(255,255,255,.08); color: #A5B4FC; }
[data-testid="stSidebar"] .stButton > button { background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.15); color: #fff; width: 100%; }
[data-testid="stSidebar"] .stButton > button:hover { background: rgba(255,255,255,.12); color: #fff; }
.brand { display: flex; align-items: center; gap: .7rem; margin-bottom: .3rem; }
.brand .logo { width: 40px; height: 40px; border-radius: 12px; background: linear-gradient(135deg, #6366F1, #06B6D4); display: flex; align-items: center; justify-content: center; font-size: 1.3rem; }
.brand b { color: #fff; font-size: 1.05rem; }

:focus-visible { outline: 2px solid var(--primary); outline-offset: 2px; }
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Hàm hỗ trợ
# ---------------------------------------------------------------------------
def html(s: str):
    """Ghi HTML gọn một dòng để Markdown không hiểu nhầm là code block."""
    st.markdown("".join(line.strip() for line in s.splitlines()), unsafe_allow_html=True)


def show_table(data):
    try:
        st.dataframe(data, width="stretch", hide_index=True)
    except Exception:
        st.dataframe(data, use_container_width=True)


def show_image(path):
    try:
        st.image(path, width="stretch")
    except Exception:
        st.image(path, use_container_width=True)


def stats_row(total, passed, failed):
    html(f"""
    <div class="stats">
      <div class="stat"><div class="v">{total}</div><div class="l">Lần đã chạy</div></div>
      <div class="stat pass"><div class="v">{passed}</div><div class="l">Đạt</div></div>
      <div class="stat fail"><div class="v">{failed}</div><div class="l">Lỗi</div></div>
    </div>""")


def stepper(has_cases, has_runs, has_report):
    steps = [
        ("1", "Nhập yêu cầu", "User Story", True),
        ("2", "Tạo Test Case", "AI viết kịch bản", has_cases),
        ("3", "Chạy tự động", "Playwright", has_runs),
        ("4", "Phân tích lỗi", "Báo cáo Bug", has_report),
    ]
    out, marked_next = "", False
    for n, title, sub, done in steps:
        cls = "done" if done else ""
        if not done and not marked_next:
            cls, marked_next = "next", True
        mark = "✓" if done else n
        out += f'<div class="st-step {cls}"><div class="n">{mark}</div><div><b>{title}</b><small>{sub}</small></div></div>'
    html(f'<div class="steps">{out}</div>')


# ---------------------------------------------------------------------------
# Trạng thái
# ---------------------------------------------------------------------------
ss = st.session_state
ss.setdefault("test_cases", None)
ss.setdefault("runs", {"passed": 0, "failed": 0})
ss.setdefault("last", None)  # {"kind": "pass"|"fail", "result": {...}, "report": str|None}

# ---------------------------------------------------------------------------
# Thanh bên
# ---------------------------------------------------------------------------
with st.sidebar:
    html('<div class="brand"><div class="logo">🤖</div><b>NVT_AI QA</b></div>')
    st.caption("Trợ lý kiểm thử phần mềm")
    st.markdown("---")
    st.markdown("**Trang được kiểm thử**")
    st.markdown("`fl1s.vn`")
    st.markdown("**Tài khoản mẫu**")
    st.markdown("`nguyenvanthieu`")
    st.markdown("---")
    if st.button("Xóa kết quả"):
        ss["test_cases"], ss["last"] = None, None
        ss["runs"] = {"passed": 0, "failed": 0}
        st.rerun()

# ---------------------------------------------------------------------------
# Đầu trang
# ---------------------------------------------------------------------------
html("""
<div class="hero">
  <h1>Kiểm thử phần mềm nhanh hơn với AI</h1>
  <p>Từ một User Story đến báo cáo Bug hoàn chỉnh: AI viết kịch bản, Playwright chạy thử, AI phân tích lỗi.</p>
</div>""")

stepper(
    has_cases=bool(ss["test_cases"]),
    has_runs=(ss["runs"]["passed"] + ss["runs"]["failed"]) > 0,
    has_report=bool(ss["last"] and ss["last"].get("report")),
)

tab1, tab2, tab3 = st.tabs(["📋  Tạo Test Cases", "⚙️  Chạy tự động", "🧭  AI Khám phá (Bonus)"])

# ---------------------------------------------------------------------------
# TAB 1
# ---------------------------------------------------------------------------
with tab1:
    user_story = st.text_area(
        "User Story",
        value="Là một người dùng, tôi có thể đăng nhập vào hệ thống bằng username và password.",
        height=120,
        help="Mô tả chức năng cần kiểm thử: Là một..., tôi muốn..., để...",
    )

    if st.button("🚀 Tạo Test Cases", type="primary"):
        with st.spinner("AI đang viết kịch bản kiểm thử..."):
            ss["test_cases"] = generate_test_cases(user_story)
        if not ss["test_cases"]:
            st.error("Không thể tạo Test Cases. Kiểm tra API key và kết nối mạng, rồi thử lại.")

    st.write("")
    cases = ss["test_cases"]
    if cases:
        df = pd.DataFrame(cases)
        html(f"""
        <div class="banner pass"><div class="ic">✓</div>
        <div><b>Đã tạo {len(df)} kịch bản kiểm thử</b><span>Xem bảng bên dưới hoặc tải về để dùng tiếp</span></div></div>""")
        show_table(cases)
        st.download_button(
            "⬇️ Tải Test Cases (CSV)",
            data=df.to_csv(index=False).encode("utf-8-sig"),
            file_name="test_cases.csv",
            mime="text/csv",
        )
    else:
        with st.container(key="box_empty"):
            html("""
            <div class="box-title">Chưa có Test Case nào</div>
            <div class="card-desc" style="margin:0">Nhập User Story ở trên rồi chọn <b>Tạo Test Cases</b>. Kết quả sẽ hiện ở đây.</div>""")

# ---------------------------------------------------------------------------
# TAB 2
# ---------------------------------------------------------------------------
with tab2:
    r = ss["runs"]
    stats_row(r["passed"] + r["failed"], r["passed"], r["failed"])

    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container(key="card_pass"):
            html("""
            <span class="tag pass">Kỳ vọng: đạt</span>
            <div class="card-title">Đăng nhập thành công</div>
            <p class="card-desc">Nhập đúng tài khoản để xác nhận luồng đăng nhập hoạt động.</p>
            <div class="creds">nguyenvanthieu / secret_sauce</div>""")
            run_pass = st.button("▶ Chạy test case (Pass)", key="btn_pass")

    with col2:
        with st.container(key="card_fail"):
            html("""
            <span class="tag fail">Kỳ vọng: lỗi</span>
            <div class="card-title">Đăng nhập thất bại</div>
            <p class="card-desc">Cố tình nhập sai mật khẩu để kiểm tra khả năng bắt lỗi của hệ thống.</p>
            <div class="creds">nguyenvanthieu / mat_khau_sai_roi</div>""")
            run_fail = st.button("▶ Chạy test case (Tạo Bug)", key="btn_fail")

    # --- Chạy kịch bản ---
    if run_pass:
        with st.spinner("Playwright đang mở trình duyệt..."):
            res = run_login_test("nguyenvanthieu", "nguyenvanthieu123", expected_to_pass=True)
        ok = res["status"] == "passed"
        ss["runs"]["passed" if ok else "failed"] += 1
        ss["last"] = {"kind": "pass", "result": res, "report": None}
        if ok:
            st.balloons()

    if run_fail:
        with st.spinner("Playwright đang chạy và thu thập bằng chứng lỗi..."):
            res = run_login_test("nguyenvanthieu", "mat_khau_sai_roi", expected_to_pass=True)
        report = None
        if res["status"] == "failed":
            ss["runs"]["failed"] += 1
            with st.spinner("AI đang đọc mã HTML và log lỗi để viết báo cáo..."):
                report = generate_bug_report(
                    test_case_info="Test case: Đăng nhập với mật khẩu sai",
                    error_log=res["error_log"],
                    html_context=res["html_context"],
                )
        else:
            ss["runs"]["passed"] += 1
        ss["last"] = {"kind": "fail", "result": res, "report": report}

    # --- Hiển thị kết quả gần nhất (giữ nguyên khi bấm nút tải) ---
    last = ss["last"]
    if last:
        res = last["result"]
        if res["status"] == "passed":
            html("""
            <div class="banner pass"><div class="ic">✓</div>
            <div><b>Test passed</b><span>Trình duyệt đã đăng nhập thành công</span></div></div>""")
        else:
            html("""
            <div class="banner fail"><div class="ic">✕</div>
            <div><b>Test failed</b><span>Đã thu thập ảnh chụp màn hình và log lỗi</span></div></div>""")

            left, right = st.columns(2, gap="large")
            with left:
                with st.container(key="box_shot"):
                    html('<div class="box-title">📸 Ảnh chụp màn hình lúc lỗi</div>')
                    if os.path.exists(res["screenshot"]):
                        show_image(res["screenshot"])
                    else:
                        st.warning("Không tìm thấy ảnh chụp màn hình.")
                    with st.expander("Xem log lỗi"):
                        st.code(res["error_log"], language="text")
            with right:
                with st.container(key="box_report"):
                    html('<div class="box-title">🧠 Báo cáo Bug do AI viết</div>')
                    st.markdown(last["report"] or "_Chưa có báo cáo._")
                    if last["report"]:
                        st.download_button(
                            "⬇️ Tải báo cáo (.md)",
                            data=str(last["report"]).encode("utf-8"),
                            file_name="bug_report.md",
                            mime="text/markdown",
                        )
# ---------------------------------------------------------------------------
# TAB 3: AI KHÁM PHÁ (BONUS)
# ---------------------------------------------------------------------------
with tab3:
    html("""
    <div class="box-title" style="font-size: 1.3rem;">🧭 Tính năng Thưởng: AI Tự động Khám phá Website</div>
    <div class="card-desc">Nhập URL bất kỳ, Playwright sẽ vào thu thập giao diện ngầm và AI sẽ phân tích xem nên test những gì.</div>
    """)
    
    col_url, col_btn = st.columns([4, 1])
    with col_url:
        target_url = st.text_input("URL trang web cần quét:", value="https://fl1s.vn/", label_visibility="collapsed")
    with col_btn:
        scan_btn = st.button("🔍 Quét & Phân tích", use_container_width=True, type="primary")
        
    if scan_btn:
        with st.container(key="box_explore"):
            with st.spinner(f"Đang cử Playwright quét nội dung {target_url}..."):
                from test_runner import get_page_elements
                elements = get_page_elements(target_url)
                
            if elements:
                st.success("✅ Đã trích xuất cấu trúc giao diện thành công! AI đang lên chiến lược...")
                from llm_helper import explore_and_suggest
                with st.spinner("QA Manager AI đang phân tích dữ liệu..."):
                    suggestion = explore_and_suggest(target_url, elements)
                    st.markdown("---")
                    st.markdown(suggestion)
            else:
                st.error("❌ Không thể quét trang web. Vui lòng kiểm tra lại kết nối mạng hoặc thử URL khác (Lưu ý: Một số web chặn Bot chặn quét).")