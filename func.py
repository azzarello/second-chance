import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
from pprint import pprint
import string

# Dictionary of crimes that are not eligible for criminal procedure law sealing
# Source: https://www.nycourts.gov/FORMS/cpl_160.59_sealing_application/pdfs/CPL_160.59_Sealing_Application.pdf#page=5
ineligibleCrimes = {
    # Sex Offenses
    "130.20": "Sexual Misconduct",
    "130.25": "Rape 3rd Degree",
    "130.30": "Rape 2nd Degree",
    "130.35": "Rape 1st Degree",
    "130.40": "Criminal Sexual Act 3rd Degree",
    "130.45": "Criminal Sexual Act 2nd Degree",
    "130.50": "Criminal Sexual Act 1st Degree",
    "130.52": "Forcible Touching",
    "130.53": "Persistent Sexual Abuse",
    "130.55": "Sexual Abuse 3rd Degree",
    "130.60": "Sexual Abuse 2nd Degree",
    "130.65": "Sexual Abuse 1st Degree",
    "130.65-a": "Aggravated Sexual Abuse 4th degree",
    "130.66": "Aggravated Sexual Abuse 3rd Degree",
    "130.67": "Aggravated Sexual Abuse 2nd Degree",
    "130.70": "Aggravated Sexual Abuse 1st Degree",
    "130.75": "Course of Sexual Conduct Against a Child 1st Degree",
    "130.80": "Course of Sexual Conduct Against a Child 2nd Degree",
    "130.85": "Female Genital Mutilation",
    "130.90": "Facilitating a Sex Offense with a Controlled Substance",
    "130.95": "Predatory Sexual Assult",
    "130.96": "Predatory Sexual Assault Against a Child",
    "263.05": "Use of a Child in a Sexual Performance",
    "263.10": "Promoting an Obscene Sexual Performance by a Child",
    "263.11": "Possessing an Obscene Sexual Performance by a Child",
    "263.15": "Promoting a Sexual Performance by a Child",
    "263.16": "Possessing a Sexual Performance by a Child",
    "263.30": "Facilitating a Sexual Performance by a Child with a Controlled Substance or Alcohol",
    # Homicide Offenses
    "125.10": "Criminally Negligent Homicide",
    "125.11": "Aggravated Criminally Negligent Homicide",
    "125.12": "Vehicular Manslaughter 2nd Degree",
    "125.13": "Vehicular Manslaughter 1st Degree",
    "125.14": "Aggravated Vehicular Homicide",
    "125.15": "Manslaughter 2nd Degree",
    "125.20": "Manslaughter 1st Degree",
    "125.21": "Aggravated Manslaughter 2nd Degree",
    "125.22": "Aggravated Manslaughter 1st Degree",
    "125.25": "Murder 2nd Degree",
    "125.26": "Aggravated Murder",
    "125.27": "Murder 1st Degree",
    "125.40": "Abortion 2nd Degree",
    "125.45": "Abortion 1st Degree",
    "125.50": "Self-Abortion 2nd Degree",
    "125.55": "Self Abortion 1st Degree",
    "125.60": "Issuing Abortion Articles",
    # Class B Violent Felony Offenses
    "110/125.25": "Attempted Murder 2nd Degree",
    "110/135.25": "Attempted Kidnapping 1st Degree",
    "110/150.20": "Attempted Arson 1st Degree",
    "120.10": "Assault 1st Degree",
    "135.20": "Kidnapping 2nd Degree",
    "140.30": "Burglary 1st Degree",
    "150.15": "Arson 2nd Degree",
    "160.15": "Robbery 1st Degree",
    "230.34(5)(a)&(b)": "Sex Trafficking",
    "255.27": "Incest 1st Degree",
    "265.04": "Criminal Possession of a Weapon 1st Degree",
    "265.09": "Criminal Use of a Firearm 1st Degree",
    "265.13": "Criminal Sale of a Firearm 1st Degree",
    "120.11": "Aggravated Assault upon a Police Officer or a Peace Officer",
    "120.07": "Gang Assault 1st Degree",
    "215.17": "Intimidating a Victim or Witness 1st Degree",
    "490.35": "Hindering Prosecution of Terrorism 1st Degree",
    "490.40": "Criminal Possession of a Chemical Weapon or Biological Weapon 2nd Degree",
    "490.47": "Criminal Use of a Chemical Weapon or Biological Weapon 3rd Degree",
    # Class C Violent Felony Offenses (includes any attempts to commit any of the Class B felony offenses listed above)
    "120.08": "Assault on a Peace Officer, Police Officer, Fireman or Emergency Medical Services Professional",
    "120.09": "Assault on a Judge",
    "120.06": "Gang Assault 2nd Degree",
    "121.13": "Strangulation 1st Degree",
    "140.25": "Burglary 2nd Degree",
    "160.10": "Robbery 2nd Degree",
    "265.03": "Criminal Possession of a Weapon 2nd Degree",
    "265.08": "Criminal Use of a Firearm 2nd Degree",
    "265.12": "Criminal Sale of a Firearm 2nd Degree",
    "265.14": "Criminal Sale of a Firearm with the Aid of a Minor",
    "265.19": "Aggravated Criminal Possession of a Weapon",
    "490.15": "Soliciting or Providing Support for an Act of Terrorism 1st Degree",
    "490.30": "Hindering Prosecution of Terrorism 2nd Degree",
    "490.37": "Criminal Possession of a Chemical Weapon or Biological Weapon 3rd Degree",
    # Class D Violent Felony Offenses (any attempt to commit any of the Class C violent felony offenses listed above)
    "120.02": "Reckless Assault of a Child",
    "120.05": "Assault 2nd Degree",
    "120.18": "Menacing a Police Officer or Peace Officer",
    "120.60": "Stalking 1st Degree",
    "121.12": "Strangulation 2nd Degree",
    "130.30": "Rape 2nd Degree",
    "130.45": "Criminal Sexual Act 2nd Degree",
    "130.65": "Sexual Abuse 1st Degree",
    "130.80": "Course of Sexual Conduct Against a Child 2nd Degree",
    "130.66": "Aggravated Sexual Abuse 3rd Degree",
    "130.90": "Facilitating a Sex Offense with a Controlled Substance",
    "135.35(3)(a)&(b)": "Labor Trafficking",
    "265.11": "Criminal Sale of a Firearm 3rd Degree",
    "215.16": "Intimidating a Victim or Witness 2nd Degree",
    "490.10": "Soliciting or Providing Support for an Act of Terrorism 2nd Degree",
    "490.20": "Making a Terroristic Threat",
    "240.60": "Falsely Reporting an Incident 1st Degree",
    "240.62": "Placing a False Bomb or Hazardous Substance 1st Degree",
    "240.63": "Placing a False Bomb or Hazardous Substance in a Sports Stadium or Arena, Mass Transportation Facility or Enclosed Shopping Mall",
    "405.18": "Aggravated Unpermitted Use of Indoor Pyrotechnics 1st Degree",
    # Class E Violent Felony Offenses
    "130.53": "Persistent Sexual Abuse",
    "130.65a": "Aggravated Sexual Abuse 4th Degree",
    "240.55": "Falsely Reporting an Incident 2nd Degree",
    "240.61": "Placing a False Bomb or Hazardous Substance 2nd Degree",
    # Conspiracy Offenses
    "105.10": "Conspiracy 4th Degree",
    "105.13": "Conspiracy 3rd Degree",
    "105.15": "Conspiracy 2nd Degree",
    "105.17": "Conspiracy 1st Degree"
}

