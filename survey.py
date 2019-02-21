#!/usr/bin/env python

import requests, sys, time, os, argparse
from lxml.html import fromstring


def main():
    os.system('clear')

    parser = argparse.ArgumentParser()

    parser.add_argument('-d', help='Domain Listed Files', nargs=1, dest='domain', required=True)
    parser.add_argument('-p', help='Payloads (Word lines)', nargs=1, dest='payload', required=True)

    args = parser.parse_args()

    file_domain = args.domain[0]
    payloads = args.payload[0]

    with open(file_domain) as f:
        for domain in f.readlines():
            print "\n\nLoading :: %s ...." % domain
            with open(payloads) as p:
                to_print = "\n%3s| %10s | %10s | %30s | %30s\n" % ('Code', 'Redirect', 'Reason', 'URL', 'Title')
                print to_print
                for payload in p.readlines():
                    try:
                        path = '%s%s' % (domain.strip(), payload.strip())
                        resp = requests.get(path, verify=True)
                        tree = fromstring(resp.content)
                        title = tree.findtext('.//title')
                        history = ', '.join(map(lambda r: str(r.status_code), resp.history))
                        to_print = "%3s | %10s | %10s | %30s | %30s" % (resp.status_code, history, resp.reason, resp.url, title or '')
                        print to_print
                    except Exception, e:
                        print "\n\n __ Exception __ \n", e

if __name__ == '__main__':
    main()
