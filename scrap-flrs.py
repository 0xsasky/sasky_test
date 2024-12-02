#!/usr/bin/python3

#Try to use many IG user with the max_id string to see whether the max_id is related to specific user or not
#site:github.com instagram scrapper
#https://github.com/topics/instagram-scraper
#https://github.com/vasilisa-che/instagram-followers-and-bio-scraper/blob/main/followers-scraper.py
#https://github.com/chenchih/Python-Project/blob/main/Selenium/Instagram-crawl/1.GetFollowing_FollowerList/follower_medium_2022.py

import datetime
import requests
import argparse
import sqlite3
import random
import json
import time
import csv
import sys
import re
import os


MAIN_SESSION=None





#If not used, then any random name.
#If used, then a username we own to be a sign of the "END" of the scraping process.
#If used, then the username should be added at the end of usernames file(-d users.txt).



db_name=""

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "db_file.txt"), 'r') as db_file:
    line=db_file.readline().strip()

    if line:
        db_name = line
    else:
        print(f"File db_file is empty!")
        sys.exit(1)

db_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), db_name)


#THIS IS STATIC, DON'T CHANGE it, PUT "sekomekobeko1721921" at the end of the users.txt file,
#whether you are running scrap-flrs.py --folowings, or --followrs, or just you want ot scrape the users
#This "sekomekobeko1721921" is a sign that we have finished all of the users.

counter=0
counter2=0
CRONJOB_USERNAME="sekomekobeko1721921"

requests_delay=1
requests_limit=500
not_found_limit=10
followers_requests_delay=1
followings_requests_delay=1

country_code_regex=re.compile(r'\+\s*(?:1[\s()-]*(?:242|246|264|268|284|340|345|441|473|649|664|670|671|684|721|758|767|784|809|868|869|876)|1|2(?:0|7|1[12368]|2[0-9]|3[0-9]|4[0-689]|5[0-8]|6[0-9]|9[01789])|3(?:[0-469]|5[0-9]|7[0-9]|8[0-35679])|4(?:[013-9]|2[013])|5(?:[1-8]|0[0-9]|9[0-9])|6(?:[0-6]|7[02-9]|8[0-35-9]|9[0-2])|7|8(?:[1246]|5[02356]|70|8[06])|9(?:[0-58]|6[0-8]|7[013-7]|9[2-68]))')

is_number_regex=re.compile(r'(?:\+\s*)?\d(?:[\s()-]*\d){4,}')

email_regex=re.compile(r'''\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b''', re.I)


is_flag_regex=re.compile(r'[\U0001F1E6-\U0001F1FF]{2}')

# from argparse import HelpFormatter



_USER_PROPS=['id', 'username', 'full_name', 'biography', 'has_clips', 'highlight_reel_count', 'is_private', 'is_verified', 'is_business_account', 'business_category_name', 'external_url', 'profile_pic_url', 'profile_pic_url_hd']


_USER_PROPS2=['link','id', 'username', 'full_name', 'biography', 'has_clips', 'highlight_reel_count', 'is_private', 'is_verified', 'is_business_account', 'business_category_name', 'external_url', 'profile_pic_url', 'profile_pic_url_hd', 'joined_date']

#big_list, next_max_id
_FOLLOWERS_PROPS=['pk_id', 'username','full_name', 'is_private', 'is_verified', 'has_anonymous_profile_picture']


_FOLLOWERS_PROPS2=['pk_id', 'username', 'link', 'full_name', 'is_private', 'is_verified', 'has_anonymous_profile_picture']


