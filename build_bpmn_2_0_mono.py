# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

def build_bpmn_2_0_monochrome(output_file):
    mxfile = ET.Element('mxfile', {
        'host': 'app.diagrams.net',
        'agent': 'M-Hotel BPMN 2.0 Engine',
        'version': '24.0.0'
    })
    
    diagram = ET.SubElement(mxfile, 'diagram', {
        'name': '3.8 - BPMN Quản trị tài sản & Bảo trì',
        'id': 'bpmn_3_8_monochrome'
    })
    
    # 2250 width, 680 height
    model = ET.SubElement(diagram, 'mxGraphModel', {
        'dx': '1422', 'dy': '850', 'grid': '1', 'gridSize': '10', 'guides': '1',
        'tooltips': '1', 'connect': '1', 'arrows': '1', 'fold': '1', 'page': '0',
        'pageScale': '1', 'pageWidth': '2300', 'pageHeight': '700', 'math': '0', 'shadow': '0'
    })
    
    root = ET.SubElement(model, 'root')
    ET.SubElement(root, 'mxCell', {'id': '0'})
    ET.SubElement(root, 'mxCell', {'id': '1', 'parent': '0'})
    
    # Pool M-Hotel
    pool_w = 2240
    pool_h = 600
    pool_x = 20
    pool_y = 20
    
    pool = ET.SubElement(root, 'mxCell', {
        'id': 'pool',
        'value': 'Khách Sạn M – Cơ sở 1 Gia Lai (Quy trình quản trị tài sản &amp; bảo trì buồng phòng)',
        'style': 'swimlane;html=1;horizontal=0;startSize=24;collapsible=0;fontSize=10;fontStyle=1;fillColor=#ffffff;swimlaneFillColor=#ffffff;strokeColor=#000000;strokeWidth=1;whiteSpace=wrap;fontFamily=Helvetica;fontColor=#000000;',
        'vertex': '1',
        'parent': '1'
    })
    ET.SubElement(pool, 'mxGeometry', {'x': str(pool_x), 'y': str(pool_y), 'width': str(pool_w), 'height': str(pool_h), 'as': 'geometry'})
    
    # 4 Swimlanes
    lanes_conf = [
        ('lane_hk', 'Bộ phận buồng phòng &amp; Lễ tân', 0, 150),
        ('lane_maint', 'Bộ phận kỹ thuật &amp; Bảo trì', 150, 160),
        ('lane_erp', 'Hệ thống ERP Odoo 19', 310, 140),
        ('lane_stock', 'Bộ phận kho vật tư', 450, 150),
    ]
    
    lane_w = pool_w - 24
    for l_id, l_name, l_y, l_h in lanes_conf:
        l_cell = ET.SubElement(root, 'mxCell', {
            'id': l_id,
            'value': l_name,
            'style': 'swimlane;html=1;horizontal=0;startSize=24;collapsible=0;fontSize=9;fontStyle=1;fillColor=#ffffff;swimlaneFillColor=#ffffff;strokeColor=#000000;strokeWidth=1;whiteSpace=wrap;fontFamily=Helvetica;fontColor=#000000;',
            'vertex': '1',
            'parent': 'pool'
        })
        ET.SubElement(l_cell, 'mxGeometry', {'x': '24', 'y': str(l_y), 'width': str(lane_w), 'height': str(l_h), 'as': 'geometry'})

    # STYLES (Strict BPMN 2.0 Standard, 100% Monochrome Black & White)
    s_start = 'shape=mxgraph.bpmn.event;perimeter=ellipsePerimeter;aspect=fixed;outline=standard;symbol=general;labelBackgroundColor=#ffffff;fontSize=8.5;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;outlineConnect=0;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1;fontFamily=Helvetica;fontColor=#000000;'
    s_start_timer = 'shape=mxgraph.bpmn.event;perimeter=ellipsePerimeter;aspect=fixed;outline=standard;symbol=timer;labelBackgroundColor=#ffffff;fontSize=8.5;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;outlineConnect=0;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1;fontFamily=Helvetica;fontColor=#000000;'
    s_end = 'shape=mxgraph.bpmn.event;perimeter=ellipsePerimeter;aspect=fixed;outline=end;symbol=general;labelBackgroundColor=#ffffff;fontSize=8.5;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;outlineConnect=0;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2.5;fontFamily=Helvetica;fontColor=#000000;'
    s_gw = 'shape=mxgraph.bpmn.gateway2;perimeter=rhombusPerimeter;background=none;outline=none;symbol=exclusiveGw;labelBackgroundColor=#ffffff;fontSize=8.5;verticalLabelPosition=top;verticalAlign=bottom;align=center;html=1;outlineConnect=0;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1;fontFamily=Helvetica;fontColor=#000000;'
    
    # Task markers
    s_task_user = 'shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=8;container=1;expand=0;collapsible=0;fontSize=8.5;taskMarker=user;spacingTop=6;spacingBottom=0;spacingLeft=2;spacingRight=2;html=1;outlineConnect=0;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1;fontFamily=Helvetica;fontColor=#000000;align=center;verticalAlign=middle;'
    s_task_service = 'shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=8;container=1;expand=0;collapsible=0;fontSize=8.5;taskMarker=service;spacingTop=6;spacingBottom=0;spacingLeft=2;spacingRight=2;html=1;outlineConnect=0;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1;fontFamily=Helvetica;fontColor=#000000;align=center;verticalAlign=middle;'
    s_task_manual = 'shape=mxgraph.bpmn.task2;whiteSpace=wrap;rectStyle=rounded;size=8;container=1;expand=0;collapsible=0;fontSize=8.5;taskMarker=manual;spacingTop=6;spacingBottom=0;spacingLeft=2;spacingRight=2;html=1;outlineConnect=0;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1;fontFamily=Helvetica;fontColor=#000000;align=center;verticalAlign=middle;'

    def add_node(n_id, lane_parent, val, x, y, w, h, style):
        c = ET.SubElement(root, 'mxCell', {
            'id': n_id,
            'value': val,
            'style': style,
            'vertex': '1',
            'parent': lane_parent
        })
        ET.SubElement(c, 'mxGeometry', {'x': str(x), 'y': str(y), 'width': str(w), 'height': str(h), 'as': 'geometry'})
        return c

    def add_flow(e_id, source_id, target_id, label=''):
        c = ET.SubElement(root, 'mxCell', {
            'id': e_id,
            'value': label,
            'style': 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1;fontSize=8;fontColor=#000000;fontFamily=Helvetica;labelBackgroundColor=#ffffff;',
            'edge': '1',
            'source': source_id,
            'target': target_id,
            'parent': 'pool'
        })
        ET.SubElement(c, 'mxGeometry', {'relative': '1', 'as': 'geometry'})
        return c

    # --- LANE BUỒNG PHÒNG & LỄ TÂN (y: 0 - 150) ---
    add_node('e_start_hk', 'lane_hk', 'Phát hiện sự cố<br>thiết bị tại P.104', 35, 60, 30, 30, s_start)
    add_node('t_hk_1', 'lane_hk', 'Lập biên bản sự cố<br>(hotel.incident)', 90, 50, 110, 50, s_task_user)
    add_node('gw_lock', 'lane_hk', 'Cần khóa<br>phòng?', 225, 57, 35, 35, s_gw)
    add_node('t_hk_lock', 'lane_hk', 'Tích chọn &quot;Khóa phòng&quot;<br>(block_room=True)', 285, 20, 115, 45, s_task_user)
    add_node('t_hk_nolock', 'lane_hk', 'Giữ phòng hoạt động<br>(block_room=False)', 285, 85, 115, 45, s_task_user)
    add_node('t_hk_send', 'lane_hk', 'Nhấn nút &quot;Tạo Yêu Cầu<br>Sửa Chữa (Kỹ Thuật)&quot;', 430, 50, 125, 50, s_task_user)
    
    add_node('t_hk_inspect', 'lane_hk', 'Kiểm tra hiện trường<br>&amp; nghiệm thu thiết bị', 1620, 50, 115, 50, s_task_manual)
    add_node('t_hk_resolve', 'lane_hk', 'Mở sự cố gốc, nhấn<br>&quot;Đã khắc phục&quot;', 1765, 50, 115, 50, s_task_user)
    add_node('t_hk_clean', 'lane_hk', 'Vệ sinh phòng &amp; bấm<br>&quot;Hoàn thành&quot; dọn phòng', 1985, 50, 120, 50, s_task_user)
    add_node('e_end', 'lane_hk', 'Phòng sẵn sàng<br>đón khách mới', 2145, 60, 30, 30, s_end)

    # --- LANE BỘ PHẬN KỸ THUẬT & BẢO TRÌ (y: 150 - 310) ---
    add_node('e_start_prev', 'lane_maint', 'Đến hạn bảo trì<br>định kỳ (Chu kỳ)', 35, 65, 30, 30, s_start_timer)
    add_node('t_maint_receive', 'lane_maint', 'Tiếp nhận phiếu &amp;<br>chọn thiết bị P.104', 680, 55, 115, 50, s_task_user)
    add_node('t_maint_assign', 'lane_maint', 'Phân công kỹ thuật viên<br>&amp; kéo sang In Progress', 820, 55, 120, 50, s_task_user)
    add_node('t_maint_survey', 'lane_maint', 'Đến phòng P.104<br>khảo sát &amp; đo đạc lỗi', 965, 55, 115, 50, s_task_manual)
    add_node('gw_parts', 'lane_maint', 'Cần thay<br>phụ tùng?', 1105, 62, 35, 35, s_gw)
    add_node('t_maint_direct', 'lane_maint', 'Sửa chữa tại chỗ:<br>Vệ sinh, nạp gas, siết ốc', 1165, 20, 125, 45, s_task_manual)
    add_node('t_maint_replace', 'lane_maint', 'Thay thế linh kiện<br>phụ tùng mới vào máy', 1320, 85, 120, 45, s_task_manual)
    add_node('t_maint_test', 'lane_maint', 'Vận hành thử tải 15-30p<br>&amp; kiểm tra an toàn điện', 1335, 20, 125, 45, s_task_manual)
    add_node('t_maint_finish', 'lane_maint', 'Ghi thời lượng &amp; kéo<br>sang &quot;Đã sửa chữa&quot;', 1485, 55, 115, 50, s_task_user)

    # --- LANE HỆ THỐNG ERP ODOO 19 (y: 310 - 450) ---
    add_node('t_erp_lock', 'lane_erp', 'Khóa phòng: Trạng thái<br>phòng -&gt; &quot;Bảo trì&quot;', 435, 45, 120, 50, s_task_service)
    add_node('t_erp_gen', 'lane_erp', 'Tự động tạo Phiếu bảo trì<br>(maintenance.request)', 575, 45, 125, 50, s_task_service)
    add_node('t_erp_cleaning', 'lane_erp', 'Đổi trạng thái phòng sang<br>&quot;Cần dọn dẹp&quot; (cleaning)', 1875, 45, 125, 50, s_task_service)
    add_node('t_erp_avail', 'lane_erp', 'Đổi phòng sang &quot;Sẵn sàng&quot;<br>&amp; tăng số lần bảo trì', 1985, 45, 120, 50, s_task_service)

    # --- LANE BỘ PHẬN KHO VẬT TƯ (y: 450 - 600) ---
    add_node('t_stock_export', 'lane_stock', 'Thủ kho xuất kho linh kiện<br>trên phân hệ Tồn kho', 1165, 45, 125, 50, s_task_user)

    # --- EDGES / FLOWS ---
    add_flow('f1', 'e_start_hk', 't_hk_1')
    add_flow('f2', 't_hk_1', 'gw_lock')
    add_flow('f3_y', 'gw_lock', 't_hk_lock', 'Có')
    add_flow('f3_n', 'gw_lock', 't_hk_nolock', 'Không')
    add_flow('f4_1', 't_hk_lock', 't_hk_send')
    add_flow('f4_2', 't_hk_nolock', 't_hk_send')
    
    # Send -> ERP
    add_flow('f5', 't_hk_send', 't_erp_lock')
    add_flow('f6', 't_erp_lock', 't_erp_gen')
    add_flow('f7', 't_erp_gen', 't_maint_receive')
    
    # Định kỳ -> Maint
    add_flow('f_prev', 'e_start_prev', 't_maint_receive', 'Lịch định kỳ')
    
    # Maint execution
    add_flow('f8', 't_maint_receive', 't_maint_assign')
    add_flow('f9', 't_maint_assign', 't_maint_survey')
    add_flow('f10', 't_maint_survey', 'gw_parts')
    
    # Gateway parts
    add_flow('f11_n', 'gw_parts', 't_maint_direct', 'Không')
    add_flow('f11_y', 'gw_parts', 't_stock_export', 'Có')
    
    # Stock -> Replace
    add_flow('f12', 't_stock_export', 't_maint_replace')
    add_flow('f13_1', 't_maint_replace', 't_maint_test')
    add_flow('f13_2', 't_maint_direct', 't_maint_test')
    
    # Test -> Finish
    add_flow('f14', 't_maint_test', 't_maint_finish')
    
    # Finish -> Buồng phòng nghiệm thu
    add_flow('f15', 't_maint_finish', 't_hk_inspect')
    add_flow('f16', 't_hk_inspect', 't_hk_resolve')
    
    # Resolve -> ERP Cleaning
    add_flow('f17', 't_hk_resolve', 't_erp_cleaning')
    add_flow('f18', 't_erp_cleaning', 't_hk_clean')
    
    # Clean -> ERP Available -> End
    add_flow('f19', 't_hk_clean', 't_erp_avail')
    add_flow('f20', 't_erp_avail', 'e_end')

    # Save
    tree = ET.ElementTree(mxfile)
    ET.indent(tree, space='  ', level=0)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    print(f"Monochrome BPMN 2.0 generated at: {output_file}")

if __name__ == '__main__':
    out_path = r'f:\Project Hoạch định\Sơ đồ BPMN\BPMN_3.8_Quan_Tri_Tai_San_Bao_Tri_MHotel_BPMN20_Mono.drawio'
    build_bpmn_2_0_monochrome(out_path)

