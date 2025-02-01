from playwright.sync_api import sync_playwright
import time

def search_tiktok(TuKhoa):
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=False)  
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
            )
            page = context.new_page()

            # Truy cập trang tìm kiếm TikTok
            search_url = f"https://www.tiktok.com/search?q={TuKhoa}"
            page.goto(search_url)
            
            # Đợi trang tải xong với điều kiện chắc chắn
            page.wait_for_selector("div[data-e2e='search-video-item']")
            print("Trang TikTok đã tải xong.")
            
            # Cuộn trang để tải thêm video
            for _ in range(3):
                page.mouse.wheel(0, 2000)
                page.wait_for_selector("div[data-e2e='search-video-item']", timeout=3000) 

            # Trích xuất danh sách video
            results = page.evaluate('''() => {
                let items = document.querySelectorAll('div[data-e2e="search-video-item"]');
                let data = [];
                items.forEach(item => {
                    let linkElement = item.querySelector('a');
                    let titleElement = item.querySelector('a h3');
                    if (linkElement && titleElement) {
                        data.push({
                            title: titleElement.innerText,
                            link: linkElement.href
                        });
                    }
                });
                return data;
            }''')

            browser.close()
            return KetQua
        
        except Exception as e:
            print(f"Đã xảy ra lỗi: {e}")
            browser.close()
            return []

# Cho phép người dùng nhập từ khóa
TuKhoa = input("Nhập từ khóa tìm kiếm: ")

# Chạy tìm kiếm
KetQua = search_tiktok(TuKhoa)

# In kết quả đẹp hơn
if KetQua:
    print(f"Đã tìm thấy {len(KetQua)} video cho từ khóa '{TuKhoa}':")
    for idx, result in enumerate(KetQua, 1):
        print(f"{idx}. Tiêu đề: {KetQua['title']}\n   Link: {KetQua['link']}\n")
else:
    print("Không tìm thấy kết quả.")
