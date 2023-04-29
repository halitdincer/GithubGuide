from flask import Flask

app = Flask(__name__)

@app.route('/pandas-dev/pandas')
def asv_bench():
    return {"asv_bench":"asv_bench is a benchmarking tool for Python packages.",
            "ci":"ci is a continuous integration tool for Python packages.",
            "doc":"doc is a documentation tool for Python packages.",
            "gitpod":"gitpod is a development environment tool for Python packages.",
            "pandas":"pandas is a data analysis tool for Python packages.",
            "scripts":"scripts is a collection of scripts for Python packages.",
            "typings":"typings is a type hinting tool for Python packages.",
            "web":"web is a web development tool for Python packages."}