sexOffenderCrimes = {
    "130.20": "Sexual Misconduct",
    "130.25": "Rape 3rd Degree",
    "130.30": "Rape 2nd Degree",
    "130.35": "Rape 1st Degree",
    "130.40": "Criminal Sexual Act 3rd Degree",
    "130.45": "Criminal Sexual Act 2nd Degree",
    "130.50": "Criminal Sexual Act 1st Degree",
    "130.52": "Forcible Touching",
    "130.53": "Persistent Sexual Abuse",
    "130.55": "Sexual Abuse 3rd Degree",
    "130.60": "Sexual Abuse 2nd Degree",
    "130.65": "Sexual Abuse 1st Degree",
    "130.65-a": "Aggravated Sexual Abuse 4th degree",
    "130.66": "Aggravated Sexual Abuse 3rd Degree",
    "130.67": "Aggravated Sexual Abuse 2nd Degree",
    "130.70": "Aggravated Sexual Abuse 1st Degree",
    "130.75": "Course of Sexual Conduct Against a Child 1st Degree",
    "130.80": "Course of Sexual Conduct Against a Child 2nd Degree",
    "130.85": "Female Genital Mutilation",
    "130.90": "Facilitating a Sex Offense with a Controlled Substance",
    "130.95": "Predatory Sexual Assult",
    "130.96": "Predatory Sexual Assault Against a Child",
    "263.05": "Use of a Child in a Sexual Performance",
    "263.10": "Promoting an Obscene Sexual Performance by a Child",
    "263.11": "Possessing an Obscene Sexual Performance by a Child",
    "263.15": "Promoting a Sexual Performance by a Child",
    "263.16": "Possessing a Sexual Performance by a Child",
    "263.30": "Facilitating a Sexual Performance by a Child with a Controlled Substance or Alcohol"
}

