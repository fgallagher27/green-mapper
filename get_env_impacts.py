"""
This script cleans and formats data on the 
environmental impact (in terms of C02 emissions)
of different forms of public transport
"""

import os


class EnvImpacts():
    """
    A container for environmental impact of each transport mode.
    
    Attributes:
        co2 (dict): a dictionary containing gCO2e/passenger km by transport mode
    """

    def __init__(self):

        # these figures are gCO2e/passenger km
        self.co2 = {
            # assumption of 0
            # ignores calories from extra food required, CO2 from respiration etc
            'walking': 0,
            'cycle': 0, # some estimates of ~ 16 https://ourworldindata.org/travel-carbon-footprint

            # https://tfl.gov.uk/corporate/transparency/freedom-of-information/foi-request-detail?referenceId=FOI-1827-2223
            'tube': 40.5,
            'overground': 29.2,
            'dlr': 33.3,
            'bus': 98.6,

            # https://www.london.gov.uk/who-we-are/what-london-assembly-does/questions-mayor/find-an-answer/expansion-tram-services-2
            'tram': 40.5 * 0.46,
            
            # https://tfl.gov.uk/corporate/transparency/freedom-of-information/foi-request-detail?referenceId=FOI-1845-2223
            'elizabeth-line': 25.0,

            # https://www.nationalrail.co.uk/greener/
            'national-rail': 35.0,

            # No clear data source so proxies used
            'river-bus': 29.2, # use overground as proxy - electric motors
            'cablecar': 40.5 * 0.46, # use tram as proxy - electric cable power
        }
