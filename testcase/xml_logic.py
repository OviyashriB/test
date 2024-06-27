import xml.etree.ElementTree as ET

def find_company_names(xml_file_path):
    try:
        tree = ET.parse(xml_file_path) #Element tree
        root = tree.getroot()

        company_names = []

        for company_element in root.findall('.//CompanyName'):
            company_name = company_element.text
            if company_name:
                company_names.append(company_name)

        return company_names

    except ET.ParseError:
        return "Error: Invalid XML file."

xml_file_path = r"C:\Users\aWeSoME jAN\Downloads\test_purpose.xml"
company_names = find_company_names(xml_file_path)

if isinstance(company_names, list) and company_names:
    for i, name in enumerate(company_names, start=1):
        print(f"Company {i}: {name}")
else:
    print("No CompanyName elements found in the XML.")


# alternate method using tag search
# def find_elements_by_tag(xml_file_path, tag):
#     try:
#         tree = ET.parse(xml_file_path)
#         root = tree.getroot()

#         elements = []

#         # Iterate through all elements with the specified tag
#         for element in root.iter(tag):
#             element_text = element.text
#             if element_text:
#                 elements.append(element_text)

#         return elements

#     except ET.ParseError:
#         return "Error: Invalid XML file."

# xml_file_path = r"C:\Users\aWeSoME jAN\Downloads\test_purpose.xml"
# tag_to_search = 'CompanyName'
# company_names = find_elements_by_tag(xml_file_path, tag_to_search)

# if isinstance(company_names, list) and company_names:
#     for i, name in enumerate(company_names, start=1):
#         print(f"Company {i}: {name}")
# else:
#     print(f"No '{tag_to_search}' elements found in the XML.")


def retrieve_ordered_dates(xml_file_path, customer_id, validation_date):
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        validation_datetime = datetime.strptime(validation_date, '%d/%m/%Y')

        for i, order_element in enumerate(root.findall('.//Order'), start=1):
            customer_id_element = order_element.find('CustomerID')
            if customer_id_element is not None and customer_id in customer_id_element.text:
                order_date_element = order_element.find('OrderDate')
                if order_date_element is not None:
                    order_datetime = datetime.strptime(order_date_element.text, '%Y-%m-%dT%H:%M:%S')
                    if order_datetime > validation_datetime:
                        ordered_date = convert_to_12_hour_clock_with_date(order_date_element.text)
                        print(f"{i} -> Ordered Date and Time: {ordered_date}")

    except ET.ParseError:
        return "Error: Invalid XML file."

 

xml_file_path = r"C:\Users\aWeSoME jAN\Downloads\test_purpose.xml"

customer_id_to_search = 'GREAL'

validation_date = '30/09/1997'

retrieve_ordered_dates(xml_file_path, customer_id_to_search, validation_date)