countries={'376': {'country': 'Andorra', 'abbrv': 'AD'}, '971': {'country': 'United Arab Emirates', 'abbrv': 'AE'}, '93': {'country': 'Afghanistan', 'abbrv': 'AF'}, '1-268': {'country': 'Antigua and Barbuda', 'abbrv': 'AG'}, '1-264': {'country': 'Anguilla', 'abbrv': 'AI'}, '355': {'country': 'Albania', 'abbrv': 'AL'}, '374': {'country': 'Armenia', 'abbrv': 'AM'}, '244': {'country': 'Angola', 'abbrv': 'AO'}, '672': {'country': ['Antarctica', 'Heard Island and McDonald Islands', 'Norfolk Island'], 'abbrv': ['AQ', 'HM', 'NF']}, '54': {'country': 'Argentina', 'abbrv': 'AR'}, '1-684': {'country': 'American Samoa', 'abbrv': 'AS'}, '43': {'country': 'Austria', 'abbrv': 'AT'}, '61': {'country': ['Australia', 'Cocos (Keeling) Islands', 'Christmas Island'], 'abbrv': ['AU', 'CC', 'CX']}, '297': {'country': 'Aruba', 'abbrv': 'AW'}, '358': {'country': ['Alland Islands', 'Finland'], 'abbrv': ['AX', 'FI']}, '994': {'country': 'Azerbaijan', 'abbrv': 'AZ'}, '387': {'country': 'Bosnia and Herzegovina', 'abbrv': 'BA'}, '1-246': {'country': 'Barbados', 'abbrv': 'BB'}, '880': {'country': 'Bangladesh', 'abbrv': 'BD'}, '32': {'country': 'Belgium', 'abbrv': 'BE'}, '226': {'country': 'Burkina Faso', 'abbrv': 'BF'}, '359': {'country': 'Bulgaria', 'abbrv': 'BG'}, '973': {'country': 'Bahrain', 'abbrv': 'BH'}, '257': {'country': 'Burundi', 'abbrv': 'BI'}, '229': {'country': 'Benin', 'abbrv': 'BJ'}, '590': {'country': ['Saint Barthelemy', 'Guadeloupe', 'Saint Martin (French part)'], 'abbrv': ['BL', 'GP', 'MF']}, '1-441': {'country': 'Bermuda', 'abbrv': 'BM'}, '673': {'country': 'Brunei Darussalam', 'abbrv': 'BN'}, '591': {'country': 'Bolivia', 'abbrv': 'BO'}, '55': {'country': 'Brazil', 'abbrv': 'BR'}, '1-242': {'country': 'Bahamas', 'abbrv': 'BS'}, '975': {'country': 'Bhutan', 'abbrv': 'BT'}, '47': {'country': ['Bouvet Island', 'Norway', 'Svalbard and Jan Mayen'], 'abbrv': ['BV', 'NO', 'SJ']}, '267': {'country': 'Botswana', 'abbrv': 'BW'}, '375': {'country': 'Belarus', 'abbrv': 'BY'}, '501': {'country': 'Belize', 'abbrv': 'BZ'}, '1': {'country': ['Canada', 'Puerto Rico', 'United States'], 'abbrv': ['CA', 'PR', 'US']}, '243': {'country': 'Congo - Kinshasa', 'abbrv': 'CD'}, '236': {'country': 'Central African Republic', 'abbrv': 'CF'}, '242': {'country': 'Congo - Brazzaville', 'abbrv': 'CG'}, '41': {'country': 'Switzerland', 'abbrv': 'CH'}, '225': {'country': "Cote d'Ivoire", 'abbrv': 'CI'}, '682': {'country': 'Cook Islands', 'abbrv': 'CK'}, '56': {'country': 'Chile', 'abbrv': 'CL'}, '237': {'country': 'Cameroon', 'abbrv': 'CM'}, '86': {'country': 'China', 'abbrv': 'CN'}, '57': {'country': 'Colombia', 'abbrv': 'CO'}, '506': {'country': 'Costa Rica', 'abbrv': 'CR'}, '53': {'country': 'Cuba', 'abbrv': 'CU'}, '238': {'country': 'Cape Verde', 'abbrv': 'CV'}, '599': {'country': 'Curacao', 'abbrv': 'CW'}, '357': {'country': 'Cyprus', 'abbrv': 'CY'}, '420': {'country': 'Czech Republic', 'abbrv': 'CZ'}, '49': {'country': 'Germany', 'abbrv': 'DE'}, '253': {'country': 'Djibouti', 'abbrv': 'DJ'}, '45': {'country': 'Denmark', 'abbrv': 'DK'}, '1-767': {'country': 'Dominica', 'abbrv': 'DM'}, '1-809': {'country': 'Dominican Republic', 'abbrv': 'DO'}, '213': {'country': 'Algeria', 'abbrv': 'DZ'}, '593': {'country': 'Ecuador', 'abbrv': 'EC'}, '372': {'country': 'Estonia', 'abbrv': 'EE'}, '20': {'country': 'Egypt', 'abbrv': 'EG'}, '212': {'country': ['Western Sahara', 'Morocco'], 'abbrv': ['EH', 'MA']}, '291': {'country': 'Eritrea', 'abbrv': 'ER'}, '34': {'country': 'Spain', 'abbrv': 'ES'}, '251': {'country': 'Ethiopia', 'abbrv': 'ET'}, '679': {'country': 'Fiji', 'abbrv': 'FJ'}, '500': {'country': ['Falkland Islands (Malvinas)', 'South Georgia and the South Sandwich Islands'], 'abbrv': ['FK', 'GS']}, '691': {'country': 'Micronesia', 'abbrv': 'FM'}, '298': {'country': 'Faroe Islands', 'abbrv': 'FO'}, '33': {'country': 'France', 'abbrv': 'FR'}, '241': {'country': 'Gabon', 'abbrv': 'GA'}, '44': {'country': ['United Kingdom', 'Guernsey', 'Isle of Man', 'Jersey'], 'abbrv': ['GB', 'GG', 'IM', 'JE']}, '1-473': {'country': 'Grenada', 'abbrv': 'GD'}, '995': {'country': 'Georgia', 'abbrv': 'GE'}, '594': {'country': 'French Guiana', 'abbrv': 'GF'}, '233': {'country': 'Ghana', 'abbrv': 'GH'}, '350': {'country': 'Gibraltar', 'abbrv': 'GI'}, '299': {'country': 'Greenland', 'abbrv': 'GL'}, '220': {'country': 'Gambia', 'abbrv': 'GM'}, '224': {'country': 'Guinea', 'abbrv': 'GN'}, '240': {'country': 'Equatorial Guinea', 'abbrv': 'GQ'}, '30': {'country': 'Greece', 'abbrv': 'GR'}, '502': {'country': 'Guatemala', 'abbrv': 'GT'}, '1-671': {'country': 'Guam', 'abbrv': 'GU'}, '245': {'country': 'Guinea-Bissau', 'abbrv': 'GW'}, '592': {'country': 'Guyana', 'abbrv': 'GY'}, '852': {'country': 'Hong Kong', 'abbrv': 'HK'}, '504': {'country': 'Honduras', 'abbrv': 'HN'}, '385': {'country': 'Croatia', 'abbrv': 'HR'}, '509': {'country': 'Haiti', 'abbrv': 'HT'}, '36': {'country': 'Hungary', 'abbrv': 'HU'}, '62': {'country': 'Indonesia', 'abbrv': 'ID'}, '353': {'country': 'Ireland', 'abbrv': 'IE'}, '91': {'country': 'India', 'abbrv': 'IN'}, '246': {'country': 'British Indian Ocean Territory', 'abbrv': 'IO'}, '964': {'country': 'Iraq', 'abbrv': 'IQ'}, '98': {'country': 'Iran', 'abbrv': 'IR'}, '354': {'country': 'Iceland', 'abbrv': 'IS'}, '39': {'country': 'Italy', 'abbrv': 'IT'}, '1-876': {'country': 'Jamaica', 'abbrv': 'JM'}, '962': {'country': 'Jordan', 'abbrv': 'JO'}, '81': {'country': 'Japan', 'abbrv': 'JP'}, '254': {'country': 'Kenya', 'abbrv': 'KE'}, '996': {'country': 'Kyrgyzstan', 'abbrv': 'KG'}, '855': {'country': 'Cambodia', 'abbrv': 'KH'}, '686': {'country': 'Kiribati', 'abbrv': 'KI'}, '269': {'country': 'Comoros', 'abbrv': 'KM'}, '1-869': {'country': 'Saint Kitts and Nevis', 'abbrv': 'KN'}, '850': {'country': "North Korea", 'abbrv': 'KP'}, '82': {'country': 'South Korea', 'abbrv': 'KR'}, '965': {'country': 'Kuwait', 'abbrv': 'KW'}, '1-345': {'country': 'Cayman Islands', 'abbrv': 'KY'}, '7': {'country': ['Kazakhstan', 'Russian Federation'], 'abbrv': ['KZ', 'RU']}, '856': {'country': "Lao People's Democratic Republic", 'abbrv': 'LA'}, '961': {'country': 'Lebanon', 'abbrv': 'LB'}, '1-758': {'country': 'Saint Lucia', 'abbrv': 'LC'}, '423': {'country': 'Liechtenstein', 'abbrv': 'LI'}, '94': {'country': 'Sri Lanka', 'abbrv': 'LK'}, '231': {'country': 'Liberia', 'abbrv': 'LR'}, '266': {'country': 'Lesotho', 'abbrv': 'LS'}, '370': {'country': 'Lithuania', 'abbrv': 'LT'}, '352': {'country': 'Luxembourg', 'abbrv': 'LU'}, '371': {'country': 'Latvia', 'abbrv': 'LV'}, '218': {'country': 'Libya', 'abbrv': 'LY'}, '377': {'country': 'Monaco', 'abbrv': 'MC'}, '373': {'country': 'Moldova', 'abbrv': 'MD'}, '382': {'country': 'Montenegro', 'abbrv': 'ME'}, '261': {'country': 'Madagascar', 'abbrv': 'MG'}, '692': {'country': 'Marshall Islands', 'abbrv': 'MH'}, '389': {'country': 'North Macedonia', 'abbrv': 'MK'}, '223': {'country': 'Mali', 'abbrv': 'ML'}, '95': {'country': 'Myanmar', 'abbrv': 'MM'}, '976': {'country': 'Mongolia', 'abbrv': 'MN'}, '853': {'country': 'Macao', 'abbrv': 'MO'}, '1-670': {'country': 'Northern Mariana Islands', 'abbrv': 'MP'}, '596': {'country': 'Martinique', 'abbrv': 'MQ'}, '222': {'country': 'Mauritania', 'abbrv': 'MR'}, '1-664': {'country': 'Montserrat', 'abbrv': 'MS'}, '356': {'country': 'Malta', 'abbrv': 'MT'}, '230': {'country': 'Mauritius', 'abbrv': 'MU'}, '960': {'country': 'Maldives', 'abbrv': 'MV'}, '265': {'country': 'Malawi', 'abbrv': 'MW'}, '52': {'country': 'Mexico', 'abbrv': 'MX'}, '60': {'country': 'Malaysia', 'abbrv': 'MY'}, '258': {'country': 'Mozambique', 'abbrv': 'MZ'}, '264': {'country': 'Namibia', 'abbrv': 'NA'}, '687': {'country': 'New Caledonia', 'abbrv': 'NC'}, '227': {'country': 'Niger', 'abbrv': 'NE'}, '234': {'country': 'Nigeria', 'abbrv': 'NG'}, '505': {'country': 'Nicaragua', 'abbrv': 'NI'}, '31': {'country': 'Netherlands', 'abbrv': 'NL'}, '977': {'country': 'Nepal', 'abbrv': 'NP'}, '674': {'country': 'Nauru', 'abbrv': 'NR'}, '683': {'country': 'Niue', 'abbrv': 'NU'}, '64': {'country': 'New Zealand', 'abbrv': 'NZ'}, '968': {'country': 'Oman', 'abbrv': 'OM'}, '507': {'country': 'Panama', 'abbrv': 'PA'}, '51': {'country': 'Peru', 'abbrv': 'PE'}, '689': {'country': 'French Polynesia', 'abbrv': 'PF'}, '675': {'country': 'Papua New Guinea', 'abbrv': 'PG'}, '63': {'country': 'Philippines', 'abbrv': 'PH'}, '92': {'country': 'Pakistan', 'abbrv': 'PK'}, '48': {'country': 'Poland', 'abbrv': 'PL'}, '508': {'country': 'Saint Pierre and Miquelon', 'abbrv': 'PM'}, '870': {'country': 'Pitcairn', 'abbrv': 'PN'}, '970': {'country': 'Palestine', 'abbrv': 'PS'}, '351': {'country': 'Portugal', 'abbrv': 'PT'}, '680': {'country': 'Palau', 'abbrv': 'PW'}, '595': {'country': 'Paraguay', 'abbrv': 'PY'}, '974': {'country': 'Qatar', 'abbrv': 'QA'}, '262': {'country': ['Reunion', 'French Southern Territories', 'Mayotte'], 'abbrv': ['RE', 'TF', 'YT']}, '40': {'country': 'Romania', 'abbrv': 'RO'}, '381': {'country': 'Serbia', 'abbrv': 'RS'}, '250': {'country': 'Rwanda', 'abbrv': 'RW'}, '966': {'country': 'Saudi Arabia', 'abbrv': 'SA'}, '677': {'country': 'Solomon Islands', 'abbrv': 'SB'}, '248': {'country': 'Seychelles', 'abbrv': 'SC'}, '249': {'country': 'Sudan', 'abbrv': 'SD'}, '46': {'country': 'Sweden', 'abbrv': 'SE'}, '65': {'country': 'Singapore', 'abbrv': 'SG'}, '290': {'country': 'Saint Helena', 'abbrv': 'SH'}, '386': {'country': 'Slovenia', 'abbrv': 'SI'}, '421': {'country': 'Slovakia', 'abbrv': 'SK'}, '232': {'country': 'Sierra Leone', 'abbrv': 'SL'}, '378': {'country': 'San Marino', 'abbrv': 'SM'}, '221': {'country': 'Senegal', 'abbrv': 'SN'}, '252': {'country': 'Somalia', 'abbrv': 'SO'}, '597': {'country': 'Suriname', 'abbrv': 'SR'}, '211': {'country': 'South Sudan', 'abbrv': 'SS'}, '239': {'country': 'Sao Tome and Principe', 'abbrv': 'ST'}, '503': {'country': 'El Salvador', 'abbrv': 'SV'}, '1-721': {'country': 'Sint Maarten (Dutch part)', 'abbrv': 'SX'}, '963': {'country': 'Syrian Arab Republic', 'abbrv': 'SY'}, '268': {'country': 'Swaziland', 'abbrv': 'SZ'}, '1-649': {'country': 'Turks and Caicos Islands', 'abbrv': 'TC'}, '235': {'country': 'Chad', 'abbrv': 'TD'}, '228': {'country': 'Togo', 'abbrv': 'TG'}, '66': {'country': 'Thailand', 'abbrv': 'TH'}, '992': {'country': 'Tajikistan', 'abbrv': 'TJ'}, '690': {'country': 'Tokelau', 'abbrv': 'TK'}, '670': {'country': 'Timor-Leste', 'abbrv': 'TL'}, '993': {'country': 'Turkmenistan', 'abbrv': 'TM'}, '216': {'country': 'Tunisia', 'abbrv': 'TN'}, '676': {'country': 'Tonga', 'abbrv': 'TO'}, '90': {'country': 'Turkey', 'abbrv': 'TR'}, '1-868': {'country': 'Trinidad and Tobago', 'abbrv': 'TT'}, '688': {'country': 'Tuvalu', 'abbrv': 'TV'}, '886': {'country': 'Taiwan', 'abbrv': 'TW'}, '255': {'country': 'United Republic of Tanzania', 'abbrv': 'TZ'}, '380': {'country': 'Ukraine', 'abbrv': 'UA'}, '256': {'country': 'Uganda', 'abbrv': 'UG'}, '598': {'country': 'Uruguay', 'abbrv': 'UY'}, '998': {'country': 'Uzbekistan', 'abbrv': 'UZ'}, '379': {'country': 'Vatican City', 'abbrv': 'VA'}, '1-784': {'country': 'Saint Vincent and the Grenadines', 'abbrv': 'VC'}, '58': {'country': 'Venezuela', 'abbrv': 'VE'}, '1-284': {'country': 'British Virgin Islands', 'abbrv': 'VG'}, '1-340': {'country': 'US Virgin Islands', 'abbrv': 'VI'}, '84': {'country': 'Vietnam', 'abbrv': 'VN'}, '678': {'country': 'Vanuatu', 'abbrv': 'VU'}, '681': {'country': 'Wallis and Futuna', 'abbrv': 'WF'}, '685': {'country': 'Samoa', 'abbrv': 'WS'}, '383': {'country': 'Kosovo', 'abbrv': 'XK'}, '967': {'country': 'Yemen', 'abbrv': 'YE'}, '27': {'country': 'South Africa', 'abbrv': 'ZA'}, '260': {'country': 'Zambia', 'abbrv': 'ZM'}, '263': {'country': 'Zimbabwe', 'abbrv': 'ZW'}}

