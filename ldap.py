import xml.etree.ElementTree as ET, csv, urllib.request

def query_ldap(id):
	tree = ET.parse(urllib.request.urlopen('[your_ldap_server]/Query?serverID=[server_id]&searchBase=o=[the_org]&Prebuilt=true&scope=2&filter=id=' + id ))
	ns = {'dsml': 'http://www.dsml.org/DSML','env':'http://schemas.xmlsoap.org/soap/envelope/'}
	body = tree.find('env:Body',ns)
	entry = body.find('dsml:dsml/dsml:directory-entries/dsml:entry',ns)
	emp = []
	if entry is not None:
		emp = ['','','','']
		sso = entry.find("dsml:attr[@name='uid']/dsml:value",ns)
		if sso is not None and sso.text is not None: emp[0] = sso.text
		name = entry.find("dsml:attr[@name='cn']/dsml:value",ns)
		if name is not None and name.text is not None: emp[1] = name.text
		email = entry.find("dsml:attr[@name='mail']/dsml:value",ns)
		if email is not None and email.text is not None: emp[2] = email.text
		country = entry.find("dsml:attr[@name='c']/dsml:value",ns)
		if country is not None and country.text is not None: emp[3] = country.text
	else:
		print('Could not find ' + id)
	return emp

ids_list=open('list_of_ids.txt','r')
idx = 0;
with open('output.csv','w', newline='',encoding='utf-8') as f:
	writer = csv.writer(f, dialect='excel')
	writer.writerow(['id','name','email','country'])
	for id in ids_list:
		print (idx , ' ', id)
		idx += 1
		record = query_ldap(id)
		if record: writer.writerow(record)
