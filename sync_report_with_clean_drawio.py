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

def set_table_borders(table, color="B0B0B0", sz="4", val="single"):
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

# 41 Bước quy trình bán hàng chuẩn 4 cột theo phong cách báo cáo của anh chị
steps_senior_style = [
    ("1", "Khách hàng", "Có nhu cầu lưu trú", 
     "Khách xuất hiện nhu cầu tìm kiếm và đặt phòng nghỉ tại Khách Sạn M (Cơ sở 1 tại Thôn Dương Liễu Tây, xã Bình Dương, tỉnh Gia Lai)."),
    ("2", "Khách hàng", "Kênh đặt phòng?", 
     "Cổng rẽ nhánh: Khách hàng lựa chọn đặt phòng qua trang thông tin điện tử của khách sạn hoặc liên hệ trực tiếp lễ tân tại quầy / qua số điện thoại đường dây nóng."),
    ("3", "Khách hàng", "Điền biểu mẫu đặt phòng trên trang web", 
     "Khách truy cập địa chỉ đặt phòng trên trang thông tin điện tử, nhập họ tên, số điện thoại, thư điện tử, căn cước công dân, chọn chi nhánh Gia Lai, hạng phòng và thời gian lưu trú."),
    ("4", "Hệ thống ERP", "Nhận đặt phòng, tạo đơn nháp", 
     "Hệ thống tiếp nhận yêu cầu từ trang web, tự động tìm kiếm hồ sơ khách cũ qua số điện thoại/thư điện tử hoặc tạo hồ sơ khách mới, tự động tạo Đơn đặt phòng ở trạng thái Dự thảo."),
    ("5", "Khách hàng", "Liên hệ lễ tân để đặt phòng", 
     "Khách đến trực tiếp quầy lễ tân khách sạn hoặc gọi điện thoại đến đường dây nóng để yêu cầu đặt phòng."),
    ("6", "Bộ phận lễ tân", "Nhận yêu cầu, tra cứu phòng, lập đơn nháp", 
     "Lễ tân tiếp nhận thông tin từ khách, mở công cụ tra cứu phòng trống trên hệ thống để tìm phòng khả dụng thuộc chi nhánh Gia Lai và thời gian lưu trú, sau đó lập đơn đặt phòng ở trạng thái Dự thảo."),
    ("7", "Bộ phận lễ tân", "Xác nhận đơn đặt phòng", 
     "Lễ tân kiểm tra lại toàn bộ thông tin trên đơn đặt phòng và bấm nút xác nhận đơn trên hệ thống."),
    ("8", "Hệ thống ERP", "Kiểm tra phòng còn trống, báo kết quả cho khách", 
     "Hệ thống kích hoạt cơ chế kiểm tra chéo tự động, quét dữ liệu đặt phòng thời gian thực để đối soát lịch phòng và thông báo kết quả cho khách hàng."),
    ("9", "Hệ thống ERP", "Còn phòng?", 
     "Cổng kiểm tra điều kiện: Nếu phát hiện trùng lịch với đơn khác trong cùng khung giờ, hệ thống chuyển sang kết thúc do trùng lịch; nếu phòng còn trống, chuyển sang tính giá và xác nhận."),
    ("10", "Hệ thống ERP", "Kết thúc (trùng lịch)", 
     "Hệ thống phát tín hiệu báo trùng lịch đặt phòng và yêu cầu khách hàng chọn lại phòng hoặc thời gian khác."),
    ("11", "Khách hàng", "Nhận kết quả kiểm tra phòng", 
     "Khách hàng nhận được phản hồi từ hệ thống về tình trạng phòng mình vừa chọn."),
    ("12", "Khách hàng", "Còn phòng?", 
     "Cổng kiểm tra kết quả: Nếu trùng lịch, khách hàng quay lại bước chọn kênh để đặt lại; nếu còn trống, khách hàng tiếp tục sang bước nộp tiền đặt cọc."),
    ("13", "Hệ thống ERP", "Tính giá, đơn đã xác nhận, phòng đã đặt", 
     "Hệ thống tự động tra cứu biểu giá theo mùa và ngày lễ để áp giá chính xác. Đơn đặt phòng chuyển trạng thái Đã xác nhận và phòng tương ứng tự động đổi sang trạng thái Đã đặt trước."),
    ("14", "Khách hàng", "Nộp tiền đặt cọc", 
     "Khách hàng thanh toán khoản tiền cọc thỏa thuận để giữ chỗ (bằng tiền mặt hoặc chuyển khoản qua ngân hàng)."),
    ("15", "Bộ phận kế toán", "Thu tiền đặt cọc", 
     "Nhân viên kế toán tiếp nhận tiền cọc từ khách và ghi nhận số tiền cọc vào đơn đặt phòng trên hệ thống. Hệ thống tự động tính lại số tiền còn lại phải thanh toán = Tổng tiền − Tiền cọc."),
    ("16", "Bộ phận kế toán", "Xuất hóa đơn tiền cọc", 
     "Kế toán phát hành hóa đơn hoặc phiếu thu tiền đặt cọc gửi cho khách hàng, lưu vết cấn trừ vào hóa đơn quyết toán cuối cùng."),
    ("17", "Khách hàng", "Nhận hóa đơn tiền cọc", 
     "Khách hàng nhận hóa đơn xác nhận đã hoàn tất thủ tục nộp tiền cọc giữ phòng."),
    ("18", "Khách hàng", "Đến ngày nhận phòng", 
     "Sự kiện trung gian định thời: Khách hàng di chuyển đến khách sạn vào đúng ngày giờ nhận phòng đã đăng ký."),
    ("19", "Khách hàng", "Xuất trình giấy tờ tùy thân", 
     "Khách hàng tiến đến quầy Lễ tân, xuất trình Căn cước công dân hoặc Hộ chiếu để làm thủ tục nhận phòng."),
    ("20", "Bộ phận lễ tân", "Đối chiếu giấy tờ, nhận phòng, giao thẻ từ", 
     "Lễ tân kiểm tra giấy tờ tùy thân, đối chiếu hồ sơ trên hệ thống, thực hiện nhận phòng trên phần mềm và bàn giao thẻ từ mở cửa phòng cho khách."),
    ("21", "Hệ thống ERP", "Cập nhật đơn đang lưu trú, phòng có khách", 
     "Hệ thống chuyển trạng thái đơn sang Đang lưu trú, đổi trạng thái phòng sang Đang có khách và tự động gán tên khách hàng vào trường khách đang ở của phòng."),
    ("22", "Khách hàng", "Yêu cầu dịch vụ khi lưu trú", 
     "Trong suốt kỳ nghỉ, khách hàng có nhu cầu sử dụng thêm dịch vụ khách sạn (giặt ủi, ăn uống tại phòng...) hoặc tiêu dùng đồ uống, đồ ăn nhẹ có tính phí trong phòng."),
    ("23", "Bộ phận lễ tân", "Ghi nhận dịch vụ phát sinh (lặp lại)", 
     "Lễ tân mở đơn đặt phòng, nhập các dòng chi phí dịch vụ phát sinh. Hệ thống tự động tính thành tiền và cộng dồn vào tổng tiền thanh toán (thao tác lặp lại nhiều lần)."),
    ("24", "Khách hàng", "Yêu cầu trả phòng", 
     "Khách hàng hoàn tất kỳ lưu trú, đến quầy Lễ tân hoặc gọi điện thông báo yêu cầu làm thủ tục trả phòng."),
    ("25", "Bộ phận lễ tân", "Nhận yêu cầu, báo buồng phòng kiểm tra", 
     "Lễ tân tiếp nhận thông báo trả phòng, phát tín hiệu liên hệ bộ phận buồng phòng kiểm tra thực tế hiện trạng phòng trước khi chốt hóa đơn."),
    ("26", "Bộ phận buồng phòng", "Kiểm tra phòng, báo đồ uống và vật dụng đã dùng", 
     "Nhân viên buồng phòng đến phòng kiểm tra thiết bị, kiểm đếm số lượng đồ uống, đồ ăn nhẹ khách đã sử dụng và báo cáo số liệu về quầy Lễ tân."),
    ("27", "Bộ phận lễ tân", "Bổ sung phát sinh, bấm trả phòng", 
     "Lễ tân nhập bổ sung các chi phí đồ uống tiêu dùng vào đơn đặt phòng, thu lại thẻ từ phòng và nhấn nút Trả phòng trên hệ thống."),
    ("28", "Hệ thống ERP", "Cập nhật trả phòng, tạo phiếu dọn phòng", 
     "Hệ thống cập nhật đơn sang Đã trả phòng, đổi phòng sang Cần dọn dẹp, xóa tên khách đang ở và tự động sinh một nhiệm vụ dọn phòng khẩn cấp cho buồng phòng."),
    ("29", "Bộ phận lễ tân", "Lập hóa đơn", 
     "Lễ tân nhấn nút Tạo hóa đơn trên đơn đặt phòng để hệ thống tự động bóc tách chi phí tiền phòng và toàn bộ dịch vụ phát sinh sang chứng từ hóa đơn."),
    ("30", "Bộ phận kế toán", "Kiểm tra hóa đơn, trừ tiền cọc, yêu cầu thanh toán", 
     "Kế toán kiểm tra các dòng chi tiết trên hóa đơn, cấn trừ số tiền cọc đã thu trước đó, xuất Hóa đơn bán hàng và thông báo số tiền còn lại cần thanh toán cho khách."),
    ("31", "Khách hàng", "Nhận hóa đơn", 
     "Khách hàng kiểm tra bảng kê chi tiết các khoản chi phí lưu trú và số tiền còn lại phải thanh toán trên hóa đơn."),
    ("32", "Khách hàng", "Thanh toán", 
     "Khách hàng thanh toán số tiền còn lại bằng tiền mặt, thẻ ngân hàng hoặc quét mã chuyển khoản."),
    ("33", "Bộ phận kế toán", "Nhận thanh toán, vào sổ hóa đơn", 
     "Kế toán nhận đủ tiền, xác nhận hóa đơn để vào sổ kế toán và bấm Ghi nhận thanh toán. Hóa đơn chuyển trạng thái sang Đã thanh toán."),
    ("34", "Bộ phận kế toán", "Kết thúc (Tài chính)", 
     "Sự kiện kết thúc của nhánh tài chính: Giao dịch được thanh toán đầy đủ và lưu sổ kế toán hợp lệ."),
    ("35", "Khách hàng", "Kết thúc (Khách hàng)", 
     "Sự kiện kết thúc của khách hàng: Nhận hóa đơn hoàn tất, kết thúc kỳ nghỉ thành công và rời khách sạn."),
    ("36", "Bộ phận buồng phòng", "Nhận phiếu, dọn phòng, kiểm tra thiết bị", 
     "Nhân viên buồng phòng nhận nhiệm vụ dọn phòng ưu tiên trên màn hình, bấm Bắt đầu, tiến hành thay đồ vải, vệ sinh phòng và rà soát trang thiết bị."),
    ("37", "Bộ phận buồng phòng", "Có sự cố?", 
     "Cổng kiểm tra điều kiện: Nếu phát hiện hư hỏng thiết bị, chuyển sang xử lý sự cố phối hợp kỹ thuật; nếu phòng bình thường, chuyển sang hoàn thành dọn phòng."),
    ("38", "Bộ phận buồng phòng", "Xử lý sự cố (phối hợp bộ phận kỹ thuật)", 
     "Nhân viên lập biên bản sự cố, tích chọn Khóa phòng để hệ thống tự động chuyển phòng sang Bảo trì, đồng thời tạo phiếu yêu cầu bảo trì chuyển kỹ thuật sửa chữa."),
    ("39", "Bộ phận buồng phòng", "Hoàn thành dọn phòng", 
     "Sau khi vệ sinh sạch sẽ, bổ sung đầy đủ vật tư tiêu hao cá nhân và nước khoáng theo tiêu chuẩn, nhân viên bấm nút Hoàn thành trên nhiệm vụ buồng phòng."),
    ("40", "Hệ thống ERP", "Phòng sẵn sàng, xuất kho vật tư", 
     "Hệ thống cập nhật nhiệm vụ hoàn tất, tự động khôi phục trạng thái phòng về Sẵn sàng đón khách mới, đồng thời tự động xuất kho trừ vật tư tiêu hao theo định mức."),
    ("41", "Hệ thống ERP", "Kết thúc (Vận hành phòng)", 
     "Sự kiện kết thúc của nhánh buồng phòng: Phòng khách sạn đã sạch sẽ, đầy đủ tiện nghi và sẵn sàng phục vụ lượt khách lưu trú tiếp theo.")
]

