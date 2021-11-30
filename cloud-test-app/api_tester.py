import requests

BASE = 'http://127.0.0.1:5000/'
headers = {'Content-type':'application/json'}

# response = requests.get(BASE + 'api')
# print(response.text)

# payload = "{\n\t\"metadata\": {\n\t\t\"Name\": \"Underscore\",\n\t\t\"Version\": \"1.0.0\",\n\t\t\"ID\": \"underscore\"\n\t},\n\t\"data\": {\n\t\t\"Content\": \"\",\n\t\t\"URL\": \"https://github.com/jashkenas/underscore\",\n\t\t\"JSProgram\": \"if (process.argv.length === 7) {\\nconsole.log('Success')\\nprocess.exit(0)\\n} else {\\nconsole.log('Failed')\\nprocess.exit(1)\\n}\\n>\"\n\t}\n}"

# payload = "{\n\t\"metadata\": {\n\t\t\"Name\": \"chalk\",\n\t\t\"Version\": \"0.1.2\",\n\t\t\"ID\": \"package1\"\n\t},\n\t\"data\": {\n\t\t\"Content\": \"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\",\n\t\t\"URL\": \"https://github.com/jashkenas/underscore\",\n\t\t\"JSProgram\": \"if (process.argv.length === 7) {\\nconsole.log('Success')\\nprocess.exit(0)\\n} else {\\nconsole.log('Failed')\\nprocess.exit(1)\\n}\\n>\"\n\t}\n}"
# response = requests.post(BASE + '/package', data=payload, headers=headers)
# print(response.text)

# response = requests.get(BASE + '/package/package1/rate', headers=headers)
# print(response.text)

response = requests.get(BASE + '/package/package6', headers=headers)
print(response.text)

# payload = "{\n\t\"metadata\": {\n\t\t\"Name\": \"chalk\",\n\t\t\"Version\": \"0.1.2\",\n\t\t\"ID\": \"package1\"\n\t},\n\t\"data\": {\n\t\t\"Content\": \"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\",\n\t\t\"URL\": \"https://github.com/jashkenas/underscore\",\n\t\t\"JSProgram\": \"if (process.argv.length === 7) {\\nconsole.log('Success')\\nprocess.exit(0)\\n} else {\\nconsole.log('Failed')\\nprocess.exit(1)\\n}\\n>\"\n\t}\n}"
# response = requests.put(BASE + '/package/package1', data=payload, headers=headers)
# print(response.text)

# response = requests.get(BASE + '/package/package2', headers=headers)
# print(response.text)

# response = requests.delete(BASE + '/package/package1')
# print(response.text)

# response = requests.delete(BASE + 'package/byName/chalk')
# print(response.text)

# response = requests.delete(BASE + '/reset')
# print(response.text)




