import json
import os

import pandas as pd
import psycopg2
from tqdm import tqdm

# password = ""
# user = ""
# connection_string = "dbname=orcid user={u} password={p} host=10.3.1.14".format(u=user, p=password)
dictt = {'NaN': '',
         'Afghanistan': 'AF',
         'Albania': 'AL',
         'Algeria': 'DZ',
         'American Samoa': 'AS',
         'Andorra': 'AD',
         'Angola': 'AO',
         'Anguilla': 'AI',
         'Antarctica': 'AQ',
         'Antigua and Barbuda': 'AG',
         'Argentina': 'AR',
         'Armenia': 'AM',
         'Aruba': 'AW',
         'Australia': 'AU',
         'Austria': 'AT',
         'Azerbaijan': 'AZ',
         'Bahamas': 'BS',
         'Bahrain': 'BH',
         'Bangladesh': 'BD',
         'Barbados': 'BB',
         'Belarus': 'BY',
         'Belgium': 'BE',
         'Belize': 'BZ',
         'Benin': 'BJ',
         'Bermuda': 'BM',
         'Bhutan': 'BT',
         'Bolivia, Plurinational State of': 'BO',
         'Bonaire, Sint Eustatius and Saba': 'BQ',
         'Bosnia and Herzegovina': 'BA',
         'Botswana': 'BW',
         'Bouvet Island': 'BV',
         'Brazil': 'BR',
         'British Indian Ocean Territory': 'IO',
         'Brunei Darussalam': 'BN',
         'Bulgaria': 'BG',
         'Burkina Faso': 'BF',
         'Burundi': 'BI',
         'Cambodia': 'KH',
         'Cameroon': 'CM',
         'Canada': 'CA',
         'Cape Verde': 'CV',
         'Cayman Islands': 'KY',
         'Central African Republic': 'CF',
         'Chad': 'TD',
         'Chile': 'CL',
         'China': 'CN',
         'Christmas Island': 'CX',
         'Cocos (Keeling) Islands': 'CC',
         'Colombia': 'CO',
         'Comoros': 'KM',
         'Congo': 'CG',
         'Congo, the Democratic Republic of the': 'CD',
         'Cook Islands': 'CK',
         'Costa Rica': 'CR',
         'Croatia': 'HR',
         'Cuba': 'CU',
         'Curaçao': 'CW',
         'Cyprus': 'CY',
         'Czech Republic': 'CZ',
         "Côte d'Ivoire": 'CI',
         'Denmark': 'DK',
         'Djibouti': 'DJ',
         'Dominica': 'DM',
         'Dominican Republic': 'DO',
         'Ecuador': 'EC',
         'Egypt': 'EG',
         'El Salvador': 'SV',
         'Equatorial Guinea': 'GQ',
         'Eritrea': 'ER',
         'Estonia': 'EE',
         'Ethiopia': 'ET',
         'Falkland Islands (Malvinas)': 'FK',
         'Faroe Islands': 'FO',
         'Fiji': 'FJ',
         'Finland': 'FI',
         'France': 'FR',
         'French Guiana': 'GF',
         'French Polynesia': 'PF',
         'French Southern Territories': 'TF',
         'Gabon': 'GA',
         'Gambia': 'GM',
         'Georgia': 'GE',
         'Germany': 'DE',
         'Ghana': 'GH',
         'Gibraltar': 'GI',
         'Greece': 'GR',
         'Greenland': 'GL',
         'Grenada': 'GD',
         'Guadeloupe': 'GP',
         'Guam': 'GU',
         'Guatemala': 'GT',
         'Guernsey': 'GG',
         'Guinea': 'GN',
         'Guinea-Bissau': 'GW',
         'Guyana': 'GY',
         'Haiti': 'HT',
         'Heard Island and McDonald Islands': 'HM',
         'Holy See (Vatican City State)': 'VA',
         'Honduras': 'HN',
         'Hong Kong': 'HK',
         'Hungary': 'HU',
         'Iceland': 'IS',
         'India': 'IN',
         'Indonesia': 'ID',
         'Iran, Islamic Republic of': 'IR',
         'Iraq': 'IQ',
         'Ireland': 'IE',
         'Isle of Man': 'IM',
         'Israel': 'IL',
         'Italy': 'IT',
         'Jamaica': 'JM',
         'Japan': 'JP',
         'Jersey': 'JE',
         'Jordan': 'JO',
         'Kazakhstan': 'KZ',
         'Kenya': 'KE',
         'Kiribati': 'KI',
         "Korea, Democratic People's Republic of": 'KP',
         'Korea, Republic of': 'KR',
         'Kuwait': 'KW',
         'Kyrgyzstan': 'KG',
         "Lao People's Democratic Republic": 'LA',
         'Latvia': 'LV',
         'Lebanon': 'LB',
         'Lesotho': 'LS',
         'Liberia': 'LR',
         'Libya': 'LY',
         'Liechtenstein': 'LI',
         'Lithuania': 'LT',
         'Luxembourg': 'LU',
         'Macao': 'MO',
         'Macedonia, the former Yugoslav Republic of': 'MK',
         'Madagascar': 'MG',
         'Malawi': 'MW',
         'Malaysia': 'MY',
         'Maldives': 'MV',
         'Mali': 'ML',
         'Malta': 'MT',
         'Marshall Islands': 'MH',
         'Martinique': 'MQ',
         'Mauritania': 'MR',
         'Mauritius': 'MU',
         'Mayotte': 'YT',
         'Mexico': 'MX',
         'Micronesia, Federated States of': 'FM',
         'Moldova, Republic of': 'MD',
         'Monaco': 'MC',
         'Mongolia': 'MN',
         'Montenegro': 'ME',
         'Montserrat': 'MS',
         'Morocco': 'MA',
         'Mozambique': 'MZ',
         'Myanmar': 'MM',
         'Namibia': 'NA',
         'Nauru': 'NR',
         'Nepal': 'NP',
         'Netherlands': 'NL',
         'New Caledonia': 'NC',
         'New Zealand': 'NZ',
         'Nicaragua': 'NI',
         'Niger': 'NE',
         'Nigeria': 'NG',
         'Niue': 'NU',
         'Norfolk Island': 'NF',
         'Northern Mariana Islands': 'MP',
         'Norway': 'NO',
         'Oman': 'OM',
         'Pakistan': 'PK',
         'Palau': 'PW',
         'Palestine, State of': 'PS',
         'Panama': 'PA',
         'Papua New Guinea': 'PG',
         'Paraguay': 'PY',
         'Peru': 'PE',
         'Philippines': 'PH',
         'Pitcairn': 'PN',
         'Poland': 'PL',
         'Portugal': 'PT',
         'Puerto Rico': 'PR',
         'Qatar': 'QA',
         'Romania': 'RO',
         'Russian Federation': 'RU',
         'Rwanda': 'RW',
         'Réunion': 'RE',
         'Saint Barthélemy': 'BL',
         'Saint Helena, Ascension and Tristan da Cunha': 'SH',
         'Saint Kitts and Nevis': 'KN',
         'Saint Lucia': 'LC',
         'Saint Martin (French part)': 'MF',
         'Saint Pierre and Miquelon': 'PM',
         'Saint Vincent and the Grenadines': 'VC',
         'Samoa': 'WS',
         'San Marino': 'SM',
         'Sao Tome and Principe': 'ST',
         'Saudi Arabia': 'SA',
         'Senegal': 'SN',
         'Serbia': 'RS',
         'Seychelles': 'SC',
         'Sierra Leone': 'SL',
         'Singapore': 'SG',
         'Sint Maarten (Dutch part)': 'SX',
         'Slovakia': 'SK',
         'Slovenia': 'SI',
         'Solomon Islands': 'SB',
         'Somalia': 'SO',
         'South Africa': 'ZA',
         'South Georgia and the South Sandwich Islands': 'GS',
         'South Sudan': 'SS',
         'Spain': 'ES',
         'Sri Lanka': 'LK',
         'Sudan': 'SD',
         'Suriname': 'SR',
         'Svalbard and Jan Mayen': 'SJ',
         'Swaziland': 'SZ',
         'Sweden': 'SE',
         'Switzerland': 'CH',
         'Syrian Arab Republic': 'SY',
         'Taiwan': 'TW',
         'Tajikistan': 'TJ',
         'Tanzania': 'TZ',
         'Thailand': 'TH',
         'Timor-Leste': 'TL',
         'Togo': 'TG',
         'Tokelau': 'TK',
         'Tonga': 'TO',
         'Trinidad and Tobago': 'TT',
         'Tunisia': 'TN',
         'Turkey': 'TR',
         'Turkmenistan': 'TM',
         'Turks and Caicos Islands': 'TC',
         'Tuvalu': 'TV',
         'Uganda': 'UG',
         'Ukraine': 'UA',
         'United Arab Emirates': 'AE',
         'United Kingdom': 'GB',
         'United States': 'US',
         'United States Minor Outlying Islands': 'UM',
         'Uruguay': 'UY',
         'Uzbekistan': 'UZ',
         'Vanuatu': 'VU',
         'Venezuela, Bolivarian Republic of': 'VE',
         'Viet Nam': 'VN',
         'Virgin Islands, British': 'VG',
         'Virgin Islands, U.S.': 'VI',
         'Wallis and Futuna': 'WF',
         'Western Sahara': 'EH',
         'Yemen': 'YE',
         'Zambia': 'ZM',
         'Zimbabwe': 'ZW',
         'Åland Islands': 'AX'}


