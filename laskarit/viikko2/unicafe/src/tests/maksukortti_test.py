import unittest
from maksukortti import Maksukortti


class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_kortin_saldo_on_alussa_oikein(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

    def test_kortin_saldo_kasvaa_ladattaessa(self):
        self.maksukortti.lataa_rahaa(100)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 11.00 euroa")
        self.maksukortti.lataa_rahaa(1234)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 23.34 euroa")

    def test_kortin_saldo_vahenee_jos_raha_riittaa(self):
        self.maksukortti.ota_rahaa(100)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 9.00 euroa")
        self.maksukortti.ota_rahaa(1)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 8.99 euroa")

    def test_kortin_saldo_ei_muutu_jos_rahaa_ei_riita(self):
        self.maksukortti.ota_rahaa(2000)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

    def test_metodi_ota_rahaa_palauttaa_true_kun_raha_riittaa(self):
        self.assertEqual(self.maksukortti.ota_rahaa(1000), True)

    def test_metodi_ota_rahaa_palauttaa_true_kun_raha_ei_riita(self):
        self.assertEqual(self.maksukortti.ota_rahaa(2000), False)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)
