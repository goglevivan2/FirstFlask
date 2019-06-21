from xml.dom import minidom
Name=''
ID=''
def xcreate(tovar,name,id):
    Name = name
    #создаём объект
    doc = minidom.Document()

    #корневой тег root
    root = doc.createElement('root')
    doc.appendChild(root)
    print('xcreate work')
    name = doc.createElement('name')
    text = doc.createTextNode('Order')
    name.appendChild(text)
    root.appendChild(name)
    for i in tovar:
        #первый блок product
        product = doc.createElement('product')
        product.setAttribute('color', 'white')
        ID = str(id)
        article = doc.createElement('id')
        text = doc.createTextNode(str(i[0]))
        article.appendChild(text)
        article.setAttribute('color', 'white')
        product.appendChild(article)


        #цена
        size = doc.createElement('size')
        text = doc.createTextNode(str(i[1]))
        size.appendChild(text)
        size.setAttribute('red', 'green')
        product.appendChild(size)

        root.appendChild(product)

    #запись в файл
    filename = 'orders/'+ Name +ID+'.xml'
    xml_str = doc.toprettyxml(indent="  ")
    with open(filename, "w") as f:
        f.write(xml_str)
