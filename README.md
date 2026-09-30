# 🤖 Trợ lý Kiểm thử Phần mềm AI (AI QA Assistant)

## 📌 Giới thiệu dự án
AI QA Assistant là một quy trình kiểm thử tự động khép kín (End-to-End Testing Workflow) tích hợp Trí tuệ nhân tạo. Ứng dụng giúp các nhóm QA tự động hóa việc phân tích yêu cầu, sinh kịch bản kiểm thử, thực thi trên trình duyệt và tự động viết báo cáo lỗi (Bug Report) khi có sự cố.

## 🎯 Mục tiêu kiểm thử (Target Website)
**Trang web được chọn:** `https://fl1s.vn/` (Trang dịch vụ trực tuyến thực tế).
**Lý do chọn:** 
Thay vì chọn các trang web demo đơn giản (như saucedemo), tôi quyết định thử thách giải pháp của mình trên một hệ thống thực tế đang hoạt động. Trang web này sử dụng cơ chế xác thực qua AJAX và hiển thị thông báo qua Popup (SweetAlert2) thay vì chuyển trang ngay lập tức. Điều này đòi hỏi script Automation phải xử lý các bài toán thực tế như thao tác DOM bất đồng bộ và kiểm thử UI động, giúp chứng minh rõ nét tư duy xử lý vấn đề thay vì chỉ "record and play".

## ⚙️ Kiến trúc & Quy trình làm việc (Workflow)
Hệ thống được xây dựng trên **Python, Streamlit, Playwright và Google Gemini API (2.5-Flash)**.
1. **Yêu cầu (Input):** Người dùng nhập User Story (VD: Đăng nhập hệ thống).
2. **Sinh Test Case (AI):** Gemini API phân tích và sinh ra tối thiểu 15 Test Cases (bao phủ Positive, Negative, Boundary, Validation) dưới định dạng chuẩn JSON.
3. **Thực thi (Playwright):** Kịch bản kiểm thử được chạy ngầm/hiển thị trên Chromium. 
4. **Phân tích lỗi (AI):** Nếu Test Case thất bại, Playwright sẽ chụp ảnh màn hình và trích xuất mã HTML DOM tại thời điểm lỗi. AI sẽ đọc Log lỗi + HTML để chẩn đoán nguyên nhân (Root Cause).
5. **Khám phá (Bonus):** Playwright quét toàn bộ nút bấm/links trên một URL bất kỳ và yêu cầu AI đóng vai QA Manager để lên chiến lược kiểm thử.

## 🚀 Hướng dẫn cài đặt và chạy ứng dụng

**1. Cài đặt môi trường:**
Yêu cầu: Python 3.9+
```bash
python -m venv venv
# Kích hoạt môi trường:
venv\Scripts\activate # (Windows) hoặc source venv/bin/activate # (Mac/Linux)
2. Cài đặt thư viện:

Bash
pip install streamlit playwright google-genai pandas python-dotenv
playwright install chromium
3. Cấu hình API Key:
Tạo file .env ở thư mục gốc và thêm: GEMINI_API_KEY=your_api_key_here

4. Khởi chạy:

Bash
streamlit run app.py
⚠ Những hạn chế hiện tại
Phụ thuộc vào ID/Class tĩnh: Code Playwright hiện đang hard-code các bộ định vị (Locator). Nếu fl1s.vn thay đổi giao diện, script có thể bị gãy (Brittle test).

Tốc độ giới hạn của API Miễn phí: Đôi khi gặp lỗi 503 Service Unavailable do giới hạn rate limit của Gemini API công cộng.