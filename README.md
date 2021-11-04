<p align="center">
<a href="https://github.com/Cvaniak/RichWatch"><img alt="" src="./documentation/RichWatchLogo.png" width="70%"></a>
</p>  

RichWatch is **TUI** (Textual User Interface) for **AWS Cloud Watch**.  
It formats and pretty prints **Cloud Watch**'s logs so they are much more readable.  
Because it works in terminal, you can have updates from your **Lambdas** and other **AWS** services next to your hand, automatically refreshed and represented in beautiful way by excelent **Python** library [**Rich**]("www.costam.com") and [**Textual**]("www.costam.com"),

## **Content**
- [What is the difference?](#what-is-the-difference)
- [Setup and Usage](#setup-and-usage)
- [TODO](#todo)

# What is the difference?
So this is example Log output from **AWS Cloud Watch**:  
![Test](./documentation/AWSLogs.png)    
And here is same output but using **RichWatch**: 
![Test](./documentation/RichWatchTui.png)  
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
# Setup and Usage
* boto3 
* * AWS ~/.aws/config
[default]
region=<change here>
aws_access_key_id=<change here>
aws_secret_access_key=<change here>
* pip install 
* 

# TODO
* Set custom and default style
* Support AWS CLI profilles
* Save logs to file
* Check for updates and only download the latest
* Linters configuration
* As a PyPi package
* Custom TAGs
* Custom refresh time
* Collapse all ENDs, STARTs and REPORTs
* Better TreeView
* Better StatusView

> ⚠️ The TUI version of RichWatch is base on **Textual** witch is in progress. If you see any bugs please let me know. Currently TUI is only working for *Linux* and *Macs* but on *Windows* you can run this in script version.