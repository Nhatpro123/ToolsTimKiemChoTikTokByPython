from playwright.sync_api import sync_playwright

def search_tiktok(keyword):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Đặt False để kiểm tra
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
        )
        page = context.new_page()
        
        # Truy cập trang tìm kiếm TikTok
        search_url = f"https://www.tiktok.com/search?q={keyword}"
        page.goto(search_url)
        page.wait_for_timeout(5000)

        # Cuộn trang để tải thêm video
        for _ in range(3):
            page.mouse.wheel(0, 2000)
            page.wait_for_timeout(3000)

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
        return results

# Chạy tìm kiếm
results = search_tiktok("review mỹ phẩm")
for result in results:
    print(result)
