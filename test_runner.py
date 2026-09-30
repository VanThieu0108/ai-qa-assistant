from playwright.sync_api import sync_playwright

def run_login_test(username, password, expected_to_pass=True):
    """
    Kịch bản tự động hóa kiểm thử trang FL1S.VN
    """
    result = {
        "status": "passed",
        "error_log": "",
        "screenshot": "",
        "html_context": ""
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context()
        page = context.new_page()
        
        try:
            print(f"Bắt đầu test trang FL1S với User: '{username}'")
            
            # 1. Truy cập trang đăng nhập
            page.goto("https://fl1s.vn/auth/login") 
            
            # 2. Điền thông tin (Dựa vào cấu trúc HTML)
            page.fill("input[name='username']", username)
            page.fill("input[name='password']", password)
            
            # 3. Bấm nút đăng nhập
            page.click("button[type='submit']")
            
            # 4. Kiểm tra kết quả (Assertion)
            # Chờ 3 giây để web xử lý và popup kịp hiện lên
            page.wait_for_timeout(3000) 
            
            if expected_to_pass:
                # KIỂM TRA MỚI: Tìm xem trên màn hình có chữ "Đăng nhập thành công" không
                # hoặc kiểm tra URL có chuyển hướng không
                success_popup = page.locator("text='Đăng nhập thành công'")
                is_popup_visible = success_popup.is_visible()
                is_url_changed = "/home" in page.url or page.url == "https://fl1s.vn/"
                
                assert is_popup_visible or is_url_changed, "Lỗi: Không thấy thông báo đăng nhập thành công và cũng không chuyển trang."
            else:
                # Nếu mong đợi Fail (nhập sai pass)
                assert "login" in page.url, "Lỗi nghiêm trọng: Nhập sai mật khẩu nhưng hệ thống lại cho qua!"
                
        except Exception as e:
            print("❌ Cảnh báo: Test case thất bại! Đang thu thập bằng chứng...")
            result["status"] = "failed"
            result["error_log"] = str(e)
            
            # Chụp ảnh màn hình lưu lại
            screenshot_path = "error_screenshot.png"
            page.screenshot(path=screenshot_path)
            result["screenshot"] = screenshot_path
            
            # Lấy toàn bộ mã HTML lúc bị lỗi
            result["html_context"] = page.content()
            
        finally:
            browser.close()
            
    return result

def get_page_elements(url):
    """
    Hàm này dùng Playwright chạy ngầm (headless), truy cập URL,
    và thu thập các thành phần tương tác (inputs, buttons, links) gửi cho AI.
    """
    with sync_playwright() as p:
        # headless=True để chạy ngầm, không mở trình duyệt lên cho nhanh
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=15000) # Cho tối đa 15s để load web
            page.wait_for_timeout(3000)
            
            # Chạy mã JavaScript ngầm để thu thập thẻ HTML
            elements = page.evaluate("""() => {
                const inputs = Array.from(document.querySelectorAll('input')).map(e => e.name || e.placeholder || e.type);
                const buttons = Array.from(document.querySelectorAll('button')).map(e => e.innerText || e.type);
                const links = Array.from(document.querySelectorAll('a')).map(e => e.innerText || e.href);
                return {
                    title: document.title,
                    inputs: inputs.filter(Boolean).slice(0, 15),
                    buttons: buttons.filter(Boolean).slice(0, 15),
                    links: links.filter(Boolean).slice(0, 15)
                };
            }""")
            return elements
        except Exception as e:
            print(f"Lỗi khi quét web: {e}")
            return None
        finally:
            browser.close()
# Chạy thử nghiệm
if __name__ == "__main__":
    # Test case 1: Đăng nhập thất bại (Vì ta chưa có tài khoản thật)
    print("\n--- CHẠY TEST CASE 1: ĐĂNG NHẬP THẤT BẠI ---")
    res = run_login_test("taikhoan_test", "mat_khau_sai_123", expected_to_pass=True)
    
    if res["status"] == "failed":
        print("✅ Đã bắt được lỗi và chụp ảnh màn hình thành công!")
        print(f"Log lỗi: {res['error_log']}")