Our Python script is designed to extract security bug fixes commits and convert them into a JSON format, to be used with the pyszz implementation provided by grosa1 on GitHub. <br>
It is also able to extract relevant information from pyszz output, such as:
- developer name : number of security vulnerabilities introduced 
- percentage of commits that fix a previously introduced vulnerability 

## Usage 
1. Pull the project <br>

2. Run the following command `python3 pyszz_json_generator.py [param]` <br>
Where `param` should be replaced with the project path on which you want to extract commits related to security bug fixes. <br>
the script will generate a file called `data.json` in the folder where it is located. <br>
By default it generates entries in the following form: 
```
[
  {
    "repo_name": "apache/tomcat",
    "fix_commit_hash": "30ae3f5421"
  },
  ...
]
```
Where `"repo_name"` will be the name of the folder passed as input to the script. <br> 

3. louch `pyszz` script from <a href=https://github.com/grosa1/pyszz >this repo</a> using the `data.json` provided by the `pyszz_json_generator.py` script. <br> 

4. finally use the following command to extract information from the pyszz output <br> 
`python3 pyszz_data_analyzer.py pyszz/out/outuput.json path/to/project ` 
