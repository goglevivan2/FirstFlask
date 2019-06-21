import xml.etree.ElementTree as ET
def par(i,d):
    file = 'orders/'+i+str(d)+'.xml'
    root = ET.parse(file).getroot()
    num = 0
    for type_tag in root.findall('product'):
        num=num+1

    return num