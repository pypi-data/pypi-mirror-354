# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest
from datetime import datetime

from fei_ws.clients.client import FEIEntrySystemClient
from fei_ws.clients.client import FEIEntrySystem3Client
from fei_ws.clients.errors import (
    FEIWSAuthException,
    FEIWSConfigException,
    FEIWSApiException,
)
from fei_ws.clients import FEIWSClient


class FEIWSClientTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import fei_ws.config as config

        config.FEI_WS_BASE_URL = "https://idata.fei.org/"
        cls.client = FEIWSClient(username="10199930", password="123456")

    def test_no_auth(self):
        with self.assertRaises(FEIWSConfigException) as exp:
            client = FEIWSClient(username="", password="")
        self.assertEqual(
            str(exp.exception), "Could not login: username and password are empty."
        )

    def test_invalid_credentials(self):
        with self.assertRaises(FEIWSAuthException) as exp:
            client = FEIWSClient(username="my", password="secret")
        self.assertEqual(str(exp.exception), "Could not login: PasswordNotMatch")

    def test_call_without_login(self):
        client = FEIWSClient(username="10199930", password="123456")
        client._ows_client.set_default_soapheaders({})
        with self.assertRaises(FEIWSApiException):
            result = client.find_athlete(fei_ids=[10000412])

    def test_fei_api_error(self):
        with self.assertRaises(FEIWSApiException) as exp:
            self.client.get_season_list(discipline_code="X")
        self.assertEqual(exp.exception.code, "InvalidDisciplineCode")

    def test_findAthlete_using_invalid_id(self):
        result = self.client.find_athlete(fei_ids=[999999])
        self.assertEqual(len(result), 0)

    def test_findAthlete_by_id(self):
        result = self.client.find_athlete(fei_ids=[10000412])
        self.assertEqual(result[0]["Firstname"], "Jeroen")
        self.assertEqual(result[0]["FamilyName"], "Dubbeldam")

    def test_findAthlete_by_id_normalize_off(self):
        self.client.normalize = False
        result = self.client.find_athlete(fei_ids=[10000412])
        self.assertEqual(result[0]["Firstname"], "Jeroen")
        self.assertEqual(result[0]["FamilyName"], "DUBBELDAM")
        self.client.normalize = True

    def test_findAthlete_by_name(self):
        result = self.client.find_athlete(first_name="Jeroen", family_name="Dubbeldam ")
        self.assertEqual(result[0]["Firstname"], "Jeroen")

    def test_get_version(self):
        result = self.client.get_version()
        self.assertEqual("2.253.0", result)

    def test_commonws_without_argument(self):
        self.client._common_data.clear()
        result = self.client.get_common_data("getVersion")
        self.assertEqual("2.253.0", result)

    def test_commonws_caching(self):
        self.client._common_data["getVersion"] = "cache_value"
        result = self.client.get_common_data("getVersion")
        self.assertEqual(result, "cache_value")

    def test_commonws_with_argument(self):
        result = self.client.get_common_data("getSeasonList", DisciplineCode="S")
        self.assertTrue(result)

    def test_findHorse_by_id(self):
        result = self.client.find_horse(fei_ids=["105IG70"])
        self.assertEqual("Farah", result[0]["BirthName"])

    def test_findHorse_by_id_normalize_off(self):
        self.client.normalize = False
        result = self.client.find_horse(fei_ids=["NED08021"])
        self.assertEqual(result[0]["BirthName"], "TOTILAS")
        self.client.normalize = True

    # def test_find_horse_trainer_by_horse_id(self):
    #     result = self.client.search_horse_trainers(person_fei_id=10180941)
    #     self.assertEqual(2, len(result))

    def test_findHorse_by_name(self):
        result = self.client.find_horse(name="TOTILAS")
        self.assertEqual(result[0]["BirthName"], "Totilas")

    def test_findEvent_by_id(self):
        result = self.client.find_event(id="2012_CI_0209")
        self.assertEqual(result[0].ShowID, "2012_CI_0209")

    def test_findEvent_by_venue_and_start(self):
        result = self.client.find_event(
            venue_name="Aachen", show_date_from=datetime(2013, 6, 25)
        )
        self.assertEqual(result[0].ShowID, "2013_CI_0051")

    def test_findOfficial_by_id(self):
        result = self.client.find_official(any_id="10050866")
        self.assertEqual("Braspenning", result[0].FamilyName)
        self.assertEqual("Harry", result[0].FirstName)

    def test_findOfficial_by_id_normalize_off(self):
        self.client.normalize = False
        result = self.client.find_official(any_id="10050866")
        self.assertEqual(result[0].FamilyName, "BRASPENNING")
        self.assertEqual(result[0].FirstName, "Harry")
        self.client.normalize = True

    def test_findOfficial_by_Name(self):
        result = self.client.find_official(any_name="Braspenning")
        joop = list(filter(lambda x: x.FirstName == "Harry", result))[0]
        self.assertEqual(joop.PersonFEIID, 10050866)

    def test_lookup_date_list_entries(self):
        result = self.client.get_lookup_date_list()
        self.assertEqual(27, len(result))

    def test_get_country_list(self):
        result = self.client.get_country_list()
        self.assertEqual(210, len(result))
        country = self.client._cs_factory.Country()
        country.ISONumeric = "999"
        country.ISOAlpha = "--"
        country.Code = "FEI"
        country.Label = "FEI Flag"
        self.assertIn(country, result)

    def test_get_discipline_list(self):
        result = self.client.get_dicipline_list()
        self.assertEqual(len(result), 9)
        discipline = self.client._cs_factory.Discipline()
        discipline.Code = "A"
        discipline.Label = "Driving"
        discipline.IsParaEquestrian = False
        self.assertIn(discipline, result)

    def test_get_issuing_body_list(self):
        result = self.client.get_issuing_body_list()
        self.assertEqual(590, len(result))

    def test_get_national_federation_list(self):
        result = self.client.get_national_federation_list()
        self.assertEqual(148, len(result))

    def test_get_horse_name_kind_change_list(self):
        result = self.client.get_horse_name_kind_change_list()
        self.assertEqual(len(result), 4)

    def test_get_document_type_list(self):
        result = self.client.get_document_type_list()
        self.assertEqual(18, len(result))

    def test_get_language_list(self):
        result = self.client.get_document_type_list()
        self.assertEqual(18, len(result))

    def test_get_category_list(self):
        result = self.client.get_category_list()
        self.assertEqual(49, len(result))

    def test_get_address_name_list(self):
        result = self.client.get_address_name_list()
        self.assertEqual(2, len(result))

    def test_get_horse_gender_list(self):
        result = self.client.get_horse_gender_list()
        self.assertEqual(2, len(result))

    def test_get_horse_fei_id_type_list(self):
        result = self.client.get_horse_fei_id_type_list()
        self.assertEqual(3, len(result))

    def test_get_person_gender_list(self):
        result = self.client.get_person_gender_list()
        self.assertEqual(2, len(result))

    def test_get_person_civility_list(self):
        result = self.client.get_person_civility_list()
        self.assertEqual(55, len(result))

    def test_get_official_function_list(self):
        result = self.client.get_official_function_list()
        self.assertEqual(10, len(result))

    def test_get_official_status_list(self):
        result = self.client.get_official_status_list()
        self.assertEqual(16, len(result))

    def test_get_message_type_list(self):
        """
        When this tests fails, the message types in errors.py need to be regenerated!
        """
        result = self.client.get_message_type_list()
        self.assertEqual(371, len(result))

    def test_get_additional_role_list(self):
        result = self.client.get_additional_role_list()
        self.assertEqual(37, len(result))

    def test_get_season_list(self):
        result = self.client.get_season_list()
        self.assertEqual(32, len(result))

    def test_get_league_list(self):
        result = self.client.get_league_list(season_code="2017/18")
        self.assertEqual(16, len(result))

    def test_name_normalization(self):
        self.assertEqual(
            "Jan Willem de Vriës", self.client._normalize_name("JAN WILLEM DE VRIËS")
        )
        self.assertEqual(
            "Angelina van't Klein Asdonk Z",
            self.client._normalize_name("ANGELINA VAN'T KLEIN ASDONK Z"),
        )
        self.assertEqual(
            "De van 't Klein Asdonk Z",
            self.client._normalize_name("DE VAN 'T KLEIN ASDONK Z"),
        )
        self.assertEqual(
            "Chesta Z SFN by SAP", self.client._normalize_name("CHESTA Z SFN BY SAP")
        )
        self.assertEqual(
            "S.A.R.L. Ecurie Rodriguez Debray",
            self.client._normalize_name("S.A.R.L. ECURIE RODRIGUEZ DEBRAY"),
        )
        self.assertEqual(
            "Gut Einhaus, LLC", self.client._normalize_name("GUT EINHAUS, LLC")
        )
        self.assertEqual(
            "100 Batosta LVIII",
            self.client._normalize_name("100 BATOSTA LVIII", roman_nummerals=True),
        )


