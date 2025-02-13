import streamlit as st
import PROJECTS.config as module_config


with open('src/style/style_home.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)  


class FRONTEND_UI_HOME():
    def __init__(self):
        pass
    def arrow_down_design(self,target_section):
        st.markdown(f"""
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
        <div style="text-align: center; margin-top: 20px;">
            <a href="#{target_section}" style="
                text-decoration: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 40px;
                display: inline-block;
            ">
                <i class="fa-solid fa-chevron-down"></i>
            </a>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""<style>
            .fa-chevron-down:hover, .fa-chevron-up:hover {
                color: yellow;
            }
            </style>""", unsafe_allow_html=True)
        
    def arrow_up_design(self,target_section):
        st.markdown(f"""
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
        <div style="text-align: center; margin-top: 20px;">
            <a href="#{target_section}" style="
                text-decoration: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 40px;
                display: inline-block;
            ">
                <i class="fa-solid fa-chevron-up"></i>
            </a>
        </div>
        """, unsafe_allow_html=True)
    def create_sidebar_toc(self):
        toc_items = [
            ("🏠  Tổng quan", "target-section"),
            ("📈  Phân tích dữ liệu", "target-section-2"),
            ("🔍  Dự đoán giá nhà", "target-section-3"),
            ("📊  Hiệu suất mô hình", "target-section-4"),
            ("🔒  Bảo mật dữ liệu", "target-section-5")
        ]
        st.sidebar.markdown(
            """
            <style>
            .toc-item:hover {
            background-color: #f0f0f0;
            cursor: pointer;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        toc_markdown = "\n".join(
            [f'<a href="#{item[1]}" class = "toc-item" style="display: block; padding: 10px; margin: 5px 0; color: rgb(0, 50, 73); text-align: left; border-radius: 5px; text-decoration: none; text-indent:6%;">{item[0]}</a>' for item in toc_items]
        )
        st.sidebar.markdown(toc_markdown, unsafe_allow_html=True)
    def sidebar_design(self):
        st.sidebar.divider()
    def main_container_design(self):
        # self.create_sidebar_toc()   
        # PART 1: HEADER
        file_path_image_logo_main = "../src/image/logo_2-Photoroom.png"
        file_path_image_logo_main = module_config.get_relative_file_path(file_path_image_logo_main)
        svg_icon_image_page_home = module_config.get_relative_file_path("../src/image/home/Sno-Blue-Arrow.svg")
        container_header= st.container()
        container_header.markdown(
            f"""
            <div style="padding: 0;text-align: center;" id="target-section-0">
                <img src='data:image/png;base64,{file_path_image_logo_main}' width='30%' >
                <h1 style=" font-size: 90px; font-weight: 700; padding-top:0;padding-bottom:10px" >
                    <span >House Price Prediction</span>
                    <img src="data:image/svg+xml;base64,{svg_icon_image_page_home}" height="70" align="center" style="margin-right: -5%; margin-top: -20px;" id="icon-home-info">
                    <span style=" background-color: rgb(41, 181, 232); padding:0px 10px;">
                    Viet Nam</span> 
                    <span style="color: #00BFFF;">in 2025</span>
                </h1>
                <p style="color: #555555;font-size: 28px;line-height: 1.25; margin-top: 38px;">
                    Khám phá và phân tích giá nhà tại Việt Nam  
                    <span style="color: #FFC107; font-weight: bold;">trong năm 2025</span> được tạo bởi
                    <span style="color: #FFC107; font-weight: bold;">nhóm developers</span> 
                    tại <span style="color: #FFC107; font-weight: bold;"> Thành phố Hồ Chí Minh</span>.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        container_header.markdown("""<style>
            [data-testid=stMainBlockContainer] {
                max-width: 64.65rem;
                
            }
            </style>""", unsafe_allow_html=True)
        
        module_config.social_media_show()
        self.arrow_down_design("target-section")
        # PART 2: MAIN CONTENT
        container_main_first = st.container()
        container_main_first.subheader("Tại sao bạn nên sử dụng ứng dụng dự đoán giá nhà?", divider="blue", anchor="target-section")
        container_main_first.markdown(
            """
            <p style="font-size: 1.2rem;">
                Lợi ích <span style="color: rgb(255, 189, 69);">chính</span> được trình bày dưới dạng thẻ hoặc hình ảnh
            </p>
            """,
            unsafe_allow_html=True
        )
        col_container_main_1, col_container_main_2, col_container_main_3, col_container_main_4 = container_main_first.columns(4)
        with col_container_main_1:
            st.markdown(
                """
                <h3 style="color: #FFC107; font-weight: bold;">Phân tích dữ liệu</h3>
                <p style="font-size: 1rem;"> 
                    Phân tích dữ liệu giá nhà chi tiết và trực quan giúp bạn nắm bắt xu hướng thị trường.
                </p>
                """, unsafe_allow_html=True
            )
            st.markdown(""" 
                        <style>
                        .scroll-button-nav-main {
                            color: #fff !important;
                            border: none;
                            padding: 10px 20px;
                            text-align: center;
                            font-size: 1rem;
                            font-weight: 400;
                            cursor: pointer;
                            border-radius: 5px;
                            background-color: rgb(0 94 124);
                            text-decoration: none;
                        }
                        </style>

                        <a href="#target-section-2" class ="scroll-button-nav-main">
                            Phân tích dữ liệu
                        </a>""", unsafe_allow_html=True)
        with col_container_main_2:
            st.markdown(
                """
                <h3 style="color: #FFC107; font-weight: bold;">Dễ dàng sử dụng</h3>
                <p style="font-size: 1rem;">
                    Giao diện thân thiện, hữu ích và dễ dàng sử dụng cho người dùng ở mọi cấp độ khác nhau.
                </p>
                """, unsafe_allow_html=True
            )
            st.markdown(""" 
                        <style>
                        .scroll-button-nav-main {
                            color: #fff !important;
                            border: none;
                            padding: 10px 20px;
                            text-align: center;
                            font-size: 1rem;
                            font-weight: 400;
                            cursor: pointer;
                            border-radius: 5px;
                            background-color: rgb(0 94 124);
                            text-decoration: none;
                        }
                        </style>

                        <a href="#target-section-3" class ="scroll-button-nav-main">
                            Dễ dàng sử dụng
                        </a>""", unsafe_allow_html=True)
        with col_container_main_3:
            st.markdown(
                """
                <h3 style="color: #FFC107; font-weight: bold;">Dự đoán giá nhà</h3>
                <p style="font-size: 1rem;">
                    Dự đoán giá nhà chính xác dựa trên dữ liệu thực tế và các mô hình học máy tiên tiến.
                </p>
                """, unsafe_allow_html=True
            )
            st.markdown(""" 
                        <style>
                        .scroll-button-nav-main {
                            color: #fff !important;
                            border: none;
                            padding: 10px 20px;
                            text-align: center;
                            font-size: 1rem;
                            font-weight: 400;
                            cursor: pointer;
                            border-radius: 5px;
                            background-color: rgb(0 94 124);
                            text-decoration: none;
                        }
                        </style>

                        <a href="#target-section-4" class ="scroll-button-nav-main">
                            Dự đoán giá nhà
                        </a>""", unsafe_allow_html=True)
        with col_container_main_4:
            st.markdown(
                """
                <h3 style="color: #FFC107; font-weight: bold;">Bảo mật dữ liệu</h3>
                <p style="font-size: 1rem;">
                    Bảo mật thông tin người dùng và dữ liệu trong doanh nghiệp của bạn một cách an toàn.
                </p>
                """, unsafe_allow_html=True
            )
            st.markdown(""" 
                        <style>
                        .scroll-button-nav-main {
                            color: #fff !important;
                            border: none;
                            padding: 10px 20px;
                            text-align: center;
                            font-size: 1rem;
                            font-weight: 400;
                            cursor: pointer;
                            border-radius: 5px;
                            background-color: rgb(0 94 124);
                            text-decoration: none;
                        }
                        </style>

                        <a href="#target-section-5" class ="scroll-button-nav-main">
                            Bảo mật dữ liệu
                        </a>""", unsafe_allow_html=True)
        
        self.arrow_down_design("target-section-2")
        # SECTION 2
        container_main_second = st.container()
        container_main_second.subheader("Phân tích dữ liệu", divider="blue", anchor="target-section-2")
        container_main_second.markdown(
            """
            <p style="font-size: 1.2rem;">
                Mô tả về <span style = "color:#FFC107;">phân tích dữ liệu</span> của ứng dụng
            </p>
            """,
            unsafe_allow_html=True
        )
        col_container_main_5, col_container_main_6 = container_main_second.columns([2,1])
        with col_container_main_5:
            image_container_section_col1 = module_config.get_relative_file_path("../src/image/home/data_system.webp")
            st.markdown(f"""
            <img src="data:image/png;base64,{image_container_section_col1}">
                        """, unsafe_allow_html=True)
        with col_container_main_6:
            st.markdown(
                """
                <h3 style="font-weight: bold;">Phân tích dữ liệu <span style="color:#FFC107">sử dụng</span> dữ liệu thực tế</h3>
                <p style="font-size: 1rem;">Ứng dụng dự đoán giá nhà được thiết kế để phân tích dữ liệu thị trường bất động sản, cung cấp thông tin chi tiết và trực quan về xu hướng giá nhà.
                <br><br> Bằng khả năng giám sát, phân tích theo thời gian thực, ứng dụng không chỉ tổng hợp và xử lý dữ liệu mà còn cung cấp một mô hình dữ liệu trực quan, dễ hiểu thông qua các biểu đồ giúp người dùng nhanh chóng nắm bắt tình hình và đưa ra các quyết định phù hợp, kịp thời. </p>
                                
                """, unsafe_allow_html=True
            )
        self.arrow_down_design("target-section-3")
        # SECTION 3
        container_main_third = st.container()
        container_main_third.subheader("Dễ dàng sử dụng", divider="blue", anchor="target-section-3")
        container_main_third.markdown(
            """
            <p style="font-size: 1.2rem;">
                Mô tả về <span style = "color:#FFC107;">dễ dàng sử dụng</span> của ứng dụng
            </p>
            """,
            unsafe_allow_html=True
        )
        col_container_main_7, col_container_main_8 = container_main_third.columns([2,3])
        with col_container_main_7:
            st.markdown(
                """
                <h3 style="font-weight: bold;">Giao diện thân thiện</h3>
                <p style="font-size: 1rem;">Giao diện của ứng dụng dự đoán giá nhà được thiết kế tối ưu và dễ sử dụng nhằm phù hợp với mọi đối tượng sử dụng. Ứng dụng này tập trung phát triển tính trực quan, thân thiện, giúp người dùng mới có thể nhanh chóng làm quen và thao tác một cách hiệu quả ngay khi bắt đầu sử dụng ứng dụng. Nhờ đó, ứng dụng giúp người dùng truy cập đến các chức năng quan trọng mà không cần trải qua quá nhiều những bước phức tạp, góp phần mang lại trải nghiệm mượt mà và dễ chịu trong công việc.

                </p>
                """, unsafe_allow_html=True)
        with col_container_main_8:
            image_container_section_col2 = module_config.get_relative_file_path("../src/image/home/image_sudung.jpg")
            st.markdown(f"""
            <img src="data:image/png;base64,{image_container_section_col2}">
                        """, unsafe_allow_html=True)
        self.arrow_down_design("target-section-4")
        # SECTION 4
        container_main_fourth = st.container()
        container_main_fourth.subheader("Dự đoán giá nhà", divider="blue", anchor="target-section-4")
        container_main_fourth.markdown(
            """
            <p style="font-size: 1.2rem;">
                Mô tả về <span style = "color:#FFC107;">dự đoán giá nhà</span> của ứng dụng
            </p>
            """,
            unsafe_allow_html=True
        )
        col_container_main_9, col_container_main_10 = container_main_fourth.columns([3,2])
        with col_container_main_9:
            image_container_section_col3 = module_config.get_relative_file_path("../src/image/home/image_hieusuat.png")
            st.markdown(f"""
            <img src="data:image/png;base64,{image_container_section_col3}">
                        """, unsafe_allow_html=True)
        with col_container_main_10:
            st.markdown(
                """
                <h3 style="font-weight: bold;">Dự đoán giá nhà</h3>
                <p style="font-size: 1rem;">Ứng dụng dự đoán giá nhà mang đến khả năng dự đoán giá nhà chính xác dựa trên dữ liệu thực tế và các mô hình học máy tiên tiến. Công cụ này hỗ trợ công việc giám sát, phân tích và đánh giá hiệu quả hoạt động của thị trường bất động sản theo thời gian thực. 
                <br> <br> Sở hữu các tính năng nổi bật như hiển thị bảng dữ liệu trực quan, báo cáo các chỉ số chi tiết, ứng dụng có thể giúp người dùng nắm bắt được tình hình chung của thị trường, từ đó đưa ra được những quyết định hợp lý và đánh giá hiệu quả đầu tư chính xác dựa trên các chỉ số đo lường hiệu suất.
                </p>
                """, unsafe_allow_html=True)
        self.arrow_down_design("target-section-5")
        # SECTION 5
        container_main_fifth = st.container()
        container_main_fifth.subheader("Bảo mật dữ liệu", divider="blue", anchor="target-section-5")
        container_main_fifth.markdown(
            """
            <p style="font-size: 1.2rem;">
                Mô tả về <span style = "color:#FFC107;">bảo mật dữ liệu</span> của ứng dụng
            </p>
            """,
            unsafe_allow_html=True
        )
        col_container_main_11, col_container_main_12 = container_main_fifth.columns([2,1])
        with col_container_main_11:
            st.markdown(
                """
                <h3 style="font-weight: bold;">Bảo mật dữ liệu</h3>
                <p style="font-size: 1rem;">Ứng dụng dự đoán giá nhà cung cấp khả năng bảo mật dữ liệu hiệu quả như kiểm soát thông tin đăng nhập, theo dõi các hoạt động chỉnh sửa của người dùng trên hệ thống, phân quyền truy cập theo mức độ người dùng nhằm tối ưu hóa việc kiểm soát an toàn thông tin và bảo mật dữ liệu. </p>
                """, unsafe_allow_html=True)
        with col_container_main_12:
            image_container_section_col4 = module_config.get_relative_file_path("../src/image/home/image_baomat.jpg")
            st.markdown(f"""
            <img src="data:image/png;base64,{image_container_section_col4}">
                        """, unsafe_allow_html=True)
        self.arrow_up_design("target-section-0")

        


def main():
    # FRONTEND_UI_HOME().sidebar_design()
    FRONTEND_UI_HOME().main_container_design()

main()
module_config.add_sidebar_footer()

