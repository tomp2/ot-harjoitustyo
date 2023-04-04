 ```mermaid
 classDiagram
    Monopoli "1" o-- "2" Noppa
    Monopoli "1" o-- "2..8" Pelaaja
    Monopoli "1" o-- "1" Pelilauta
    class Monopoli {
        List~Noppa~ nopat
        List~Pelaaja~ pelaajat
        Pelilauta pelilauta
        Aloitusruutu aloitusruutu
        Vankila vankilaruutu
    }



    Noppa : heitä() int



    Pelaaja "1" o-- "1" Pelinappula
    Pelaaja : Pelinappula pelinappula
    Pelaaja: int saldo



    Pelinappula "1" o-- "1" Ruutu
    Pelinappula : Ruutu ruutu



    Pelilauta "1" *-- "40" Ruutu
    Pelilauta : List~Ruutu~  ruudut



    Ruutu "1" -- "1" Ruutu
    Ruutu : Ruutu seuraava_ruutu
    Ruutu : 
    
    Ruutu <|-- Aloitusruutu

    Vankila --|> Ruutu
    Vankila : List~Pelaaja~ vangit
    Vankila: vangitse(Pelaaja pelaaja)
    Vankila: vapauta(Pelaaja pelaaja)

    Sattuma --|> Ruutu
    Sattuma -- Kortti
    Sattuma : suoritaKortti(Kortti kortti)

    Yhteismaa --|> Ruutu
    Yhteismaa -- Kortti
    Yhteismaa : suoritaKortti(Kortti kortti)

    Asema --|> Ruutu

    Laitos--|> Ruutu

    Katu --|> Ruutu
    Katu : str nimi
    Katu : List~Rakennus~ rakennukset
    Katu "1" ..> "0..4" Talo
    Katu "1" ..> "0..1" Hotelli



    Talo <|-- Rakennus
    Hotelli <|-- Rakennus


    
    Kortti : toiminto()*
```