flags={
    
    '🇦🇨': {'country': 'Ascension Island', 'abbrv': 'AC', 'code': ''},
    '🇦🇩': {'country': 'Andorra', 'abbrv': 'AD', 'code': '376'},
    '🇦🇪': {'country': 'United Arab Emirates', 'abbrv': 'AE', 'code': '971'},
    '🇦🇫': {'country': 'Afghanistan', 'abbrv': 'AF', 'code': '93'},
    '🇦🇬': {'country': 'Antigua and Barbuda', 'abbrv': 'AG', 'code': '1-268'},
    '🇦🇮': {'country': 'Anguilla', 'abbrv': 'AI', 'code': '1-264'},
    '🇦🇱': {'country': 'Albania', 'abbrv': 'AL', 'code': '355'},
    '🇦🇲': {'country': 'Armenia', 'abbrv': 'AM', 'code': '374'},
    '🇦🇴': {'country': 'Angola', 'abbrv': 'AO', 'code': '244'},
    '🇦🇶': {'country': 'Antarctica', 'abbrv': 'AQ', 'code': '672'},
    '🇦🇷': {'country': 'Argentina', 'abbrv': 'AR', 'code': '54'},
    '🇦🇸': {'country': 'American Samoa', 'abbrv': 'AS', 'code': '1-684'},
    '🇦🇹': {'country': 'Austria', 'abbrv': 'AT', 'code': '43'},
    '🇦🇺': {'country': 'Australia', 'abbrv': 'AU', 'code': '61'},
    '🇦🇼': {'country': 'Aruba', 'abbrv': 'AW', 'code': '297'},
    '🇦🇽': {'country': 'Alland Islands', 'abbrv': 'AX', 'code': '358'},
    '🇦🇿': {'country': 'Azerbaijan', 'abbrv': 'AZ', 'code': '994'},
    '🇧🇦': {'country': 'Bosnia and Herzegovina', 'abbrv': 'BA', 'code': '387'},
    '🇧🇧': {'country': 'Barbados', 'abbrv': 'BB', 'code': '1-246'},
    '🇧🇩': {'country': 'Bangladesh', 'abbrv': 'BD', 'code': '880'},
    '🇧🇪': {'country': 'Belgium', 'abbrv': 'BE', 'code': '32'},
    '🇧🇫': {'country': 'Burkina Faso', 'abbrv': 'BF', 'code': '226'},
    '🇧🇬': {'country': 'Bulgaria', 'abbrv': 'BG', 'code': '359'},
    '🇧🇭': {'country': 'Bahrain', 'abbrv': 'BH', 'code': '973'},
    '🇧🇮': {'country': 'Burundi', 'abbrv': 'BI', 'code': '257'},
    '🇧🇯': {'country': 'Benin', 'abbrv': 'BJ', 'code': '229'},
    '🇧🇱': {'country': 'Saint Barthelemy', 'abbrv': 'BL', 'code': '590'},
    '🇧🇲': {'country': 'Bermuda', 'abbrv': 'BM', 'code': '1-441'},
    '🇧🇳': {'country': 'Brunei Darussalam', 'abbrv': 'BN', 'code': '673'},
    '🇧🇴': {'country': 'Bolivia', 'abbrv': 'BO', 'code': '591'},
    '🇧🇶': {'country': 'Caribbean Netherlands', 'abbrv': 'BQ', 'code': ''},
    '🇧🇷': {'country': 'Brazil', 'abbrv': 'BR', 'code': '55'},
    '🇧🇸': {'country': 'Bahamas', 'abbrv': 'BS', 'code': '1-242'},
    '🇧🇹': {'country': 'Bhutan', 'abbrv': 'BT', 'code': '975'},
    '🇧🇻': {'country': 'Bouvet Island', 'abbrv': 'BV', 'code': '47'},
    '🇧🇼': {'country': 'Botswana', 'abbrv': 'BW', 'code': '267'},
    '🇧🇾': {'country': 'Belarus', 'abbrv': 'BY', 'code': '375'},
    '🇧🇿': {'country': 'Belize', 'abbrv': 'BZ', 'code': '501'},
    '🇨🇦': {'country': 'Canada', 'abbrv': 'CA', 'code': '1'},
    '🇨🇨': {'country': 'Cocos (Keeling) Islands', 'abbrv': 'CC', 'code': '61'},
    '🇨🇩': {'country': 'Congo - Kinshasa', 'abbrv': 'CD', 'code': '243'},
    '🇨🇫': {'country': 'Central African Republic', 'abbrv': 'CF', 'code': '236'},
    '🇨🇬': {'country': 'Congo - Brazzaville', 'abbrv': 'CG', 'code': '242'},
    '🇨🇭': {'country': 'Switzerland', 'abbrv': 'CH', 'code': '41'},
    '🇨🇮': {'country': "Cote d'Ivoire", 'abbrv': 'CI', 'code': '225'},
    '🇨🇰': {'country': 'Cook Islands', 'abbrv': 'CK', 'code': '682'},
    '🇨🇱': {'country': 'Chile', 'abbrv': 'CL', 'code': '56'},
    '🇨🇲': {'country': 'Cameroon', 'abbrv': 'CM', 'code': '237'},
    '🇨🇳': {'country': 'China', 'abbrv': 'CN', 'code': '86'},
    '🇨🇴': {'country': 'Colombia', 'abbrv': 'CO', 'code': '57'},
    '🇨🇵': {'country': 'Clipperton Island', 'abbrv': 'CP', 'code': ''},
    '🇨🇷': {'country': 'Costa Rica', 'abbrv': 'CR', 'code': '506'},
    '🇨🇺': {'country': 'Cuba', 'abbrv': 'CU', 'code': '53'},
    '🇨🇻': {'country': 'Cape Verde', 'abbrv': 'CV', 'code': '238'},
    '🇨🇼': {'country': 'Curacao', 'abbrv': 'CW', 'code': '599'},
    '🇨🇽': {'country': 'Christmas Island', 'abbrv': 'CX', 'code': '61'},
    '🇨🇾': {'country': 'Cyprus', 'abbrv': 'CY', 'code': '357'},
    '🇨🇿': {'country': 'Czech Republic', 'abbrv': 'CZ', 'code': '420'},
    '🇩🇪': {'country': 'Germany', 'abbrv': 'DE', 'code': '49'},
    '🇩🇬': {'country': 'Diego Garcia', 'abbrv': 'DG', 'code': ''},
    '🇩🇯': {'country': 'Djibouti', 'abbrv': 'DJ', 'code': '253'},
    '🇩🇰': {'country': 'Denmark', 'abbrv': 'DK', 'code': '45'},
    '🇩🇲': {'country': 'Dominica', 'abbrv': 'DM', 'code': '1-767'},
    '🇩🇴': {'country': 'Dominican Republic', 'abbrv': 'DO', 'code': '1-809'},
    '🇩🇿': {'country': 'Algeria', 'abbrv': 'DZ', 'code': '213'},
    '🇪🇦': {'country': 'Ceuta and Melilla', 'abbrv': 'EA', 'code': ''},
    '🇪🇨': {'country': 'Ecuador', 'abbrv': 'EC', 'code': '593'},
    '🇪🇪': {'country': 'Estonia', 'abbrv': 'EE', 'code': '372'},
    '🇪🇬': {'country': 'Egypt', 'abbrv': 'EG', 'code': '20'},
    '🇪🇭': {'country': 'Western Sahara', 'abbrv': 'EH', 'code': '212'},
    '🇪🇷': {'country': 'Eritrea', 'abbrv': 'ER', 'code': '291'},
    '🇪🇸': {'country': 'Spain', 'abbrv': 'ES', 'code': '34'},
    '🇪🇹': {'country': 'Ethiopia', 'abbrv': 'ET', 'code': '251'},
    '🇪🇺': {'country': 'European Union', 'abbrv': 'EU', 'code': ''},
    '🇫🇮': {'country': 'Finland', 'abbrv': 'FI', 'code': '358'},
    '🇫🇯': {'country': 'Fiji', 'abbrv': 'FJ', 'code': '679'},
    '🇫🇰': {'country': 'Falkland Islands (Malvinas)', 'abbrv': 'FK', 'code': '500'},
    '🇫🇲': {'country': 'Micronesia', 'abbrv': 'FM', 'code': '691'},
    '🇫🇴': {'country': 'Faroe Islands', 'abbrv': 'FO', 'code': '298'},
    '🇫🇷': {'country': 'France', 'abbrv': 'FR', 'code': '33'},
    '🇬🇦': {'country': 'Gabon', 'abbrv': 'GA', 'code': '241'},
    '🇬🇧': {'country': 'United Kingdom', 'abbrv': 'GB', 'code': '44'},
    '🇬🇩': {'country': 'Grenada', 'abbrv': 'GD', 'code': '1-473'},
    '🇬🇪': {'country': 'Georgia', 'abbrv': 'GE', 'code': '995'},
    '🇬🇫': {'country': 'French Guiana', 'abbrv': 'GF', 'code': '594'},
    '🇬🇬': {'country': 'Guernsey', 'abbrv': 'GG', 'code': '44'},
    '🇬🇭': {'country': 'Ghana', 'abbrv': 'GH', 'code': '233'},
    '🇬🇮': {'country': 'Gibraltar', 'abbrv': 'GI', 'code': '350'},
    '🇬🇱': {'country': 'Greenland', 'abbrv': 'GL', 'code': '299'},
    '🇬🇲': {'country': 'Gambia', 'abbrv': 'GM', 'code': '220'},
    '🇬🇳': {'country': 'Guinea', 'abbrv': 'GN', 'code': '224'},
    '🇬🇵': {'country': 'Guadeloupe', 'abbrv': 'GP', 'code': '590'},
    '🇬🇶': {'country': 'Equatorial Guinea', 'abbrv': 'GQ', 'code': '240'},
    '🇬🇷': {'country': 'Greece', 'abbrv': 'GR', 'code': '30'},
    '🇬🇸': {'country': 'South Georgia and the South Sandwich Islands', 'abbrv': 'GS', 'code': '500'},
    '🇬🇹': {'country': 'Guatemala', 'abbrv': 'GT', 'code': '502'},
    '🇬🇺': {'country': 'Guam', 'abbrv': 'GU', 'code': '1-671'},
    '🇬🇼': {'country': 'Guinea-Bissau', 'abbrv': 'GW', 'code': '245'},
    '🇬🇾': {'country': 'Guyana', 'abbrv': 'GY', 'code': '592'},
    '🇭🇰': {'country': 'Hong Kong', 'abbrv': 'HK', 'code': '852'},
    '🇭🇲': {'country': 'Heard Island and McDonald Islands', 'abbrv': 'HM', 'code': '672'},
    '🇭🇳': {'country': 'Honduras', 'abbrv': 'HN', 'code': '504'},
    '🇭🇷': {'country': 'Croatia', 'abbrv': 'HR', 'code': '385'},
    '🇭🇹': {'country': 'Haiti', 'abbrv': 'HT', 'code': '509'},
    '🇭🇺': {'country': 'Hungary', 'abbrv': 'HU', 'code': '36'},
    '🇮🇨': {'country': 'Canary Islands', 'abbrv': 'IC', 'code': ''},
    '🇮🇩': {'country': 'Indonesia', 'abbrv': 'ID', 'code': '62'},
    '🇮🇪': {'country': 'Ireland', 'abbrv': 'IE', 'code': '353'},
    '🇮🇲': {'country': 'Isle of Man', 'abbrv': 'IM', 'code': '44'},
    '🇮🇳': {'country': 'India', 'abbrv': 'IN', 'code': '91'},
    '🇮🇴': {'country': 'British Indian Ocean Territory', 'abbrv': 'IO', 'code': '246'},
    '🇮🇶': {'country': 'Iraq', 'abbrv': 'IQ', 'code': '964'},
    '🇮🇷': {'country': 'Iran', 'abbrv': 'IR', 'code': '98'},
    '🇮🇸': {'country': 'Iceland', 'abbrv': 'IS', 'code': '354'},
    '🇮🇹': {'country': 'Italy', 'abbrv': 'IT', 'code': '39'},
    '🇯🇪': {'country': 'Jersey', 'abbrv': 'JE', 'code': '44'},
    '🇯🇲': {'country': 'Jamaica', 'abbrv': 'JM', 'code': '1-876'},
    '🇯🇴': {'country': 'Jordan', 'abbrv': 'JO', 'code': '962'},
    '🇯🇵': {'country': 'Japan', 'abbrv': 'JP', 'code': '81'},
    '🇰🇪': {'country': 'Kenya', 'abbrv': 'KE', 'code': '254'},
    '🇰🇬': {'country': 'Kyrgyzstan', 'abbrv': 'KG', 'code': '996'},
    '🇰🇭': {'country': 'Cambodia', 'abbrv': 'KH', 'code': '855'},
    '🇰🇮': {'country': 'Kiribati', 'abbrv': 'KI', 'code': '686'},
    '🇰🇲': {'country': 'Comoros', 'abbrv': 'KM', 'code': '269'},
    '🇰🇳': {'country': 'Saint Kitts and Nevis', 'abbrv': 'KN', 'code': '1-869'},
    '🇰🇵': {'country': 'North Korea', 'abbrv': 'KP', 'code': '850'},
    '🇰🇷': {'country': 'South Korea', 'abbrv': 'KR', 'code': '82'},
    '🇰🇼': {'country': 'Kuwait', 'abbrv': 'KW', 'code': '965'},
    '🇰🇾': {'country': 'Cayman Islands', 'abbrv': 'KY', 'code': '1-345'},
    '🇰🇿': {'country': 'Kazakhstan', 'abbrv': 'KZ', 'code': '7'},
    '🇱🇦': {'country': "Lao People's Democratic Republic", 'abbrv': 'LA', 'code': '856'},
    '🇱🇧': {'country': 'Lebanon', 'abbrv': 'LB', 'code': '961'},
    '🇱🇨': {'country': 'Saint Lucia', 'abbrv': 'LC', 'code': '1-758'},
    '🇱🇮': {'country': 'Liechtenstein', 'abbrv': 'LI', 'code': '423'},
    '🇱🇰': {'country': 'Sri Lanka', 'abbrv': 'LK', 'code': '94'},
    '🇱🇷': {'country': 'Liberia', 'abbrv': 'LR', 'code': '231'},
    '🇱🇸': {'country': 'Lesotho', 'abbrv': 'LS', 'code': '266'},
    '🇱🇹': {'country': 'Lithuania', 'abbrv': 'LT', 'code': '370'},
    '🇱🇺': {'country': 'Luxembourg', 'abbrv': 'LU', 'code': '352'},
    '🇱🇻': {'country': 'Latvia', 'abbrv': 'LV', 'code': '371'},
    '🇱🇾': {'country': 'Libya', 'abbrv': 'LY', 'code': '218'},
    '🇲🇦': {'country': 'Morocco', 'abbrv': 'MA', 'code': '212'},
    '🇲🇨': {'country': 'Monaco', 'abbrv': 'MC', 'code': '377'},
    '🇲🇩': {'country': 'Moldova', 'abbrv': 'MD', 'code': '373'},
    '🇲🇪': {'country': 'Montenegro', 'abbrv': 'ME', 'code': '382'},
    '🇲🇫': {'country': 'Saint Martin (French part)', 'abbrv': 'MF', 'code': '590'},
    '🇲🇬': {'country': 'Madagascar', 'abbrv': 'MG', 'code': '261'},
    '🇲🇭': {'country': 'Marshall Islands', 'abbrv': 'MH', 'code': '692'},
    '🇲🇰': {'country': 'North Macedonia', 'abbrv': 'MK', 'code': '389'},
    '🇲🇱': {'country': 'Mali', 'abbrv': 'ML', 'code': '223'},
    '🇲🇲': {'country': 'Myanmar', 'abbrv': 'MM', 'code': '95'},
    '🇲🇳': {'country': 'Mongolia', 'abbrv': 'MN', 'code': '976'},
    '🇲🇴': {'country': 'Macao', 'abbrv': 'MO', 'code': '853'},
    '🇲🇵': {'country': 'Northern Mariana Islands', 'abbrv': 'MP', 'code': '1-670'},
    '🇲🇶': {'country': 'Martinique', 'abbrv': 'MQ', 'code': '596'},
    '🇲🇷': {'country': 'Mauritania', 'abbrv': 'MR', 'code': '222'},
    '🇲🇸': {'country': 'Montserrat', 'abbrv': 'MS', 'code': '1-664'},
    '🇲🇹': {'country': 'Malta', 'abbrv': 'MT', 'code': '356'},
    '🇲🇺': {'country': 'Mauritius', 'abbrv': 'MU', 'code': '230'},
    '🇲🇻': {'country': 'Maldives', 'abbrv': 'MV', 'code': '960'},
    '🇲🇼': {'country': 'Malawi', 'abbrv': 'MW', 'code': '265'},
    '🇲🇽': {'country': 'Mexico', 'abbrv': 'MX', 'code': '52'},
    '🇲🇾': {'country': 'Malaysia', 'abbrv': 'MY', 'code': '60'},
    '🇲🇿': {'country': 'Mozambique', 'abbrv': 'MZ', 'code': '258'},
    '🇳🇦': {'country': 'Namibia', 'abbrv': 'NA', 'code': '264'},
    '🇳🇨': {'country': 'New Caledonia', 'abbrv': 'NC', 'code': '687'},
    '🇳🇪': {'country': 'Niger', 'abbrv': 'NE', 'code': '227'},
    '🇳🇫': {'country': 'Norfolk Island', 'abbrv': 'NF', 'code': '672'},
    '🇳🇬': {'country': 'Nigeria', 'abbrv': 'NG', 'code': '234'},
    '🇳🇮': {'country': 'Nicaragua', 'abbrv': 'NI', 'code': '505'},
    '🇳🇱': {'country': 'Netherlands', 'abbrv': 'NL', 'code': '31'},
    '🇳🇴': {'country': 'Norway', 'abbrv': 'NO', 'code': '47'},
    '🇳🇵': {'country': 'Nepal', 'abbrv': 'NP', 'code': '977'},
    '🇳🇷': {'country': 'Nauru', 'abbrv': 'NR', 'code': '674'},
    '🇳🇺': {'country': 'Niue', 'abbrv': 'NU', 'code': '683'},
    '🇳🇿': {'country': 'New Zealand', 'abbrv': 'NZ', 'code': '64'},
    '🇴🇲': {'country': 'Oman', 'abbrv': 'OM', 'code': '968'},
    '🇵🇦': {'country': 'Panama', 'abbrv': 'PA', 'code': '507'},
    '🇵🇪': {'country': 'Peru', 'abbrv': 'PE', 'code': '51'},
    '🇵🇫': {'country': 'French Polynesia', 'abbrv': 'PF', 'code': '689'},
    '🇵🇬': {'country': 'Papua New Guinea', 'abbrv': 'PG', 'code': '675'},
    '🇵🇭': {'country': 'Philippines', 'abbrv': 'PH', 'code': '63'},
    '🇵🇰': {'country': 'Pakistan', 'abbrv': 'PK', 'code': '92'},
    '🇵🇱': {'country': 'Poland', 'abbrv': 'PL', 'code': '48'},
    '🇵🇲': {'country': 'Saint Pierre and Miquelon', 'abbrv': 'PM', 'code': '508'},
    '🇵🇳': {'country': 'Pitcairn', 'abbrv': 'PN', 'code': '870'},
    '🇵🇷': {'country': 'Puerto Rico', 'abbrv': 'PR', 'code': '1'},
    '🇵🇸': {'country': 'Palestine', 'abbrv': 'PS', 'code': '970'},
    '🇵🇹': {'country': 'Portugal', 'abbrv': 'PT', 'code': '351'},
    '🇵🇼': {'country': 'Palau', 'abbrv': 'PW', 'code': '680'},
    '🇵🇾': {'country': 'Paraguay', 'abbrv': 'PY', 'code': '595'},
    '🇶🇦': {'country': 'Qatar', 'abbrv': 'QA', 'code': '974'},
    '🇷🇪': {'country': 'Reunion', 'abbrv': 'RE', 'code': '262'},
    '🇷🇴': {'country': 'Romania', 'abbrv': 'RO', 'code': '40'},
    '🇷🇸': {'country': 'Serbia', 'abbrv': 'RS', 'code': '381'},
    '🇷🇺': {'country': 'Russian Federation', 'abbrv': 'RU', 'code': '7'},
    '🇷🇼': {'country': 'Rwanda', 'abbrv': 'RW', 'code': '250'},
    '🇸🇦': {'country': 'Saudi Arabia', 'abbrv': 'SA', 'code': '966'},
    '🇸🇧': {'country': 'Solomon Islands', 'abbrv': 'SB', 'code': '677'},
    '🇸🇨': {'country': 'Seychelles', 'abbrv': 'SC', 'code': '248'},
    '🇸🇩': {'country': 'Sudan', 'abbrv': 'SD', 'code': '249'},
    '🇸🇪': {'country': 'Sweden', 'abbrv': 'SE', 'code': '46'},
    '🇸🇬': {'country': 'Singapore', 'abbrv': 'SG', 'code': '65'},
    '🇸🇭': {'country': 'Saint Helena', 'abbrv': 'SH', 'code': '290'},
    '🇸🇮': {'country': 'Slovenia', 'abbrv': 'SI', 'code': '386'},
    '🇸🇯': {'country': 'Svalbard and Jan Mayen', 'abbrv': 'SJ', 'code': '47'},
    '🇸🇰': {'country': 'Slovakia', 'abbrv': 'SK', 'code': '421'},
    '🇸🇱': {'country': 'Sierra Leone', 'abbrv': 'SL', 'code': '232'},
    '🇸🇲': {'country': 'San Marino', 'abbrv': 'SM', 'code': '378'},
    '🇸🇳': {'country': 'Senegal', 'abbrv': 'SN', 'code': '221'},
    '🇸🇴': {'country': 'Somalia', 'abbrv': 'SO', 'code': '252'},
    '🇸🇷': {'country': 'Suriname', 'abbrv': 'SR', 'code': '597'},
    '🇸🇸': {'country': 'South Sudan', 'abbrv': 'SS', 'code': '211'},
    '🇸🇹': {'country': 'Sao Tome and Principe', 'abbrv': 'ST', 'code': '239'},
    '🇸🇻': {'country': 'El Salvador', 'abbrv': 'SV', 'code': '503'},
    '🇸🇽': {'country': 'Sint Maarten (Dutch part)', 'abbrv': 'SX', 'code': '1-721'},
    '🇸🇾': {'country': 'Syrian Arab Republic', 'abbrv': 'SY', 'code': '963'},
    '🇸🇿': {'country': 'Swaziland', 'abbrv': 'SZ', 'code': '268'},
    '🇹🇦': {'country': 'Tristan da Cunha', 'abbrv': 'TA', 'code': ''},
    '🇹🇨': {'country': 'Turks and Caicos Islands', 'abbrv': 'TC', 'code': '1-649'},
    '🇹🇩': {'country': 'Chad', 'abbrv': 'TD', 'code': '235'},
    '🇹🇫': {'country': 'French Southern Territories', 'abbrv': 'TF', 'code': '262'},
    '🇹🇬': {'country': 'Togo', 'abbrv': 'TG', 'code': '228'},
    '🇹🇭': {'country': 'Thailand', 'abbrv': 'TH', 'code': '66'},
    '🇹🇯': {'country': 'Tajikistan', 'abbrv': 'TJ', 'code': '992'},
    '🇹🇰': {'country': 'Tokelau', 'abbrv': 'TK', 'code': '690'},
    '🇹🇱': {'country': 'Timor-Leste', 'abbrv': 'TL', 'code': '670'},
    '🇹🇲': {'country': 'Turkmenistan', 'abbrv': 'TM', 'code': '993'},
    '🇹🇳': {'country': 'Tunisia', 'abbrv': 'TN', 'code': '216'},
    '🇹🇴': {'country': 'Tonga', 'abbrv': 'TO', 'code': '676'},
    '🇹🇷': {'country': 'Turkey', 'abbrv': 'TR', 'code': '90'},
    '🇹🇹': {'country': 'Trinidad and Tobago', 'abbrv': 'TT', 'code': '1-868'},
    '🇹🇻': {'country': 'Tuvalu', 'abbrv': 'TV', 'code': '688'},
    '🇹🇼': {'country': 'Taiwan', 'abbrv': 'TW', 'code': '886'},
    '🇹🇿': {'country': 'United Republic of Tanzania', 'abbrv': 'TZ', 'code': '255'},
    '🇺🇦': {'country': 'Ukraine', 'abbrv': 'UA', 'code': '380'},
    '🇺🇬': {'country': 'Uganda', 'abbrv': 'UG', 'code': '256'},
    '🇺🇲': {'country': 'U.S. Outlying Islands', 'abbrv': 'UM', 'code': ''},
    '🇺🇳': {'country': 'United Nations', 'abbrv': 'UN', 'code': ''},
    '🇺🇸': {'country': 'United States', 'abbrv': 'US', 'code': '1'},
    '🇺🇾': {'country': 'Uruguay', 'abbrv': 'UY', 'code': '598'},
    '🇺🇿': {'country': 'Uzbekistan', 'abbrv': 'UZ', 'code': '998'},
    '🇻🇦': {'country': 'Vatican City', 'abbrv': 'VA', 'code': '379'},
    '🇻🇨': {'country': 'Saint Vincent and the Grenadines', 'abbrv': 'VC', 'code': '1-784'},
    '🇻🇪': {'country': 'Venezuela', 'abbrv': 'VE', 'code': '58'},
    '🇻🇬': {'country': 'British Virgin Islands', 'abbrv': 'VG', 'code': '1-284'},
    '🇻🇮': {'country': 'US Virgin Islands', 'abbrv': 'VI', 'code': '1-340'},
    '🇻🇳': {'country': 'Vietnam', 'abbrv': 'VN', 'code': '84'},
    '🇻🇺': {'country': 'Vanuatu', 'abbrv': 'VU', 'code': '678'},
    '🇼🇫': {'country': 'Wallis and Futuna', 'abbrv': 'WF', 'code': '681'},
    '🇼🇸': {'country': 'Samoa', 'abbrv': 'WS', 'code': '685'},
    '🇽🇰': {'country': 'Kosovo', 'abbrv': 'XK', 'code': '383'},
    '🇾🇪': {'country': 'Yemen', 'abbrv': 'YE', 'code': '967'},
    '🇾🇹': {'country': 'Mayotte', 'abbrv': 'YT', 'code': '262'},
    '🇿🇦': {'country': 'South Africa', 'abbrv': 'ZA', 'code': '27'},
    '🇿🇲': {'country': 'Zambia', 'abbrv': 'ZM', 'code': '260'},
    '🇿🇼': {'country': 'Zimbabwe', 'abbrv': 'ZW', 'code': '263'}

}


