# wsdl-downloader

Python script to download WSDL files, its child WSDLs and referenced schemas, and rename references locally

Usage:

    python wsdldownloader.py url [path]

where url is the WSDL url, and path is the output location for the WSDL and XSD files. Path is optional, if not specified the current directory will be used.

Examples:

    python wsdldownloader.py http://hostname.domain.com/service?wsdl C:\temp
    python wsdldownloader.py http://hostname.domain.com/service?wsdl /home/username/downloads
    python wsdldownloader.py http://hostname.domain.com/service?wsdl .
    python wsdldownloader.py http://hostname.domain.com/service?wsdl

