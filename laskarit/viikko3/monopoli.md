 ```mermaid
 classDiagram
 
    Pelinappula "1" --> "1" Ruutu
    class Pelinappula {
        Ruutu ruutu
    }


    class Noppa {
        heitä() int
    }


    Pelaaja "1" --> "1" Pelinappula
    class Pelaaja {
        Pelinappula pelinappula
    }


    Pelilauta "1" --> "40" Ruutu
    class Pelilauta {
        List~Ruutu~  ruudut
    }


    Ruutu "1" --> "1" Ruutu
    class Ruutu {
        Ruutu seuraava_ruutu
    }


    Monopoli "1" --> "2" Noppa
    Monopoli "1" --> "2..8" Pelaaja
    Monopoli "1" --> "1" Pelilauta
    class Monopoli {
        List~Noppa~ nopat
        List~Pelaaja~ pelaajat
        Pelilauta pelilauta
    }
    
```
