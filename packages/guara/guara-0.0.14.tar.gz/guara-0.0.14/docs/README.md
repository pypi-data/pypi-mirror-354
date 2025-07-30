# Guará

[![PyPI Downloads](https://static.pepy.tech/badge/guara)](https://pepy.tech/projects/guara)

<img src=https://github.com/douglasdcm/guara/raw/main/docs/images/guara.jpg width="300" height="300" />

Photo by <a href="https://unsplash.com/@matcfelipe?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Mateus Campos Felipe</a> on <a href="https://unsplash.com/photos/red-flamingo-svdE4f0K4bs?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Unsplash</a>

---

## What is Guará?

Guará is a Python framework designed to simplify UI test automation. Inspired by design patterns like **Page Objects**, **App Actions**, and **Screenplay**, Guará focuses on **Page Transactions**—encapsulating user interactions (transactions) on web pages, such as Login, Logout, or Form Submissions. It’s not just a tool; it’s a programming pattern that can be adapted to any web driver, not just Selenium.

### Why Guará?
- **Simplicity**: Reduces repetitive code by encapsulating web interactions into reusable transactions.
- **Flexibility**: Works with any web driver, not limited to Selenium.
- **Clarity**: Makes test scripts more readable and maintainable.

---

## Quick Start

### Installation
Guará requires **Python 3.8+**. Install it via pip:
```shell
pip install guara
```

### Syntax
```python
Application.at(apage.DoSomething [,with_parameter=value, ...]).asserts(it.Matches, a_condition)
```

### Example in Action
```python
from selenium import webdriver
from pages import home, contact, info, setup
from guara.transaction import Application
from guara import it

def test_sample_web_page():
    # Initialize the Application with a driver
    app = Application(webdriver.Chrome())
    
    # Open the web application
    app.at(setup.OpenApp, url="https://anyhost.com/")
    
    # Change language to Portuguese and assert content
    app.at(home.ChangeToPortuguese).asserts(it.IsEqualTo, content_in_portuguese)

    # Navigate to Info page and assert text presence
    app.at(info.NavigateTo).asserts(it.Contains, "This project was born")

    # Close the web application
    app.at(setup.CloseApp)
```

### Behind the Scenes
The repetitive web driver code is encapsulated in a transaction class:
```python
from guara.transaction import AbstractTransaction

class ChangeToPortuguese(AbstractTransaction):
    def do(self, **kwargs):
        self._driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(3) > button:nth-child(1) > img").click()
        self._driver.find_element(By.CSS_SELECTOR, ".col-md-10").click()
        return self._driver.find_element(By.CSS_SELECTOR, "label:nth-child(1)").text
```

---

## Key Features

### 1. **Page Transactions**
- Encapsulates user actions into reusable transactions.
- Reduces boilerplate code and improves readability.

### 2. **Flexible Assertions**
- Use built-in assertions like `it.IsEqualTo`, `it.Contains`, and more to validate outcomes.

### 3. **Cross-Driver Compatibility**
- Works with Selenium and can be adapted to other web drivers.

### 4. **Asynchronous Execution**
- Supports asynchronous operations for modern web applications.

### 5. **ChatGPT Assistance**
- Leverage AI to generate or debug transactions.

---

### Demonstration
[![Watch the video](https://github.com/douglasdcm/guara/blob/main/docs/images/guara-demo.png?raw=true)](https://www.youtube.com/watch?v=r2pCN2jG7Nw)

### Examples
Explore practical examples in the [examples folder](https://github.com/douglasdcm/guara/tree/main/examples).

## Contributing

### How You Can Help
- **Star this project** on GitHub.
- **Share** it with your network.
- **Write** a blog post or tutorial about Guará.
- **Contribute code**: Check out the [good first issues](https://github.com/douglasdcm/guara/issues) and submit a pull request.

---

## Why the Name "Guará"?
Guará is the Tupi–Guarani name for the **Scarlet Ibis**, a vibrant bird native to South America. Just like the bird, Guará stands out for its simplicity and elegance in solving complex UI automation challenges.

---
## Used by

- [@cu-sanjay/cricket-score-scraper](https://github.com/cu-sanjay/cricket-score-scraper)
- [@theijhay/platform_automation](https://github.com/theijhay/platform_automation)
- [@srmorita/py-selenium-practices](https://github.com/srmorita/py-selenium-practices)
- [@douglasdcm/automacao_de_testes](https://github.com/douglasdcm/automacao_de_testes)
- [@chalakbilla/React-tutorials](https://github.com/chalakbilla/React-tutorials)
- [@chriskyfung/InstapaperScraper](https://github.com/chriskyfung/InstapaperScraper)


## Ready to Dive In?
Start automating with Guará today! Check out the tutorial and explore the [examples](https://github.com/douglasdcm/guara/tree/main/examples) to see how Guará can simplify your UI testing workflow.

---

**Guará**: Simplifying UI automation, one transaction at a time. 🚀
