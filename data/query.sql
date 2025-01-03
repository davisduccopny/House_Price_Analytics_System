-- Tạo Table địa chỉ tp/phường xã /
----------------------------------
CREATE TABLE public.tablename (
	tinh_thanh_pho varchar(30) NULL,
	ma_tp varchar(30) NULL,
	quan_huyen varchar(30) NULL,
	ma_qh varchar(30) NULL,
	phuong_xa varchar(30) NULL,
	ma_px varchar(30) NULL
);
----------------------------------
-- Tạo table lưu thông tin bds
-----------------------------------------
CREATE TABLE public.thong_tin_bat_dong_san (
	id BIGINT PRIMARY KEY AUTOINCREMENT,
	tieu_de varchar(255) ,
	dia_chi varchar(255) ,
	dien_tich varchar(35) ,
	gia varchar(35) ,
	so_phong_ngu varchar(35) ,
	so_phong_vs varchar(35) ,
	noi_that varchar(50) ,
	phap_ly varchar(50) ,
	huong_nha varchar(50) ,
	huong_ban_cong varchar(50) ,
	so_tang varchar(35) ,
	mat_tien varchar(30) ,
	duong_vao varchar(30) ,
	loai_bds varchar(50) ,
	toa_do varchar(100) ,
	latitude float8 ,
	longitude float8 
);
---------------------------------------------------------
-- public.danh_dau_cac_thong_tin_merge
CREATE VIEW danh_dau_cac_thong_tin_test_merged AS
SELECT 
    -- Các cột từ view ban đầu
    v.dia_chi, 
    v.gia, 
    v.kieu_bds,
    v.tinh_thanh_pho,
    v.quan_huyen,
    v.phuong_xa,
    v.chi_tiet,
    v.ten_duong,
    v.dien_tich_chuan,
    v.so_phong_ngu_danh_dau,
    v.so_phong_vs_danh_dau,
    v.noi_that_danh_dau,
    v.phap_ly_danh_dau,
    v.huong_nha_danh_dau,
    v.huong_ban_cong_danh_dau,
    v.so_tang_danh_dau,
    v.mat_tien_danh_dau,
    v.duong_vao_danh_dau,

    -- Các cột mã từ bảng table_name
    t.ma_tp, 
    t.ma_qh, 
    t.ma_px

FROM 
    danh_dau_cac_thong_tin_test v  -- VIEW đã có
JOIN 
    tablename t  -- Bảng chứa mã tỉnh, quận, xã
ON 
    v.tinh_thanh_pho = t.tinh_thanh_pho
    AND v.quan_huyen = t.quan_huyen
    AND v.phuong_xa = t.phuong_xa;
   

   ---------------------------------
   -- public.danh_dau_cac_thong_tin_test source

