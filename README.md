# Skilltracker _(ohjelmistotekniikan harjoitustyö)_

This software allows the user to track their performance in an online shooter game _recoil control_. In many online shooter games, the user can try to counteract the recoil by moving their mouse in a specific way.

## Documentation

- [Software specification/requirements](/dokumentaatio/vaatimusmaarittely.md)
- [Timesheet](/dokumentaatio/tuntikirjanpito.md)
- [Changelog](/dokumentaatio/changelog.md)

## Installation
### Method 1: For the end user
1. Install with `pip` straight from github
```bash
pip install --user git+https://github.com/tomp2/ot-harjoitustyo.git
```
2. Start the application 
```bash
python -m skilltracker
```
### Method 2: For development and testing
> Note: This method requires [poetry](https://python-poetry.org/)!
1. Clone the repository
```bash
git clone https://github.com/tomp2/ot-harjoitustyo
```
2. Navigate into the directory
```bash
cd ot-harjoitustyo
```
3. Install dependencies
```bash
poetry install
```
4. Start the application
```bash
poetry run invoke start
```