def main():
    global MAIN_SESSION
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main_session.json'), 'r') as file:
        MAIN_SESSION = json.load(file)

    if type(MAIN_SESSION) != list:
        sys.exit(1)

    args = parse_args()
    file_name = args.outfile
    file_format = args.file_format
    no_save_to_db = args.no_save
    followers = args.followers
    following = args.following
    
    username = 0
    user_file = ""
    if args.username:
        username = args.username
    else:
        user_file = args.username_file

    if args.both: followers = following = True


    #Check if the last username=CRONJOB_USERNAME=sekomekobeko1721921

    if user_file:

        path_to_user_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), user_file)

        last_username = check_last_username(path_to_user_file)

        if last_username == CRONJOB_USERNAME:

            print("The last username is already 'sekomekobeko1721921'.")

        else:
            print("The last username is not 'sekomekobeko1721921'. Appending it now.")
            with open(path_to_user_file, 'a') as file:
                file.write(f"{CRONJOB_USERNAME}\n")        
            
    if username:

        user = User(username, file_name, file_format, no_save_to_db, followers, following)

        user_info = user.basic_info

        print(user_info)
    
    else:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), user_file), 'r') as filee:
            lines=filee.readlines()
            for line in lines:
                username2 = line.strip()

                #To ignore empty lines.
                if not username2:
                    continue

                if username2 == CRONJOB_USERNAME:
                    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "followers_status.txt"), 'w') as flrs_status_file:
                        flrs_status_file.write("END")

                    print("The job has been finished!")
                    sys.exit(1)

                print(username2)

                user2 = User(username2, file_name, file_format, no_save_to_db, followers, following)
                user_info2 = user2.basic_info
                
                if not user_info2.get("bad"):
                    pass
                
        


#formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=40)
def parse_args() -> dict:
    #https://stackoverflow.com/users/901925/hpaulj
    parser = argparse.ArgumentParser(prog="Test", description="Instagram Scrapper", epilog="Examples:")
    # parser.add_argument('-h', '--help', action='help', help='Show this help message and exit')
    parser.add_argument('-u', '--username', metavar=('<username>'), help='Username to scrape', required='-d' not in sys.argv)
    parser.add_argument('-d', '--username-file', metavar=('<username-file>'), help='File contain usernames to scrape', required='-u' not in sys.argv)
    parser.add_argument('-o', '--outfile', metavar='<file>', help="output file to save data to", required='-f' in sys.argv)
    parser.add_argument('-f', '--file-format', help="file format", choices=("csv", "xlsx"), required='-o' in sys.argv)

    flags_group=parser.add_argument_group('flags', 'on/off flags: specifying multiple flags are allowed. For all flags (default: off)')
    flags_group.add_argument('--followers', action='store_true', help="only scrape followers list")
    flags_group.add_argument('--following', action='store_true', help="only scrape following list")
    flags_group.add_argument('--both', action='store_true', help="scrape followers/following list")
    flags_group.add_argument('--posts', action='store_true', help="scrape posts (TODO)")
    flags_group.add_argument('--reels', action='store_true', help="scrape reels (TODO)")
    flags_group.add_argument('--stories', action='store_true', help="scrape stories (TODO)")
    flags_group.add_argument('--highlights', action='store_true', help="scrape highlights (TODO)")
    flags_group.add_argument('--no-save', action='store_true', help="do not save data to database(i.e., scrapIG.db) (default: off)", default=False)
    return parser.parse_args()