CREATE OR REPLACE VIEW public.danh_dau_cac_thong_tin_test
AS SELECT dia_chi,
    gia,
        CASE
            WHEN dia_chi::text ~~ '%Dự án%'::text THEN 'Căn hộ/Chung cư/Dự án'::text
            ELSE 'Khác'::text
        END AS kieu_bds,
    TRIM(BOTH FROM split_part(dia_chi::text, ','::text, array_length(regexp_split_to_array(dia_chi::text, ','::text), 1))) AS tinh_thanh_pho,
        CASE
            WHEN array_length(regexp_split_to_array(dia_chi::text, ','::text), 1) > 1 THEN TRIM(BOTH FROM split_part(dia_chi::text, ','::text, array_length(regexp_split_to_array(dia_chi::text, ','::text), 1) - 1))
            ELSE NULL::text
        END AS quan_huyen,
        CASE
            WHEN array_length(regexp_split_to_array(dia_chi::text, ','::text), 1) > 2 THEN TRIM(BOTH FROM split_part(dia_chi::text, ','::text, array_length(regexp_split_to_array(dia_chi::text, ','::text), 1) - 2))
            ELSE NULL::text
        END AS phuong_xa,
    TRIM(BOTH FROM split_part(dia_chi::text, ','::text, 1)) AS chi_tiet,
    TRIM(BOTH FROM split_part(dia_chi::text, ','::text, 2)) AS ten_duong,
        CASE
            WHEN regexp_replace(dien_tich::text, '[^\d]'::text, ''::text, 'g'::text) ~ '^\d+$'::text THEN (( SELECT regexp_matches(thong_tin_bat_dong_san.dien_tich::text, '^\d+'::text) AS regexp_matches))[1]::integer
            ELSE NULL::integer
        END AS dien_tich_chuan,
        CASE
            WHEN so_phong_ngu::text = 'Không có thông tin'::text THEN NULL::character varying::text
            ELSE regexp_replace(so_phong_ngu::text, 'phòng'::text, ''::text, 'gi'::text)
        END AS so_phong_ngu_danh_dau,
        CASE
            WHEN so_phong_vs::text = 'Không có thông tin'::text THEN NULL::character varying::text
            ELSE regexp_replace(so_phong_vs::text, 'phòng'::text, ''::text, 'gi'::text)
        END AS so_phong_vs_danh_dau,
        CASE
            WHEN noi_that::text = 'Cơ bản'::text THEN 1
            WHEN noi_that::text = 'Đầy đủ'::text THEN 2
            WHEN noi_that::text = 'Không có thông tin'::text THEN NULL::integer
            ELSE 0
        END AS noi_that_danh_dau,
        CASE
            WHEN phap_ly::text = 'Sổ đỏ/Sổ hồng'::text THEN 0
            WHEN phap_ly::text = 'Đang chờ sổ'::text THEN 1
            WHEN phap_ly::text = 'Sổ đỏ'::text THEN 2
            WHEN phap_ly::text = 'Sổ hồng'::text THEN 3
            WHEN phap_ly::text = 'Không có thông tin'::text THEN NULL::integer
            ELSE 0
        END AS phap_ly_danh_dau,
        CASE
            WHEN huong_nha::text = 'Tây - Bắc'::text THEN 1
            WHEN huong_nha::text = 'Đông - Nam'::text THEN 2
            WHEN huong_nha::text = 'Đông - Bắc'::text THEN 3
            WHEN huong_nha::text = 'Tây - Nam'::text THEN 4
            WHEN huong_nha::text = 'Bắc'::text THEN 5
            WHEN huong_nha::text = 'Nam'::text THEN 6
            WHEN huong_nha::text = 'Đông'::text THEN 7
            WHEN huong_nha::text = 'Tây'::text THEN 8
            WHEN huong_nha::text = 'Không có thông tin'::text THEN NULL::integer
            ELSE 0
        END AS huong_nha_danh_dau,
        CASE
            WHEN huong_ban_cong::text = 'Tây - Bắc'::text THEN 1
            WHEN huong_ban_cong::text = 'Đông - Nam'::text THEN 2
            WHEN huong_ban_cong::text = 'Đông - Bắc'::text THEN 3
            WHEN huong_ban_cong::text = 'Tây - Nam'::text THEN 4
            WHEN huong_ban_cong::text = 'Bắc'::text THEN 5
            WHEN huong_ban_cong::text = 'Nam'::text THEN 6
            WHEN huong_ban_cong::text = 'Đông'::text THEN 7
            WHEN huong_ban_cong::text = 'Tây'::text THEN 8
            WHEN huong_ban_cong::text = 'Không có thông tin'::text THEN NULL::integer
            ELSE 0
        END AS huong_ban_cong_danh_dau,
        CASE
            WHEN so_tang::text = 'Không có thông tin'::text THEN NULL::character varying::text
            ELSE regexp_replace(so_tang::text, 'tầng'::text, ''::text, 'gi'::text)
        END AS so_tang_danh_dau,
        CASE
            WHEN mat_tien::text = 'Không có thông tin'::text THEN NULL::character varying::text
            ELSE regexp_replace(mat_tien::text, ' m'::text, ''::text, 'gi'::text)
        END AS mat_tien_danh_dau,
        CASE
            WHEN duong_vao::text = 'Không có thông tin'::text THEN NULL::character varying::text
            ELSE regexp_replace(duong_vao::text, ' m'::text, ''::text, 'gi'::text)
        END AS duong_vao_danh_dau
   FROM thong_tin_bat_dong_san;
   ----------------------------------------
-- Đánh dấu thong tin 
 CREATE VIEW danh_dau_cac_thong_tin AS
SELECT 
    ttbds.*, 
    
    -- Phân loại kiểu bất động sản
    CASE 
        WHEN dia_chi LIKE '%Dự án%' THEN 'Căn hộ/Chung cư/Dự án'
        ELSE 'Khác'
    END AS kieu_bds,

    -- Tỉnh/Thành phố (Lấy phần sau dấu phẩy cuối cùng)
    TRIM(split_part(dia_chi, ',', array_length(regexp_split_to_array(dia_chi, ','), 1))) AS tinh_thanh_pho,

    -- Quận/Huyện (Lấy phần từ dấu phẩy thứ 2 từ cuối)
    CASE
        WHEN array_length(regexp_split_to_array(dia_chi, ','), 1) > 1 THEN
            TRIM(split_part(dia_chi, ',', array_length(regexp_split_to_array(dia_chi, ','), 1) - 1))
        ELSE
            NULL
    END AS quan_huyen,

    -- Xã/Phường (Lấy phần từ dấu phẩy thứ 3 từ cuối)
    CASE
        WHEN array_length(regexp_split_to_array(dia_chi, ','), 1) > 2 THEN
            TRIM(split_part(dia_chi, ',', array_length(regexp_split_to_array(dia_chi, ','), 1) - 2))
        ELSE
            NULL
    END AS phuong_xa,

    -- Tách toàn bộ thông tin trước dấu phẩy đầu tiên (Số nhà và tên đường)
    TRIM(split_part(dia_chi, ',', 1)) AS chi_tiet,

    -- Tách Đường
    TRIM(split_part(dia_chi, ',', 2)) AS ten_duong

FROM thong_tin_bat_dong_san ttbds;


