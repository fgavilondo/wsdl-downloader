#! /usr/bin/env python
from __future__ import print_function

import os
import sys
import urllib2
import urlparse
from xml.dom import minidom


def write_file(filename, content):
    print('Writing', filename)
    with open(filename, 'w') as f:
        f.write(content)


def xml_to_pretty_string(xml):
    return xml.toprettyxml(indent='    ')


def download_wsdl_imports(wsdl_doc, output_dir):
    wsdl_import_elems = wsdl_doc.getElementsByTagName('wsdl:import')
    if wsdl_import_elems:
        print('Fetching child WSDLs for WSDL', get_wsdl_name(wsdl_doc))
    for elem in wsdl_import_elems:
        wsdl_url = elem.attributes['location'].value
        url_query_params = dict(urlparse.parse_qsl(urlparse.urlsplit(wsdl_url).query))
        child_wsdl_filename = url_query_params['wsdl'] + '.wsdl'
        path = os.path.join(output_dir, child_wsdl_filename)
        if not os.path.isfile(path):
            # only download it if not already there
            child_wsdl_doc = read_xml_from_url(wsdl_url)
            download_xsd_imports(child_wsdl_doc, output_dir)
            download_wsdl_imports(child_wsdl_doc, output_dir)
            write_file(path, xml_to_pretty_string(child_wsdl_doc))
        elem.attributes['location'].value = child_wsdl_filename


def download_xsd_imports(wsdl_doc, output_dir):
    xsd_import_elems = wsdl_doc.getElementsByTagName('xsd:import')
    if xsd_import_elems:
        print('Fetching XSD schemas for WSDL', get_wsdl_name(wsdl_doc))
    for elem in xsd_import_elems:
        xsd_url = elem.attributes['schemaLocation'].value
        url_query_params = dict(urlparse.parse_qsl(urlparse.urlsplit(xsd_url).query))
        xsd_filename = url_query_params['xsd'] + '.xsd'
        path = os.path.join(output_dir, xsd_filename)
        if not os.path.isfile(path):
            # only download it if not already there
            xsd_doc = read_xml_from_url(xsd_url)
            write_file(path, xml_to_pretty_string(xsd_doc))
        elem.attributes['schemaLocation'].value = xsd_filename


def read_xml_from_url(url):
    print('Reading', url)
    return minidom.parseString(urllib2.urlopen(url).read())


def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_wsdl_name(wsdl_doc):
    wsdl_definitions_elem = wsdl_doc.getElementsByTagName('wsdl:definitions')[0]
    attrib = wsdl_definitions_elem.attributes.get('name')
    if attrib:
        return attrib.value
    else:
        attrib = wsdl_definitions_elem.attributes.get('targetNamespace')
        return 'child wsdl for target namespace ' + attrib.value


def get_wsdl_file_name(wsdl_doc):
    return get_wsdl_name(wsdl_doc) + '.wsdl'


def process(wsdl_url, output_dir):
    ensure_dir_exists(output_dir)
    wsdl_doc = read_xml_from_url(wsdl_url)
    download_wsdl_imports(wsdl_doc, output_dir)
    download_xsd_imports(wsdl_doc, output_dir)
    wsdl_filename = get_wsdl_file_name(wsdl_doc)
    write_file(os.path.join(output_dir, wsdl_filename), xml_to_pretty_string(wsdl_doc))


def usage():
    print()
    print('Usage:')
    print()
    print('    python wsdldownloader.py url [path]')
    print()
    print('Where url is the WSDL url, and path is the output location for the WSDL and XSD files.')
    print('Path is optional, if not specified the current directory will be used.')
    print('Examples:')
    print()
    print('   python wsdldownloader.py http://hostname.domain.com/service?wsdl C:\\temp')
    print('   python wsdldownloader.py http://hostname.domain.com/service?wsdl /home/username/downloads')
    print('   python wsdldownloader.py http://hostname.domain.com/service?wsdl')
    print()


def main():
    try:
        wsdl_url = sys.argv[1]
    except IndexError:
        usage()
        exit()

    try:
        output_dir = sys.argv[2]
    except IndexError:
        output_dir = '.'

    process(wsdl_url, output_dir)


if __name__ == "__main__":
    main()
