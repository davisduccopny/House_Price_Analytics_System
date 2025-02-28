import smtplib
from jinja2 import Template
from email.utils import formataddr
import os
from email.message import EmailMessage
import random
import mysql.connector
import pandas as pd
import folium
import datetime

def connect_mysql():
    try:
        connection = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME")
        )
        if connection.is_connected():
            print("✅ Connected to MySQL database")
            return connection
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
        return None

sender_email = os.environ.get("send_mail_address")
sender_password = os.environ.get("send_mail_prediction")

def generate_otp():
    """Tạo mã OTP gồm 6 chữ số"""
    return str(random.randint(100000, 999999))

def send_confirmation_email(receiver_mail,display_name,otp_code):
    # Load confirmation email template
    try:
        with open("src/mail/confirmation_mail_template.html", "r", encoding="utf-8") as file:
            confirmation_template = Template(file.read())

        # Render template with data
        email_content = confirmation_template.render(display_name=display_name, otp_code=otp_code)

        # Create email
        msg = EmailMessage()
        msg["From"] = formataddr(("Real estate team.", f"{sender_email}"))
        msg["To"] = receiver_mail
        msg["Subject"] = "📧 Xác Nhận Đăng Ký"
        
        msg.set_content(email_content, subtype='html')
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            response = server.send_message(msg)
        if response:
            print(f"❌ Email không gửi được đến {receiver_mail}, phản hồi từ server: {response}")
            return False
        else:
            print(f"✅ Email xác nhận đã gửi thành công đến {receiver_mail}")
            return True
      
    except smtplib.SMTPRecipientsRefused as e:
        print(f"❌ Lỗi: Địa chỉ email {receiver_mail} không hợp lệ hoặc bị từ chối. {e}")
        return False

    except smtplib.SMTPException as e:
        print(f"❌ Lỗi SMTP: {e}")
        return False

    except Exception as e:
        print(f"❌ Lỗi không xác định khi gửi email đến {receiver_mail}: {e}")
        return False

def send_report_email(receiver_email,email_content):
    # Tạo email
    msg = EmailMessage()
    msg["From"] = formataddr(("Real estate team.", f"{sender_email}"))
    msg["To"] = receiver_email
    msg["Subject"] = f"📢 Báo cáo cập nhật bất động sản {datetime.datetime.now().strftime('%Y/%m/%d')}"
    msg.set_content(email_content, subtype='html')

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def query_to_dataframe(query, conn):
    cursor = conn.cursor(dictionary=True)  
    cursor.execute(query)
    data = cursor.fetchall()  
    cursor.close()
    return pd.DataFrame(data)

def load_data(conn):
    try:
        region_info = query_to_dataframe(f"SELECT tinh_thanh_pho,ma_tp FROM region_info;", conn)
        customer_email = query_to_dataframe(f"""
                                            SELECT username,region_use FROM users WHERE send_mail = 1 and send_mail IS NOT NULL;
                                            """, conn)
        house_price = query_to_dataframe(f"SELECT dia_chi, dien_tich,gia,longitude,latitude FROM thong_tin_bat_dong_san;",conn)
        return house_price,customer_email,region_info
    finally:
        conn.close()

def tao_bao_cao_html(df_khu_vuc):
    tong_bds = len(df_khu_vuc)
    gia_tb = df_khu_vuc["gia"].mean()

    danh_sach_bds = "".join(
        f"<tr><td>{row['dia_chi']}</td><td>{row['dien_tich']} m²</td><td>{row['gia']} tỷ</td></tr>"
        for _, row in df_khu_vuc.nlargest(5, "gia").iterrows()
    )
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; background-color: #f9f9f9; color: #333; }}
            h2 {{ color: #2c3e50; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #2c3e50; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            tr:hover {{ background-color: #ddd; }}
            p {{ margin: 5px 0; }}
            .footer {{ margin-top: 20px; font-size: 12px; color: gray;text-align: center; }}
        </style>
    </head>
    <body>
        <h2> 📢 Báo cáo Bất động sản - {df_khu_vuc['dia_chi'].iloc[0]}</h2>
        <p><b>Tổng số bất động sản:</b> {tong_bds}</p>
        <p><b>Giá bất động sản trung bình:</b> {gia_tb:.2f} tỷ</p>

        <h3>Top 5 bất động sản có giá cao nhất</h3>
        <table>
            <tr><th>Địa chỉ</th><th>Diện tích</th><th>Giá</th></tr>
            {danh_sach_bds}
        </table>

        <p style="font-size:12px;color:gray;">
            Bạn nhận được email này vì đã đăng ký thông tin. 
            <a href="https://yourwebsite.com/unsubscribe">Hủy đăng ký</a>
        </p>
        <div class="footer">© 2025 Team Real Estate</div>
    </body>
    </html>
    """

    return html_content

def daily_send_mail_real_estate():
    conn = connect_mysql()
    cursor = conn.cursor()
    
    df_house_price,df_customer_email,df_region_info = load_data(conn)
    distinct_regions = df_customer_email['region_use'].drop_duplicates()
    merged_regions = pd.merge(distinct_regions, df_region_info, left_on='region_use', right_on='ma_tp')
    region_names = merged_regions['tinh_thanh_pho'].drop_duplicates().tolist()
    df_house_price = df_house_price[df_house_price['dia_chi'].fillna('').str.contains('|'.join(region_names))]
    df_send_email = pd.merge(df_customer_email, df_region_info, left_on='region_use', right_on='ma_tp', how='left').drop_duplicates()
    df = df_house_price
    df = df.dropna(subset=["dia_chi", "dien_tich", "gia"]) 
    df["gia"] = df["gia"].astype(float)  

    from collections import defaultdict
    count_send = 0
    email_mapping = defaultdict(list)
    for _, row in df_send_email.iterrows():
        email_mapping[row["tinh_thanh_pho"]].append(row["username"])
    for khu_vuc in df["dia_chi"].unique():
        df_khu_vuc = df[df["dia_chi"] == khu_vuc]
        html_save = tao_bao_cao_html(df_khu_vuc) 
        if khu_vuc in email_mapping: 
            for receiver_email in email_mapping[khu_vuc]: 
                if send_report_email(receiver_email,html_save):
                    count_send += 1
    print(f"✅ Đã gửi báo cáo cho {count_send} người dùng")
# daily_send_mail_real_estate()