def records_allpersons(firstname, lastname):
    con = psycopg2.connect(user="confeval",
                        password="C0nfeval2022#",
                        host="10.3.1.14",
                        port="5432",
                        database="orcid")

    cur = con.cursor()
    query = f"select orcid  from record_name rn where Lower(unaccent(rn.family_name)) = Lower(unaccent('{lastname}'))  and Lower(unaccent(rn.given_names))= Lower(unaccent('{firstname}')) order by last_modified desc"
    cur.execute(query)
    records = cur.fetchall()
    return records


def filter_records_employment(temp, country):
    con = psycopg2.connect(user="confeval",
                        password="C0nfeval2022#",
                        host="10.3.1.14",
                        port="5432",
                        database="orcid")
    cur = con.cursor()
    query = f" select org_id,orcid,org.country,org.name from org_affiliation_relation oar inner join org on oar.org_id = org.id where org.id in (select org_id from org_affiliation_relation oar where orcid in {tuple([i[0] for i in temp])}) and oar.org_affiliation_relation_role  = 'employment' and org.country like '%{dictt.get(country, 'NaN')}%'"
    cur.execute(query)
    records = cur.fetchall()
    return records


def main():
    df = pd.read_csv('committee.csv')
    df = df[['person #', 'first name', 'last name', 'email', 'country']].drop_duplicates(subset='person #', keep='last')
    dict = {}
    for i, r in tqdm(df.iterrows()):
        # print(r['first name'].strip(),r['last name'].strip())
        temp = records_allpersons(r['first name'].strip(), r['last name'].strip())
        if len(temp) > 1:
            # temp = filter_records_email(temp)
            print('number of ambiguated id of ' + r['first name'].strip(), r['last name'].strip(), ' ' + str(len(temp)))
            temp2 = filter_records_employment(temp, r['country'])
            if len(temp2) > 0:
                dict[r['email']] = [i[1] for i in temp2]
                continue
        dict[r['email']] = temp
        # print(records_allpersons(r['first name'].strip(),r['last name'].strip()), sep='\n')

    with open("sample_other_possible.json", "w") as outfile:
        json.dump(dict, outfile)


if __name__ == "__main__":
    main()