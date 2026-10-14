
import streamlit as st

# ==========================
# CẤU HÌNH GIAO DIỆN
# ==========================
st.set_page_config(
    page_title="Tính chỉ số DTI",
    page_icon="💰",
    layout="centered"
)

st.title("💰 CÔNG CỤ TÍNH CHỈ SỐ DTI")
st.write(
    "Nhập thông tin khoản vay, thu nhập và chi phí "
    "để tính chỉ số DTI."
)

st.divider()

# ==========================
# NHẬP THÔNG TIN
# ==========================
st.subheader("1. Thông tin khoản vay")

col1, col2 = st.columns(2)

with col1:
    so_tien_vay = st.number_input(
        "Số tiền vay (VNĐ)",
        min_value=0,
        value=800_000_000,
        step=10_000_000,
        format="%d"
    )

    thoi_han_vay = st.number_input(
        "Thời hạn vay (năm)",
        min_value=1,
        value=5,
        step=1
    )

    lai_suat = st.number_input(
        "Lãi suất vay (%/năm)",
        min_value=0.0,
        value=12.0,
        step=0.5,
        format="%.2f"
    )

with col2:
    thu_nhap = st.number_input(
        "Thu nhập hàng tháng (VNĐ)",
        min_value=0,
        value=45_000_000,
        step=1_000_000,
        format="%d"
    )

    no_cu = st.number_input(
        "Nợ cũ phải trả hàng tháng (VNĐ)",
        min_value=0,
        value=10_000_000,
        step=500_000,
        format="%d"
    )

st.subheader("2. Chi phí sinh hoạt")

col3, col4 = st.columns(2)

with col3:
    chi_phi_sinh_hoat = st.number_input(
        "Chi phí sinh hoạt/người/tháng (VNĐ)",
        min_value=0,
        value=4_000_000,
        step=500_000,
        format="%d"
    )

with col4:
    so_nguoi = st.number_input(
        "Số người trong gia đình",
        min_value=1,
        value=3,
        step=1
    )

st.divider()

# ==========================
# TÍNH TOÁN DTI
# ==========================
if st.button("📊 TÍNH CHỈ SỐ DTI", type="primary",
             use_container_width=True):

    if thu_nhap <= chi_phi_sinh_hoat * so_nguoi:
        st.error(
            "Thu nhập phải lớn hơn tổng chi phí sinh hoạt "
            "của gia đình để tính DTI."
        )

    elif thoi_han_vay <= 0:
        st.error("Thời hạn vay phải lớn hơn 0.")

    else:
        # Tiền gốc phải trả hàng tháng
        tien_goc_hang_thang = (
            so_tien_vay / (thoi_han_vay * 12)
        )

        # Tiền lãi hàng tháng
        tien_lai_hang_thang = (
            so_tien_vay * (lai_suat / 100 / 12)
        )

        # Tổng nghĩa vụ trả nợ hàng tháng
        tong_tra_no = (
            tien_goc_hang_thang
            + tien_lai_hang_thang
            + no_cu
        )

        # Tổng chi phí sinh hoạt gia đình
        tong_chi_phi = chi_phi_sinh_hoat * so_nguoi

        # Thu nhập còn lại sau chi phí sinh hoạt
        thu_nhap_con_lai = thu_nhap - tong_chi_phi

        # Chỉ số DTI
        dti = tong_tra_no / thu_nhap_con_lai

        # ==========================
        # HIỂN THỊ KẾT QUẢ
        # ==========================
        st.subheader("3. Kết quả tính toán")

        col5, col6 = st.columns(2)

        with col5:
            st.metric(
                "Chỉ số DTI",
                f"{dti * 100:.2f}%"
            )

        with col6:
            st.metric(
                "Tổng tiền trả nợ/tháng",
                f"{tong_tra_no:,.0f} VNĐ"
            )

        st.write(
            f"**Thu nhập hàng tháng:** "
            f"{thu_nhap:,.0f} VNĐ"
        )
        st.write(
            f"**Tổng chi phí sinh hoạt:** "
            f"{tong_chi_phi:,.0f} VNĐ"
        )
        st.write(
            f"**Thu nhập còn lại:** "
            f"{thu_nhap_con_lai:,.0f} VNĐ"
        )

        st.progress(min(max(dti, 0.0), 1.0))

        # Quy tắc kết luận theo yêu cầu
        if dti < 0.70:
            st.error(
                "✅ ĐƯỢC VAY — DTI nhỏ hơn 70%."
            )
        else:
            st.success(
                "❌ KHÔNG ĐƯỢC VAY— DTI lớn hơn hoặc bằng 70%."
            )

        st.caption(
            "Công thức: DTI = Tổng nghĩa vụ trả nợ hàng tháng "
            "/ (Thu nhập hàng tháng - Tổng chi phí sinh hoạt)."
        )
