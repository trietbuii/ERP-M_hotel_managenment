# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

def create_bpmn_drawio(file_path):
    mxfile = ET.Element('mxfile', {
        'host': 'app.diagrams.net',
        'agent': 'M-Hotel BPMN Generator',
        'version': '24.0.0'
    })
    
    diagram = ET.SubElement(mxfile, 'diagram', {
        'name': '3.8 - Quản trị tài sản & Bảo trì buồng phòng',
        'id': 'bpmn_3_8_mhotel'
    })
    
    model = ET.SubElement(diagram, 'mxGraphModel', {
        'dx': '1422',
        'dy': '850',
        'grid': '1',
        'gridSize': '10',
        'guides': '1',
        'tooltips': '1',
        'connect': '1',
        'arrows': '1',
        'fold': '1',
        'page': '1',
        'pageScale': '1',
        'pageWidth': '3700',
        'pageHeight': '1150',
        'math': '0',
        'shadow': '0'
    })
    
    root = ET.SubElement(model, 'root')
    ET.SubElement(root, 'mxCell', {'id': '0'})
    ET.SubElement(root, 'mxCell', {'id': '1', 'parent': '0'})
    
    # 1. Main Title
    title_cell = ET.SubElement(root, 'mxCell', {
        'id': 'title',
        'value': 'SƠ ĐỒ BPMN QUY TRÌNH QUẢN TRỊ TÀI SẢN VÀ BẢO TRÌ TRANG THIẾT BỊ BUỒNG PHÒNG',
        'style': 'text;html=1;align=center;verticalAlign=middle;fontFamily=Helvetica;fontStyle=1;fontSize=24;fontColor=#0f172a;',
        'vertex': '1',
        'parent': '1'
    })
    ET.SubElement(title_cell, 'mxGeometry', {'x': '80', 'y': '20', 'width': '3500', 'height': '40', 'as': 'geometry'})
    
    subtitle_cell = ET.SubElement(root, 'mxCell', {
        'id': 'subtitle',
        'value': 'Khách Sạn M – Cơ sở Gia Lai  |  Bảo trì phòng ngừa định kỳ & Khắc phục sự cố kỹ thuật trang thiết bị buồng phòng',
        'style': 'text;html=1;align=center;verticalAlign=middle;fontFamily=Helvetica;fontSize=15;fontColor=#475569;fontStyle=2;',
        'vertex': '1',
        'parent': '1'
    })
    ET.SubElement(subtitle_cell, 'mxGeometry', {'x': '80', 'y': '65', 'width': '3500', 'height': '30', 'as': 'geometry'})
    
    # 2. Swimlanes (Horizontal)
    lanes = [
        ('lane_hk', 'BỘ PHẬN BUỒNG PHÒNG & LỄ TÂN', 110, 200, '#e0f2fe', '#f8fafc', '#0284c7'),
        ('lane_maint', 'BỘ PHẬN KỸ THUẬT & BẢO TRÌ', 310, 260, '#fef3c7', '#ffffff', '#d97706'),
        ('lane_erp', 'HỆ THỐNG ERP ODOO 19\n(m_hotel_asset & maintenance)', 570, 200, '#f3e8ff', '#faf5ff', '#7c3aed'),
        ('lane_stock_purch', 'BỘ PHẬN KHO & MUA SẮM\n(Vật tư & Phụ tùng thay thế)', 770, 200, '#ffedd5', '#fffaf5', '#ea580c'),
    ]
    
    for l_id, l_name, l_y, l_h, fill_header, fill_body, stroke in lanes:
        lane_cell = ET.SubElement(root, 'mxCell', {
            'id': l_id,
            'value': l_name,
            'style': f'swimlane;horizontal=0;startSize=55;html=1;collapsible=0;container=1;recursiveResize=0;strokeColor={stroke};strokeWidth=1.5;fillColor={fill_header};swimlaneFillColor={fill_body};fontFamily=Helvetica;fontStyle=1;fontSize=13;fontColor=#1e293b;align=center;verticalAlign=middle;whiteSpace=wrap;',
            'vertex': '1',
            'parent': '1'
        })
        ET.SubElement(lane_cell, 'mxGeometry', {'x': '80', 'y': str(l_y), 'width': '3500', 'height': str(l_h), 'as': 'geometry'})

    # Helper function for nodes
    def add_node(n_id, parent_lane, val, x, y, w, h, style):
        c = ET.SubElement(root, 'mxCell', {
            'id': n_id,
            'value': val,
            'style': style,
            'vertex': '1',
            'parent': parent_lane
        })
        ET.SubElement(c, 'mxGeometry', {'x': str(x), 'y': str(y), 'width': str(w), 'height': str(h), 'as': 'geometry'})
        return c

    # Helper function for edges
    def add_edge(e_id, source_id, target_id, label='', style=None):
        if style is None:
            style = 'edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#334155;strokeWidth=1.5;fontFamily=Helvetica;fontSize=11;fontColor=#0f172a;'
        c = ET.SubElement(root, 'mxCell', {
            'id': e_id,
            'value': label,
            'style': style,
            'edge': '1',
            'source': source_id,
            'target': target_id,
            'parent': '1'
        })
        ET.SubElement(c, 'mxGeometry', {'relative': '1', 'as': 'geometry'})
        return c

    # STYLES
    s_start = 'ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#dcfce7;strokeColor=#16a34a;strokeWidth=2;fontFamily=Helvetica;fontSize=11;fontColor=#14532d;fontStyle=1;align=center;verticalAlign=middle;'
    s_end = 'ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#fee2e2;strokeColor=#dc2626;strokeWidth=3;fontFamily=Helvetica;fontSize=11;fontColor=#7f1d1d;fontStyle=1;align=center;verticalAlign=middle;'
    s_task_hk = 'rounded=1;arcSize=12;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#0284c7;strokeWidth=1.5;fontFamily=Helvetica;fontSize=11;fontColor=#0f172a;align=center;verticalAlign=middle;shadow=0;'
    s_task_maint = 'rounded=1;arcSize=12;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#d97706;strokeWidth=1.5;fontFamily=Helvetica;fontSize=11;fontColor=#0f172a;align=center;verticalAlign=middle;shadow=0;'
    s_task_erp = 'rounded=1;arcSize=12;whiteSpace=wrap;html=1;fillColor=#faf5ff;strokeColor=#7c3aed;strokeWidth=1.5;fontFamily=Helvetica;fontSize=11;fontColor=#3b0764;fontStyle=1;align=center;verticalAlign=middle;shadow=0;'
    s_task_stock = 'rounded=1;arcSize=12;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#ea580c;strokeWidth=1.5;fontFamily=Helvetica;fontSize=11;fontColor=#0f172a;align=center;verticalAlign=middle;shadow=0;'
    s_gw = 'rhombus;whiteSpace=wrap;html=1;fillColor=#fef3c7;strokeColor=#b45309;strokeWidth=1.5;fontFamily=Helvetica;fontSize=11;fontStyle=1;fontColor=#78350f;align=center;verticalAlign=middle;'

    # --- NODES IN LANE HK ---
    add_node('start_hk', 'lane_hk', 'Phát hiện sự cố<br>thiết bị buồng phòng', 100, 75, 70, 70, s_start)
    add_node('task_hk_inc', 'lane_hk', 'Lập biên bản sự cố<br>buồng phòng<br><b>(hotel.incident)</b>', 230, 75, 140, 70, s_task_hk)
    add_node('task_hk_lock', 'lane_hk', 'Đánh giá mức độ<br>&amp; tích chọn<br><b>"Khóa phòng"</b>', 420, 75, 140, 70, s_task_hk)
    add_node('task_hk_transfer', 'lane_hk', 'Nhấn nút<br><b>"Chuyển bảo trì<br>Kỹ thuật"</b>', 610, 75, 140, 70, s_task_hk)
    add_node('task_hk_inspect', 'lane_hk', 'Kiểm tra hiện trường,<br>nghiệm thu thiết bị &amp;<br>bấm <b>"Đã khắc phục"</b>', 2850, 75, 150, 70, s_task_hk)
    add_node('task_hk_clean', 'lane_hk', 'Vệ sinh khử khuẩn,<br>bổ sung amenities &amp;<br>bấm <b>"Hoàn thành"</b>', 3180, 75, 150, 70, s_task_hk)
    add_node('end_event', 'lane_hk', 'Phòng sẵn sàng<br>đón khách mới', 3400, 75, 70, 70, s_end)

    # --- NODES IN LANE MAINT ---
    add_node('start_prev', 'lane_maint', 'Đến hạn bảo trì<br>phòng ngừa<br>định kỳ (Checklist)', 100, 105, 70, 70, s_start)
    add_node('task_maint_assign', 'lane_maint', 'Trưởng bộ phận<br>tiếp nhận phiếu &amp;<br>phân công kỹ thuật viên', 980, 105, 150, 70, s_task_maint)
    add_node('task_maint_start', 'lane_maint', 'Kéo sang <b>"Đang thực hiện"</b>,<br>mang dụng cụ đến phòng<br>khảo sát hiện trường', 1190, 105, 160, 70, s_task_maint)
    add_node('gw_parts', 'lane_maint', 'Cần thay<br>linh kiện?', 1410, 100, 80, 80, s_gw)
    add_node('task_maint_direct', 'lane_maint', 'Sửa chữa tại chỗ:<br>Vệ sinh lưới lọc, nạp gas,<br>thông van, siết ốc, reset mạch', 1540, 30, 170, 70, s_task_maint)
    add_node('task_maint_check_stock', 'lane_maint', 'Kiểm tra số lượng tồn<br>kho linh kiện phụ tùng<br>trên hệ thống Odoo', 1540, 155, 170, 70, s_task_maint)
    add_node('gw_stock', 'lane_maint', 'Còn<br>phụ tùng?', 1770, 150, 80, 80, s_gw)
    add_node('task_maint_req_stock', 'lane_maint', 'Lập phiếu xuất kho<br>vật tư phụ tùng bảo trì<br><b>(stock.picking nội bộ)</b>', 1900, 155, 160, 70, s_task_maint)
    add_node('task_maint_replace', 'lane_maint', 'Tháo dỡ linh kiện cũ,<br>tiến hành lắp ráp<br>phụ tùng thay thế mới', 2340, 105, 150, 70, s_task_maint)
    add_node('task_maint_test', 'lane_maint', 'Vận hành thử tải<br>15-30 phút &amp; kiểm tra<br>an toàn điện, rò rỉ gas/nước', 2530, 105, 160, 70, s_task_maint)
    add_node('task_maint_log', 'lane_maint', 'Cập nhật nhật ký xử lý,<br>thời lượng sửa chữa &amp;<br>bấm <b>"Đã sửa chữa"</b>', 2720, 105, 160, 70, s_task_maint)

    # --- NODES IN LANE ERP ---
    add_node('task_erp_lock', 'lane_erp', 'Tự động khóa phòng:<br>Đổi trạng thái phòng sang<br><b>"Bảo trì" (maintenance)</b>', 610, 65, 150, 70, s_task_erp)
    add_node('task_erp_gen_req', 'lane_erp', 'Tự động sinh Phiếu bảo trì<br><b>(maintenance.request)</b><br>kèm mã phòng &amp; thiết bị', 800, 65, 160, 70, s_task_erp)
    add_node('task_erp_deduct', 'lane_erp', 'Tự động trừ tồn kho &amp;<br>cộng dồn chi phí linh kiện<br>vào phiếu bảo trì', 2180, 65, 160, 70, s_task_erp)
    add_node('task_erp_cleaning', 'lane_erp', 'Giải phóng cờ khóa phòng:<br>Đổi trạng thái sang<br><b>"Cần dọn dẹp" (cleaning)</b>', 3020, 65, 160, 70, s_task_erp)
    add_node('task_erp_available', 'lane_erp', 'Đổi trạng thái phòng sang<br><b>"Sẵn sàng" (available)</b><br>&amp; lưu lịch sử tài sản', 3270, 65, 160, 70, s_task_erp)

    # --- NODES IN LANE STOCK & PURCHASING ---
    add_node('task_stock_order', 'lane_stock_purch', 'Lập đề xuất mua sắm<br>linh kiện thay thế hoặc<br><b>thay nóng từ kho dự phòng</b>', 1890, 65, 180, 70, s_task_stock)
    add_node('task_stock_deliver', 'lane_stock_purch', 'Thủ kho kiểm tra &amp;<br>xác nhận xuất kho linh kiện<br>cho Kỹ thuật viên', 2110, 65, 170, 70, s_task_stock)

    # --- EDGES / FLOWS ---
    # Luồng sự cố buồng phòng
    add_edge('e1', 'start_hk', 'task_hk_inc')
    add_edge('e2', 'task_hk_inc', 'task_hk_lock')
    add_edge('e3', 'task_hk_lock', 'task_hk_transfer')
    add_edge('e4', 'task_hk_transfer', 'task_erp_lock')
    add_edge('e5', 'task_erp_lock', 'task_erp_gen_req')
    add_edge('e6', 'task_erp_gen_req', 'task_maint_assign')
    
    # Luồng bảo trì phòng ngừa
    add_edge('e_prev', 'start_prev', 'task_maint_assign', 'Lịch định kỳ')
    
    # Kỹ thuật viên xử lý
    add_edge('e7', 'task_maint_assign', 'task_maint_start')
    add_edge('e8', 'task_maint_start', 'gw_parts')
    
    # Rẽ nhánh cần linh kiện
    add_edge('e9_no', 'gw_parts', 'task_maint_direct', 'Không')
    add_edge('e9_yes', 'gw_parts', 'task_maint_check_stock', 'Có')
    
    # Rẽ nhánh tồn kho
    add_edge('e10', 'task_maint_check_stock', 'gw_stock')
    add_edge('e11_yes', 'gw_stock', 'task_maint_req_stock', 'Còn hàng')
    add_edge('e11_no', 'gw_stock', 'task_stock_order', 'Hết hàng / Hỏng nặng')
    
    # Xuất kho và trừ kho
    add_edge('e12', 'task_maint_req_stock', 'task_stock_deliver')
    add_edge('e13', 'task_stock_order', 'task_stock_deliver', 'Bổ sung xong')
    add_edge('e14', 'task_stock_deliver', 'task_erp_deduct')
    add_edge('e15', 'task_erp_deduct', 'task_maint_replace')
    
    # Sửa xong chạy thử nghiệm
    add_edge('e16', 'task_maint_replace', 'task_maint_test')
    add_edge('e17', 'task_maint_direct', 'task_maint_test')
    
    # Đóng bảo trì và nghiệm thu
    add_edge('e18', 'task_maint_test', 'task_maint_log')
    add_edge('e19', 'task_maint_log', 'task_hk_inspect')
    add_edge('e20', 'task_hk_inspect', 'task_erp_cleaning')
    add_edge('e21', 'task_erp_cleaning', 'task_hk_clean')
    add_edge('e22', 'task_hk_clean', 'task_erp_available')
    add_edge('e23', 'task_erp_available', 'end_event')

    # Write file
    tree = ET.ElementTree(mxfile)
    ET.indent(tree, space='  ', level=0)
    tree.write(file_path, encoding='utf-8', xml_declaration=True)
    print(f"BPMN Drawio generated successfully at: {file_path}")

if __name__ == '__main__':
    out_drawio = r'f:\Project Hoạch định\Sơ đồ BPMN\BPMN_3.8_Quan_Tri_Tai_San_Bao_Tri_MHotel.drawio'
    create_bpmn_drawio(out_drawio)

