"""Generate a comprehensive, beautifully-formatted Microsoft Word (.docx) document
explaining every section of the Deep Learning Final Project Report (Group 25, Project 19).
"""
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    """Set background color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tc_pr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set internal padding for a cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tc_mar.append(node)
    tc_pr.append(tc_mar)

def create_callout_box(doc, title, text, bg_color="F0F4F8", border_color="1A237E"):
    """Create a beautiful callout box with a colored left border."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    # Left border only
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_borders = OxmlElement('w:tcBorders')
    
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), '24') # 3pt
    left.set(qn('w:space'), '0')
    left.set(qn('w:color'), border_color)
    tc_borders.append(left)
    
    for b_name in ['top', 'bottom', 'right']:
        b = OxmlElement(f'w:{b_name}')
        b.set(qn('w:val'), 'none')
        tc_borders.append(b)
    tc_pr.append(tc_borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    run_t = p.add_run(f"📌 {title}\n")
    run_t.bold = True
    run_t.font.name = "Arial"
    run_t.font.size = Pt(10.5)
    run_t.font.color.rgb = RGBColor(0x1A, 0x23, 0x7E)
    
    run_b = p.add_run(text)
    run_b.font.name = "Calibri"
    run_b.font.size = Pt(10)
    run_b.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    
    # Add small spacing after table
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(2)
    p_spacer.paragraph_format.space_after = Pt(4)

def format_table(table, col_widths, align_center=True):
    """Format table with styled header and alternating row colors."""
    if align_center:
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    for row_idx, row in enumerate(table.rows):
        is_header = (row_idx == 0)
        bg_hex = "1A237E" if is_header else ("F8F9FA" if row_idx % 2 == 1 else "FFFFFF")
        
        for col_idx, cell in enumerate(row.cells):
            cell.width = Inches(col_widths[col_idx])
            set_cell_background(cell, bg_hex)
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            
            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.1
                for run in p.runs:
                    run.font.name = "Arial" if is_header else "Calibri"
                    run.font.size = Pt(9 if is_header else 9)
                    if is_header:
                        run.bold = True
                        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                    else:
                        run.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

def generate_word_doc(out_path="Giai_Thich_Bao_Cao_Group25_Project19.docx"):
    doc = docx.Document()
    
    # Page Margins: 1 inch everywhere
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Styles Setup
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.2
    normal_style.paragraph_format.space_after = Pt(6)

    # Document Header / Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("BẢN GIẢI THÍCH CHI TIẾT BÁO CÁO ĐỒ ÁN DEEP LEARNING\nGROUP 25 — PROJECT 19 (USTH 2026-2027)")
    r_title.bold = True
    r_title.font.name = "Arial"
    r_title.font.size = Pt(16)
    r_title.font.color.rgb = RGBColor(0x1A, 0x23, 0x7E)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run("Đề tài: \"Can Synthetic Images Improve Imbalanced Classification?\"\n(Ảnh nhân tạo có thực sự cải thiện bài toán phân loại dữ liệu mất cân bằng?)")
    r_sub.italic = True
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    # Info Box Table
    info_tbl = doc.add_table(rows=6, cols=2)
    info_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        ("Học phần / Trường:", "Deep Learning Final Exam Projects 2026-2027 — Đại học KH&CN Hà Nội (USTH)"),
        ("Mã nhóm & Đề tài:", "Nhóm 25 — Đề tài số 19"),
        ("Tên file báo cáo:", "Group25_Project19_Report.pdf (11 trang chuẩn học thuật)"),
        ("GitHub Repository:", "https://github.com/hunghh22ba13147-pixel/DL2026-Group25-Project19"),
        ("Giảng viên phụ trách:", "TS. Nghiêm Thị Phương & TS. Trần Giang Sơn"),
        ("Thành viên nhóm (7 bạn):", "Hà Hiệp Hùng (Lead), Trương Việt Hoàng, Vũ Công Thành, Vương Minh Tuấn, Nguyễn Tiến Đạt, Nguyễn Trung Hiếu, Đặng Bình Dương")
    ]
    for idx, (label, val) in enumerate(info_data):
        row = info_tbl.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.text = label
        cell_val.text = val
        cell_lbl.paragraphs[0].runs[0].bold = True
        cell_lbl.paragraphs[0].runs[0].font.color.rgb = RGBColor(0x1A, 0x23, 0x7E)
    format_table(info_tbl, [2.2, 4.3])
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Introduction / Purpose of this Doc
    create_callout_box(
        doc,
        "MỤC ĐÍCH TÀI LIỆU NÀY",
        "Tài liệu này được biên soạn để diễn giải cặn kẽ từng phần trong bài báo cáo học thuật Group25_Project19_Report.pdf. "
        "Mỗi mục đều giải thích rõ: (1) Mục đích phần đó là gì, (2) Số liệu và kết quả thực nghiệm then chốt, và "
        "(3) Lập luận học thuật cốt lõi giúp các thành viên tự tin thuyết trình và trả lời chất vấn phản biện của hội đồng giảng viên."
    )

    # Function for Section Headings
    def add_sec_heading(title, level=1):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14 if level==1 else 10)
        p.paragraph_format.space_after = Pt(4 if level==1 else 3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.bold = True
        run.font.name = "Arial"
        if level == 1:
            run.font.size = Pt(13.5)
            run.font.color.rgb = RGBColor(0x1A, 0x23, 0x7E)
        else:
            run.font.size = Pt(11.5)
            run.font.color.rgb = RGBColor(0x28, 0x35, 0x93)

    # -------------------------------------------------------------
    # MỤC 1: ABSTRACT
    # -------------------------------------------------------------
    add_sec_heading("1. Mục 1: Abstract (Tóm Tắt Toàn Văn Báo Cáo)")
    p = doc.add_paragraph(
        "Mục Abstract là bản tóm lược toàn bộ nghiên cứu trong duy nhất một đoạn văn học thuật cô đọng. "
        "Giảng viên hoặc người đọc chỉ cần đọc mục này là nắm trọn vẹn từ bối cảnh, phương pháp, kết quả đến kết luận của đề tài."
    )
    p_b = doc.add_paragraph()
    p_b.add_run("• Vấn đề nghiên cứu: ").bold = True
    p_b.add_run("Trong học sâu thị giác máy tính, hiện tượng mất cân bằng dữ liệu (Class Imbalance) xảy ra thường xuyên. "
               "Hàm mất mát Cross-Entropy thông thường sẽ tối ưu theo các lớp chiếm số đông, khiến mô hình bị suy thoái nghiêm trọng trên các lớp hiếm (thiểu số).\n")
    p_b.add_run("• Giả thuyết phổ biến: ").bold = True
    p_b.add_run("Nhiều nghiên cứu và kỹ sư cho rằng mạng sinh có điều kiện (cGAN) có thể sinh thêm hàng ngàn ảnh nhân tạo cho lớp hiếm để cân bằng số lượng mẫu, "
               "từ đó giải quyết triệt để vấn đề mất cân bằng.\n")
    p_b.add_run("• Phương pháp thực nghiệm: ").bold = True
    p_b.add_run("Nhóm thiết lập tập dữ liệu CIFAR-10-LT với tỷ lệ mất cân bằng cực lớn IR = 100 (từ 4.950 ảnh xuống chỉ còn 50 ảnh/lớp). "
               "Huấn luyện mạng cGAN ResNet (kèm Spectral Normalization và DiffAugment) thuần túy trên tập train đuôi dài này, "
               "rồi dùng ảnh sinh bổ sung cho mô hình ResNet-32.\n")
    p_b.add_run("• Phát hiện thực nghiệm cốt lõi (Bất ngờ & Phản trực giác): ").bold = True
    p_b.add_run("Ảnh nhân tạo từ cGAN không những không giúp cải thiện mà còn làm tụt giảm hiệu năng! "
               "cGAN Synthetic chỉ đạt 50.26% Accuracy và 46.40% Macro-F1 (thấp hơn cả Baseline gốc 54.28%). "
               "Trong khi đó, phép tăng cường hình học truyền thống (Random Crop & Flip) vọt lên 70.01% Accuracy, "
               "và Random Oversampling kết hợp Augmentation (ROS + Aug) đạt đỉnh 70.09% Accuracy và 69.79% Macro-F1.")

    # -------------------------------------------------------------
    # MỤC 2: INTRODUCTION & RESEARCH MOTIVATION
    # -------------------------------------------------------------
    add_sec_heading("2. Mục 2: Introduction & Research Motivation (Mở Đầu & Câu Hỏi Nghiên Cứu)")
    p = doc.add_paragraph(
        "Mục này nêu bật tính cấp thiết của đề tài trong thực tiễn và đưa ra 3 câu hỏi nghiên cứu (Research Questions - RQ) "
        "định hướng cho toàn bộ bài báo cáo:"
    )
    p_b = doc.add_paragraph()
    p_b.add_run("1. Bối cảnh thực tế: ").bold = True
    p_b.add_run("Trong các bài toán quan trọng như chẩn đoán bệnh hiếm trong y tế (ảnh X-quang/ung thư), nhận diện tai nạn trong xe tự hành, "
               "hay phát hiện gian lận ngân hàng, dữ liệu luôn có phân bố đuôi dài (Long-Tailed): một số ít lớp đa số (Head classes) có bạt ngàn dữ liệu, "
               "còn các lớp cốt lõi cần nhận diện (Tail classes) lại vô cùng hiếm hoi.\n")
    p_b.add_run("2. Cơ chế lỗi của Cross-Entropy: ").bold = True
    p_b.add_run("Do số mẫu đa số quá áp đảo, tổng gradient cập nhật từ các lớp đa số sẽ đè bẹp gradient từ các lớp hiếm. "
               "Ranh giới phân lớp tuyến tính (decision boundary) bị xô lệch về phía lớp hiếm, khiến mô hình đạt độ chính xác ảo (vì đoán toàn lớp đa số) "
               "nhưng Recall trên lớp hiếm gần như bằng 0.\n")
    p_b.add_run("3. Ba câu hỏi nghiên cứu chính (RQ):").bold = True
    
    create_callout_box(
        doc,
        "3 CÂU HỎI NGHIÊN CỨU TRỌNG TÂM CỦA ĐỀ TÀI",
        "• RQ1: Bổ sung ảnh sinh từ cGAN cho các lớp thiểu số có thực sự cải thiện Top-1 Accuracy và Macro-F1 so với mô hình Baseline ERM không?\n"
        "• RQ2: So với các giải pháp mức dữ liệu kinh điển (Conventional Spatial Augmentation như Crop/Flip và Random Oversampling - ROS), phương pháp sinh ảnh nhân tạo có ưu thế hay nhược điểm gì?\n"
        "• RQ3: Những cơ chế lỗi (failure modes), hiện tượng sụp đổ mode (mode collapse) và lệch phân bố (distribution shift) nào xuất hiện khi mạng sinh phải học từ các lớp cực kỳ khan hiếm dữ liệu (50 đến 83 ảnh)?"
    )

    # -------------------------------------------------------------
    # MỤC 3: RELATED WORK AND THEORETICAL FOUNDATIONS
    # -------------------------------------------------------------
    add_sec_heading("3. Mục 3: Related Work (Nghiên Cứu Liên Quan & Cơ Sở Lý Thuyết)")
    p = doc.add_paragraph(
        "Mục này phân tích 3 nhánh nghiên cứu nền tảng để khẳng định cơ sở lý luận vững chắc của nhóm:"
    )
    doc.add_paragraph(
        "• 3.1 Long-Tailed Visual Recognition: Trích dẫn công trình Cui et al. (CVPR 2019) về lý thuyết 'số mẫu hiệu dụng' "
        "(effective number of samples) giải thích tại sao bổ sung thêm mẫu cho lớp đa số không đem lại thêm nhiều thông tin; "
        "Cao et al. (NeurIPS 2019) với LDAM loss thiết lập biên phân cách dựa trên căn bậc bốn của số mẫu; "
        "và Kang et al. (ICLR 2020) với kỹ thuật tách rời học biểu diễn và phân lớp (Decoupling)."
    )
    doc.add_paragraph(
        "• 3.2 Conditional Generative Modeling under Data Scarcity: Trình bày kiến trúc cGAN của Miyato & Koyama (ICLR 2018) "
        "dùng Projection Discriminator để điều kiện hóa nhãn lớp; Spectral Normalization (Miyato et al., 2018) để khống chế hằng số Lipschitz <= 1; "
        "và DiffAugment (Zhao et al., NeurIPS 2020) giúp mạng cGAN học ổn định ngay cả khi tập train rất ít mẫu."
    )
    doc.add_paragraph(
        "• 3.3 Synthetic Data Pitfalls & Model Collapse: Nhắc tới cảnh báo kinh điển của Ravuri & Vinyals (ICLR 2019) và công trình trên tạp chí Nature (2024) "
        "của Shumailov et al. về 'Sự sụp đổ của mô hình' (Model Collapse) khi AI được huấn luyện trên dữ liệu do chính AI tạo ra, "
        "làm mất mát phương sai đặc trưng ở các vùng đuôi của phân bố."
    )

    # -------------------------------------------------------------
    # MỤC 4: DATASET AND DATA PARTITIONING PROTOCOL
    # -------------------------------------------------------------
    add_sec_heading("4. Mục 4: Dataset and Data Partitioning Protocol (Tập Dữ Liệu & Quy Chuẩn Phân Chia)")
    p = doc.add_paragraph(
        "Mục này mô tả chi tiết tập dữ liệu CIFAR-10-LT và quy trình bảo vệ dữ liệu cực kỳ nghiêm ngặt nhằm tránh hoàn toàn hiện tượng rò rỉ (Data Leakage):"
    )
    doc.add_paragraph(
        "• Công thức phân rã hàm mũ (Exponential Decay): Theo chuẩn Cui et al. (2019), số ảnh của lớp c (từ 0 đến 9) tuân theo: "
        "n_c = min( floor( N_max * (1 / IR)^(c / (C - 1)) ), 5000 - V_c ), với N_max = 5000, IR = 100, C = 10, V_c = 50. "
        "Tổng tập train đuôi dài có đúng 12.356 ảnh."
    )
    doc.add_paragraph(
        "• Chính sách Không rò rỉ dữ liệu (Zero Leakage Policy): Nhiều đồ án sinh viên mắc lỗi dùng tập validation mất cân bằng "
        "hoặc để mạng cGAN nhìn thấy tập validation/test. Đồ án của nhóm trích riêng 50 ảnh/lớp (500 ảnh) làm tập Validation cân bằng độc lập. "
        "Mạng cGAN chỉ được train duy nhất trên 12.356 ảnh train đuôi dài. Tập test 10.000 ảnh chuẩn chỉ được đánh giá 1 lần duy nhất."
    )

    # Table of Class Distribution
    p_t1 = doc.add_paragraph()
    p_t1.add_run("Bảng 1b: Phân bố số lượng mẫu huấn luyện chi tiết của CIFAR-10-LT (IR=100)").bold = True
    cdist_tbl = doc.add_table(rows=11, cols=5)
    cdist_data = [
        ("ID Lớp", "Tên Lớp (CIFAR-10)", "Nhóm Phân Phối (Shot)", "Số Ảnh Huấn Luyện", "Tỷ Lệ (%)"),
        ("0", "Airplane (Máy bay)", "Many-shot (>1,000)", "4,950", "40.06%"),
        ("1", "Automobile (Ô tô)", "Many-shot (>1,000)", "2,997", "24.26%"),
        ("2", "Bird (Chim)", "Many-shot (>1,000)", "1,796", "14.54%"),
        ("3", "Cat (Mèo)", "Medium-shot (100-1000)", "1,077", "8.72%"),
        ("4", "Deer (Hươu)", "Medium-shot (100-1000)", "645", "5.22%"),
        ("5", "Dog (Chó)", "Medium-shot (100-1000)", "387", "3.13%"),
        ("6", "Frog (Ếch)", "Medium-shot (100-1000)", "232", "1.88%"),
        ("7", "Horse (Ngựa)", "Few-shot (<100)", "139", "1.12%"),
        ("8", "Ship (Tàu thủy)", "Few-shot (<100)", "83", "0.67%"),
        ("9", "Truck (Xe tải)", "Few-shot (<100)", "50", "0.40%")
    ]
    for r_idx, row_vals in enumerate(cdist_data):
        row = cdist_tbl.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            row.cells[c_idx].text = val
    format_table(cdist_tbl, [0.8, 1.6, 1.8, 1.2, 1.1])
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # MỤC 5: METHODOLOGY & MATHEMATICAL MODELING
    # -------------------------------------------------------------
    add_sec_heading("5. Mục 5: Methodology and Mathematical Modeling (Phương Pháp Nghiên Cứu & Toán Học)")
    doc.add_paragraph(
        "Mục này trình bày chi tiết kiến trúc mô hình và các chứng minh toán học giải thích bản chất vì sao ảnh sinh thất bại:"
    )
    doc.add_paragraph(
        "• 5.1 Classifier Backbone (ResNet-32): Kiến trúc chuẩn cho ảnh 32x32 với đúng 466.906 tham số. "
        "Tối ưu bằng SGD (momentum 0.9, weight decay 5e-4), Cosine Annealing learning rate (0.1 với 500 bước warm-up), "
        "batch size 128, chạy đủ 10.000 bước (~103 epoch) để đảm bảo hội tụ hoàn toàn."
    )
    doc.add_paragraph(
        "• 5.2 Conditional GAN (SN-Projection cGAN + DiffAugment): Generator dùng Conditional Batch Normalization (CondBN). "
        "Discriminator dùng chiếu vector nhãn: D(x, y) = psi(phi(x)) + phi(x)^T e(y) và Spectral Normalization. "
        "Áp dụng DiffAugment (dịch chuyển, đổi màu, cutout) và theo dõi trung bình trượt EMA (decay 0.999) của Generator để sinh ảnh."
    )
    doc.add_paragraph(
        "• 5.3 Sáu chiến lược so sánh: (1) Baseline ERM, (2) Conventional Augmentation (Crop/Flip), (3) Random Oversampling (ROS), "
        "(4) ROS + Aug, (5) cGAN Synthetic (T=1000 và T=5000), (6) cGAN Syn + Conv Aug."
    )
    doc.add_paragraph(
        "• 5.4 Phân tích lý thuyết (Theoretical Analysis):"
    )

    create_callout_box(
        doc,
        "CHỨNG MINH TOÁN HỌC: TẠI SAO ẢNH SINH TỪ GAN LẠI THẤT BẠI TRÊN DỮ LIỆU HIẾM?",
        "1. Sai số xấp xỉ mật độ (Density Estimation Error):\n"
        "Theo Arora et al. (2017), sai số khoảng cách Jensen-Shannon giữa phân bố thật P_c và phân bố sinh G_c bị chặn dưới:\n"
        "       E[JS(P_c || G_c)] >= Omega( d / N_c )\n"
        "Trong đó d là số chiều không gian ảnh, N_c là số lượng mẫu thật. Với lớp đa số (N_0 = 4.950), mẫu dồi dào nên sai số nhỏ. "
        "Nhưng với lớp cực hiếm như Xe tải (N_9 = 50), N_c quá nhỏ dẫn tới sai số cực lớn! Discriminator nhanh chóng 'học vẹt' thuộc lòng 50 ảnh này, "
        "khiến gradient truyền về Generator bị triệt tiêu (vanishing gradient). Generator bị sụp đổ mode (mode collapse) thành một vài điểm mờ.\n\n"
        "2. Giới hạn thích ứng miền Ben-David (Domain Adaptation Bound):\n"
        "Theo định lý Ben-David et al. (2010), sai số thực tế R(f) trên dữ liệu test thật bị chặn bởi:\n"
        "       R(f) <= R_syn(f) + 1/2 * d_HΔH(P_real, P_syn) + lambda\n"
        "Vì ảnh cGAN bị lỗi và mờ nhòe nên khoảng cách phân bố d_HΔH giữa ảnh thật và ảnh sinh là rất lớn. Do đó, dù mạng classifier có học tốt đến mấy trên tập ảnh sinh (R_syn gần 0) "
        "thì sai số trên dữ liệu thật R(f) vẫn rất cao! Ngược lại, phép tăng cường Crop/Flip có d_HΔH = 0 tuyệt đối vì chỉ biến đổi hình học trên chính ảnh thật."
    )

    # -------------------------------------------------------------
    # MỤC 6: EXPERIMENTAL SETUP
    # -------------------------------------------------------------
    add_sec_heading("6. Mục 6: Experimental Setup & Verification Protocol (Thiết Lập Thực Nghiệm)")
    doc.add_paragraph(
        "Mục này đảm bảo tính minh bạch và độ lặp lại của bài báo khoa học. Thực nghiệm được thực thi trên GPU NVIDIA RTX 3060 Laptop (6GB VRAM), "
        "PyTorch 2.5.1, CUDA 12.4. Mọi cấu hình chuẩn được chạy lặp lại qua 3 random seeds độc lập (Seed 0, Seed 1, Seed 2) "
        "để tính trung bình mẫu (mean) và độ lệch chuẩn (std)."
    )

    # -------------------------------------------------------------
    # MỤC 7: RESULTS AND DISCUSSION
    # -------------------------------------------------------------
    add_sec_heading("7. Mục 7: Benchmark Results and Empirical Findings (Kết Quả Thực Nghiệm & Thảo Luận)")
    doc.add_paragraph(
        "Đây là phần quan trọng nhất chứng minh kết luận của đề tài bằng số liệu định lượng cụ thể:"
    )

    # Main Benchmark Table
    p_t2 = doc.add_paragraph()
    p_t2.add_run("Bảng 2: Kết quả đối chuẩn toàn diện trên tập CIFAR-10 Test (Trung bình ± Độ lệch chuẩn qua các Seed)").bold = True
    res_tbl = doc.add_table(rows=8, cols=6)
    res_data = [
        ("Phương Pháp", "Tăng Cường (Aug)", "Số Seed", "Độ Chính Xác (Acc %)", "Macro-F1 (%)", "Few-Shot Recall (%)"),
        ("Baseline (ERM)", "Không", "3", "54.28 ± 2.13", "52.14 ± 3.02", "29.78 ± 8.66"),
        ("Conventional Augmentation", "Crop + Flip", "3", "70.01 ± 0.32", "69.60 ± 0.13", "48.38 ± 2.56"),
        ("Random Oversampling (ROS)", "Không", "3", "45.23 ± 0.31", "42.26 ± 1.54", "21.83 ± 7.29"),
        ("ROS + Conventional Aug.", "Crop + Flip", "3", "70.09 ± 1.84", "69.79 ± 1.99", "51.37 ± 5.73 (Cao nhất)"),
        ("cGAN Synthetic (T=1000)", "Không", "1", "50.26 ± 0.00", "46.40 ± 0.00", "16.73 ± 0.00"),
        ("cGAN Synthetic (T=5000)", "Không", "1", "47.52 ± 0.00", "43.48 ± 0.00", "15.60 ± 0.00 (Tụt sâu)"),
        ("cGAN Syn + Conv Aug (T=1000)", "Crop + Flip", "1", "68.76 ± 0.00", "67.88 ± 0.00", "43.70 ± 0.00")
    ]
    for r_idx, row_vals in enumerate(res_data):
        row = res_tbl.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            row.cells[c_idx].text = val
    format_table(res_tbl, [1.8, 1.0, 0.6, 1.1, 1.0, 1.2])
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "• Trả lời RQ1: Ảnh sinh làm tụt hiệu năng! Khi đệm thêm ảnh sinh cGAN đến T=1000, Accuracy tụt từ 54.28% xuống 50.26% (-4.02%), "
        "Macro-F1 giảm từ 52.14% xuống 46.40% (-5.74%). Khi đệm đến T=5000 (cân bằng hoàn toàn số lượng mẫu 1:1), Accuracy tụt tiếp xuống 47.52% "
        "và Few-shot recall rớt từ 29.78% xuống còn 15.60% (giảm gần một nửa!)."
    )
    doc.add_paragraph(
        "• Trả lời RQ2: Sự vượt trội tuyệt đối của Augmentation truyền thống! Chỉ cần Random Crop & Flip đơn giản, Accuracy đã vọt từ 54.28% lên 70.01% (+15.73%). "
        "Đặc biệt, mô hình ROS kết hợp Augmentation (ROS + Aug) đạt quán quân toàn diện với 70.09% Acc, 69.79% F1 và 51.37% Few-shot recall."
    )
    doc.add_paragraph(
        "• Phân tích độ nhạy theo số lượng ảnh sinh T (Mục 7.3 & Figure 2): Khi tăng T từ 250 -> 500 -> 1000 -> 2500 -> 5000, "
        "tỷ lệ ảnh nhân tạo / ảnh thật ở lớp hiếm tăng từ 5:1 lên tới 100:1! Dòng gradient từ ảnh nhân tạo lấn át hoàn toàn ảnh thật, "
        "khiến mô hình bị suy thoái hiệu năng đơn điệu (Monotonic degradation)."
    )

    # -------------------------------------------------------------
    # MỤC 8: ERROR & QUALITATIVE ANALYSIS
    # -------------------------------------------------------------
    add_sec_heading("8. Mục 8: In-Depth Error Diagnostics (Chẩn Đoán Lỗi & Phân Tích Định Tính)")
    doc.add_paragraph(
        "Mục này phân tích nguyên nhân sâu xa đằng sau hiện tượng tụt giảm hiệu năng:"
    )
    doc.add_paragraph(
        "• 8.1 Sụp đổ Mode (Mode Collapse - Figure 3): Khi quan sát lưới ảnh sinh 10x10 từ G_ema (Figure 3), "
        "ở các lớp đầu (Máy bay, Ô tô) ảnh sinh có kết cấu rõ ràng. Nhưng ở các lớp cuối (Ngựa, Tàu, Xe tải), "
        "mạng chỉ sinh ra các mảng màu bệt mờ nhạt lặp đi lặp lại. Khi đưa 4.950 ảnh xe tải sinh này vào huấn luyện, "
        "mô hình ResNet-32 bị 'học thuộc' các tạo tác giả mạo (artifacts) thay vì học đặc trưng xe tải thật."
    )
    doc.add_paragraph(
        "• 8.2 Lệch phân bố & Ma trận nhầm lẫn (Figure 4): Trên ma trận nhầm lẫn chuẩn hóa, mô hình cGAN thường xuyên đoán nhầm lớp hiếm "
        "sang các lớp lân cận (Xe tải bị nhầm thành Ô tô, Chó bị nhầm thành Mèo). Do ảnh cGAN thiếu chi tiết biên cạnh tần số cao, "
        "classifier chỉ bấu víu vào màu sắc tần số thấp chung chung."
    )
    doc.add_paragraph(
        "• 8.3 Hình học không gian đặc trưng: Các mẫu ảnh nhân tạo ép biểu diễn của lớp thiểu số co cụm vào một miền con hẹp. "
        "Khi kiểm tra với ảnh test tự nhiên có góc chụp đa dạng, các ảnh thật rơi ra ngoài ranh giới phân loại, tạo ra tỷ lệ False Negative cực cao."
    )

    # -------------------------------------------------------------
    # MỤC 9: PRACTICAL ENGINEERING RECOMMENDATIONS
    # -------------------------------------------------------------
    add_sec_heading("9. Mục 9: Practical Engineering Recommendations (Khuyến Nghị Kỹ Thuật Thực Tế)")
    create_callout_box(
        doc,
        "4 BÀI HỌC KỸ THUẬT THỰC CHIẾN RÚT RA TỪ NGHIÊN CỨU",
        "1. Đừng vội vàng sinh ảnh khi dữ liệu hiếm (<100 mẫu): Mạng sinh chưa qua chọn lọc sẽ đưa thêm nhiễu vào dữ liệu hơn là tín hiệu có ích. Phép tăng cường hình học luôn phải là ưu tiên số 1.\n"
        "2. Kết hợp Oversampling với điều chuẩn mạnh: Oversampling đơn thuần sẽ bị học vẹt (45.23%), nhưng khi đi kèm phép xoay/lật/cắt (ROS + Aug) sẽ tạo nên mô hình mạnh nhất (70.09%).\n"
        "3. Luôn giám sát bằng tập Validation cân bằng: Đánh giá bằng tập validation mất cân bằng sẽ tạo ảo tưởng mô hình đang học tốt, trong khi lớp hiếm đang bị bỏ rơi hoàn toàn.\n"
        "4. Kiểm định độ đa dạng ảnh sinh trước khi train: Bắt buộc phải tính toán độ đa dạng nội lớp (LPIPS, khoảng cách cosine) của ảnh do AI sinh trước khi nạp vào mạng thị giác."
    )

    # -------------------------------------------------------------
    # MỤC 10 & 11: LIMITATIONS & CONCLUSION
    # -------------------------------------------------------------
    add_sec_heading("10. Mục 10 & 11: Limitations and Conclusion (Giới Hạn & Kết Luận)")
    doc.add_paragraph(
        "• Giới hạn của nghiên cứu: Nhóm tập trung vào mạng cGAN huấn luyện từ đầu (from scratch) trên CIFAR-10. "
        "Các mô hình Diffusion tiền huấn luyện khổng lồ (như Stable Diffusion) có thể sinh tốt hơn nhờ tri thức tích lũy từ trước, "
        "nhưng sẽ vi phạm quy tắc rò rỉ dữ liệu ngoài. Đồng thời, nghiên cứu chưa áp dụng bộ lọc ảnh dựa trên độ tự tin (Confidence Filtering)."
    )
    doc.add_paragraph(
        "• Kết luận đanh thép: Nghiên cứu khẳng định câu trả lời cho câu hỏi ở tiêu đề là KHÔNG — Việc sinh thêm ảnh bằng cGAN "
        "không giúp cải thiện mà còn làm suy thoái mô hình phân loại mất cân bằng do hiện tượng sụp đổ mode và lệch phân bố. "
        "Các phương pháp biến đổi hình học truyền thống (Crop/Flip) và ROS + Aug vẫn là vũ khí vượt trội, đơn giản và hiệu quả nhất."
    )

    # -------------------------------------------------------------
    # MỤC 12 & PHỤ LỤC: REFERENCES & REPRODUCIBILITY
    # -------------------------------------------------------------
    add_sec_heading("11. Mục 12 & Phụ lục: References & Reproducibility Checklist (Tài Liệu & Tái Lập)")
    doc.add_paragraph(
        "• 20 Tài liệu tham khảo: Trích dẫn đầy đủ các công trình kinh điển từ Krizhevsky (2009), Goodfellow (2014), He et al. ResNet (2016), "
        "Cui et al. CB-Loss (2019), Cao et al. LDAM (2019), Zhao et al. DiffAugment (2020), đến Shumailov et al. (Nature 2024)."
    )
    doc.add_paragraph(
        "• Bảng 4 Phụ lục: Kê khai cấu hình kiểm thử (NVIDIA RTX 3060, i7-12700H, RAM 32GB, PyTorch 2.5.1, CUDA 12.4), "
        "câu lệnh chạy toàn bộ thực nghiệm (python src/run_experiments.py --device cuda) và câu lệnh biên dịch báo cáo PDF "
        "(python src/build_report.py Group25_Project19_Report.pdf) kèm link GitHub để người chấm kiểm tra độ lặp lại 100%."
    )

    # Save Document
    doc.save(out_path)
    print(f"Successfully generated Word document: {out_path}")

if __name__ == "__main__":
    generate_word_doc()
