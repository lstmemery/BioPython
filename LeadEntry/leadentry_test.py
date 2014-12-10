from __future__ import unicode_literals

__author__ = 'memery'

import leadentry
import unittest
import mock

class LeadEntryTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.url = 'http://www.mesenchymalcellnews.com/issue/volume-6-45-dec-2/'
        cls.soup = leadentry.make_soup(cls.url)
        cls.publication_titles = leadentry.parse_connexon(cls.soup)
        #with mock.patch('__builtin__.raw_input', return_value='25430711') as mocked:
        cls.pubmed_list = leadentry.look_up_titles(cls.publication_titles)
        cls.records = leadentry.fetch_from_pubmed(cls.pubmed_list)
        cls.record = cls.records[0]
        cls.institute = leadentry.split_institute(cls.record.get('AD'), 0)
        cls.inst_without_postal = leadentry.split_institute(cls.record.get('AD'), 4)

    def test_parse_connexon_proper_length(self):
        self.assertEqual(10, len(leadentry.parse_connexon(self.soup)))

    def test_urllib_connection(self):
        pass

    def test_get_pub_date(self):
        self.assertEqual('11/26/2014', leadentry.get_pub_date(self.record))

    def test_name_split(self):
        self.assertEqual(('Mendez', 'Julio'), leadentry.name_split('Mendez, Julio J'))

    def test_find_email_exists(self):
        self.assertEqual('laura.niklason@yale.edu', leadentry.find_email(self.record, 'Niklason'))

    def test_find_email_does_not_exist(self):
        self.assertEqual('', leadentry.find_email(self.record, 'Mendez'))

    def test_doi_success(self):
        self.assertEqual('http://dx.doi.org/10.1016/j.biomaterials.2014.11.011', leadentry.clean_doi(self.record))

    def test_split_institute(self):
        self.assertEqual('Department of Anesthesiology, Yale University, New Haven, CT 06520, USA; Department of '
                         'Biomedical Engineering, Yale University, New Haven, CT 06520, USA',
                         leadentry.split_institute(self.record.get('AD'), 0))

    def test_find_company(self):
        self.assertEqual('Yale University', leadentry.parse_institute(self.institute).get('Company'))

    def test_find_department(self):
        self.assertEqual('Department of Anesthesiology', leadentry.parse_institute(self.institute).get('Department'))

    def test_find_city(self):
        self.assertEqual('New Haven', leadentry.parse_institute(self.institute).get('City'))

    def test_find_state(self):
        self.assertEqual('CT', leadentry.parse_institute(self.institute).get('State'))

    def test_find_postal(self):
        self.assertEqual('06520', leadentry.parse_institute(self.institute).get('Postal'))

    def test_find_country(self):
        self.assertEqual('USA', leadentry.parse_institute(self.institute).get('Country'))

    def test_split_no_postal_state(self):
        self.assertEqual('CT', leadentry.parse_institute(self.inst_without_postal).get('State'))