from src.base import logger
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger

# Common properties
GENDER = "male"
LANGUAGE = "en"
STREET = "Street-1"
BIRTHDAY = "13/08/1980"

# IL as default
IL_STATE = ""
IL_ZIP = "70100"
IL_COUNTRY = "IL"
IL_CITY = "Ashdod"
IL_PHONE_PREFIX = "+972"
IL_STATE_CODE = 398
IL_COUNTRY_CODE = 104


@automation_logger(logger)
def choose_customer_details(country_code, state_number):
    """
    This method is used to provide the customer with country and state data.
    4 scenarios are handled:
    1. Country code 1 - responding with default data (IL)
    2. Country code > 1, no state number - responding only with country data
    3. Country code > 1, state number provided - responding with all relevant country and state data
    4. Country code > 1, invalid state number provided - responding with default data (IL)

    :param country_code: used to select a country from the "countries" DB table
    :param state_number: used to select one of the states of the selected country, data taken from the "states" DB table
    :return: Dictionary that contains relevant country and state data.
    """
    default_details = {
            "STATE": "FL",
            "ZIP": "70100",
            "COUNTRY": "IL",
            "CITY": "Ashdod",
            "PHONE_PREFIX": "+972",
            "STATE_CODE": 398,
            "COUNTRY_CODE": 376
        }
    if country_code == 1:
        return default_details
    elif state_number:
        country_id = str(country_code)
        query = F"select country.id, country.numcode code, country.name, country.iso3, country.prefix, states.iso, " \
            F"states.id from country join states on states.parentCountry = country.id where country.id={country_id}"

        db_country_data = Instruments.run_mysql_query(query)

        try:
            state = db_country_data[state_number][5]
            zip_code = "32801"
            country = db_country_data[state_number][3]
            city = "Ramat-Gan"
            phone_prefix = F"+{db_country_data[state_number][4]}"
            state_code = db_country_data[state_number][6]
            country_code = db_country_data[state_number][1]

            return dict(STATE=state, ZIP=zip_code, COUNTRY=country, CITY=city, PHONE_PREFIX=phone_prefix,
                        STATE_CODE=state_code, COUNTRY_CODE=country_code)
        except Exception as e:
            logger.logger.exception(
                F"Country with code {country_code} doesn't have {state_number} states. Responding with default data", e)
            return default_details

    else:
        country_id = str(country_code)
        query = F"select country.id, country.numcode code, country.name, country.iso3, country.prefix from country " \
                F"where country.id = {country_id} "

        db_country_data = Instruments.run_mysql_query(query)

        state = None
        zip_code = "32801"
        country = db_country_data[0][3]
        city = "Ramat Gan"
        phone_prefix = F"+{db_country_data[0][4]}"
        state_code = None
        country_code = db_country_data[0][1]

        return dict(STATE=state, ZIP=zip_code, COUNTRY=country, CITY=city, PHONE_PREFIX=phone_prefix,
                    STATE_CODE=state_code, COUNTRY_CODE=country_code)
