# Python script to download WSDL files, referenced schemas, and rename references locally

Does not work with Python 3.x. Python 2.7 available [here](https://www.python.org/downloads/)

Usage:

    python wsdldownloader.py url wsdl-schema-mapping xml-schema-mapping [path]

* url: The url of the WSDL to download.
* wsdl-schema-mapping: Name of the WSDL schema namespace mapping in your WSDL. Usually "wsdl", e.g. xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
* xml-schema-mapping: Name of the XML schema namespace mapping in your WSDL. Usually "xsd", e.g. xmlns:xsd="http://www.w3.org/2001/XMLSchema"
* path: the output location for the WSDL and XSD files. If not specified the current directory will be used.

Examples:

    python wsdldownloader.py http://hostname.domain.com/service?wsdl wsdl xsd C:\temp
    python wsdldownloader.py http://hostname.domain.com/service?wsdl wsdl xsd /home/username/downloads
    python wsdldownloader.py http://hostname.domain.com/service?wsdl w s