def check_last_username(file_path):

    with open(file_path, 'r') as file:

        lines = file.readlines()

        if lines:
            last_username = lines[-1].strip()
        else:
            last_username = None
    return last_username



def validate_username(username: str) -> str:
    return username.replace('@', '') if username.startswith('@') else username

def validate_file_name(filename, file_format):
    if filename:
        return filename if filename.endswith(f'.{file_format}') else f'{filename}.{file_format}'
    else:
        return filename

def write_to_file(filename, file_format, user_info):

    user_keys=user_info.keys()
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename), 'w') as file:
        if file_format == 'csv':
            csv_writer = csv.DictWriter(file, user_keys)
            csv_writer.writeheader()
            csv_writer.writerow(user_info)
            print(f'Data saved to: {filename}')
            return 1
        else:
            pass

def write_to_db(user_data: dict) -> bool:
    global counter
    global counter2
    # 0 => False

    success = 0
    try:
        db = sqlite3.connect(db_name)
        cr = db.cursor()

        #username = user_data['username']

        #is_exists=cr.execute('SELECT id FROM users where username = ?', (username,)).fetchone()

        #if is_exists:
        #    cr.execute('DELETE FROM users where username = ?', (username,))

        #print(f"This is userdata: {user_data}")
        user_data_keys=user_data.keys()
        columns = ', '.join(user_data_keys)
        placeholders = ':'+', :'.join(user_data_keys)
        
            
        query = 'INSERT INTO users (%s) VALUES (%s)' % (columns, placeholders)
        print(user_data)
        cr.execute(query, user_data)
        db.commit()
        counter += 1

        #reset counter2 because we want only the 10 not-found users in a row.
        #not 10 not-found users between them valid users!
        counter2 = 0

    except Exception as e:
        print(f'Error occured: {type(e)}')

    except:
        print('Error occured in write_to_db func!')

    else:
        #re-assign success to 1 in 'else', if there was no exception raised
        success = 1

    finally:
        cr.close()
        db.close()

    return success

def send_req(username: str) -> requests.Response:


    session = MAIN_SESSION.copy()

    headers = session[1]
    headers['Referer'] = f'https://www.instagram.com/{username}/'
    cookies=session[2]

    return requests.get(f'https://www.instagram.com/api/v1/users/web_profile_info/?username={username}', headers=headers, cookies=cookies, timeout=20)

def parse_response(resp: requests.Response) -> dict:

    accurate_numbers = list()
    not_accurate_numbers = list()
    emails = list()

    user_data = dict()

    if resp is not None and resp.status_code == 200:

        from_json_resp = resp.json()["data"]["user"]



        #username has been found
        if from_json_resp:


            for prop in _USER_PROPS: user_data[prop] = from_json_resp[prop]

            user_data['following_count'] = from_json_resp["edge_follow"]["count"]
            user_data['followers_count'] = from_json_resp["edge_followed_by"]["count"]
            user_data['posts_count'] = from_json_resp["edge_owner_to_timeline_media"]["count"]
            user_data['link'] = f'https://instagram.com/{from_json_resp["username"]}/'
            user_data['joined_date'] = "todo"
            
            numbers = is_number_regex.findall(from_json_resp['biography'])
            country_name = None

            if numbers:

                for num in numbers:
                    country_code = country_code_regex.findall(num)
                    if country_code:

                        country_code = country_code[0]

                        num = num.replace(country_code, "").strip()

                        country_code = re.sub(r'^\D*', '', country_code)

                        country_code = re.sub(r'\D+', '-', country_code)

                        num = f'+{country_code} {num}'

                        accurate_numbers.append(num)

                        if country_name is None:

                            #returns string or list
                            country_name = countries[country_code]['country']
                            abbrv = countries[country_code]['abbrv']

                            if type(country_name) == list:
                                country_name = None


                        # print(country_code, country_name, abbrv)
                    else:
                        #972 is Israel code
                        israel_code = re.findall(r'\+\D*972', num)

                        #ignore israel code
                        if israel_code:
                            continue

                        not_accurate_numbers.append(num)

            if country_name is None:
                all_flags=is_flag_regex.findall(from_json_resp['biography'])

                if all_flags:
                    country_name2=list()
                    for flag in all_flags:
                        if flag == '🇵🇸' or flag == '🇺🇦':
                            continue
                        if flags.get(flag):
                            
                            country_name2.append(flags.get(flag)['country'])

                    country_name = list(dict.fromkeys(country_name2))


            if type(country_name) == str:
                user_data['country'] = country_name
            elif type(country_name) == list:
                user_data['country'] = ' | '.join(country_name)
            else:
                user_data['country']=''

            emails = email_regex.findall(from_json_resp['biography'])

            user_data['email'] = ' | '.join(emails) if emails else ''

            user_data['phone'] = ' | '.join(accurate_numbers) if accurate_numbers else ''

            user_data['possible_phone'] = ' | '.join(not_accurate_numbers) if not_accurate_numbers else ''

            return user_data

        #status_code: 200, but the user not found, this is also not abvious behavior
        #{'user': None}
        #Suspended accounts status_code is "200".
        #You can't use the "username" of a suspended account.
        #ctasnghwy
        #eouoqjpvl
        #These are two suspended accounts with the password "Abdo23Medo298" "2024-May-27"
        #Try to takeover the username after 180 day, and check if it is possible. 
        #another un-obvious behaviour the user is exists but it tells you that not found.
        #Status_code: 200, {'user': None}
        #Username: piratesgrog, cannot be found!
        #{"data":{"user":null},"status":"ok"}
        else:
            print(f"Status_code: {resp.status_code}, {resp.json()['data']}")
            print(resp.text)
    
            return 0


    #This means the session cannot get more:
    #too many requests.
    #The account here is usually not suspended, rather it is a challenge to "DISMISS"
    elif resp.status_code == 429:

        print(f"Status_code: {resp.status_code}")
        print(resp.text)
        return 55


    #Not_found_user, the username can be both available to use or not available
    #404 here is not clearly obvious what exactly it is.
    elif resp.status_code == 404:

        print(f"Status_code: {resp.status_code}")
        print(resp.text)
        return 0

    else:
        print(f"Status_code: {resp.status_code}")
        print(resp.text)
        return 44