# Thư viện dữ liệu cấu trúc theo mục a, b, c... của các anh chị
# CẬP NHẬT CHÍNH XÁC 100% CƠ SỞ GIA LAI THEO BẢNG DỮ LIỆU CỦA BẠN (KHÔNG CHÊM TIẾNG ANH)
data_libraries_senior = [
    {
        "sub_id": "a. Khách hàng",
        "table_title": "Bảng 3.3: Đặc tả thư viện dữ liệu khách hàng",
        "fig_title": "Hình 3.2: Dữ liệu khách hàng",
        "headers": ["STT", "Tên thuộc tính", "Đặc tả ý nghĩa", "Ghi chú"],
        "rows": [
            ["1", "Mã khách hàng", "Chuỗi ký tự định danh duy nhất cho mỗi khách hàng trong hệ thống.", "Hệ thống tự động sinh."],
            ["2", "Tên khách hàng", "Họ và tên đầy đủ của cá nhân hoặc tên tổ chức lưu trú.", "Trường bắt buộc nhập."],
            ["3", "Số điện thoại", "Số điện thoại di động để liên lạc và nhận mã đặt phòng.", "Trường bắt buộc nhập, dùng tra cứu lịch sử."],
            ["4", "Địa chỉ thư điện tử", "Địa chỉ hộp thư điện tử của khách hàng để gửi phiếu xác nhận.", "Dùng gửi xác nhận đặt phòng tự động."],
            ["5", "Số định danh cá nhân", "Số Căn cước công dân hoặc Hộ chiếu của khách lưu trú.", "Bắt buộc theo quy định khai báo lưu trú."],
            ["6", "Ngày cấp định danh", "Ngày cấp thẻ Căn cước công dân hoặc Hộ chiếu.", "Phục vụ khai báo lưu trú công an."],
            ["7", "Nơi cấp định danh", "Cơ quan có thẩm quyền cấp giấy tờ tùy thân.", "Phục vụ khai báo lưu trú công an."],
            ["8", "Quốc tịch", "Quốc gia nơi khách hàng mang quốc tịch.", "Mặc định: Việt Nam."],
            ["9", "Địa chỉ thường trú", "Nơi cư trú hợp pháp hoặc địa chỉ liên lạc thường xuyên của khách.", "Ghi nhận trên hồ sơ khách hàng."],
            ["10", "Ghi chú sở thích", "Lưu ý về sở thích, thói quen phòng và yêu cầu phục vụ đặc biệt.", "Phục vụ nâng cao chất lượng dịch vụ."]
        ],
        "widths": [0.6, 1.8, 3.0, 1.1]
    },
    {
        "sub_id": "b. Hạng phòng (Cơ sở 1 – Gia Lai)",
        "table_title": "Bảng 3.4: Đặc tả thư viện dữ liệu hạng phòng tại Cơ sở 1 (Gia Lai)",
        "fig_title": "Hình 3.3: Dữ liệu hạng phòng cơ sở Gia Lai",
        "headers": ["STT", "Tên hạng phòng", "Sức chứa", "Cấu hình số giường", "Đơn giá niêm yết theo đêm (VNĐ)", "Số lượng phòng"],
        "rows": [
            ["1", "Phòng đơn", "2 khách", "1 giường đôi lớn", "250.000", "5 phòng (P.101, P.102, P.103, P.201, P.202)"],
            ["2", "Phòng đôi", "4 khách", "2 giường đôi", "350.000", "5 phòng (P.104, P.105, P.203, P.204, P.301)"],
            ["3", "Phòng ba giường", "6 khách", "3 giường đơn hoặc giường đôi", "500.000", "2 phòng (P.205, P.302)"],
            ["4", "Phòng tập thể", "6 khách", "6 giường đơn hoặc giường tầng", "1.000.000", "1 phòng (P.303)"]
        ],
        "widths": [0.5, 1.4, 0.9, 1.5, 1.3, 1.5]
    },
    {
        "sub_id": "c. Danh mục phòng khách sạn (Cơ sở 1 – Gia Lai)",
        "table_title": "Bảng 3.5: Đặc tả thư viện dữ liệu danh mục phòng tại Cơ sở 1 (Gia Lai)",
        "fig_title": "Hình 3.4: Dữ liệu danh mục 13 phòng khách sạn tại Cơ sở Gia Lai",
        "headers": ["STT", "Vị trí tầng", "Mã phòng", "Loại phòng", "Sức chứa", "Số giường", "Đơn giá / đêm (VNĐ)"],
        "rows": [
            ["1", "Tầng 1", "P.101", "Phòng đơn", "2 khách", "1 giường đôi lớn", "250.000"],
            ["2", "Tầng 1", "P.102", "Phòng đơn", "2 khách", "1 giường đôi lớn", "250.000"],
            ["3", "Tầng 1", "P.103", "Phòng đơn", "2 khách", "1 giường đôi lớn", "250.000"],
            ["4", "Tầng 1", "P.104", "Phòng đôi", "4 khách", "2 giường đôi", "350.000"],
            ["5", "Tầng 1", "P.105", "Phòng đôi", "4 khách", "2 giường đôi", "350.000"],
            ["6", "Tầng 2", "P.201", "Phòng đơn", "2 khách", "1 giường đôi lớn", "250.000"],
            ["7", "Tầng 2", "P.202", "Phòng đơn", "2 khách", "1 giường đôi lớn", "250.000"],
            ["8", "Tầng 2", "P.203", "Phòng đôi", "4 khách", "2 giường đôi", "350.000"],
            ["9", "Tầng 2", "P.204", "Phòng đôi", "4 khách", "2 giường đôi", "350.000"],
            ["10", "Tầng 2", "P.205", "Phòng ba giường", "6 khách", "3 giường đơn hoặc giường đôi", "500.000"],
            ["11", "Tầng 3", "P.301", "Phòng đôi", "4 khách", "2 giường đôi", "350.000"],
            ["12", "Tầng 3", "P.302", "Phòng ba giường", "6 khách", "3 giường đơn hoặc giường đôi", "500.000"],
            ["13", "Tầng 3", "P.303", "Phòng tập thể", "6 khách", "6 giường đơn hoặc giường tầng", "1.000.000"]
        ],
        "widths": [0.5, 0.9, 0.9, 1.4, 0.9, 1.5, 1.0]
    },
    {
        "sub_id": "d. Bảng giá phòng theo mùa và ngày lễ",
        "table_title": "Bảng 3.6: Đặc tả thư viện dữ liệu bảng giá theo mùa và ngày lễ",
        "fig_title": "Hình 3.5: Dữ liệu bảng giá theo mùa",
        "headers": ["STT", "Tên thuộc tính", "Đặc tả ý nghĩa", "Ghi chú"],
        "rows": [
            ["1", "Tên biểu giá", "Tên gọi quy định giá (Mùa hè, Dịp lễ tết, Cuối tuần...).", "Trường bắt buộc nhập."],
            ["2", "Hạng phòng áp dụng", "Hạng phòng được thiết lập biểu giá riêng biệt.", "Trường bắt buộc nhập."],
            ["3", "Loại hình mùa vụ", "Phân loại: Mùa cao điểm, Cuối tuần, Ngày lễ, Chương trình ưu đãi.", "Trường bắt buộc nhập."],
            ["4", "Ngày bắt đầu áp dụng", "Mốc thời gian bắt đầu có hiệu lực của khung giá.", "Trường bắt buộc nhập."],
            ["5", "Ngày kết thúc áp dụng", "Mốc thời gian hết hiệu lực của khung giá.", "Trường bắt buộc nhập."],
            ["6", "Giá mùa theo đêm", "Đơn giá thuê theo đêm trong khung thời gian quy định (VNĐ).", "Trường bắt buộc nhập."],
            ["7", "Giá mùa theo giờ", "Đơn giá thuê theo giờ trong khung thời gian quy định (VNĐ).", "Trường bắt buộc nhập."],
            ["8", "Trạng thái hiệu lực", "Cờ xác định biểu giá đang bật áp dụng hay tạm ngừng.", "Mặc định: Bật hiệu lực."]
        ],
        "widths": [0.6, 1.8, 3.0, 1.1]
    },
    {
        "sub_id": "e. Đơn đặt phòng",
        "table_title": "Bảng 3.7: Đặc tả thư viện dữ liệu đơn đặt phòng",
        "fig_title": "Hình 3.6: Dữ liệu đơn đặt phòng",
        "headers": ["STT", "Tên thuộc tính", "Đặc tả ý nghĩa", "Ghi chú"],
        "rows": [
            ["1", "Mã đơn đặt phòng", "Ký hiệu định danh đơn đặt phòng tự sinh theo quy tắc hệ thống.", "Tự động sinh; Chỉ đọc."],
            ["2", "Hồ sơ khách hàng", "Thông tin khách hàng đứng tên đại diện đặt phòng.", "Trường bắt buộc nhập."],
            ["3", "Số điện thoại", "Số điện thoại liên hệ của khách đặt.", "Kế thừa từ hồ sơ khách."],
            ["4", "Địa chỉ thư điện tử", "Hộp thư điện tử nhận thông báo xác nhận đặt phòng.", "Kế thừa từ hồ sơ khách."],
            ["5", "Số Căn cước công dân", "Số định danh tùy thân của khách lưu trú.", "Kế thừa từ hồ sơ khách."],
            ["6", "Chi nhánh tiếp nhận", "Cơ sở khách sạn thực hiện dịch vụ lưu trú (Cơ sở 1 Gia Lai).", "Trường bắt buộc nhập."],
            ["7", "Phòng bố trí", "Số phòng khách sạn được xếp chỗ cụ thể (Ví dụ: P.201, P.204, P.305...).", "Trường bắt buộc nhập."],
            ["8", "Hạng phòng", "Hạng phòng tương ứng của phòng được xếp.", "Kế thừa từ phòng."],
            ["9", "Hình thức thuê", "Lựa chọn hình thức: Thuê theo đêm hoặc Thuê theo giờ.", "Mặc định: Theo đêm."],
            ["10", "Thời gian nhận phòng", "Ngày giờ nhận phòng dự kiến hoặc thực tế.", "Áp dụng thuê theo đêm."],
            ["11", "Thời gian trả phòng", "Ngày giờ trả phòng dự kiến hoặc thực tế.", "Áp dụng thuê theo đêm."],
            ["12", "Số đêm lưu trú", "Tổng số đêm khách đăng ký lưu trú.", "Tính toán tự động."],
            ["13", "Ngày thuê theo giờ", "Ngày khách đến sử dụng phòng theo giờ.", "Áp dụng thuê theo giờ."],
            ["14", "Giờ bắt đầu thuê", "Giờ khách bắt đầu nhận phòng.", "Áp dụng thuê theo giờ."],
            ["15", "Giờ kết thúc thuê", "Giờ khách dự kiến trả phòng.", "Tính toán tự động."],
            ["16", "Số giờ thuê", "Tổng số giờ khách đăng ký sử dụng phòng.", "Mặc định: 2 giờ."],
            ["17", "Đơn giá phòng áp dụng", "Đơn giá phòng sau khi đối soát biểu giá mùa vụ.", "Tính toán tự động."],
            ["18", "Chi tiết dịch vụ phát sinh", "Danh sách các khoản dịch vụ và đồ dùng tiêu thụ trong kỳ.", "Quan hệ bảng chi tiết."],
            ["19", "Tiền thuê phòng", "Thành tiền phòng = Đơn giá × Số đêm (hoặc × Số giờ).", "Tính toán tự động."],
            ["20", "Tiền dịch vụ phát sinh", "Tổng tiền các dịch vụ phụ trợ sử dụng trong kỳ lưu trú.", "Tính toán tự động."],
            ["21", "Tổng tiền thanh toán", "Tổng chi phí = Tiền thuê phòng + Tiền dịch vụ phát sinh.", "Tính toán tự động."],
            ["22", "Tiền đặt cọc", "Số tiền khách đã nộp giữ chỗ trước.", "Mặc định: 0 VNĐ."],
            ["23", "Tiền còn lại phải trả", "Số tiền cần thu khi trả phòng = Tổng tiền − Tiền cọc.", "Tính toán tự động."],
            ["24", "Trạng thái đơn", "Trạng thái: Dự thảo, Đã xác nhận, Đang lưu trú, Đã trả phòng, Đã xuất hóa đơn, Đã hủy.", "Mặc định: Dự thảo."],
            ["25", "Hóa đơn liên kết", "Chứng từ hóa đơn tài chính tương ứng của đơn.", "Trường chỉ đọc."],
            ["26", "Ghi chú đặc biệt", "Yêu cầu riêng của khách hoặc ghi chú nội bộ của lễ tân.", "Trường tùy chọn."]
        ],
        "widths": [0.6, 1.8, 3.0, 1.1]
    },
    {
        "sub_id": "f. Chi tiết dịch vụ phát sinh",
        "table_title": "Bảng 3.8: Đặc tả thư viện dữ liệu chi tiết dịch vụ phát sinh",
        "fig_title": "Hình 3.7: Dữ liệu chi tiết dịch vụ phát sinh",
        "headers": ["STT", "Tên thuộc tính", "Đặc tả ý nghĩa", "Ghi chú"],
        "rows": [
            ["1", "Đơn đặt phòng liên kết", "Đơn đặt phòng cha sở hữu dòng dịch vụ này.", "Trường bắt buộc; Xóa theo đơn."],
            ["2", "Sản phẩm dịch vụ", "Mặt hàng tiêu dùng hoặc dịch vụ gia tăng khách sử dụng.", "Liên kết danh mục sản phẩm."],
            ["3", "Tên dịch vụ hiển thị", "Tên mô tả dịch vụ hoặc đồ uống tiêu dùng thực tế.", "Trường bắt buộc nhập."],
            ["4", "Số lượng sử dụng", "Số lượng đơn vị dịch vụ hoặc sản phẩm tiêu thụ.", "Mặc định: 1.0."],
            ["5", "Đơn vị tính", "Đơn vị đo lường (chai, lon, lần, chiếc, giờ...).", "Kế thừa từ danh mục."],
            ["6", "Đơn giá bán", "Giá bán một đơn vị sản phẩm hoặc dịch vụ (VNĐ).", "Trường bắt buộc nhập."],
            ["7", "Thành tiền dòng", "Thành tiền = Số lượng × Đơn giá bán.", "Tính toán tự động."]
        ],
        "widths": [0.6, 1.8, 3.0, 1.1]
    },
    {
        "sub_id": "g. Chứng từ đặt cọc",
        "table_title": "Bảng 3.9: Đặc tả thư viện dữ liệu chứng từ đặt cọc",
        "fig_title": "Hình 3.8: Dữ liệu chứng từ đặt cọc",
        "headers": ["STT", "Tên thuộc tính", "Đặc tả ý nghĩa", "Ghi chú"],
        "rows": [
            ["1", "Mã đơn đặt phòng", "Mã định danh đơn đặt phòng phát sinh giao dịch nộp cọc.", "Trường bắt buộc."],
            ["2", "Khách hàng nộp cọc", "Họ tên khách hàng hoặc đơn vị thực hiện thanh toán tiền cọc.", "Lấy từ hồ sơ khách."],
            ["3", "Số tiền đặt cọc", "Số tiền cọc thực tế khách hàng đã thanh toán (VNĐ).", "Trường bắt buộc nhập."],
            ["4", "Hình thức nộp cọc", "Phương thức thanh toán: Tiền mặt, Chuyển khoản, Thẻ ngân hàng.", "Ghi nhận vào phiếu thu."],
            ["5", "Thời điểm nộp cọc", "Ngày giờ nhân viên kế toán thu ngân nhận tiền cọc.", "Ghi nhận thời gian thực."],
            ["6", "Người thu tiền", "Nhân viên kế toán / thu ngân chịu trách nhiệm tiếp nhận.", "Gán theo người dùng hệ thống."],
            ["7", "Trạng thái cấn trừ", "Xác nhận tiền cọc đã được khấu trừ tự động vào hóa đơn thanh toán.", "Tính toán tự động."]
        ],
        "widths": [0.6, 1.8, 3.0, 1.1]
    },
    {
        "sub_id": "h. Nhiệm vụ buồng phòng",
        "table_title": "Bảng 3.10: Đặc tả thư viện dữ liệu nhiệm vụ buồng phòng",
        "fig_title": "Hình 3.9: Dữ liệu nhiệm vụ buồng phòng",
        "headers": ["STT", "Tên thuộc tính", "Đặc tả ý nghĩa", "Ghi chú"],
        "rows": [
            ["1", "Mã nhiệm vụ", "Ký hiệu định danh công việc tự sinh theo quy định hệ thống.", "Tự động sinh; Chỉ đọc."],
            ["2", "Phòng cần xử lý", "Số phòng khách sạn cần dọn dẹp hoặc kiểm tra (Ví dụ: P.201, P.204...).", "Trường bắt buộc nhập."],
            ["3", "Hạng phòng", "Hạng phòng tương ứng để xác định định mức vật tư tiêu hao.", "Kế thừa từ phòng."],
            ["4", "Chi nhánh trực thuộc", "Cơ sở khách sạn phát sinh nhiệm vụ dọn phòng (Cơ sở Gia Lai).", "Kế thừa từ phòng."],
            ["5", "Loại hình công việc", "Phân loại: Dọn sau trả phòng, Dọn phòng đang ở, Tổng vệ sinh định kỳ.", "Mặc định: Dọn sau trả phòng."],
            ["6", "Nhân viên thực hiện", "Nhân viên buồng phòng được giao trách nhiệm trực tiếp.", "Phân công theo ca trực."],
            ["7", "Mức độ ưu tiên", "Độ khẩn cấp: Bình thường, Ưu tiên, Khẩn cấp.", "Mặc định: Khẩn cấp khi trả phòng."],
            ["8", "Trạng thái công việc", "Trạng thái: Chưa nhận, Đang dọn, Hoàn thành, Hủy.", "Mặc định: Chưa nhận."],
            ["9", "Thời điểm bắt đầu", "Thời gian nhân viên bấm bắt đầu công việc dọn phòng.", "Cập nhật tự động."],
            ["10", "Thời điểm hoàn thành", "Thời gian nhân viên bấm hoàn tất công việc dọn phòng.", "Cập nhật tự động."],
            ["11", "Đơn đặt phòng gốc", "Đơn đặt phòng vừa trả kích hoạt sinh tự động nhiệm vụ này.", "Trường liên kết tham chiếu."],
            ["12", "Ghi chú buồng phòng", "Nhắc nhở đặc biệt về hiện trạng vệ sinh phòng hoặc lưu ý của khách.", "Trường tùy chọn."]
        ],
        "widths": [0.6, 1.8, 3.0, 1.1]
    },
    {
        "sub_id": "i. Biên bản sự cố buồng phòng",
        "table_title": "Bảng 3.11: Đặc tả thư viện dữ liệu biên bản sự cố buồng phòng",
        "fig_title": "Hình 3.10: Dữ liệu biên bản sự cố buồng phòng",
        "headers": ["STT", "Tên thuộc tính", "Đặc tả ý nghĩa", "Ghi chú"],
        "rows": [
            ["1", "Mã biên bản sự cố", "Ký hiệu định danh biên bản tự sinh theo quy định.", "Tự động sinh; Bắt buộc."],
            ["2", "Tên sự cố tóm tắt", "Mô tả ngắn gọn sự cố hỏng hóc hoặc mất mát trang thiết bị.", "Trường bắt buộc nhập."],
            ["3", "Phòng phát sinh sự cố", "Số phòng ghi nhận xảy ra hư hỏng trang thiết bị.", "Trường bắt buộc nhập."],
            ["4", "Đơn đặt phòng liên quan", "Đơn đặt phòng của khách đang ở hoặc vừa trả phòng (nếu có).", "Trường liên kết tham chiếu."],
            ["5", "Khách hàng liên đới", "Khách hàng có liên quan đến việc làm hỏng hóc trang thiết bị.", "Kế thừa từ đơn đặt phòng."],
            ["6", "Mức độ nghiêm trọng", "Phân loại: Mức độ nhẹ, Trung bình, Nghiêm trọng.", "Mặc định: Trung bình."],
            ["7", "Khóa phòng bảo trì", "Cờ đánh dấu: Nếu chọn, phòng tự động chuyển sang trạng thái Bảo trì.", "Mặc định: Tắt."],
            ["8", "Trạng thái xử lý", "Trạng thái: Tiếp nhận, Đang xử lý, Đã khắc phục, Hủy bỏ.", "Mặc định: Tiếp nhận."],
            ["9", "Chi tiết hiện trạng", "Mô tả tường trình chi tiết nguyên nhân và hiện trường hư hại.", "Trường mô tả chi tiết."],
            ["10", "Kết quả khắc phục", "Biện pháp kỹ thuật và kết quả sửa chữa của bộ phận bảo trì.", "Trường ghi nhận kết quả."]
        ],
        "widths": [0.6, 1.8, 3.0, 1.1]
    },
    {
        "sub_id": "j. Định mức vật tư buồng phòng",
        "table_title": "Bảng 3.12: Đặc tả thư viện dữ liệu định mức vật tư buồng phòng",
        "fig_title": "Hình 3.11: Dữ liệu định mức vật tư buồng phòng",
        "headers": ["STT", "Tên thuộc tính", "Đặc tả ý nghĩa", "Ghi chú"],
        "rows": [
            ["1", "Tên định mức", "Tên quy định định mức theo hạng phòng và loại vật tư.", "Trường tính toán tự động."],
            ["2", "Hạng phòng áp dụng", "Hạng phòng được thiết lập tiêu chuẩn cấp phát vật tư (Phòng đơn, Phòng đôi...).", "Trường bắt buộc nhập."],
            ["3", "Chi nhánh áp dụng", "Cơ sở áp dụng định mức này (Cơ sở 1 Gia Lai).", "Trường tùy chọn."],
            ["4", "Vật tư tiêu hao", "Đồ dùng vệ sinh cá nhân, khăn tắm hoặc nước khoáng miễn phí.", "Trường bắt buộc nhập."],
            ["5", "Đơn vị tính", "Đơn vị đo lường (chai, gói, chiếc, bộ...).", "Kế thừa từ danh mục."],
            ["6", "Số lượng định mức", "Số lượng vật tư cấp phát tiêu chuẩn cho mỗi lượt dọn.", "Mặc định: 1.0."],
            ["7", "Lượt dọn áp dụng", "Áp dụng cho: Mọi lượt dọn, Dọn sau trả phòng, Dọn phòng đang ở, Tổng vệ sinh.", "Mặc định: Mọi lượt dọn."]
        ],
        "widths": [0.6, 1.8, 3.0, 1.1]
    },
    {
        "sub_id": "k. Hóa đơn tài chính",
        "table_title": "Bảng 3.13: Đặc tả thư viện dữ liệu hóa đơn tài chính",
        "fig_title": "Hình 3.12: Dữ liệu hóa đơn tài chính",
        "headers": ["STT", "Tên thuộc tính", "Đặc tả ý nghĩa", "Ghi chú"],
        "rows": [
            ["1", "Mã số hóa đơn", "Chuỗi ký tự định danh duy nhất cho chứng từ tài chính trong hệ thống.", "Tự động sinh theo cấu trúc."],
            ["2", "Khách hàng thanh toán", "Thông tin đối tượng chịu trách nhiệm thanh toán hóa đơn lưu trú.", "Lấy từ hồ sơ khách hàng."],
            ["3", "Ngày lập hóa đơn", "Ngày phát hành chứng từ thanh toán chính thức.", "Mặc định ngày hiện tại."],
            ["4", "Đơn đặt phòng gốc", "Đơn đặt phòng lưu trú là căn cứ phát sinh hóa đơn.", "Liên kết đơn đặt phòng."],
            ["5", "Chi tiết dòng hóa đơn", "Bóc tách từng dòng: Dòng tiền thuê phòng và các dòng dịch vụ phát sinh.", "Bắt buộc có ít nhất 1 dòng."],
            ["6", "Tổng tiền hóa đơn", "Tổng giá trị dịch vụ khách sạn trước khi trừ tiền đặt cọc.", "Tính toán tự động."],
            ["7", "Số tiền cấn trừ cọc", "Khoản tiền đặt cọc đã thu trước được khấu trừ trực tiếp vào hóa đơn.", "Lấy từ đơn đặt phòng."],
            ["8", "Số tiền còn lại phải thu", "Số tiền thực tế khách hàng cần thanh toán khi nhận hóa đơn.", "Tính toán tự động."],
            ["9", "Trạng thái hóa đơn", "Trạng thái: Dự thảo, Đã vào sổ, Đang thanh toán, Đã thanh toán, Hủy.", "Mặc định: Dự thảo."]
        ],
        "widths": [0.6, 1.8, 3.0, 1.1]
    }
]

