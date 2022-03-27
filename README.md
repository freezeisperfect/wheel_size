# Wheel Size parser
This tool parses pages from wheel-size.com. Project forked from pythonfullstack/wheel_size and base for tool was made in original project.

Parsing tool saves data of wheel sizes in csv as `Auto`,`Model`,`Generation`,`Tire`,`Rim`,`Stock/not stock size`.

How to run tool:

1. Open proxy.py and enter the URL of your proxy address. You can also use several proxies to parse data faster.
2. Install this list of packages: `bs4`, `requests`, `selenium`, `proxy`
```
pip install bs4
pip install requests
pip install selenium
pip install proxy
```
3. Run main.py
```
python3 main.py
```
4. Wait until data will be parsed and enjoy!
