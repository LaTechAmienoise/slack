# About

Script to help manage a slack team. Since it's not possible at the moment (September 2015) to invite or revoke a user
using the Web API, the script display a list of email to users to add and to remove.
 

# Requirements

  * python3
  * python3-virtualenv

# Installation

    git clone https://github.com/LaTechAmienoise/slack
    cd slack
    virtualenv -p /usr/bin/python3 .
    ./bin/pip install -r requirements.txt

# Configuration

First, you need [to create a Slack Token](https://api.slack.com/web) (see at the bottom of the page).

Create ``config.ini`` from ``config.ini.sample`` with the following contents:
  
    [slack]
    token = xoxp-xxxxxxxx
    
    [csv]
    delimiter = ,
    quotechar = "

# Usage

    % ./bin/python csv2slack.py users.csv
    INFO:root:Found 19 users in CSV
    INFO:requests.packages.urllib3.connectionpool:Starting new HTTPS connection (1): slack.com
    INFO:root:Found 5 users in Slack
    Users to add: aa@bb.com, cc@dd.com 
    Users to delete: ee@bb.com, ff@gg.com