def is_user_exists_in_db(username):

    # 0 => False
    success = 0
    try:
        db = sqlite3.connect(db_name)
        cr = db.cursor()

        #creating a table does not require using commit() method.
        
        cr.execute('''CREATE TABLE if not exists users(app_id integer primary key, {} text, {} text, {} text, {} text, {} text, {} boolean, {} text, {} boolean, {} boolean, {} boolean, {} text, {} text, {} text, {} text, following_count text, followers_count text, posts_count text, country text, email text, phone text, possible_phone text, {} text)'''.format(*_USER_PROPS2))

        cr.execute('''CREATE TABLE if not exists followers(app_id integer primary key, main_user text, next_max_id text, track_token text, {} text, {} text, {} text, {} text, {} text, {} text, {} text)'''.format(*_FOLLOWERS_PROPS2))

        cr.execute('''CREATE TABLE if not exists following(app_id integer primary key, main_user text, next_max_id text, track_token text, {} text, {} text, {} text, {} text, {} text, {} text, {} text)'''.format(*_FOLLOWERS_PROPS2))

        cr.execute('''CREATE TABLE if not exists user_not_found(app_id integer primary key, main_user text)''')

        cr.execute('''CREATE TABLE if not exists has_no_flrs(app_id integer primary key, main_user text)''')
        cr.execute('''CREATE TABLE if not exists has_no_flws(app_id integer primary key, main_user text)''')

        cr.execute('''CREATE TABLE if not exists track_flr(app_id integer primary key, main_user text, next_max_id text, big_list boolean, track_token text)''')
        cr.execute('''CREATE TABLE if not exists track_flw(app_id integer primary key, main_user text, next_max_id text, big_list boolean, track_token text)''')

        is_exists=cr.execute('SELECT id FROM users where username = ?', (username,)).fetchone()
        db.commit()
        
        user_id=''
        is_private=''
        user_info=dict()
        if is_exists:
            user_id = is_exists[0]
            #print("abdo1")
            is_private=cr.execute('SELECT is_private FROM users where username = ?', (username,)).fetchone()[0]
            #print("abdo2")
            user_info['id'] = user_id
            user_info['username'] = username
            user_info['is_private'] = int(is_private)
            #print(user_info)

        return user_info if is_exists else 0


    except Exception as e:
        print(f'Error occured: {type(e)}')

    except:
        print('Error occured in is_user_exists_in_db func!')

    else:
        #re-assign success to 1 in 'else', if there was no exception raised
        success = 1

    finally:
        cr.close()
        db.close()

    return success



def get_user_info(username: str, no_save: bool = False) -> dict:
    global counter
    global counter2
    track_unkown_error=0
    
    try:
        user_data = is_user_exists_in_db(username)
        
        if type(user_data) is dict:
            print(f'Username: {username} exists in the database')
            #print(f'#'*70)
        else:
            #WTF does this counter < requests_limit do!!!
            #if counter < requests_limit:
        
            resp = send_req(username)

            
            user_data = parse_response(resp)

            #429, too many requests, the session cannot get anymore users.
            if user_data == 55:
                sys.exit(1)

            #Unkown error
            if user_data == 44:
                track_unkown_error=1
                sys.exit(1)

            if not user_data:
                counter2 += 1
                print(f'Username: {username}, cannot be found!')
                with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'not-found-users.txt'), 'a') as file2:
                    file2.write(username+'\n')
                print(f'#'*70)
                if counter2 == not_found_limit:
                    
                    sys.exit(1)
                
                time.sleep(requests_delay)
                return {"bad": "user_data is not properly parsed"}

            if no_save == False:
                if write_to_db(user_data):
                    print(f'Request_{counter}')
                    print(f'{username} data has been saved to the database')
                    print(f'#'*70)
                else:
                    print(f'Request_{counter}')
                    print(f'Failed to save {username} data to the database!')
                    print(f'#'*70)
                    
            time.sleep(requests_delay)
           # else:                
           #     sys.exit(1)

        return user_data

    except Exception as e:
        print(f'Error occuredA: {e}, in get_user_info func!')
        sys.exit(1)

    except SystemExit:
        #if counter == requests_limit:
            #print(f'END: {counter} requests has been sent!')
        #else:
        if counter2 == not_found_limit:
            print(f'There are {not_found_limit} not found usernames!')
        elif track_unkown_error == 1:
            print(f"There was unkown error!")
        else:
            print(f"Status_code_429: Too_many_requests, You need new session. Usually the user was not suspended!")
        sys.exit(1)

    except:
        print('Error occured in get_user_info func!')
        sys.exit(1)

def search_flr_next_id(username):
    try:
        db=sqlite3.connect(db_name)
        cr=db.cursor()

        res=cr.execute('SELECT * FROM track_flr where main_user = ? ORDER BY app_id DESC LIMIT 1', (username,)).fetchone()
        # print(f'this is res: {res}')

        if res:
            next_max_id=res[2]
            track_token=res[4]

            if next_max_id == '' or next_max_id != 'end':
                cr.execute('DELETE FROM followers where next_max_id = ? and main_user = ? and track_token = ?', (next_max_id, username, track_token))

                db.commit()
                cr.execute('DELETE FROM track_flr where next_max_id = ? and main_user = ? and track_token = ?', (next_max_id, username, track_token))
                db.commit()
                return next_max_id
            else:
                return 'end'

        else:
            return ''

    except Exception:
        print('Error search')
    except:
        print('Error searchA')

    finally:
        cr.close()
        db.close()

def get_followers(user_info: dict):

    if "bad" in user_info:
        print("bad_user")
        return 1

    if user_info['is_private']:
        print(f'>Username: \'{user_info["username"]}\' is private, cannot get their followers...')
        return 0
        

    count = 1

    session = MAIN_SESSION.copy()
    headers = session[1]
    cookies = session[2]
    
    username = user_info['username']
    headers['Referer'] = f'https://www.instagram.com/{username}/followers'
    user_id = user_info['id']

    if not username or not user_id:
        raise ValueError('There is no username or user_id specifid')



    #We should test the internet connection one time, before trying to get the next_max_id:
    #To make sure that we are not going to delete any records if there are no internet.
    test_req = requests.get("https://example.com")

    if test_req.status_code != 200:
        raise ValueError('There is no internet connection.')
    
    next_max_id=search_flr_next_id(username)

    print(f'next_max_id is: ~{next_max_id}~')
    if next_max_id == 'end':
        print(f'Followers already exist for user: {username}')
        print("#"*70)

        #cronjob_username in the top of the file.
        #it should be replaced with the last username that we want to scrape.
        #We don't need the following lines unless there is a cronjob for followers.

        # if username == CRONJOB_USERNAME:
        #     with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "followers_status.txt"), "w") as flrs_file:
        #        flrs_file.write("END")

        return

    big_list = True
    #next_max_id = ''
    req_start_time = 20
    #time_to_sleep = 1

    #time.sleep(2)

    while big_list:

        track_token=random_gen()

        followers_data = list()
        #if (time.perf_counter() - req_start_time) < 30:
        #    raise ValueError('Time is less than 30sec')
        #print('after 15sec')

        #req_start_time = time.perf_counter()

        resp = requests.get(f'https://www.instagram.com/api/v1/friendships/{user_id}/followers/?count=100&max_id={next_max_id}&search_surface=follow_list_page', headers=headers, cookies=cookies, timeout=20)

        if resp is not None and resp.status_code == 200:
            print('response not None and is 200')
            from_json_resp = resp.json()

            users=from_json_resp['users']

            # User has followers.
            if users:

                #followers_data = users.copy()
                print('has_followers: ', count)
                count += 1
                
                users_list_len=len(users)

                for i in range(users_list_len):
                    followers_data.append(users[i])


                followers_data.append({'main_user': username, 'next_max_id': next_max_id, 'big_list': big_list, 'track_token': track_token})

                big_list = from_json_resp['big_list']
                #print(f"This is big_list{big_list}")
                if big_list:
                    next_max_id = from_json_resp['next_max_id']
                else:
                    next_max_id = 'end'
                    # if username == CRONJOB_USERNAME:
                    #     with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "followers_status.txt"), "w") as flrs_file2:
                    #         flrs_file2.write("END")

                    #print(f"this is next_max_id: {next_max_id}")
                    print(f"Followers have been fetched for user: '{username}'")
                    print(f"#"*70)

                # We need to store them into the database...
                if not write_flr_to_db(followers_data):
                    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "flrs.txt"), 'a') as faffa:
                        faffa.write(f'User: \'{username}\' Failed to save a response of followers into the database!!'+'\n')

                print("time to sleep 30sec")
                time.sleep(followers_requests_delay)

            # User has no followers.
            else:
                
                print(f'>Username: \'{username}\' has no followers...')
                break


        #{"message":"checkpoint_required","checkpoint_url":"https://www.instagram.com/challenge/?next=/api/v1/friendships/2921951046/followers/%253Fcount%253D100%2526max_id%253DQVFBOUxMVTVYWklrWEZIY3ZfTnhZZ0VsZ1BHVENVY0pjQkM4QTNHYVZ2QkR5V3h0QXJIMllCeUdsTzYxc2dTMWFzczRiZ21UTmJ1YU01RDhEbEFTeHJxLQ%253D%253D%2526search_surface%253Dfollow_list_page","lock":true,"flow_render_type":0,"status":"fail"}
        ##The account here is usually not suspended, rather it is a challenge to "DISMISS"
        elif resp.status_code in [400, 401]:
            print(f"resp.status_code = {resp.status_code}")
            print(resp.text)
            sys.exit(1)


        else:
            print(f"resp.status_code = {resp.status_code}")
            print(resp.text)
            break

    else:

        track_token=random_gen()

        if not write_flr_to_db({'main_user': username,'next_max_id': next_max_id, 'big_list': big_list, 'track_token': track_token}):
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "flrs.txt"), "a") as faffa2:
                faffa2.write(f'User: \'{username}\' Faild to save next_max_id and big_list into the database in a request!!'+'\n')






