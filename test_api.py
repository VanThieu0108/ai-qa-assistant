import os
from google import genai
from dotenv import load_dotenv

# Tải API Key từ file .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("❌ LỖI: Chưa tìm thấy GEMINI_API_KEY trong file .env")
    exit()

try:
    print("Đang kết nối tới Google Gemini bằng mô hình gemini-2.5-flash...")
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Gửi một câu hỏi ngắn để test
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents='Xin chào, hãy trả lời ngắn gọn 1 câu để xác nhận bạn đang hoạt động.'
    )
    
    print("\n✅ THÀNH CÔNG! API Key của bạn hoàn toàn hợp lệ và CÓ THỂ sử dụng bản 2.5-flash.")
    print("🤖 AI trả lời:", response.text)
    
except Exception as e:
    print("\n❌ CÓ LỖI XẢY RA:")
    print(e)