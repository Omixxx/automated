Our Python script is designed to extract security bug fixes commits and convert them into a JSON format, to be used with the pyszz implementation provided by grosa1 on GitHub.

## Usage 
First do the pull <br>
Second, run the following command `python3 pyszz_json_generator.py [param]` <br>
Where `param` should be replaced with the project path on which you want to extract commits related to security bug fixes.


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
Where `"repo_name"` will be the name of the folder passed as input to the script. 
