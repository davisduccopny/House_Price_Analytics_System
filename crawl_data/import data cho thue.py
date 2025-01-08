import time
import random
import psycopg2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from urllib.parse import urljoin
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# Thiết lập User-Agent để giả lập trình duyệt của người dùng
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Initialize the Service object with the path to your chromedriver
service = Service('chromedriver.exe')  # Thay bằng đường dẫn đúng của bạn
driver = webdriver.Chrome(service=service, options=chrome_options)

# Kết nối đến PostgreSQL
def connect_db():
    try:
        connection = psycopg2.connect(
            dbname="postgres",  # Thay bằng tên cơ sở dữ liệu của bạn
            user="postgres",  # Thay bằng tên người dùng của bạn
            password="123",  # Thay bằng mật khẩu của bạn
            host="localhost",  # Thay bằng host nếu cần
            port="5432"  # Cổng mặc định của PostgreSQL
        )
        return connection
    except Exception as e:
        print(f"Không thể kết nối đến cơ sở dữ liệu: {e}")
        return None

# Hàm chèn dữ liệu vào cơ sở dữ liệu
def insert_property_data(data): 
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            insert_query = """
                INSERT INTO thong_tin_bat_dong_san (
                    tieu_de, dia_chi, dien_tich, gia, so_phong_ngu, so_phong_vs, noi_that, 
                    phap_ly, huong_nha, huong_ban_cong, so_tang, mat_tien, duong_vao, loai_bds
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(insert_query, data)
            conn.commit()
            print(f"Đã chèn {len(data)} bất động sản vào cơ sở dữ liệu.")
        except Exception as e:
            print(f"Lỗi khi chèn dữ liệu: {e}")
        finally:
            cursor.close()
            conn.close()

# Hàm thu thập thông tin chi tiết bất động sản
def crawl_property_specs(url, loai_bds):
    driver.get(url)
    driver.implicitly_wait(5)

    property_data = []

    try:
        title = driver.find_element(By.XPATH, '//h1[@class="re__pr-title pr-title js__pr-title"]').text
    except NoSuchElementException:
        title = 'Không có tiêu đề'

    try:
        short_description = driver.find_element(By.XPATH, '//span[@class="re__pr-short-description js__pr-address"]').text
    except NoSuchElementException:
        short_description = 'Không có mô tả ngắn'

    # Khởi tạo một từ điển để lưu trữ các thông số bất động sản
    property_specs = {
        "Diện tích": 'Không có thông tin',
        "Mức giá": 'Không có thông tin',
        "Hướng nhà": 'Không có thông tin',
        "Hướng ban công": 'Không có thông tin',
        "Số tầng": 'Không có thông tin',
        "Số phòng ngủ": 'Không có thông tin',
        "Số toilet": 'Không có thông tin',
        "Pháp lý": 'Không có thông tin',
        "Nội thất": 'Không có thông tin',
        "Mặt tiền": 'Không có thông tin',
        "Đường vào": 'Không có thông tin'
    }

    # Duyệt qua tất cả các phần tử trong mục thông số kỹ thuật
    spec_items = driver.find_elements(By.XPATH, '//div[@class="re__pr-specs-content-item"]')
    
    for item in spec_items:
        try:
            spec_title = item.find_element(By.XPATH, './/span[@class="re__pr-specs-content-item-title"]').text
            spec_value = item.find_element(By.XPATH, './/span[@class="re__pr-specs-content-item-value"]').text
            
            # Cập nhật thông tin vào từ điển
            if spec_title in property_specs:
                property_specs[spec_title] = spec_value

        except NoSuchElementException:
            continue

    # Lấy giá trị từ từ điển property_specs
    dien_tich = property_specs["Diện tích"]
    gia = property_specs["Mức giá"]
    huong_nha = property_specs["Hướng nhà"]
    huong_ban_cong = property_specs["Hướng ban công"]
    so_tang = property_specs["Số tầng"]
    so_phong_ngu = property_specs["Số phòng ngủ"]
    so_phong_vs = property_specs["Số toilet"]
    phap_ly = property_specs["Pháp lý"]
    noi_that = property_specs["Nội thất"]
    mat_tien = property_specs["Mặt tiền"]
    duong_vao = property_specs["Đường vào"]

    # Chuẩn bị dữ liệu cho cơ sở dữ liệu
    property_data.append(( 
        title, short_description, dien_tich, gia, so_phong_ngu, so_phong_vs, noi_that, 
        phap_ly, huong_nha, huong_ban_cong, so_tang, mat_tien, duong_vao, loai_bds
    ))

    return property_data

# Hàm thu thập dữ liệu từ trang danh sách
def crawl_data(driver, loai_bds):
    scroll_pause_time = random.uniform(1, 3)  # Thêm thời gian chờ ngẫu nhiên giữa các lần cuộn
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)
    
    elems = driver.find_elements(By.XPATH, '//a[@class="js__product-link-for-product-id"]')
    
    page_data = []
    
    for elem in elems:
        href = elem.get_attribute('href')
        if href:
            full_link = urljoin('https://batdongsan.com.vn', href)
            page_data.append(full_link)
    
    return page_data

# Chương trình chính
def main():
    n = 1  # Bắt đầu từ trang 1
    try:
        while True:
            url = f"https://batdongsan.com.vn/nha-dat-cho-thue/p{n}"  # Đặt URL mặc định
            loai_bds = 1  # Đánh dấu là mua bán
            if "cho-thue" in url:  # Nếu URL thuộc loại cho thuê
                loai_bds = 2    

            print(f"Opening URL: {url}")
            driver.get(url)
            driver.implicitly_wait(5)

            # Crawl data from the current page
            page_data = crawl_data(driver, loai_bds)

            # Thu thập dữ liệu từ từng liên kết bất động sản
            for link in page_data:
                print(f"Crawling property specs from: {link}")
                property_data = crawl_property_specs(link, loai_bds)
                if property_data:
                    insert_property_data(property_data)  # Chèn dữ liệu vào cơ sở dữ liệu

            # Thời gian chờ trước khi chuyển sang trang tiếp theo
            time.sleep(5)

            # Tăng số trang
            n += 1

            # Dừng vòng lặp sau một số trang nhất định (tùy chọn)
            if n > 10000000000000:  # Điều chỉnh theo nhu cầu
                
                break

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Đóng trình duyệt
        driver.quit()

# Thực hiện hàm chính
if __name__ == "__main__":
    main()
