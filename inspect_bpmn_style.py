import xml.etree.ElementTree as ET

tree = ET.parse('ERP-M_hotel_managenment/BPMN_QuyTrinhBanHang_MHotel.drawio')
root = tree.getroot()
for c in root.findall('.//mxCell'):
    style = c.attrib.get('style', '')
    val = c.attrib.get('value', '')
    if 'shape=mxgraph.bpmn' in style or 'swimlane' in style:
        print(f"[{c.attrib.get('id')}] val='{val[:30]}' style='{style}'\n")