def build_senior_style_report():
    workspace_dir = '/home/trietbui/Documents/HK5/Hoach_Dinh/ERP-M_hotel_managenment'
    docx_path = os.path.join(workspace_dir, 'Bao_Cao_3.2_Quy_Trinh_Ban_Hang_MHotel.docx')
    img_path = os.path.join(workspace_dir, 'BPMN_QuyTrinh_BanHang_MHotel.png')
    md_path = '/home/trietbui/.gemini/antigravity-ide/brain/9b53c714-5a07-4012-a46d-90801bdc1ee1/DacTa_BPMN_BanHang_Format.md'

    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(0.79)
        section.bottom_margin = Inches(0.79)
        section.left_margin = Inches(1.18)
        section.right_margin = Inches(0.79)

    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(13)
    style_normal.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    style_normal.paragraph_format.line_spacing = 1.25
    style_normal.paragraph_format.space_after = Pt(4)

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(15)
        run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(11)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0x2A, 0x4B, 0x7C)
        return p

    def add_h4(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
        return p

    def add_sub_item(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        return p

    def add_caption(text, is_table=False):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        if is_table:
            run.bold = True
        else:
            run.italic = True
        return p

    def add_styled_table(headers, data, col_widths=None):
        table = doc.add_table(rows=len(data) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table, color="B0B0B0")

        hdr_cells = table.rows[0].cells
        for idx, title in enumerate(headers):
            hdr_cells[idx].text = title
            set_cell_background(hdr_cells[idx], "E9ECEF")
            set_cell_margins(hdr_cells[idx], top=120, bottom=120, left=140, right=140)
            hdr_cells[idx].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = hdr_cells[idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            for r in p.runs:
                r.bold = True
                r.font.name = 'Times New Roman'
                r.font.size = Pt(12)
                r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

        for row_idx, row_data in enumerate(data):
            row_cells = table.rows[row_idx + 1].cells
            bg_color = "FFFFFF" if row_idx % 2 == 0 else "F8F9FA"
            for col_idx, cell_value in enumerate(row_data):
                row_cells[col_idx].text = str(cell_value)
                set_cell_background(row_cells[col_idx], bg_color)
                set_cell_margins(row_cells[col_idx], top=90, bottom=90, left=130, right=130)
                row_cells[col_idx].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                p = row_cells[col_idx].paragraphs[0]
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.15
                if col_idx == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(11.5)

        if col_widths:
            for row in table.rows:
                for idx, w in enumerate(col_widths):
                    row.cells[idx].width = Inches(w)

        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_before = Pt(2)
        p_after.paragraph_format.space_after = Pt(4)
        return table

    # 3.2. Quy trình bán hàng
    add_h2("3.2. Quy trình bán hàng")
    doc.add_paragraph(
        "Quy trình bán hàng của chuỗi Khách Sạn M phản ánh toàn bộ vòng đời lưu trú của khách hàng, "
        "từ khi tiếp nhận nhu cầu đặt phòng qua trang thông tin điện tử hoặc trực tiếp tại quầy lễ tân, "
        "thực hiện kiểm tra phòng và thu tiền đặt cọc giữ chỗ, làm thủ tục nhận phòng, ghi nhận các chi phí dịch vụ "
        "và đồ uống phát sinh trong kỳ nghỉ, cho đến quyết toán trả phòng, lập hóa đơn tài chính và tự động điều phối "
        "bộ phận buồng phòng thực hiện dọn dẹp, kiểm tra thiết bị, hoàn trả phòng về trạng thái sẵn sàng đón lượt khách tiếp theo. "
        "Việc chuẩn hóa quy trình này trên nền tảng hệ thống hoạch định nguồn lực doanh nghiệp Odoo 19 giúp theo dõi tình trạng "
        "phòng và doanh thu theo thời gian thực, ngăn chặn triệt để tình trạng trùng lịch đặt phòng và tạo nền tảng dữ liệu "
        "đồng bộ xuyên suốt giữa các bộ phận."
    )

    # 3.2.1. BPMN
    add_h3("3.2.1. BPMN")
    doc.add_paragraph(
        "Sơ đồ quy trình nghiệp vụ bán hàng được mô hình hóa theo chuẩn BPMN quốc tế với 5 làn tác nghiệp rõ ràng: "
        "Khách hàng, Bộ phận lễ tân, Bộ phận kế toán, Hệ thống ERP, và Bộ phận buồng phòng. "
        "Bố cục sơ đồ được tối ưu hóa, tinh giản trực quan, thể hiện đầy đủ các luồng trao đổi thông tin, "
        "các điểm kiểm tra ràng buộc phòng trống và cơ chế xử lý ngoại lệ sự cố thiết bị."
    )

    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.add_run().add_picture(img_path, width=Inches(6.3))

    add_caption("Hình 3.1: Sơ đồ BPMN quy trình bán hàng chuỗi Khách Sạn M")

    # 3.2.2. Đặc tả
    add_h3("3.2.2. Đặc tả")
    add_h4("3.2.2.1. Đặc tả các bước của quy trình bán hàng")
    add_caption("Bảng 3.2: Đặc tả các bước quy trình bán hàng", is_table=True)
    step_headers = ["STT", "Đối tượng thực hiện", "Mô tả các bước", "Ghi chú"]
    step_widths = [0.5, 1.4, 2.0, 2.6]
    add_styled_table(step_headers, steps_senior_style, col_widths=step_widths)

    add_h4("3.2.2.2. Đặc tả thư viện dữ liệu")
    doc.add_paragraph(
        "Thư viện dữ liệu quy trình bán hàng được thiết kế chặt chẽ trên nền tảng Odoo 19, "
        "đáp ứng đầy đủ các nghiệp vụ quản lý khách sạn thực tế tại Cơ sở 1 (Thôn Dương Liễu Tây, xã Bình Dương, tỉnh Gia Lai). "
        "Cơ sở Gia Lai có quy mô gồm 13 phòng bố trí từ tầng 1 đến tầng 3 với 4 hạng phòng tiêu chuẩn: "
        "Phòng đơn (250.000 VNĐ/đêm), Phòng đôi (350.000 VNĐ/đêm), Phòng ba giường (500.000 VNĐ/đêm) và Phòng tập thể (1.000.000 VNĐ/đêm). "
        "Toàn bộ các bảng dữ liệu cốt lõi được đặc tả chi tiết dưới đây:"
    )

    for item in data_libraries_senior:
        add_sub_item(item["sub_id"])
        add_caption(item["table_title"], is_table=True)
        add_styled_table(item["headers"], item["rows"], col_widths=item["widths"])
        p_fig = add_caption(f"[{item['fig_title']} — Đính kèm ảnh chụp biểu mẫu dữ liệu thực tế trên Odoo 19]")
        p_fig.paragraph_format.space_after = Pt(8)

    # 3.2.3. Minh họa
    add_h3("3.2.3. Minh họa")
    add_h4("3.2.3.1. Minh họa quy trình trên hệ thống Odoo")

    steps_illustration = [
        ("Bước 1: Vào danh mục Khách sạn, chọn 'Tra cứu & Đặt phòng' để tiến hành tra cứu phòng trống.",
         "Nhân viên Lễ tân truy cập vào hệ thống, mở giao diện công cụ tra cứu. Màn hình cho phép chọn nhanh Cơ sở 1 (Gia Lai), "
         "hạng phòng mong muốn (Phòng đơn, Phòng đôi, Phòng ba giường, Phòng tập thể) và khung thời gian lưu trú.",
         "Hình 3.13: Bước 1 quy trình bán hàng trên Odoo"),
        ("Bước 2: Nhập thông tin tra cứu gồm Chi nhánh Gia Lai, Hạng phòng (Ví dụ: Phòng đôi), Hình thức thuê và Thời gian lưu trú, bấm 'Tìm phòng trống'.",
         "Hệ thống tự động lọc danh sách các phòng khả dụng thời gian thực trong 13 phòng của chi nhánh Gia Lai, loại trừ toàn bộ phòng đang có khách hoặc bị trùng lịch với các đơn khác.",
         "Hình 3.14: Bước 2 quy trình bán hàng trên Odoo"),
        ("Bước 3: Chọn phòng khả dụng (Ví dụ: P.104 - Phòng đôi) và bấm 'Đặt phòng ngay' để tạo Đơn đặt phòng ở trạng thái Dự thảo.",
         "Hệ thống tự động kế thừa thông tin cơ sở Gia Lai, hạng phòng Phòng đôi và số phòng P.104 với đơn giá niêm yết 350.000 VNĐ/đêm sang form Đơn đặt phòng mới.",
         "Hình 3.15: Bước 3 quy trình bán hàng trên Odoo"),
        ("Bước 4: Nhập số tiền đặt cọc thỏa thuận vào đơn đặt phòng, hệ thống tự động tính lại số tiền còn lại phải thanh toán.",
         "Thu ngân tiếp nhận tiền đặt cọc từ khách (Ví dụ: 200.000 VNĐ), nhập vào trường 'Tiền đặt cọc'. Khách thuê 2 đêm với tổng tiền phòng là 700.000 VNĐ. "
         "Hệ thống tự động tính: Số tiền còn lại = 700.000 − 200.000 = 500.000 VNĐ.",
         "Hình 3.16: Bước 4 quy trình bán hàng trên Odoo"),
        ("Bước 5: Nhấn 'Xác nhận' đơn đặt phòng, hệ thống tự động kích hoạt cơ chế chống trùng lịch và áp giá mùa vụ, chuyển trạng thái đơn sang 'Đã xác nhận' và phòng sang 'Đã đặt trước'.",
         "Cơ chế ràng buộc kiểm tra xung đột thời gian được kích hoạt tự động. Nếu hợp lệ, hệ thống áp dụng biểu giá tương ứng và giữ chỗ phòng P.104 thành công.",
         "Hình 3.17: Bước 5 quy trình bán hàng trên Odoo"),
        ("Bước 6: Khi khách đến nhận phòng, đối chiếu giấy tờ tùy thân và nhấn 'Nhận phòng'. Đơn chuyển sang 'Đang lưu trú' và phòng chuyển sang 'Đang có khách'.",
         "Lễ tân tiếp nhận Căn cước công dân hoặc Hộ chiếu, kiểm tra thông tin, thực hiện nhận phòng trên hệ thống, mã hóa thẻ từ và bàn giao chìa khóa phòng P.104 cho khách.",
         "Hình 3.18: Bước 6 quy trình bán hàng trên Odoo"),
        ("Bước 7: Theo dõi trạng thái phòng trên giao diện Sơ đồ phòng trực quan theo màu sắc.",
         "Lễ tân và ban quản lý có thể quan sát toàn bộ hiện trạng 13 phòng khách sạn tại Cơ sở Gia Lai tại giao diện trực quan theo các màu quy chuẩn (Xanh lá: Sẵn sàng, Vàng: Đã đặt trước, Đỏ: Đang có khách, Xanh dương: Cần dọn dẹp, Nâu: Bảo trì).",
         "Hình 3.19: Bước 7 quy trình bán hàng trên Odoo"),
        ("Bước 8: Trong kỳ lưu trú, ghi nhận các dịch vụ và đồ uống phát sinh vào tab Chi tiết dịch vụ của đơn đặt phòng.",
         "Khi khách hàng gọi dịch vụ giặt ủi hoặc sử dụng đồ uống trong phòng, lễ tân thêm dòng dịch vụ tương ứng. Hệ thống tự động tính thành tiền và cộng dồn vào tổng chi phí.",
         "Hình 3.20: Bước 8 quy trình bán hàng trên Odoo"),
        ("Bước 9: Khi khách trả phòng, lễ tân thông báo buồng phòng kiểm tra thực tế, bổ sung chi phí đồ uống tiêu dùng và nhấn 'Trả phòng'.",
         "Sau khi nhân viên buồng phòng kiểm tra và báo các khoản đồ uống đã dùng, lễ tân hoàn tất việc bổ sung dịch vụ phát sinh, thu lại thẻ phòng P.104 và bấm nút Trả phòng.",
         "Hình 3.21: Bước 9 quy trình bán hàng trên Odoo"),
        ("Bước 10: Hệ thống tự động chuyển đơn sang 'Đã trả phòng', phòng sang 'Cần dọn dẹp' và tự động sinh Nhiệm vụ buồng phòng khẩn cấp.",
         "Hệ thống xóa thông tin khách đang lưu trú, chuyển phòng P.104 sang trạng thái Cần dọn dẹp và tự động tạo phiếu nhiệm vụ cho bộ phận buồng phòng với mức ưu tiên Khẩn cấp.",
         "Hình 3.22: Bước 10 quy trình bán hàng trên Odoo"),
        ("Bước 11: Nhân viên buồng phòng nhận nhiệm vụ, bấm 'Bắt đầu' dọn dẹp và thay đồ vải.",
         "Nhân viên buồng phòng truy cập danh sách nhiệm vụ trên hệ thống, tiếp nhận công việc dọn phòng P.104 vừa trả và tiến hành vệ sinh sạch sẽ.",
         "Hình 3.23: Bước 11 quy trình bán hàng trên Odoo"),
        ("Bước 12: Buồng phòng hoàn thành vệ sinh, bấm 'Hoàn thành'. Hệ thống tự động chuyển phòng về 'Sẵn sàng' và tự động xuất tiêu hao vật tư theo định mức.",
         "Khi bấm Hoàn thành, phòng P.104 được khôi phục về trạng thái Sẵn sàng để mở bán cho lượt khách mới. Đồng thời, hệ thống tự động ghi nhận tiêu hao vật tư buồng phòng theo định mức của Phòng đôi.",
         "Hình 3.24: Bước 12 quy trình bán hàng trên Odoo"),
        ("Bước 13: Lễ tân nhấn 'Tạo hóa đơn' trên đơn đặt phòng, hệ thống tự động tạo hóa đơn khách hàng với đầy đủ tiền phòng và tiền dịch vụ.",
         "Hệ thống bóc tách tự động dòng tiền thuê phòng (2 đêm × 350.000 VNĐ = 700.000 VNĐ) và toàn bộ các dòng dịch vụ phát sinh trong kỳ lưu trú sang chứng từ hóa đơn bán hàng.",
         "Hình 3.25: Bước 13 quy trình bán hàng trên Odoo"),
        ("Bước 14: Kế toán kiểm tra hóa đơn, đối trừ tiền đặt cọc đã thu trước đó và nhấn 'Xác nhận' để vào sổ kế toán.",
         "Kế toán kiểm tra hóa đơn, đối trừ khoản cọc 200.000 VNĐ đã thu, xác định số tiền còn lại phải thu là 500.000 VNĐ (cộng tiền dịch vụ phát sinh nếu có), xuất Hóa đơn bán hàng và thông báo cho khách.",
         "Hình 3.26: Bước 14 quy trình bán hàng trên Odoo"),
        ("Bước 15: Kế toán bấm 'Ghi nhận thanh toán' để hoàn tất thu số tiền còn lại, hóa đơn chuyển sang trạng thái 'Đã thanh toán'.",
         "Khách hàng thanh toán số tiền còn lại bằng tiền mặt, thẻ ngân hàng hoặc chuyển khoản. Kế toán ghi nhận thanh toán hoàn tất và bàn giao hóa đơn cho khách.",
         "Hình 3.27: Bước 15 quy trình bán hàng trên Odoo")
    ]

    for title, desc, cap in steps_illustration:
        doc.add_paragraph(title)
        doc.add_paragraph(desc)
        p_c = doc.add_paragraph()
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.paragraph_format.space_before = Pt(4)
        p_c.paragraph_format.space_after = Pt(8)
        run = p_c.add_run(f"[{cap} — Đính kèm ảnh giao diện thực tế hệ thống Odoo 19]")
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        run.italic = True

    # 3.2.3.2. Ngoại lệ
    add_h4("3.2.3.2. Ngoại lệ")

    exceptions_senior = [
        ("a. Xử lý trùng lịch khi tiếp nhận đặt phòng", [
            ("Bước 1: Tiếp nhận yêu cầu chọn phòng đã có khách đặt trước trong cùng khung giờ.",
             "Khách hàng yêu cầu đặt phòng P.101 tại chi nhánh Gia Lai trong khoảng thời gian đã được một đơn khác xác nhận giữ chỗ trước.",
             "Hình 3.28: Bước 1 trường hợp trùng lịch đặt phòng trên Odoo"),
            ("Bước 2: Hệ thống kích hoạt ràng buộc chống trùng lịch và hiển thị cảnh báo lỗi, chặn lưu đơn.",
             "Hàm kiểm tra ràng buộc tự động phát hiện xung đột và hiển thị thông báo lỗi, ngăn chặn hoàn toàn việc phát sinh lỗi đặt trùng phòng.",
             "Hình 3.29: Bước 2 trường hợp trùng lịch đặt phòng trên Odoo"),
            ("Bước 3: Lễ tân mở lại công cụ tra cứu phòng trống để đổi sang phòng khác cùng hạng khả dụng.",
             "Lễ tân chọn nhanh phòng P.102 hoặc P.103 (cùng thuộc hạng Phòng đơn tại tầng 1) còn trống cho khách mà không làm gián đoạn quy trình phục vụ.",
             "Hình 3.30: Bước 3 trường hợp trùng lịch đặt phòng trên Odoo")
        ]),
        ("b. Xử lý sự cố kỹ thuật và khóa phòng bảo trì", [
            ("Bước 1: Nhân viên buồng phòng phát hiện thiết bị hư hỏng, vào mục Sự cố buồng phòng bấm 'Tạo mới'.",
             "Trong quá trình dọn dẹp hoặc kiểm tra phòng P.205, nếu phát hiện trang thiết bị (điều hòa, tivi, bình nóng lạnh...) bị hư hỏng, nhân viên tạo biên bản sự cố.",
             "Hình 3.31: Bước 1 trường hợp sự cố buồng phòng trên Odoo"),
            ("Bước 2: Điền thông tin sự cố, chọn phòng và tích chọn 'Khóa phòng', phòng tự động chuyển sang trạng thái Bảo trì.",
             "Khi tích chọn Khóa phòng, hệ thống tự động đổi trạng thái phòng P.205 sang Bảo trì và ngăn không cho lễ tân xếp khách vào phòng này.",
             "Hình 3.32: Bước 2 trường hợp sự cố buồng phòng trên Odoo"),
            ("Bước 3: Bấm nút tạo phiếu yêu cầu bảo trì kỹ thuật chuyển giao cho bộ phận kỹ thuật khắc phục.",
             "Hệ thống tự động sinh phiếu bảo trì trong phân hệ bảo trì thiết bị và thông báo cho đội ngũ kỹ thuật tiến hành sửa chữa.",
             "Hình 3.33: Bước 3 trường hợp sự cố buồng phòng trên Odoo")
        ]),
        ("c. Hủy đơn đặt phòng sau khi đã đặt cọc", [
            ("Bước 1: Khách hàng thông báo hủy đơn, lễ tân mở đơn đặt phòng đã xác nhận.",
             "Khách hàng liên hệ thông báo hủy chuyến đi đến Gia Lai trước ngày nhận phòng theo quy định hoàn hủy của khách sạn.",
             "Hình 3.34: Bước 1 trường hợp hủy đơn sau khi đặt cọc trên Odoo"),
            ("Bước 2: Lễ tân nhấn 'Hủy phòng', đơn chuyển trạng thái Đã hủy và phòng được giải phóng về Sẵn sàng.",
             "Hệ thống giải phóng phòng P.104 bị giữ chỗ về trạng thái Sẵn sàng để mở bán cho khách hàng khác trên toàn hệ thống.",
             "Hình 3.35: Bước 2 trường hợp hủy đơn sau khi đặt cọc trên Odoo"),
            ("Bước 3: Kế toán tạo hóa đơn điều chỉnh giảm (giấy báo có) để hoàn tiền cọc cho khách theo chính sách.",
             "Kế toán vào hóa đơn đặt cọc, thực hiện đảo hóa đơn (giảm trừ) và hoàn lại tiền cọc (sau khi trừ phí phạt hủy nếu có) cho khách hàng.",
             "Hình 3.36: Bước 3 trường hợp hủy đơn sau khi đặt cọc trên Odoo")
        ])
    ]

    for ex_group_title, ex_steps in exceptions_senior:
        add_sub_item(ex_group_title)
        for s_title, s_desc, s_cap in ex_steps:
            doc.add_paragraph(s_title)
            doc.add_paragraph(s_desc)
            p_c = doc.add_paragraph()
            p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_c.paragraph_format.space_before = Pt(4)
            p_c.paragraph_format.space_after = Pt(8)
            run = p_c.add_run(f"[{s_cap} — Đính kèm ảnh giao diện thực tế hệ thống Odoo 19]")
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11)
            run.italic = True

    doc.save(docx_path)
    print(f"Đã xuất thành công tệp Word chuyên đề: {docx_path}")

    # Xuất Markdown đặc tả
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("# ĐẶC TẢ QUY TRÌNH BÁN HÀNG — CHUỖI KHÁCH SẠN M-HOTEL\n")
        f.write("*(Trình bày chuẩn theo cấu trúc báo cáo Hoạch định Nguồn lực Doanh nghiệp – Dữ liệu chuẩn Cơ sở 1 Gia Lai)*\n\n")
        f.write("## 1. Thông tin doanh nghiệp & Cơ sở 1 (Gia Lai)\n")
        f.write("- **Tên tiếng Việt**: Khách Sạn M\n")
        f.write("- **Tên viết tắt**: M-Hotel\n")
        f.write("- **Trụ sở chính (Cơ sở 1)**: Thôn Dương Liễu Tây, xã Bình Dương, tỉnh Gia Lai\n")
        f.write("- **Chi nhánh mở rộng (Cơ sở 2)**: 125 Thùy Vân, Phường Thắng Tam, TP. Vũng Tàu, Tỉnh Bà Rịa – Vũng Tàu\n")
        f.write("- **Mã số thuế**: 4101567890\n")
        f.write("- **Ngày thành lập**: 18/09/2012\n")
        f.write("- **Trang thông tin điện tử**: https://m-hotel.vn\n\n")
        f.write("## 2. Bảng 3.2: Đặc tả các bước quy trình bán hàng\n\n")
        f.write("| STT | Đối tượng thực hiện | Mô tả các bước | Ghi chú |\n")
        f.write("| :---: | :--- | :--- | :--- |\n")
        for s in steps_senior_style:
            f.write(f"| {s[0]} | {s[1]} | {s[2]} | {s[3]} |\n")
        
        f.write("\n\n## 3. Đặc tả thư viện dữ liệu cốt lõi (Cơ sở 1 – Gia Lai)\n\n")
        for item in data_libraries_senior:
            f.write(f"### {item['sub_id']}\n\n")
            f.write(f"**{item['table_title']}**\n\n")
            f.write("| " + " | ".join(item['headers']) + " |\n")
            f.write("| " + " | ".join([":---:" if i==0 else ":---" for i in range(len(item['headers']))]) + " |\n")
            for r in item['rows']:
                f.write("| " + " | ".join(r) + " |\n")
            f.write(f"\n*{item['fig_title']}*\n\n")

    print(f"Đã xuất thành công tệp Markdown đặc tả: {md_path}")

if __name__ == '__main__':
    build_senior_style_report()
