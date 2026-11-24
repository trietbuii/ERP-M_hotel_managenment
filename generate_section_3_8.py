# -*- coding: utf-8 -*-
import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_table_borders(table, color="000000", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_section_3_8_docx_v4(output_path):
    doc = Document()
    
    # Page setup
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0, 0, 0)
    
    def add_p(text, bold=False, italic=False, size=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.name = 'Times New Roman'
        run.font.size = Pt(size)
        return p

    def add_heading_main(text):
        return add_p(text, bold=True, size=13, space_before=12, space_after=6)

    def add_subheading(text):
        return add_p(text, bold=True, size=12.5, space_before=8, space_after=4)

    def add_figure_caption(text):
        return add_p(text, italic=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=8)

    def add_table_title(text):
        return add_p(text, bold=True, size=12, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=8, space_after=4)

    def format_table(table, col_widths, headers, rows):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table)
        
        # Header
        hdr_cells = table.rows[0].cells
        for i, h_text in enumerate(headers):
            hdr_cells[i].text = h_text
            set_cell_background(hdr_cells[i], "F0F0F0")
            set_cell_margins(hdr_cells[i], 120, 120, 140, 140)
            p = hdr_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            run = p.runs[0]
            run.bold = True
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10.5)
            
        # Data rows
        for row_idx, data_row in enumerate(rows):
            row_cells = table.add_row().cells
            for col_idx, cell_value in enumerate(data_row):
                row_cells[col_idx].text = str(cell_value)
                set_cell_margins(row_cells[col_idx], 80, 80, 100, 100)
                p = row_cells[col_idx].paragraphs[0]
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.15
                if col_idx == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                elif col_idx == 1:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                if p.runs:
                    p.runs[0].font.name = 'Times New Roman'
                    p.runs[0].font.size = Pt(10)

        # Set widths
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = width

    # Content generation
    add_heading_main("3.8. Quy trình quản trị tài sản và bảo trì trang thiết bị buồng phòng")
    
    intro_p = (
        "Quy trình quản trị tài sản và bảo trì trang thiết bị buồng phòng giữ vai trò then chốt trong "
        "việc duy trì năng lực phục vụ, bảo toàn giá trị cơ sở vật chất, tối ưu hóa chi phí đầu tư tài sản cố định "
        "và chi phí vận hành, đồng thời bảo đảm duy trì xuyên suốt tiêu chuẩn dịch vụ lưu trú 4 sao tại chuỗi "
        "Khách Sạn M (Cơ sở 1: Thôn Dương Liễu Tây, xã Bình Dương, tỉnh Gia Lai). Quy trình được chuẩn hóa dựa trên "
        "sự kết hợp giữa phân hệ Quản lý buồng phòng, phân hệ Kỹ thuật & Bảo trì trên hệ thống Odoo 19 "
        "và quy chuẩn kiểm tra kỹ thuật thực tế (SOP) tại buồng phòng."
    )
    add_p(intro_p)
    
    add_subheading("3.8.1. BPMN")
    add_figure_caption("Hình 3.70: Sơ đồ BPMN quy trình quản trị tài sản và bảo trì trang thiết bị buồng phòng chuỗi Khách Sạn M")
    
    add_subheading("3.8.2. Đặc tả")
    add_subheading("3.8.2.1. Đặc tả các bước của quy trình")
    add_table_title("Bảng 3.22: Đặc tả các bước quy trình quản trị tài sản và bảo trì trang thiết bị buồng phòng")
    
    steps_data = [
        ("1", "Bộ phận Buồng phòng / Lễ tân", "Phát hiện hư hỏng thiết bị (hoặc kích hoạt lịch bảo dưỡng định kỳ)",
         "Nhân viên buồng phòng rà soát thiết bị khi dọn phòng (hoặc bộ phận kỹ thuật chủ động khởi tạo yêu cầu bảo dưỡng phòng ngừa định kỳ trên hệ thống)."),
        ("2", "Bộ phận Buồng phòng", "Lập biên bản sự cố buồng phòng",
         "Nhân viên mở phân hệ Sự cố & Hư hỏng buồng phòng, tạo mới biên bản: chọn số phòng, nhập tiêu đề tóm tắt lỗi hỏng hóc và chọn mức độ nghiêm trọng (Nhẹ, Trung bình, Nghiêm trọng)."),
        ("3", "Bộ phận Buồng phòng", "Đánh giá mức độ nghiêm trọng và quyết định khóa phòng",
         "Cổng rẽ nhánh: Nếu sự cố ảnh hưởng trực tiếp đến việc phục vụ khách (như điều hòa hỏng, chập điện), nhân viên tích chọn Khóa phòng để chặn đón khách."),
        ("4", "Hệ thống ERP", "Tự động chuyển trạng thái phòng sang “Bảo trì / Sửa chữa”",
         "Hệ thống ngay lập tức chuyển trạng thái phòng sang Bảo trì / Sửa chữa (màu cam/nâu) trên sơ đồ phòng trực quan, tự động chặn mọi thao tác đặt và xếp phòng của lễ tân."),
        ("5", "Bộ phận Buồng phòng", "Bấm nút “Tạo Yêu Cầu Sửa Chữa (Kỹ Thuật)”",
         "Trên giao diện biên bản sự cố, nhân viên bấm nút chuyển giao để bàn giao lệnh công tác sang phân hệ Kỹ thuật & Bảo trì. Trạng thái sự cố chuyển sang Đang xử lý."),
        ("6", "Hệ thống ERP", "Tự động sinh Phiếu yêu cầu bảo trì kỹ thuật",
         "Hệ thống tự động tạo bản ghi Phiếu yêu cầu sửa chữa, tự động gắn số phòng phát sinh, kế thừa tiêu đề sự cố, liên kết biên bản sự cố gốc và gán mức độ ưu tiên tương ứng."),
        ("7", "Trưởng bộ phận Kỹ thuật", "Tiếp nhận phiếu bảo trì và chọn thiết bị cần sửa chữa",
         "Mở danh sách phiếu tại phân hệ Kỹ thuật, mở chi tiết phiếu bảo trì và chọn thiết bị cụ thể cần can thiệp từ danh mục thiết bị đã được trang bị tại phòng."),
        ("8", "Trưởng bộ phận Kỹ thuật", "Phân công kỹ thuật viên và lên lịch xử lý",
         "Chỉ định kỹ thuật viên chuyên trách phụ trách trực tiếp, gán đội bảo trì và thiết lập thời gian dự kiến hoàn thành."),
        ("9", "Kỹ thuật viên", "Chuyển phiếu sang “Đang thực hiện” và đến hiện trường",
         "Trên bảng Kanban bảo trì, kéo phiếu sang cột Đang thực hiện, chuẩn bị trang thiết bị đồ nghề chuyên dụng và di chuyển đến phòng để khảo sát thực tế."),
        ("10", "Kỹ thuật viên", "Khảo sát hiện trường và chẩn đoán nguyên nhân sự cố",
         "Đo đạc các thông số kỹ thuật, đối chiếu mã định danh số Serial gắn trên thiết bị thực tế với hồ sơ quản lý tài sản để xác định chính xác nguyên nhân hỏng hóc."),
        ("11", "Kỹ thuật viên", "Cổng rẽ nhánh: Xác định phương án linh kiện thay thế",
         "Đánh giá tình trạng thiết bị: Nếu là lỗi nhẹ có thể xử lý tại chỗ thì tiến hành sửa chữa, bảo dưỡng; nếu linh kiện bị hư hỏng thì chuyển sang luồng xuất phụ tùng thay thế."),
        ("12", "Kỹ thuật viên", "[Không thay linh kiện] Thực hiện bảo dưỡng / sửa chữa tại chỗ",
         "Thực hiện các thao tác kỹ thuật: vệ sinh màng lọc gió, xịt rửa dàn tản nhiệt, nạp bổ sung gas, siết chặt các điểm đấu nối điện hoặc thông tắc đường ống nước ngưng."),
        ("13", "Kỹ thuật viên & Thủ kho", "[Có thay linh kiện] Xuất kho phụ tùng trên phân hệ Tồn kho",
         "Kỹ thuật viên thông báo cho thủ kho; thủ kho kiểm tra và lập phiếu xuất kho nội bộ trên phân hệ Tồn kho để xuất cấp đúng chủng loại phụ tùng thay thế."),
        ("14", "Kỹ thuật viên", "Lắp đặt phụ tùng thay thế và hoàn thiện thiết bị",
         "Tiến hành tháo dỡ linh kiện hư hỏng, lắp ráp phụ tùng thay thế mới đúng quy chuẩn kỹ thuật và tiêu chuẩn an toàn của nhà sản xuất."),
        ("15", "Kỹ thuật viên", "Vận hành thử nghiệm và kiểm tra an toàn kỹ thuật",
         "Bật thiết bị vận hành liên tục 15-30 phút dưới tải tiêu chuẩn, kiểm tra nhiệt độ làm việc, dòng điện định mức, kiểm tra rò rỉ và đo độ ồn hoạt động."),
        ("16", "Kỹ thuật viên", "Ghi nhận thời lượng công tác và mô tả phương án xử lý",
         "Cập nhật tổng số giờ làm việc thực tế và ghi chú chi tiết phương án kỹ thuật đã khắc phục vào phần mô tả của phiếu bảo trì trên hệ thống."),
        ("17", "Kỹ thuật viên", "Chuyển phiếu bảo trì sang trạng thái “Đã sửa chữa”",
         "Kéo phiếu bảo trì sang cột Đã sửa chữa trên bảng Kanban để xác nhận hoàn tất lệnh công tác của bộ phận kỹ thuật."),
        ("18", "Bộ phận Buồng phòng", "Kiểm tra hiện trường và nghiệm thu thiết bị sau sửa chữa",
         "Nhân viên buồng phòng đến phòng kiểm tra thiết bị vận hành ổn định, khu vực làm việc sạch sẽ, gọn gàng và xác nhận hoàn thành công tác bảo trì."),
        ("19", "Bộ phận Buồng phòng", "Xác nhận “Đã khắc phục” trên biên bản sự cố gốc",
         "Nhân viên mở lại biên bản sự cố buồng phòng gốc, bấm nút xác nhận Đã khắc phục. Trạng thái biên bản sự cố chính thức chuyển sang Đã khắc phục."),
        ("20", "Hệ thống ERP", "Tự động chuyển trạng thái phòng sang “Cần dọn dẹp”",
         "Hệ thống tự động giải phóng cờ khóa phòng, chuyển trạng thái phòng từ Bảo trì / Sửa chữa về Cần dọn dẹp (màu xanh dương) để buồng phòng làm sạch trước khi đón khách."),
        ("21", "Bộ phận Buồng phòng", "Tiến hành vệ sinh buồng phòng và hoàn tất",
         "Thực hiện lau chùi, khử khuẩn, bổ sung đồ vải và đồ tiêu hao amenities theo đúng định mức buồng phòng, sau đó bấm hoàn tất dọn phòng."),
        ("22", "Hệ thống ERP", "Khôi phục trạng thái phòng sang “Sẵn sàng” đón khách",
         "Hệ thống tự động đổi trạng thái phòng sang Sẵn sàng với màu xanh lá trên sơ đồ phòng trực quan, cho phép lễ tân tiếp tục xếp khách lưu trú."),
        ("23", "Hệ thống ERP", "Tự động lưu vết lịch sử bảo trì trên hồ sơ phòng",
         "Hệ thống tự động cộng dồn số lần bảo trì trên nút thống kê của phòng và lưu trữ toàn bộ lịch sử các phiếu sửa chữa đã thực hiện tại phòng.")
    ]
    format_table(doc.add_table(rows=1, cols=4), [Inches(0.5), Inches(1.8), Inches(2.3), Inches(2.4)],
                 ["STT", "Đối tượng thực hiện", "Mô tả các bước", "Ghi chú"], steps_data)
                 
    add_subheading("3.8.2.2. Đặc tả thư viện dữ liệu")
    
    # a. Danh mục thiết bị trong phòng
    add_subheading("a. Danh mục thiết bị trong phòng (maintenance.equipment)")
    add_table_title("Bảng 3.23: Đặc tả thư viện dữ liệu thiết bị trong phòng")
    equip_data = [
        ("1", "Tên thiết bị", "Tên nhận diện của thiết bị (Ví dụ: Điều hòa Daikin 1.5HP, Tivi Samsung 43 inch).", "Trường bắt buộc nhập."),
        ("2", "Số Serial", "Số Serial Number / Mã vạch của nhà sản xuất gắn trên máy (Ví dụ: DAIKIN-15-104-GL).", "Duy nhất theo từng thiết bị."),
        ("3", "Phòng đặt thiết bị", "Số phòng khách sạn được bố trí lắp đặt thiết bị này.", "Khóa ngoại liên kết danh mục phòng."),
        ("4", "Nhóm thiết bị", "Chủng loại thiết bị (Điện tử, Điện lạnh, Thiết bị vệ sinh...).", "Khóa ngoại nhóm thiết bị."),
        ("5", "Đội ngũ bảo trì", "Đội kỹ thuật phụ trách bảo dưỡng (Ví dụ: Đội bảo trì nội bộ).", "Khóa ngoại đội kỹ thuật."),
        ("6", "Kỹ thuật viên phụ trách", "Nhân sự kỹ thuật được chỉ định theo dõi tình trạng máy.", "Khóa ngoại tài khoản người dùng."),
        ("7", "Ngày đưa vào sử dụng", "Thời điểm thiết bị bắt đầu vận hành tại buồng phòng.", "Kiểu ngày tháng (Date).")
    ]
    format_table(doc.add_table(rows=1, cols=4), [Inches(0.5), Inches(1.8), Inches(3.0), Inches(1.7)],
                 ["STT", "Tên thuộc tính", "Đặc tả ý nghĩa", "Ghi chú"], equip_data)
    add_figure_caption("(Hình 3.71: Dữ liệu hồ sơ trang thiết bị buồng phòng trên Odoo 19)")
    
    # b. Phiếu yêu cầu bảo trì thiết bị buồng phòng
    add_subheading("b. Phiếu yêu cầu bảo trì thiết bị buồng phòng (maintenance.request)")
    add_table_title("Bảng 3.24: Đặc tả thư viện dữ liệu phiếu yêu cầu bảo trì kỹ thuật")
    req_data = [
        ("1", "Tiêu đề yêu cầu", "Tóm tắt sự cố (Tự sinh theo cú pháp: [Số phòng] + Tiêu đề sự cố).", "Trường bắt buộc nhập."),
        ("2", "Phòng phát sinh", "Số phòng khách sạn cần sửa chữa.", "Khóa ngoại liên kết danh mục phòng."),
        ("3", "Biên bản sự cố liên quan", "Nguồn gốc biên bản sự cố buồng phòng kích hoạt phiếu này.", "Khóa ngoại biên bản sự cố."),
        ("4", "Thiết bị cần bảo trì", "Thiết bị cụ thể lắp tại phòng cần can thiệp kỹ thuật.", "Khóa ngoại danh mục thiết bị."),
        ("5", "Mức độ ưu tiên", "Độ khẩn cấp: Thấp, Bình thường, Khẩn cấp.", "Tự động quy đổi từ mức độ sự cố."),
        ("6", "Loại bảo trì", "Phân loại: Khắc phục sự cố hoặc Phòng ngừa định kỳ.", "Mặc định: Khắc phục sự cố."),
        ("7", "Đội ngũ bảo trì", "Đội kỹ thuật chịu trách nhiệm giải quyết phiếu.", "Khóa ngoại đội kỹ thuật."),
        ("8", "Người phụ trách", "Kỹ thuật viên trực tiếp thực hiện công tác sửa chữa.", "Khóa ngoại tài khoản người dùng."),
        ("9", "Giai đoạn xử lý", "Tiến độ xử lý: Đề nghị mới, Đang thực hiện, Đã sửa chữa, Loại bỏ.", "Theo dõi trên bảng Kanban."),
        ("10", "Thời lượng sửa chữa", "Tổng số giờ làm việc thực tế của kỹ thuật viên.", "Kiểu số thực (Giờ)."),
        ("11", "Mô tả kỹ thuật", "Mô tả triệu chứng hỏng hóc và ghi chú phương án xử lý.", "Trường văn bản tự do.")
    ]
    format_table(doc.add_table(rows=1, cols=4), [Inches(0.5), Inches(1.8), Inches(3.0), Inches(1.7)],
                 ["STT", "Tên thuộc tính", "Đặc tả ý nghĩa", "Ghi chú"], req_data)
    add_figure_caption("(Hình 3.72: Dữ liệu phiếu yêu cầu bảo trì kỹ thuật trên Odoo 19)")

    # c. Biên bản sự cố & hư hỏng buồng phòng
    add_subheading("c. Biên bản sự cố & hư hỏng buồng phòng (hotel.incident)")
    add_table_title("Bảng 3.25: Đặc tả thư viện dữ liệu biên bản sự cố buồng phòng")
    inc_data = [
        ("1", "Mã sự cố", "Mã số định danh duy nhất (Ví dụ: INC/2026/00015).", "Hệ thống tự sinh, chỉ đọc."),
        ("2", "Tiêu đề sự cố", "Tên tóm tắt lỗi hỏng hóc (Ví dụ: Điều hòa không mát, nhỏ giọt nước).", "Trường bắt buộc nhập."),
        ("3", "Phòng xảy ra sự cố", "Số phòng khách sạn phát sinh sự cố.", "Khóa ngoại liên kết danh mục phòng."),
        ("4", "Mức độ nghiêm trọng", "Phân cấp: Nhẹ, Trung bình, Nghiêm trọng.", "Mặc định: Trung bình."),
        ("5", "Khóa phòng", "Cờ điều khiển: Nếu tích chọn Có, phòng tự đổi sang Bảo trì / Sửa chữa.", "Mặc định: Không."),
        ("6", "Phiếu bảo trì Kỹ thuật", "Liên kết sang chứng từ phiếu bảo trì đã chuyển giao.", "Tự động gán khi bấm chuyển."),
        ("7", "Trạng thái sự cố", "Vòng đời sự cố: Mới tiếp nhận, Đang xử lý, Đã khắc phục, Đã hủy.", "Mặc định: Mới tiếp nhận."),
        ("8", "Kết quả khắc phục", "Ghi nhận giải pháp và kết quả nghiệm thu thiết bị.", "Cập nhật khi nghiệm thu.")
    ]
    format_table(doc.add_table(rows=1, cols=4), [Inches(0.5), Inches(1.8), Inches(3.0), Inches(1.7)],
                 ["STT", "Tên thuộc tính", "Đặc tả ý nghĩa", "Ghi chú"], inc_data)
    add_figure_caption("(Hình 3.73: Dữ liệu biên bản sự cố buồng phòng trên Odoo 19)")

    # d. Danh mục phòng tích hợp quản trị tài sản
    add_subheading("d. Danh mục phòng tích hợp quản trị tài sản (hotel.room)")
    add_table_title("Bảng 3.26: Đặc tả thuộc tính quản trị tài sản trên hồ sơ phòng khách sạn")
    room_data = [
        ("1", "Số phòng", "Mã số phòng khách sạn (Ví dụ: P.101, P.104, P.201...).", "Duy nhất theo từng cơ sở."),
        ("2", "Trạng thái phòng", "6 trạng thái: Sẵn sàng, Đã đặt trước, Đang có khách, Cần dọn dẹp, Bảo trì / Sửa chữa, Khóa tạm thời.", "Quyết định khả năng mở bán."),
        ("3", "Danh sách thiết bị trong phòng", "Danh mục toàn bộ các thiết bị gắn liền với phòng này.", "Kế thừa phân hệ kỹ thuật."),
        ("4", "Số lượng thiết bị", "Tổng số lượng thiết bị đang bố trí tại phòng (hiển thị trên Smart Button).", "Hệ thống tự tính toán."),
        ("5", "Lịch sử bảo trì phòng", "Danh sách toàn bộ các phiếu yêu cầu sửa chữa đã phát sinh tại phòng.", "Lưu trữ lịch sử sửa chữa."),
        ("6", "Số lần bảo trì", "Tổng số lượt bảo trì kỹ thuật đã ghi nhận tại phòng (hiển thị trên Smart Button).", "Hệ thống tự tính toán.")
    ]
    format_table(doc.add_table(rows=1, cols=4), [Inches(0.5), Inches(1.8), Inches(3.0), Inches(1.7)],
                 ["STT", "Tên thuộc tính", "Đặc tả ý nghĩa", "Ghi chú"], room_data)
    add_figure_caption("(Hình 3.74: Dữ liệu hồ sơ phòng tích hợp thiết bị và bảo trì trên Odoo 19)")

    # Section 3.8.3
    add_subheading("3.8.3. Minh họa")
    add_subheading("3.8.3.1. Minh họa quy trình trên hệ thống Odoo")
    
    steps_illus = [
        ("Bước 1: Tra cứu danh mục trang thiết bị buồng phòng theo từng số phòng trên Odoo",
         "Nhân viên quản lý truy cập phân hệ Khách Sạn (M-Hotel) -> Kỹ Thuật & Thiết Bị -> chọn menu Thiết Bị Theo Từng Phòng. Màn hình hiển thị danh sách toàn bộ các tài sản được định vị theo từng số phòng, trong đó có Điều hòa Daikin 1.5HP và Tivi Samsung 43 inch tại phòng P.104.",
         "Hình 3.78: Bước 1 danh mục trang thiết bị buồng phòng theo từng phòng trên Odoo"),
        
        ("Bước 2: Xem chi tiết hồ sơ tài sản Điều hòa Daikin 1.5HP phòng P.104",
         "Mở chi tiết thiết bị Điều hòa Daikin 1.5HP (Serial: DAIKIN-15-104-GL). Giao diện hiển thị đầy đủ thông tin: Phòng đặt thiết bị P.104, Đội bảo trì nội bộ, ngày bắt đầu đưa vào vận hành và chủng loại thiết bị điện lạnh.",
         "Hình 3.79: Bước 2 chi tiết hồ sơ thiết bị Điều hòa Daikin phòng P.104 trên Odoo"),
         
        ("Bước 3: Nhân viên buồng phòng lập biên bản sự cố và tích chọn “Khóa phòng”",
         "Khi phát hiện máy lạnh không mát trong ca dọn phòng, nhân viên mở menu Buồng Phòng & Sự Cố -> Sự Cố & Hư Hỏng Buồng Phòng, bấm Mới: Nhập tiêu đề “Điều hòa không mát, có tiếng kêu rè rè”, chọn phòng P.104, chọn mức độ nghiêm trọng Trung bình và tích chọn Khóa phòng (Không đón khách).",
         "Hình 3.80: Bước 3 lập biên bản sự cố buồng phòng và chọn Khóa phòng P.104 trên Odoo"),
         
        ("Bước 4: Trạng thái phòng P.104 tự động chuyển sang “Bảo trì / Sửa chữa”",
         "Nhờ cơ chế liên thông của module m_hotel_asset, khi biên bản sự cố được lưu với cờ Khóa phòng được bật, trên Sơ đồ phòng trực quan, phòng P.104 ngay lập tức chuyển sang trạng thái Bảo trì / Sửa chữa với màu cam/nâu, tự động ngăn chặn lễ tân đặt và xếp phòng.",
         "Hình 3.81: Bước 4 trạng thái phòng P.104 tự động chuyển sang Bảo trì trên Odoo"),
         
        ("Bước 5: Bấm nút “Tạo Yêu Cầu Sửa Chữa (Kỹ Thuật)” trên biên bản sự cố",
         "Trên giao diện biên bản sự cố, nhân viên buồng phòng bấm nút Tạo Yêu Cầu Sửa Chữa (Kỹ Thuật). Hệ thống tự động sinh bản ghi Phiếu bảo trì liên kết với sự cố, hiển thị mã phiếu tại trường Phiếu bảo trì Kỹ thuật và chuyển biên bản sự cố sang trạng thái Đang xử lý.",
         "Hình 3.82: Bước 5 bấm nút chuyển giao yêu cầu sửa chữa kỹ thuật trên Odoo"),
         
        ("Bước 6: Mở phiếu bảo trì, chọn thiết bị và phân công kỹ thuật viên",
         "Trưởng bộ phận kỹ thuật mở menu Phiếu Sửa Chữa Kỹ Thuật, mở phiếu [P.104] Điều hòa không mát, chọn thiết bị Điều hòa Daikin 1.5HP từ danh sách thiết bị thuộc phòng P.104 và chỉ định kỹ thuật viên phụ trách trực tiếp.",
         "Hình 3.83: Bước 6 chọn thiết bị và phân công kỹ thuật viên trên phiếu bảo trì Odoo"),
         
        ("Bước 7: Kỹ thuật viên chuyển trạng thái phiếu bảo trì sang “Đang thực hiện”",
         "Kỹ thuật viên kéo phiếu bảo trì sang cột Đang thực hiện trên bảng Kanban phân hệ Bảo trì, mang dụng cụ chuyên dụng đến phòng P.104 để tiến hành đo đạc thông số và chẩn đoán lỗi.",
         "Hình 3.84: Bước 7 chuyển trạng thái phiếu bảo trì sang Đang thực hiện trên Odoo"),
         
        ("Bước 8: Thực hiện sửa chữa và xuất kho phụ tùng trên phân hệ Tồn kho (nếu cần)",
         "Kỹ thuật viên tiến hành vệ sinh dàn tản nhiệt, nạp bổ sung gas lạnh (hoặc nếu cần thay tụ quạt thì phối hợp cùng thủ kho lập phiếu xuất kho nội bộ trên phân hệ Tồn kho theo nghiệp vụ Odoo chuẩn).",
         "Hình 3.85: Bước 8 kỹ thuật viên ghi nhận thao tác sửa chữa thiết bị trên Odoo"),
         
        ("Bước 9: Vận hành chạy thử nghiệm tải thiết bị (SOP Kỹ thuật) và cập nhật thời lượng",
         "Cho máy lạnh chạy kiểm tra 20 phút đạt nhiệt độ lạnh sâu 22°C ổn định. Kỹ thuật viên cập nhật số giờ làm việc thực tế (1.0 giờ) và ghi chú phương án kỹ thuật đã thực hiện vào phần mô tả của phiếu bảo trì.",
         "Hình 3.86: Bước 9 cập nhật thời lượng và mô tả kết quả sửa chữa trên Odoo"),
         
        ("Bước 10: Chuyển phiếu bảo trì sang trạng thái “Đã sửa chữa”",
         "Kỹ thuật viên kéo phiếu bảo trì sang cột Đã sửa chữa trên Kanban Odoo để hoàn tất lệnh công tác của bộ phận kỹ thuật.",
         "Hình 3.87: Bước 10 chuyển phiếu bảo trì sang cột Đã sửa chữa trên Odoo"),
         
        ("Bước 11: Buồng phòng nghiệm thu và bấm “Đã khắc phục” trên biên bản sự cố gốc",
         "Nhân viên buồng phòng đến kiểm tra thực tế tại phòng P.104, mở lại biên bản sự cố gốc và bấm nút Đã khắc phục. Lúc này, hệ thống tự động đổi trạng thái phòng P.104 từ Bảo trì / Sửa chữa sang Cần dọn dẹp.",
         "Hình 3.88: Bước 11 bấm Đã khắc phục sự cố và phòng chuyển về Cần dọn dẹp trên Odoo"),
         
        ("Bước 12: Hoàn tất dọn phòng và kiểm tra Smart Button trên hồ sơ phòng P.104",
         "Sau khi buồng phòng hoàn thành vệ sinh, phòng P.104 trở về trạng thái Sẵn sàng. Mở hồ sơ phòng P.104: Smart Button “Thiết bị” hiển thị 2 tài sản và Smart Button “Bảo trì” hiển thị số lượt bảo trì đã được tích lũy thêm 1 lượt thành công.",
         "Hình 3.89: Bước 12 Smart Button cập nhật lịch sử bảo trì trên hồ sơ phòng P.104 trên Odoo")
    ]
    
    for title, desc, fig in steps_illus:
        add_p(title, bold=True, space_before=6, space_after=2)
        add_p(desc, space_before=0, space_after=4)
        add_figure_caption(fig)

    # Section 3.8.3.2 Ngoại lệ
    add_subheading("3.8.3.2. Ngoại lệ")
    
    add_p(
        "a. Xử lý sự cố kỹ thuật nhẹ không cần khóa phòng (Khóa phòng = Không)",
        bold=True, space_before=6, space_after=4
    )
    add_p(
        "Bối cảnh: Thiết bị gặp lỗi nhỏ không ảnh hưởng lớn đến sinh hoạt của khách (như remote tivi hết pin, đèn ngủ chập chờn "
        "hoặc vòi nước rỉ giọt nhẹ). Nhân viên buồng phòng lập biên bản sự cố nhưng không tích chọn Khóa phòng:"
    )
    ex_a_steps = [
        ("Bước 1: Tạo biên bản sự cố không chọn Khóa phòng. Phòng vẫn giữ nguyên trạng thái hiện tại (Sẵn sàng hoặc Đang có khách), không bị chuyển sang Bảo trì / Sửa chữa.",
         "Hình 3.90: Ghi nhận sự cố kỹ thuật nhẹ không tích chọn Khóa phòng trên Odoo"),
        ("Bước 2: Bấm tạo phiếu bảo trì kỹ thuật để kỹ thuật viên đến thay pin hoặc siết ốc nhanh trong ngày mà không làm gián đoạn việc kinh doanh phòng.",
         "Hình 3.91: Phiếu bảo trì phát sinh nhưng phòng vẫn ở trạng thái kinh doanh bình thường trên Odoo")
    ]
    for step_t, fig in ex_a_steps:
        add_p(step_t, bold=True, space_before=4, space_after=2)
        add_figure_caption(fig)

    add_p(
        "b. Phiếu kỹ thuật đã “Đã sửa chữa” nhưng biên bản sự cố gốc chưa được đóng",
        bold=True, space_before=8, space_after=4
    )
    add_p(
        "Bối cảnh: Kỹ thuật viên đã sửa xong thiết bị và chuyển phiếu bảo trì sang Đã sửa chữa, nhưng nhân viên buồng phòng chưa đến "
        "kiểm tra hiện trường hoặc quên bấm nút Đã khắc phục trên biên bản sự cố gốc:"
    )
    ex_b_steps = [
        ("Bước 1: Phòng vẫn duy trì trạng thái Bảo trì / Sửa chữa trên hệ thống vì hệ thống chỉ kích hoạt mở phòng khi biên bản sự cố đổi sang trạng thái Đã khắc phục.",
         "Hình 3.92: Phòng vẫn ở trạng thái Bảo trì do sự cố gốc chưa được xác nhận hoàn tất trên Odoo"),
        ("Bước 2: Giám sát buồng phòng kiểm tra danh sách sự cố tồn đọng, mở biên bản sự cố đối chiếu với phiếu bảo trì đã hoàn tất và bấm Đã khắc phục để giải phóng phòng về Cần dọn dẹp.",
         "Hình 3.93: Thao tác xác nhận khắc phục sự cố tồn đọng để giải phóng trạng thái phòng trên Odoo")
    ]
    for step_t, fig in ex_b_steps:
        add_p(step_t, bold=True, space_before=4, space_after=2)
        add_figure_caption(fig)

    add_p(
        "c. Thiết bị hỏng nặng không thể sửa chữa — Chuyển giai đoạn “Loại bỏ” trên Kanban",
        bold=True, space_before=8, space_after=4
    )
    add_p(
        "Bối cảnh: Thiết bị chập cháy nghiêm trọng, hỏng lốc máy nén điều hòa không thể phục hồi hoặc chi phí sửa chữa quá cao so với giá trị tài sản:"
    )
    ex_c_steps = [
        ("Bước 1: Kỹ thuật viên kéo phiếu bảo trì sang cột Loại bỏ trên bảng Kanban của phân hệ Bảo trì.",
         "Hình 3.94: Kéo phiếu bảo trì sang cột Loại bỏ trên Kanban Odoo"),
        ("Bước 2: Kỹ thuật viên gỡ số phòng khỏi hồ sơ thiết bị cũ và liên kết mã thiết bị mới thay thế vào hồ sơ phòng P.104 trên Odoo.",
         "Hình 3.95: Cập nhật thiết bị thay thế mới vào danh mục trang thiết bị phòng P.104 trên Odoo")
    ]
    for step_t, fig in ex_c_steps:
        add_p(step_t, bold=True, space_before=4, space_after=2)
        add_figure_caption(fig)

    doc.save(output_path)
    print(f"Generated successfully: {output_path}")

if __name__ == '__main__':
    out_file = r"f:\Project Hoạch định\ERP-M_hotel_managenment\Bao_Cao_3.8_Quy_Trinh_Quan_Tri_Tai_San_Bao_Tri_MHotel.docx"
    build_section_3_8_docx_v4(out_file)
