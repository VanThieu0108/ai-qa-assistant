import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Tải cấu hình từ file .env
load_dotenv()

# Lấy API Key từ file .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Chưa tìm thấy GEMINI_API_KEY. Vui lòng kiểm tra lại file .env")

# Khởi tạo client mới theo chuẩn thư viện google-genai
client = genai.Client(api_key=GEMINI_API_KEY)

def generate_test_cases(user_story):
    """
    Hàm này nhận đầu vào là một User Story và nhờ AI sinh ra các Test Cases dưới định dạng JSON.
    """
    
    prompt = f"""
    Bạn là một Kỹ sư Kiểm thử Phần mềm (QA Engineer) xuất sắc. 
    Nhiệm vụ của bạn là phân tích User Story dưới đây và tạo ra ít nhất 15 kịch bản kiểm thử (Test Cases).
    Bạn phải bao phủ đủ 4 loại test: Positive, Negative, Boundary (Ranh giới), Validation (Xác thực).
    
    User Story: "{user_story}"
    
    Cấu trúc mỗi object trong mảng JSON phải đúng form sau:
    [
        {{
            "id": "TC01",
            "title": "Tên test case ngắn gọn (tiếng Việt)",
            "type": "Positive / Negative / Boundary / Validation",
            "steps": "1. ... 2. ... 3. ...",
            "expected_result": "Kết quả mong đợi"
        }}
    ]
    """
    
    try:
        # Gọi API với model gemini-2.5-flash (model mới nhất)
        # Sử dụng config ép AI trả về chuẩn JSON (response_mime_type)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        
        result_text = response.text.strip()
        
        # Chuyển chuỗi JSON text thành một List các Object trong Python
        test_cases = json.loads(result_text)
        return test_cases
        
    except json.JSONDecodeError as e:
        print(f"Lỗi: AI trả về định dạng JSON không chuẩn. Dữ liệu gốc: {result_text}")
        return None
    except Exception as e:
        print(f"Lỗi khi gọi API: {e}")
        return None

def generate_bug_report(test_case_info, error_log, html_context):
    """
    Hàm này nhận đầu vào là thông tin test case bị fail, log lỗi và HTML của trang web.
    Nó sẽ nhờ AI phân tích và trả về Bug Report định dạng Markdown.
    """
    prompt = f"""
    Bạn là một QA Engineer. Một kịch bản kiểm thử tự động đã thất bại.
    Hãy phân tích dữ liệu lỗi dưới đây và viết một Báo cáo Lỗi (Bug Report) thật chuyên nghiệp bằng Markdown.

    1. THÔNG TIN TEST CASE BỊ FAIL:
    {test_case_info}

    2. LOG LỖI TỪ HỆ THỐNG AUTOMATION:
    {error_log}

    3. MÃ HTML CỦA TRANG TẠI THỜI ĐIỂM BỊ LỖI (Dùng để chẩn đoán nguyên nhân):
    {html_context[:5000]}  # Chỉ lấy 5000 ký tự đầu để tránh AI bị ngợp thông tin

    YÊU CẦU BÁO CÁO LỖI PHẢI CÓ CÁC MỤC SAU:
    - **Tiêu đề lỗi (Bug Title)**
    - **Trường hợp kiểm thử (Test Case)**
    - **Kết quả mong đợi (Expected Result)**
    - **Kết quả thực tế (Actual Result)** (Dựa vào log lỗi)
    - **Mức độ nghiêm trọng (Severity)** (High/Medium/Low kèm giải thích)
    - **Nguyên nhân gốc rễ dự đoán (Possible Root Cause)** (Dựa vào việc đọc HTML và Log)
    - **Đề xuất khắc phục (Recommendation)**
    """
    
    try:
        # Ở đây ta không cần ép kiểu JSON, cứ để AI sinh Markdown bình thường
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        print(f"Lỗi khi nhờ AI phân tích lỗi: {e}")
        return "Không thể tạo báo cáo lỗi."
    
def explore_and_suggest(url, elements_data):
    """
    AI đọc dữ liệu cấu trúc web và đề xuất chiến lược kiểm thử.
    """
    prompt = f"""
    Bạn là một QA Manager (Quản lý Kiểm thử) cấp cao. Tôi đang muốn kiểm thử trang web: {url}.
    Hệ thống Automation của tôi đã quét được một số thành phần giao diện chính của trang như sau:
    {json.dumps(elements_data, ensure_ascii=False, indent=2)}
    
    Dựa vào các nút bấm, ô nhập liệu và liên kết trên, hãy đề xuất 5 TÍNH NĂNG QUAN TRỌNG NHẤT cần phải ưu tiên kiểm thử trên trang này.
    Yêu cầu trình bày bằng Markdown thật chuyên nghiệp:
    - Mỗi tính năng là 1 Heading (Dùng Icon cho đẹp).
    - Giải thích NGẮN GỌN lý do tại sao nó quan trọng.
    - Đề xuất nhanh 2 Test Case cho tính năng đó (1 Positive, 1 Negative).
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        return f"Lỗi khi gọi AI: {e}"
# --- ĐOẠN CODE TEST THỬ SỰ KẾT HỢP GIỮA PLAYWRIGHT VÀ AI ---
if __name__ == "__main__":
    from test_runner import run_login_test # Import Playwright từ file test_runner
    
    print("1. Đang chạy Automation Test cố tình gây lỗi...")
    test_info = "Đăng nhập với username đúng và password sai ('mat_khau_sai_roi')"
    
    # Chạy thử test case mồi (sẽ sinh ra lỗi)
    test_result = run_login_test("standard_user", "mat_khau_sai_roi", expected_to_pass=True)
    
    if test_result["status"] == "failed":
        print("\n2. Test đã thất bại. Đang gửi bằng chứng cho AI phân tích...\n")
        
        # Gửi dữ liệu cho AI
        bug_report = generate_bug_report(
            test_case_info=test_info,
            error_log=test_result["error_log"],
            html_context=test_result["html_context"]
        )
        
        print("================ BÁO CÁO LỖI DO AI TẠO ================\n")
        print(bug_report)
        print("\n=======================================================")