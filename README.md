<p align="center">
<a href="https://github.com/Cvaniak/RichWatch"><img alt="" src="./documentation/RichWatchLogo.png" width="70%"></a>
</p>  

<a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/-python-black?logo=python&logoColor=brightgreen"></a>
<a href="https://github.com/pfs/black"><img alt="Black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://github.com/Cvaniak/RichWatch/blob/main/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/Cvaniak/RichWatch?color=black"></a>

**RichWatch** is **TUI** (Textual User Interface) for **AWS Cloud Watch**.  
It formats and pretty prints **Cloud Watch**'s logs so they are much more readable.  
Because it works in terminal, you can have updates from your **Lambdas** and other **AWS** services next to your hand, automatically refreshed and represented in beautiful way by excelent **Python** library [**Rich**](https://github.com/willmcgugan/rich) and [**Textual**](https://github.com/willmcgugan/textual),

## **Content**
- [Dry run 🔍](#dry-run-)
- [What is the difference❓](#what-is-the-difference)
- [Setup and Usage ⚙️](#setup-and-usage-️)
    - [**AWS credentials for Boto3**](#aws-credentials-for-boto3)
    - [**Install requirements**](#install-requirements)
    - [**Setup Log Group file**](#setup-log-group-file)
    - [**Run App**](#run-app)
- [TODO 📝](#todo-)

# Dry run 🔍
Now you can try it without **AWS** account! If you wonder how UI looks like or how you can use it or you just looking for example of app created with **Textual**, now you can [**Install requirements**](#install-requirements) and run app with:
```bash
python3 rich_watch.py dry-run
```
and it will show you flow with example offline data.

# What is the difference❓
So this is example Log output from **AWS Cloud Watch**:  
![Test](./documentation/AWSLogs.png)    
And here is same output but using **RichWatch**: 
![Test](./documentation/RichWatchTui.png)
  > ⚠️ There is no theme setup yet so **Rich** format is based of your terminal Theme. Setup for this screenshot is `zsh` with `agnoster` in `Tilda` console.  

And both are for same **Lambda** code:
```python
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    logger.info("Output from logging.info()")
    logger.debug("Output from logging.debug()")
    logger.error("Output from logging.error()")
    print("Output from print()")
    return {
        'statusCode': 200,
        'body': json.dumps('This is from response!')
    }
```
# Setup and Usage ⚙️
### **AWS credentials for Boto3**
To start you need to setup credentials for **AWS**. You can do this using **AWS Command Line**, in `~/.aws/credentials` file or via `export` command of environment variables. You can read more about this [here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html).
### **Install requirements**
You need `Python` and `pip` in version `3.6` or higher.  
Then you need to install requirements:
```bash
pip3 install -r requirements.txt
```
### **Setup Log Group file**
Then you need to create `log_group.yaml` file like this:
```yaml
region: eu-west-0
project-a:
  - path: /aws/lambda/test-lambda-0
    custom-name: my-lambda-0
    region: eu-west-0
  - path: /aws/lambda/test-lambda-1
    custom-name: my-lambda-1
    region: eu-west-1
  - path: /aws/lambda/test-lambda-2
    region: eu-west-2
  - path: /aws/lambda/test-lambda-3
    custom-name: my-lambda3
```
First region is optional default region. Then you can provide any name ex. `project-a`. It does not change anything for now later it will be used to group lambdas in tree view. Then you can provide list of lambdas where:
 * `path` is obligatory and it is path to log group,
 *  `custom-name` is optional and this is place where you can name your lambda (otherwise it will display last part after `/`),
 *  `region` witch will overwrite default `region`. If both `region` values are not set, then value from your `AWS` client setup will be used.
### **Run App**
Then you can run app:
```bash
python3 rich_watch.py
```
or get logs once and printout to stdout with:
```bash
python3 main.py <log_group>
```


# TODO 📝
☑️ Check for updates and only download the latest  
☑️ Save logs to file  
☑️ Dry run (demo without AWS account)  
☑️ Add more examples for dry-run  
☑️ Better TreeView (with custom names)  
⭕ Configure how many logs should be downloaded  
⭕ Set default style  
⭕ Allow for custom style  
⭕ Support AWS CLI profiles  
⭕ Create RichCloud a PyPi package  
⭕ Custom log TAGs highlight  
⭕ Custom refresh time  
⭕ Collapse all ENDs, STARTs and REPORTs, ect.  
⭕ Better StatusView  

> ⚠️ The TUI version of RichWatch is base on **Textual** witch is in progress. If you see any bugs please let me know. Currently TUI is only working for *Linux* and *Macs* but on *Windows* you can run this in script version.
