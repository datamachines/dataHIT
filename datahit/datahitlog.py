from datetime import datetime

def log(text, ltype="INFO"):
    rundate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("DMC RuleUI", ltype, rundate, text)
