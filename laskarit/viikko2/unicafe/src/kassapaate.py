class Kassapaate:
    def __init__(self):
        self.kassassa_rahaa = 100000
        self.edulliset = 0
        self.maukkaat = 0
        self.edullinen_hinta = 240
        self.maukas_hinta = 400

    def syo_edullisesti_kateisella(self, maksu):
        if maksu < self.edullinen_hinta:
            return maksu

        self.kassassa_rahaa += self.edullinen_hinta
        self.edulliset += 1
        return maksu - self.edullinen_hinta

    def syo_maukkaasti_kateisella(self, maksu):
        if maksu < self.maukas_hinta:
            return maksu

        self.kassassa_rahaa += self.maukas_hinta
        self.maukkaat += 1
        return maksu - self.maukas_hinta

    def syo_edullisesti_kortilla(self, kortti):
        if kortti.saldo < self.edullinen_hinta:
            return False

        kortti.ota_rahaa(self.edullinen_hinta)
        self.edulliset += 1
        return True

    def syo_maukkaasti_kortilla(self, kortti):
        if kortti.saldo < self.maukas_hinta:
            return False

        kortti.ota_rahaa(self.maukas_hinta)
        self.maukkaat += 1
        return True

    def lataa_rahaa_kortille(self, kortti, summa):
        if summa < 0:
            return

        kortti.lataa_rahaa(summa)
        self.kassassa_rahaa += summa
