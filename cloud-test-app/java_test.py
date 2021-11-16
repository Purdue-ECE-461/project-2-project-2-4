import subprocess

command_line_arg = "{'repository': 'chalk/chalk', 'dependencies': ['^6.1.0', '^9.0.2']}"
output = subprocess.run(["java", "-jar", "trustworthiness_copy-1.0-SNAPSHOT-jar-with-dependencies.jar", command_line_arg], capture_output=True)

print("STDOUT: ", output.stdout.decode("utf-8"))
print("\n\n\nSTDERR: ", output.stdout.decode("utf-8"))
print(output.args)
print("\n", output)
test = b'URL from conURL: https://api.github.com/repos/chalk/chalk/readme\\nRESPONSE = 200\\nCalculating correctness score...\\nCloning chalk/chalk.git ...\\nLocal repo ./tempRepo still exists\\nDeleting and trying again...\\nDeleting repo clone in local directory ./tmpRepo\\njava.lang.NullPointerException: Cannot invoke \"org.eclipse.jgit.api.Git.close()\" because \"this.git\" is null\\njava.nio.file.NoSuchFileException: ./tmpRepo\\nCalculating responsiveness score...\\nCalculating bus factor score...\\nURL from conURL: https://api.github.com/repos/chalk/chalk/contributors\\nRESPONSE = 200\\nCalculating license score...\\nCalculating ramp up time score...\\nURL from conURL: https://api.github.com/repos/chalk/chalk/git/trees/master\\nIn Else block: Exception in httpreq: \\n{\"Scores\":[{\"url\":\"chalk/chalk\",\"correctnessScore\":-1.0,\"responsivenessScore\":0.99561405,\"busFactor\":1.0,\"licenseScore\":1.0,\"rampUpTimeScore\":1.0,\"dependencyRatio\":1.0,\"netScore\":0.3991228}]}\\n'


test = test.decode('utf-8')
print("\n\n\n",test)
printout={
            "description": "Welcome to the Package Manager API!", 
            "Available Commands": {
                "View Packages" : "/packages",
                "Reset System" : "/reset",
                "Upload Package" : "/package",
                "Package by Name" : "/package/byName/{name}",
                "Package by ID" : "/package/{id}",
                "Package Rating by ID" : "/package/{id}/rate"
            }
        } 
        
print(printout)