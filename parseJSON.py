import json
from os import replace
import os
import subprocess

f = open("./src/test/resources/jsonTestFiles/chalk-package.json")
# f2 = open("newfile.json")
jsonData = json.load(f)
data = {}
data['repository'] = jsonData['repository']
data['dependencies'] = list(jsonData['dependencies'].values())
# print(list(data['dependencies'].values()))

# print(str(jsonData))
s = str(data).replace("\'", r'\"')
s = str(data)
# s = r'\"' + s + r'\"'
# print(r'\"' + s + r'\"')
print(subprocess.run(["echo", s], capture_output=True))

print(subprocess.run(["java", "-jar", "target/trustworthiness_copy-1.0-SNAPSHOT-jar-with-dependencies.jar", s], capture_output=True))

# java -jar ./target/trustworthiness_copy-1.0-SNAPSHOT.jar 
with open('jsonTemp.json', 'w') as outfile:
    json.dump(jsonData, outfile)

f.close()