charge_field = {
    'charge-dropdown': 'charge-type',
    'offense-description': 'offense-description',
    'pl-number': 'pl-number',
    'disposition-dropdown': 'disposition',
    'date-disposition': 'start-date',
    'sentence-completion': 'sentence-complete',
    'date-completion': 'end-date'
}


def generate_ny_counties():
    county_list = []
    with open('data/ny_counties.txt') as f:
        content = f.readlines()
        # print(content)
        county_list = [{'label': elem.strip(), 'value': elem.strip()}
                       for elem in content]
    return county_list


def generate_crime_entry(num):
    ret = []
    for i in range(1, int(num)+1):
        ret.append(crime_entry_div(i))
    return ret


def crime_entry_div(offense_no):
    return html.Div(children=[

        html.Br(),
        html.H5(children="Crime #"+str(offense_no)),


        html.P(children='What is the charge type?'),
        dcc.RadioItems(id=('charge-dropdown-' + str(offense_no)), options=[
            {'label': 'Misdemeanor', 'value': 'Misdemeanor'},
            {'label': 'Minor', 'value': 'Minor'},
            {'label': 'Felony', 'value': 'Felony'},
        ]),

        html.Br(),
        html.P(children='Any offense description?'),
        dcc.Input(
            type='text',
            value='',
            id='offense-description-' + str(offense_no)
        ),

        html.Br(),
        html.P(children='What is the PL number?'),
        dcc.Input(
            type='text',
            value='',
            id=('pl-number-' + str(offense_no)),
        ),

        html.Hr(),
        html.P(children='Disposition'),
        dcc.RadioItems(id=('disposition-dropdown-' + str(offense_no)), options=[
            {'label': 'Guilty', 'value': 'Guilty'},
            {'label': 'Not Guilty', 'value': 'Not Guilty'},
            {'label': 'Pending', 'value': 'Pending'},
        ],
            value='Guilty'
        ),

        html.Br(),
        html.P(children='What is the date of disposition?'),
        dcc.DatePickerSingle(
            id=('date-disposition-'+str(offense_no)),
            date=datetime(2010, 1, 1)
        ),



        html.Hr(),

        html.P(children='Have you completed your sentence?'),
        dcc.RadioItems(
            options=[
                {'label': 'Yes', 'value': 'YES'},
                {'label': 'No', 'value': 'NO'},
            ],
            value='YES',
            id=('sentence-completion-'+str(offense_no))
        ),

        html.Br(),
        html.P(children='What is the date of sentence completion?'),
        dcc.DatePickerSingle(
            id=('date-completion-'+str(offense_no)),
            date=datetime(2020, 1, 1)
        ),
        html.Hr(),
        
        ], className="four columns", style={"background-color":"white"})

# Eligible list index reference
# [0] DO YOU HAVE MORE THAN TWO (2) CRIMINAL CONVICTIONS (MISDEMEANOR OR FELONY)?
# [1] DO YOU HAVE MORE THAN ONE FELONY CONVICTION?
# [2] HAVE LESS THAN TEN YEARS PASSED SINCE YOUR LAST CRIMINAL CONVICTION?
# [3] ARE YOU REQUIRED TO REGISTER AS A SEX OFFENDER?
# [4] ARE YOU APPLYING TO SEAL AN INELIGIBLE OFFENSE?
# [5] DO YOU CURRENTLY HAVE AN OPEN CRIMINAL CASE?
# 0 is no; default is all 0
# 1 is yes


