import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti


class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.kassassa_rahaa_alussa = self.kassapaate.kassassa_rahaa
        self.edulliset_alussa = self.kassapaate.edulliset
        self.maukkaat_alussa = self.kassapaate.maukkaat

        self.maksukortti = Maksukortti(1000)
        self.saldo_alussa = self.maksukortti.saldo

        self.maukas_hinta = 400
        self.edullinen_hinta = 240

    def test_konstruktori_asettaa_rahan_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100_000)  # add assertion here

    def test_konstruktori_asettaa_maukkaat_oikein(self):
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_konstruktori_asettaa_edulliset_oikein(self):
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_kateismaksu_kasvattaa_kassaa(self):
        self.kassapaate.syo_edullisesti_kateisella(self.edullinen_hinta)
        odotettu_kassassa_rahaa = self.kassassa_rahaa_alussa + self.edullinen_hinta
        self.assertEqual(
            self.kassapaate.kassassa_rahaa,
            odotettu_kassassa_rahaa
        )

        self.kassapaate.syo_maukkaasti_kateisella(self.maukas_hinta)
        odotettu_kassassa_rahaa += self.maukas_hinta
        self.assertEqual(
            self.kassapaate.kassassa_rahaa,
            odotettu_kassassa_rahaa
        )

    def test_kateismaksu_kasvattaa_lounaiden_lukumaaria(self):
        self.kassapaate.syo_edullisesti_kateisella(self.edullinen_hinta)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.kassapaate.syo_edullisesti_kateisella(10000)
        self.assertEqual(self.kassapaate.edulliset, 2)

        self.kassapaate.syo_maukkaasti_kateisella(self.maukas_hinta)
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.kassapaate.syo_maukkaasti_kateisella(10000)
        self.assertEqual(self.kassapaate.maukkaat, 2)

    def test_kateismaksu_antaa_oikean_vaihtorahan(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(self.edullinen_hinta), 0)
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(1000), 1000 - self.edullinen_hinta)

        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(self.maukas_hinta), 0)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(1000), 1000 - self.maukas_hinta)

    def test_riittamaton_kateismaksu_hoidetaan_oikein(self):
        maksu = self.maukas_hinta - 1
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(maksu), maksu)
        self.assertEqual(self.kassapaate.kassassa_rahaa, self.kassassa_rahaa_alussa)
        self.assertEqual(self.kassapaate.edulliset, self.edulliset_alussa)
        self.assertEqual(self.kassapaate.maukkaat, self.maukkaat_alussa)

        maksu = self.edullinen_hinta - 1
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(maksu), maksu)
        self.assertEqual(self.kassapaate.kassassa_rahaa, self.kassassa_rahaa_alussa)
        self.assertEqual(self.kassapaate.edulliset, self.edulliset_alussa)
        self.assertEqual(self.kassapaate.maukkaat, self.maukkaat_alussa)

    def test_onnistunut_korttimaksu_veloittaa_kortilta_ja_viestii_onnistumisen(self):
        tulos_maksu_onnistui = self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo, self.saldo_alussa - self.edullinen_hinta)
        self.assertTrue(tulos_maksu_onnistui)
        saldo_nyt = self.maksukortti.saldo

        tulos_maksu_onnistui = self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo, saldo_nyt - self.maukas_hinta)
        self.assertTrue(tulos_maksu_onnistui)

    def test_korttimaksu_ei_kasvata_kassaa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, self.kassassa_rahaa_alussa)

        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, self.kassassa_rahaa_alussa)

    def test_korttimaksu_kasvattaa_lounaiden_lukumaaria(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 1)

        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_riittamaton_korttimaksu_hoidetaan_oikein(self):
        riittamaton_saldo = self.edullinen_hinta - 1
        riittamaton_kortti = Maksukortti(riittamaton_saldo)

        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(riittamaton_kortti), False)
        self.assertEqual(riittamaton_kortti.saldo, riittamaton_saldo)
        self.assertEqual(self.kassapaate.edulliset, self.edulliset_alussa)
        self.assertEqual(self.kassapaate.maukkaat, self.maukkaat_alussa)

        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(riittamaton_kortti), False)
        self.assertEqual(riittamaton_kortti.saldo, riittamaton_saldo)
        self.assertEqual(self.kassapaate.edulliset, self.edulliset_alussa)
        self.assertEqual(self.kassapaate.maukkaat, self.maukkaat_alussa)

    def test_kortin_lataus_muuttaa_kortin_saldoa(self):
        summa = 1500
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, summa),
        self.assertEqual(self.maksukortti.saldo, self.saldo_alussa + summa)

    def test_kortin_lataus_muuttaa_kassan_kokoa(self):
        summa = 1500
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, summa),
        self.assertEqual(self.kassapaate.kassassa_rahaa, self.kassassa_rahaa_alussa + summa)

    def test_kortille_ei_voi_ladata_negatiivista_summaa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa, self.kassassa_rahaa_alussa)
        self.assertEqual(self.maksukortti.saldo, self.saldo_alussa)


if __name__ == '__main__':
    unittest.main()
