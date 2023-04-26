# Skilltracker

> **ot-harjoitustyö** (this is a university software development course practise project)

This software allows the user to track their performance in an online shooter game _recoil control_. In many online
shooter games, the user can try to counteract the recoil by moving their mouse in a specific way.

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#downloads">Downloads</a></li>
    <li>
      <a href="#installation">Installation</a></li>
      <ul>
        <li><a href="#method-1-for-end-user-using-pipx">For end user using pipx</a></li>
        <li><a href="#method-2-for-end-user-using-pip">For end user using pip</a></li>
        <li><a href="#method-3-for-development-and-testing-using-poetry">For development and testing using poetry</a></li>
      </ul>
    <li>
      <a href="#documentation">Documentation</a>
      <ul>
        <li><a href="/dokumentaatio/vaatimusmaarittely.md">Software specification/requirements</a></li>
        <li><a href="/dokumentaatio/tuntikirjanpito.md">Timesheet</a></li>
        <li><a href="/dokumentaatio/changelog.md">Changelog</a></li>
      </ul>
    </li>
  </ol>
</details>

---

## Downloads

**Latest release available [here!](https://github.com/tomp2/ot-harjoitustyo/releases/tag/viikko5)**

## Installation

### Method 1: For end user using `pipx`:

1. Install [pipx](https://github.com/pypa/pipx). Pipx installs Python apps to nice isolated environments.
2. Install straight from GitHub using `pipx`
   ```bash
   pipx install git+https://github.com/tomp2/ot-harjoitustyo.git
   ```
3. Start the application from the command line
   ```bash
   skilltracker
   ```

### Method 2: For end user using `pip`

1. Create a virtual environment (optional but _very_ recommended!)
      ```bash
      python -m venv venv
      ```
2. Activate the virtual environment (if using one)

   | Platform           | Command |
   |:-------------------|:--------|
   | POSIX/bash         | `source venv/bin/activate` |
   | Windows/PowerShell | `venv\Scripts\Activate.ps1` |
3. Install from GitHub using `pip`
   ```bash
   pip install git+https://github.com/tomp2/ot-harjoitustyo.git
   ```
4. Start the application from the command line
   ```bash
   python -m skilltracker
   ```
   The virtual environment must be activated to launch with the above command.
   Activate the venv when using the app again later.

### Method 3: For development and testing using `poetry`
1. Install [poetry](https://python-poetry.org/)
2. Clone the repository
   ```bash
   git clone https://github.com/tomp2/ot-harjoitustyo
   ```
3. Navigate into the directory
    ```bash
    cd ot-harjoitustyo
    ```
4. Install dependencies
    ```bash
    poetry install
    ```
5. Start the application
    ```bash
    poetry run invoke start
    ```

_Oneliner:_
```bash
git clone https://github.com/tomp2/ot-harjoitustyo &&
  cd ot-harjoitustyo && poetry install && poetry run invoke start
```

## Documentation

- [Software specification/requirements](/dokumentaatio/vaatimusmaarittely.md)
- [Timesheet](/dokumentaatio/tuntikirjanpito.md)
- [Changelog](/dokumentaatio/changelog.md)