class FEIEntrySystemV3TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import fei_ws.config as config

        config.FEI_ESV3_BASE_URL = "https://ies3-api.fei.org/"
        cls.client = FEIEntrySystem3Client(username="oc_ws", password="OC_WS")

    def test_no_auth(self):
        with self.assertRaises(FEIWSConfigException) as exp:
            client = FEIEntrySystem3Client(username="", password="")
        self.assertEqual(
            str(exp.exception), "Could not login: username and password are empty."
        )

    def test_invalid_credentials(self):
        with self.assertRaises(FEIWSAuthException) as exp:
            client = FEIEntrySystem3Client(username="my", password="secret")
        self.assertEqual(
            "('Could not login: PasswordNotMatch', 401)", str(exp.exception)
        )

    def test_set_session(self):
        auth_header = self.client._session.headers["Authorization"]
        response = self.client.set_session("10199930", "123456")
        self.assertEqual(200, response.status_code)
        new_header = self.client._session.headers["Authorization"]
        self.assertNotEqual(auth_header, new_header)

    def test_get_shows(self):
        self.client.set_session("10199930", "123456")
        data = self.client.get_shows(sort="-date_start", venue="aachen")
        self.assertTrue(data)

    def test_get_show_entries(self):
        self.client.set_session("10199930", "123456")
        data = self.client.get_show_entries("2022_CI_0001")
        self.assertTrue(data)

    def test_get_event_entries(self):
        self.client.set_session("10199930", "123456")
        data = self.client.get_event_entries("2022_CI_0001_S_S_01")
        self.assertTrue(data)

    def test_get_event_entries_xml(self):
        self.client.set_session("10199930", "123456")
        data = self.client.get_event_entries_file(
            "2022_CI_0001_S_S_01", format="xml", xml_extended="1"
        )
        self.assertTrue(data)

    def test_get_event_entries_detail(self):
        self.client.set_session("10199930", "123456")
        data = self.client.get_event_entries_detailed("2022_CI_0001_S_S_01")
        self.assertEqual(data["Generated"]["Software"], "FEI Entry System")
        self.assertEqual(data["Generated"]["SoftwareVersion"], "3.0")
        self.assertTrue(data["ShowEntries"]["Show"])
        self.assertTrue(len(data["ShowEntries"]["Events"]) == 1)

    def test_get_authorizations(self):
        self.client.set_session("10199930", "123456")
        data = self.client.get_authorizations()
        self.assertEqual(
            data,
            [
                "A-REJ-WA",
                "H-REJ-WA",
                "A-ACC-SU",
                "H-ACC-SU",
                "A-REJ-SU",
                "H-REJ-SU",
                "A-CRJ-SU",
                "H-CRJ-SU",
                "H-SUBST",
                "A-CRJ-WA",
                "H-CRJ-WA",
                "A-ACC-SU-N",
                "H-ACC-SU-N",
                "A-REJ-SU-N",
                "H-REJ-SU-N",
                "A-CRJ-SU-N",
                "H-CRJ-SU-N",
                "H-SUBST-N",
                "A-ACC-NOS",
                "A-REJ-NOS",
                "A-ACCEPT",
                "H-ACCEPT",
                "H-ACC-NOS",
                "H-REJ-NOS",
                "H-SWAP",
            ],
        )


class FEIEntrySystemTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = FEIEntrySystemClient()

    def test_get_event_entries_empty(self):
        data = self.client.get_event_entries("2019_CI_0139_S_S_01")
        self.assertEqual({}, data)

    def test_get_event_entries(self):
        data = self.client.get_event_entries("2019_CI_0139_D_S_02")
        self.assertTrue(data)
        self.assertEqual("FEI Entry System", data["Generated"]["Software"])
        self.assertEqual("1.0", data["Generated"]["SoftwareVersion"])
        self.assertEqual("2019_CI_0139", data["ShowEntries"]["Show"]["FEIID"])
        self.assertTrue(len(data["ShowEntries"]["Athletes"]) > 1)
        self.assertTrue(len(data["ShowEntries"]["Horses"]) > 1)
        self.assertTrue(
            "2019_CI_0139_D_S_02", data["ShowEntries"]["Events"][0]["FEIID"]
        )

    def test_get_show_entries(self):
        data = self.client.get_show_entries("2019_CI_0139")
        self.assertTrue(data)
        self.assertEqual("FEI Entry System", data["Generated"]["Software"])
        self.assertEqual("1.0", data["Generated"]["SoftwareVersion"])
        self.assertEqual("2019_CI_0139", data["ShowEntries"]["Show"]["FEIID"])
        self.assertTrue(len(data["ShowEntries"]["Athletes"]) > 1)
        self.assertTrue(len(data["ShowEntries"]["Horses"]) > 1)
        self.assertTrue(len(data["ShowEntries"]["Events"]) > 1)


if __name__ == "__main__":
    unittest.main()
