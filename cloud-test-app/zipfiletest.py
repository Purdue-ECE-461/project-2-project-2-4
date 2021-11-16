import base64

fin = open('project-2-starter-4.zip', 'rb')
fin_read = fin.read()
zipasbytes = base64.b64encode(fin_read)
fin.close()
print(zipasbytes)
print(type(zipasbytes))