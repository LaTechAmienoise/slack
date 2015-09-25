#!/usr/bin/env python

import slacker
import configparser
import os
import argparse
import logging
import sys
import csv


def loadconfig(filename=None):
    """
    Load configuration from INI file, see config.ini.sample
    :param filename: Filename to read, if set to None, look at config.ini in the same directory than the script.
    :return: a configparser.ConfigParser object
    """
    if filename is None:
        filename = '%s/config.ini' % os.path.dirname(os.path.realpath(__file__))
    logging.debug("Reading configuration from %s" % filename)
    config = configparser.ConfigParser()
    config.read(filename)
    try:
        config['slack']['token']
        config['csv']['delimiter']
        config['csv']['quotechar']
    except KeyError as e:
        logging.critical('Require key is missing: %s' % e)
        sys.exit(1)
    return config


def main(args):
    config = loadconfig()
    # Create lists with expected and real members
    expected = dict()
    real = dict()
    # Read CSV file to get expected members
    with open(args.csv, newline='') as csvinput:
        input = csv.reader(csvinput, delimiter=config['csv']['delimiter'], quotechar=config['csv']['quotechar'])
        for (email, firstname, lastname) in input:
            if '@' in email:
                expected[email] = dict()
                expected[email]['firstname'] = firstname
                expected[email]['lastname'] = lastname
    logging.info("Found %s users in CSV" % len(expected))

    # Get real members from Slack
    slack = slacker.Slacker(config['slack']['token'])
    response = slack.users.list()
    for user in response.body['members']:
        email = user['profile']['email']
        real[email] = dict()
        real[email]['firstname'] = user['profile']['first_name']
        real[email]['lastname'] = user['profile']['last_name']

    logging.info("Found %s users in Slack" % len(real))

    # Create members that doesn't exists
    buffer = []
    for user in expected.keys() - real.keys():
        buffer.append('%s %s <%s>' % (expected[user]['firstname'],
                                      expected[user]['lastname'],
                                      user))
    print("Users to add: %s" % ', '.join(buffer))
    print("Users to delete: %s" % ', '.join(real.keys() - expected.keys()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Synchronize slack users with the given CSV file')
    parser.add_argument('-s', '--dry-run', dest='dry', const=True,
                        action='store_const', help='Simulate a run (dry run)')
    parser.add_argument('-d', '--debug', dest='debug', const=True,
                        action='store_const', help='Enable debug messages')
    parser.add_argument('csv', help='CSV file')
    args = parser.parse_args()
    if args.dry or args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    main(args)
