# 📓 Nhật ký sử dụng AI (AI Worklog)

Tài liệu này ghi lại quá trình tôi tương tác, kiểm soát và tối ưu hóa sự hỗ trợ của Trí tuệ Nhân tạo trong dự án này.

## 1. Các công cụ AI đã sử dụng
- **Google Gemini 2.5 Flash (via API):** Đóng vai trò là "Não bộ" sinh kịch bản kiểm thử, phân tích mã HTML DOM khi có lỗi và lên chiến lược test.
- **ChatGPT (GPT-4o):** Đóng vai trò là "Pair-programmer" hỗ trợ tôi thiết kế giao diện UI/UX bằng Streamlit, tạo CSS tùy chỉnh và debug các lỗi cú pháp Python.

## 2. Cách AI đã hỗ trợ tôi
- **Viết Regex và JSON Schema:** Thay vì tự parse dữ liệu text, tôi đã nhờ AI thiết lập cấu trúc để Gemini trả về chuẩn JSON 100%, giúp dễ dàng binding lên bảng (DataFrame) của Streamlit.
- **Phân tích nguyên nhân gốc rễ (Root Cause):** Việc đưa mã HTML DOM bị lỗi cho AI đọc tỏ ra cực kỳ hiệu quả. AI có thể nhận diện được các class báo lỗi (như `error-message`) ẩn trong DOM để đưa ra suy luận kỹ thuật cho báo cáo Bug, thay vì chỉ đoán bừa.

## 3. Lỗi sai của AI & Cách tôi kiểm chứng, khắc phục
Trong quá trình phát triển, tôi không giao phó hoàn toàn cho AI mà phải liên tục kiểm chứng và điều chỉnh:

*   **Sự cố 1: AI trả về định dạng rác (Markdown block)**
    *   *Vấn đề:* Ban đầu, Gemini thường xuyên bọc kết quả JSON trong thẻ ```json ... ``` khiến hàm `json.loads()` của Python bị sập.
    *   *Cách khắc phục:* Tôi đã chuyển sang thư viện `google-genai` mới nhất và cấu hình `response_mime_type="application/json"` trong tham số gọi API để ép hệ thống trả về JSON thuần túy ở cấp độ nền tảng.
*   **Sự cố 2: Lỗi False Negative (Báo lỗi giả) khi xử lý Popup**
    *   *Vấn đề:* Playwright báo kịch bản Đăng nhập thất bại, nhưng ảnh chụp màn hình lại hiển thị thông báo "Đăng nhập thành công" rất to. Nguyên nhân do AI/Script chỉ chờ sự thay đổi URL, trong khi web thực tế dùng Ajax và SweetAlert2 để hiện Popup trước khi chuyển trang.
    *   *Cách khắc phục:* Bằng tư duy QA, tôi đã can thiệp vào logic kiểm thử. Tôi thay đổi Assertion: yêu cầu Playwright đợi thêm 3 giây và quét tìm `locator("text='Đăng nhập thành công'")` thay vì chỉ phụ thuộc vào URL. Lỗi False Negative được khắc phục hoàn toàn.

## 4. Kế hoạch cải thiện trong 7 ngày tới
Nếu có thêm thời gian, tôi sẽ triển khai các tính năng sau:
1. **Cơ chế Tự phục hồi (Self-healing Locators):** Khi một nút bấm bị đổi tên class, tôi sẽ cho Playwright ném toàn bộ HTML cho AI tìm lại nút bấm đó dựa trên ngữ cảnh, thay vì để test case bị crash cứng.
2. **Kiểm thử luồng Checkout (Thanh toán):** Mở rộng hệ thống để test các kịch bản phức tạp hơn như chọn sản phẩm -> điền form giao hàng -> thanh toán giả lập.
3. **Tích hợp CI/CD:** Đóng gói ứng dụng thành Docker Container và tạo GitHub Actions để luồng AI Test này tự động chạy mỗi khi có code mới được Push lên nhánh main.