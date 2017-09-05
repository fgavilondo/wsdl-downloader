#! /usr/bin/env python
from __future__ import print_function

import os
import sys
import urllib2  # Python 2 only
import urlparse  # Python 2 only
from xml.dom import minidom

INDENT_LEVEL = 2

DOWNLOADED_URLS = []


def write_file(filename, content):
    print('Writing', filename)
    with open(filename, 'w') as f:
        f.write(content)


def xml_to_pretty_string(xml):
    return xml.toprettyxml(indent=' ' * INDENT_LEVEL)


def is_already_downloaded(url):
    return url in DOWNLOADED_URLS


def mark_as_downloaded(url):
    DOWNLOADED_URLS.append(url)


def get_url_query_params_as_dict(url):
    return dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))


def download_wsdl_imports(wsdl_doc, output_dir):
    wsdl_import_elems = wsdl_doc.getElementsByTagName('wsdl:import')
    if wsdl_import_elems:
        print('Fetching child WSDLs')
    for elem in wsdl_import_elems:
        child_wsdl_url = elem.attributes['location'].value
        if is_already_downloaded(child_wsdl_url):
            print(child_wsdl_url, 'already downloaded - ignoring.')
            continue
        child_wsdl_doc = read_xml_from_url(child_wsdl_url)
        download_wsdl_imports(child_wsdl_doc, output_dir)
        download_xsd_imports(child_wsdl_doc, output_dir)
        url_query_params = get_url_query_params_as_dict(child_wsdl_url)
        child_wsdl_filename = url_query_params['wsdl'] + '.wsdl'
        path = os.path.join(output_dir, child_wsdl_filename)
        write_file(path, xml_to_pretty_string(child_wsdl_doc))
        elem.attributes['location'].value = child_wsdl_filename
        mark_as_downloaded(child_wsdl_url)


def download_xsd_imports(wsdl_doc, output_dir):
    xsd_import_elems = wsdl_doc.getElementsByTagName('xsd:import')
    if xsd_import_elems:
        print('Fetching XSD schemas')
    for elem in xsd_import_elems:
        xsd_url = elem.attributes['schemaLocation'].value
        if is_already_downloaded(xsd_url):
            print('Ignoring', xsd_url, ': already downloaded')
            continue
        xsd_doc = read_xml_from_url(xsd_url)
        url_query_params = get_url_query_params_as_dict(xsd_url)
        xsd_filename = url_query_params['xsd'] + '.xsd'
        path = os.path.join(output_dir, xsd_filename)
        write_file(path, xml_to_pretty_string(xsd_doc))
        elem.attributes['schemaLocation'].value = xsd_filename
        mark_as_downloaded(xsd_url)


def read_xml_from_url(url):
    print('Reading', url)
    text = urllib2.urlopen(url).read()
    return minidom.parseString(text)


def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_main_wsdl_name(wsdl_url, wsdl_doc):
    wsdl_definitions_elem = wsdl_doc.getElementsByTagName('wsdl:definitions')[0]
    attrib = wsdl_definitions_elem.attributes.get('name')
    if attrib and attrib.value:
        return attrib.value
    else:
        path = urlparse.urlsplit(wsdl_url).path
        path = path[1:]  # remove the leading '/'
        return path.replace('/', '-')  # replace all other '/' with dashes


def get_main_wsdl_file_name(wsdl_url, wsdl_doc):
    return get_main_wsdl_name(wsdl_url, wsdl_doc) + '.wsdl'


def process(wsdl_url, output_dir):
    ensure_dir_exists(output_dir)
    wsdl_doc = read_xml_from_url(wsdl_url)
    download_wsdl_imports(wsdl_doc, output_dir)
    download_xsd_imports(wsdl_doc, output_dir)
    wsdl_filename = get_main_wsdl_file_name(wsdl_url, wsdl_doc)
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
    wsdl_url = ''
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
