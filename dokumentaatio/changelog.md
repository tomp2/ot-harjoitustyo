# Changelog

## Viikko 5

- Lisätty puuttuva kirjasto projektin metatiedoista
- Lisätty/korjattu projektin taskeja
- Saatu taskit toimimaan Windowsilla
- Jos sovelluksessa tapahtuu virhe, tulee käyttäjän ruudulle ilmoitus
- Importtien refaktorointia
- Uudelleennimetty muttujia noudattamaan yleisiä kätänteitä
- Erota Database luokasta käyttäjien lukuun/kirjoitukseen liittyvät metodit omaan
  `UserRepository` luokaan `user_repository.py` moduuliin
- Uusi ominaisuus: käyttäjä voi poistaa tilinsä
- Parannelty UI:n tekstejä
- Kirjoitettu testit `database.py` moduulille

## Viikko 6

- Refaktoroi kokonaan sovelluksen konfiguraatiokoodi pois toml:ista ->
  ympäristömuuttujiin ja oletusasetuksiin settings.py moduulissa
- Sovelluksen konfiguraation validointi Pydantic kirjastolla
- Sovelluksen asetuksia voi muuttaa ympäristömuuttujilla
- Lisätty Registry luokat luokille
    - `UserRepository` -> `UserRepositoryRegistry`
    - `Settings` -> `SettingRegistry`