def expunge_eligibility(num_crimes, state, offense, sentence_completion, disposition, disp_date, county_state, end_date):
    eligible_list = [0, 0, 0, 0, 0, 0]
    # 1. Check to see if more than 2 criminal convictions
    if (num_crimes > 2):
        eligible_list[0] = 1
    # 2. Do you have more than one felony conviction
    felony = 0
    for case in offense:
        if case[0] == "Felony":
            felony += 1
    if felony > 1:
        eligible_list[1] = 1

    # 3. Check to see if less than ten years since last criminal conviction
    current_date = datetime.now()
    """ Make the date a date time object """
    # print(disp_date)
    for case in disp_date:
        print(case)
        ten_after_disp = datetime(
            case.year + 10, case.month, case.day)
        print(ten_after_disp)
        if(ten_after_disp >= current_date):
            eligible_list[2] = 1
            break

    # 4. Check if ineligible
    # 5. Check if registered as sex criminal
    for case in offense:
        # Found a non-eligible case for sealing
        # print (case_no)
        if case[2] in ineligibleCrimes:
            eligible_list[3] = 1
            # See if they are a sex offender
            if case[2] in sexOffenderCrimes:
                eligible_list[4] = 1

    # 6. Do you currently have a criminal case
    for case in disposition:
        if (case == "Pending"):
            eligible_list[5] = 1
            break
    eligible_condition = True
    for i in eligible_list:
        if i == 1:
            eligible_condition = False
            break
    return eligible_list, eligible_condition


def parse_charges(charges):
    parsed_charges = []
    num_crimes = len(charges)
    state = 'NY'
    offense = []
    sentence_completion = []
    disposition = []
    disp_date = []
    county_state = []
    end_date = []
    for i in range(len(charges)):
        parsed_charge = {}
        curr_charge = charges[i]
        try:
            curr_charge = curr_charge['props']['children']
        except Exception:
            pass
        for i in range(len(curr_charge)):
            value = curr_charge[i]
            props = value['props']
            try:
                key = charge_field.get(props['id'].rpartition('-')[0])
                if 'value' in props:
                    value = props['value']
                elif 'date' in props:
                    value = props['date']
                else:
                    value = ''
                if (value != ''):
                    parsed_charge[key] = value
            except Exception:
                pass
        parsed_charges.append(parsed_charge)
    pprint(parsed_charges)
    for el in parsed_charges:
        pprint(el)
        try:
            if 'charge-type' in el:
                charge_type = el['charge-type']
            else:
                charge_type = None
            if 'offense-description' in el:
                offense_description = el['offense-description']
            else:
                offense_description = None
            if 'pl-number' in el:
                pl_number = el['pl-number']
            else:
                pl_number = None
            offense_tuple = (charge_type, offense_description, pl_number)
        except Exception:
            pass
        try:
            offense.append(offense_tuple)
        except Exception:
            pass
        try:
            sentence_completion.append(el['sentence-completion'])
        except Exception:
            pass
        try:
            disposition.append(el['disposition'])
        except Exception:
            pass
        try:
            disp_date.append(datetime(el.get('start-date')))
        except Exception:
            pass
        try:
            end_date.append(el['end-date'])
        except Exception:
            pass
    print('disp date')
    print(disp_date)
    eligible_list, eligible = expunge_eligibility(
        num_crimes, state, offense, sentence_completion, disposition, disp_date, county_state, end_date)
    return eligible_list, eligible


def output_answers(eligible_list, eligible):
    ret = []
    print(eligible_list)
    for item in eligible_list:
        if item == 1:
            ret.append("√")
        else:
            ret.append("X")

    return_message = ""
    if (eligible):
        return_message = "CONGRATS! You can be free now!"
    else:
        return_message = "SORRY, you are not eligible for expungement."

    return ret[0], ret[1], ret[2], ret[3], ret[4], ret[5], return_message