def write_flr_to_db(flr_or_next):

    # 0 => False
    success = 0
    try:
        db = sqlite3.connect(db_name)
        cr = db.cursor()

        if type(flr_or_next) == list:
            flr_list_len=len(flr_or_next)

            track_req=flr_or_next[-1]


            insert_query='INSERT INTO track_flr (main_user, next_max_id, big_list, track_token) VALUES(?,?,?,?)'
            val=(track_req["main_user"], track_req["next_max_id"], track_req["big_list"], track_req["track_token"])
            cr.execute(insert_query, val)
            db.commit()

            #--------------------------------------------------------
            #', '.join([':' + prop for prop in _FOLLOWERS_PROPS2])
            #The same as:
            #placeholders = ':'+', :'.join(_FOLLOWERS_PROPS2)
            #-------------------------------------------------------

            flrs_column_names = 'main_user, next_max_id, track_token, '+', '.join(_FOLLOWERS_PROPS2)
            placeholders = ':'+', :'.join(_FOLLOWERS_PROPS2)

            #query = 'INSERT INTO followers VALUES ("%s", "%s", %s)' % (track_req["main_user"], track_req["next_max_id"], placeholders)

            query = 'INSERT INTO followers (%s) VALUES (:main_user, :next_max_id, :track_token, %s)' % (flrs_column_names, placeholders)


            #print(f'query => {query}')

            for i in range(flr_list_len - 1):
                flr_or_next[i]["link"] = f"https://instagram.com/{flr_or_next[i]['username']}/"
                flr_or_next[i]["main_user"] = track_req["main_user"]
                flr_or_next[i]["next_max_id"] = track_req["next_max_id"]
                flr_or_next[i]["track_token"] = track_req["track_token"]
                cr.execute(query, flr_or_next[i])

            db.commit()

        #type is dict=>track
        else:
            track_req=flr_or_next
            #track_req["main_user"], track_req["next_max_id"], track_req["big_list"]
            insert_query='INSERT INTO track_flr (main_user, next_max_id, big_list, track_token) VALUES(?,?,?,?)'

            val=(track_req["main_user"], track_req["next_max_id"], track_req["big_list"], track_req["track_token"])

            cr.execute(insert_query, val)
            db.commit()


    except Exception as e:
        print(f'Error occuredA: {type(e)}')

    except:
        print('Error occured in write_flr_to_db func!')

    else:
        #re-assign success to 1 in 'else', if there was no exception raised
        success = 1

    finally:
        cr.close()
        db.close()

    return success

def search_flw_next_id(username):
    try:
        db=sqlite3.connect(db_name)
        cr=db.cursor()

        res=cr.execute('SELECT * FROM track_flw where main_user = ? ORDER BY app_id DESC LIMIT 1', (username,)).fetchone()

        if res:
            next_max_id=res[2]
            track_token=res[4]

            if next_max_id == '' or next_max_id != 'end':
                cr.execute('DELETE FROM following where next_max_id = ? and main_user = ? and track_token = ?', (next_max_id, username, track_token))

                db.commit()
                cr.execute('DELETE FROM track_flw where next_max_id = ? and main_user = ? and track_token = ?', (next_max_id, username, track_token))
                db.commit()
                return next_max_id
            else:
                return 'end'

        else:
            return ''

    except Exception:
        print('Error search')
    except:
        print('Error searchA')

    finally:
        cr.close()
        db.close()

def get_following(user_info: dict):

    if "bad" in user_info:
        return 1

    if user_info['is_private']:
        print(f'>Username: \'{user_info["username"]}\' is private, cannot get their followings...')
        return 0

    session = MAIN_SESSION.copy()
    headers = session[1]
    cookies = session[2]
    
    username = user_info['username']
    headers['Referer'] = f'https://www.instagram.com/{username}/following'
    user_id = user_info['id']

    if not username or not user_id:
        raise ValueError('There is no username or user_id specifid')

    #print(username, user_id)

    #We should test the internet connection one time, before trying to get the next_max_id:
    #To make sure that we are not going to delete any records if there are no internet.
    test_req = requests.get("https://example.com")

    if test_req.status_code != 200:
        raise ValueError('There is no internet connection.')

    next_max_id=search_flw_next_id(username)

    print(f'next_max_id is: ~{next_max_id}~')
    if next_max_id == 'end':
        print(f'Followings already exist for user: {username}')
        print("#"*70)
        #cronjob_username in the top of the file.
        #it should be replaced with the last username that we want to scrape.
        #We don't need the following lines unless there is a cronjob for followers.
        
        # if username == CRONJOB_USERNAME:
        #     with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "followings_status.txt"), "w") as flws_file:
        #        flws_file.write("END")
        return

    big_list = True
    #next_max_id = ''
    req_start_time = 20
    #time_to_sleep = 1
    
    #time.sleep(2)
    print("Lol")
    while big_list:

        track_token=random_gen()

        following_data = list()
        #if (time.perf_counter() - req_start_time) < 10:
        #    raise ValueError('Time is less than 30sec')
        #print('after 15sec')

        #req_start_time = time.perf_counter()

        resp = requests.get(f'https://www.instagram.com/api/v1/friendships/{user_id}/following/?count=200&max_id={next_max_id}', headers=headers, cookies=cookies, timeout=20)

        if resp is not None and resp.status_code == 200:
            from_json_resp = resp.json()

            users=from_json_resp['users']

            # User has followers.
            if users:
            
                print("has_followings")
                users_list_len=len(users)

                for i in range(users_list_len):
                    following_data.append(users[i])


                following_data.append({'main_user': username, 'next_max_id': next_max_id, 'big_list': big_list, 'track_token': track_token})

                big_list = from_json_resp['big_list']
                if big_list:
                    next_max_id = from_json_resp['next_max_id']
                else:
                    next_max_id = 'end'

                    # if username == CRONJOB_USERNAME:
                    #     with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "followings_status.txt"), "w") as flws_file2:
                    #         flws_file2.write("END")

                    print(f"Followings have been fetched for user: '{username}'")
                    print("#"*70)

                # We need to store them into the database...
                if not write_flw_to_db(following_data):
                    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "flws.txt"), 'a') as faff:
                        faff.write(f'User: \'{username}\' Failed to save a response of followings into the database!!'+'\n')
                
                print("time to sleep 30sec")
                time.sleep(followings_requests_delay)

            # User has no followers.
            else:
                
                print(f'>Username: \'{username}\' has no followings...')
                break


        elif resp.status_code == 400:
            print(f"resp.status_code = {resp.status_code}")
            print(resp.text)
            sys.exit(1)

        else:
            print(f"resp.status_code = {resp.status_code}")
            print(resp.text)
            break

    else:
        track_token=random_gen()

        if not write_flw_to_db({'main_user': username,'next_max_id': next_max_id, 'big_list': big_list, 'track_token': track_token}):
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "flws.txt"), "a") as faff2:
                faff2.write(f'User: \'{username}\' Faild to save next_max_id and big_list into the database in a request!!'+'\n')


def random_gen():

    # Define your character set
    character_set = '0123456789abcdefghijklmnopqrstuv'

    # Set the length of the random string you want to generate
    string_length = 32  # Adjust as needed

    # Generate the random string
    random_string = ''.join(random.choice(character_set) for _ in range(string_length))

    return random_string


def write_flw_to_db(flw_or_next):

    # 0 => False
    success = 0
    try:
        db = sqlite3.connect(db_name)
        cr = db.cursor()

        if type(flw_or_next) == list:
            flw_list_len=len(flw_or_next)

            track_req=flw_or_next[-1]

            insert_query='INSERT INTO track_flw (main_user, next_max_id, big_list, track_token) VALUES(?,?,?,?)'

            val=(track_req["main_user"], track_req["next_max_id"], track_req["big_list"], track_req["track_token"])
            cr.execute(insert_query, val)
            db.commit()


            flws_column_names = 'main_user, next_max_id, track_token, '+', '.join(_FOLLOWERS_PROPS2)
            placeholders = ':'+', :'.join(_FOLLOWERS_PROPS2)

            query = 'INSERT INTO following (%s) VALUES (:main_user, :next_max_id, :track_token, %s)' % (flws_column_names, placeholders)

            #print(f'query => {query}')

            #Don't remove the "-1" here.
            for i in range(flw_list_len -1 ):
                flw_or_next[i]["link"] = f"https://instagram.com/{flw_or_next[i]['username']}/"
                flw_or_next[i]["main_user"] = track_req["main_user"]
                flw_or_next[i]["next_max_id"] = track_req["next_max_id"]
                flw_or_next[i]["track_token"] = track_req["track_token"]
                cr.execute(query, flw_or_next[i])

            db.commit()

        #type is dict=>track
        else:
            track_req=flw_or_next
            #track_req["main_user"], track_req["next_max_id"], track_req["big_list"]
            insert_query='INSERT INTO track_flw (main_user, next_max_id, big_list, track_token) VALUES(?,?,?,?)'

            val=(track_req["main_user"], track_req["next_max_id"], track_req["big_list"], track_req["track_token"])

            cr.execute(insert_query, val)
            db.commit()


    except Exception as e:
        print(f'Error occuredA: {type(e)}')

    except:
        print('Error occured in write_flw_to_db func!')

    else:
        #re-assign success to 1 in 'else', if there was no exception raised
        success = 1

    finally:
        cr.close()
        db.close()

    return success





class FollowersList:
    def __init__(self):
        pass

    def count(self):
        pass



class User:
    def __init__(self, username, file_name, file_format, no_save=False, followers=False, following=False):

        self.no_save = no_save
        self.username = validate_username(username)
        self.basic_info = get_user_info(self.username, self.no_save)
        self.file_format = file_format
        self.file_name = validate_file_name(file_name, self.file_format)
        if self.file_name:
            write_to_file(self.file_name, self.file_format, self.basic_info)

        self.followers = followers
        self.following = following

        if self.followers:
            get_followers(self.basic_info)

        if self.following:
            get_following(self.basic_info)



if __name__ == "__main__":
    main()

# user_data('alquran_99_')

#not_found
#user_data('zakariyae_ivar')

# info=user_data('ali_haiderofficial')

# for k,v in info.items():
#     print(f'{k} => {v}')



# user=User('@sa5ky_1')

# followers=user.followers()
# following=user.following()


# class Followers:
#     def __init__(self, main_user):
#         self.main_user=main_user
#         self.id = self.full_name = self.is_verified = self.is_private = self.link = self.has_anonymous_pic = self.profile_pic_url = None        
        
#     def count(self):
#         return 1070

# class Following:
#     def __init__(self, main_user):
#         self.main_user=main_user
#         self.id = self.full_name = self.is_verified = self.is_private = self.link = self.has_anonymous_pic = self.profile_pic_url = None

#     def count(self):
#         return 200
