# Tutorial
## Canonical implementation
This is the simplest implementation to warm up the framework. It uses the `OpenApp` and `CloseApp` transactions to open the web page of Google, to assert the title of the page is `Google` and to close the web application. More details about each component of the framework are explained in further sessions. First install Selenium with `pip install selenium`

```python
# test_guara.py

from selenium import webdriver
from guara import it
from guara.transaction import Application, AbstractTransaction


class OpenApp(AbstractTransaction):
    def do(
        self, url: str,
    ) -> str:
        self._driver.get(url)
        return self._driver.title


class CloseApp(AbstractTransaction):
    def do(self) -> None:
        self._driver.quit()


def test_canonical():
    google = Application(webdriver.Chrome())
    google.when(OpenApp, url="http://www.google.com",).asserts(it.IsEqualTo,"Google")
    google.then(CloseApp)
```

## Basic practical example

This is a basic search of the term "guara" on Google. To follow the steps create the files `home.py` and `test_tutorial.py` at the same folder.

```python
# home.py

from selenium.webdriver.common.by import By
from guara.transaction import AbstractTransaction


class Search(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)

    def do(self, text):
        # Sends the received text to the textbox in the UI
        self._driver.find_element(By.NAME, "q").send_keys(text)
        
        # Click the button to search
        self._driver.find_element(By.NAME, "btnK").click()
        
        # Waits the next page appears and returns the label of the first tab "All".
        # It will be used by assertions in the next sessions.  
        return self._driver.find_element(
            By.CSS_SELECTOR, ".Ap1Qsc > a:nth-child(1) > div:nth-child(1)"
        ).text
```
- `class Search`: is a concrete transaction. Notice that the name of the class is an action and not a noun as usually saw in OOP. It is intentional to make the statement in the test more natural.
- `def __init__`: is the same for all transactions. It passes the `driver` to the `AbstractTransaction`.
- `def do`: is the *ugly* implementation of the method. It uses the private attribute `self._driver` inherited from `AbstractTransaction` to call `find_element`, `send_keys`, `click` and `text` from Selenium Webdriver. Notice the parameter `text`. It is received from the automation via `kwargs`. More details in further sessions.

```python
# test_tutorial.py

import pytest

# Imports the module with the transactions of the Home page
import home

from selenium import webdriver

# Imports the Application to build and run the automation
from guara.transaction import Application

# Imports the module with the strategies to asset the result
from guara import it

@pytest.fixture
def google():
    # Instantiates the Application to run the automation
    google = Application(webdriver.Chrome())

    # Some interesting things happen here.
    # The framework is used to setup the web application.
    # The method `at` from `app` is the key point here as it
    # receives a transaction (AbstractTransaction) and its `kwargs`.
    # Internally `at` executes the `do` method of the transaction and
    # holds the result in the property `result` which is going to be
    # presented soon.
    # `OpenApp` is a concrete transaction.
    # The `url` is passed to the `at` method by `kwargs`.
    # The result returned by `at` is asserted by `asserts`
    # using the strategy `it.IsEqualTo`.
    google.at(
        OpenApp,
        url="http://www.google.com",
    ).asserts(it.IsEqualTo, "Google")
    yield google

    # Uses the concrete transaction `CloseApp` to close the web application
    google.at(CloseApp)


def test_google_search(google: Application):
    # With the `app` received from the fixture the similar things
    # explained previously in the fixture happens.
    # The transaction `home.Search` with the parameter `text`
    # is passed to `at` and the result is asserted by `asserts` with
    # the strategy `it.IsEqualTo`
    google.at(home.Search, text="guara").asserts(it.IsEqualTo, "All")

```
- `class Application`: is the runner of the automation. It receives the `driver` and passes it hand by hand to transactions.
- `def at`: receives the transaction created on `home.py` and its parameters. Notice the usage of the module name `home` to make the readability of the statement as plain English. The parameters are passed explicitly for the same purpose. So the `google.at(home.Search, text="guara")` is read `Google at home [page] search [for] text "guara"`. The terms `page` and `for` could be added to the implementation to make it more explicit, like `google.at(homePage.Search, for_text="guara")`. This is a decision the tester may make while developing the transactions. 
- `def asserts`: receives a strategy to compare the result against an expected value. Again, the focus on readability is kept. So, `asserts(it.IsEqualTo, "All")` can be read `asserts it is equal to 'All'`
- `it.IsEqualTo`: is one of the strategies to compare the actual and the expected result. Other example is the `it.Contains` which checks if the value is present in the page. Notice that the assertion is very simple: it validates just one value. The intention here is keep the framework simple, but robust. The tester is able to extend the strategies inheriting from `IAssertion`.

## Extending assertions
The strategies to assert the result can e extended by inheriting from `IAssertion` as following:

```python
# The code is the same of the previous session.
# The unnecessary details were not duplicated
# import IAssertion 
from guara.transaction import Application, IAssertion

# Implements a new assertion to check variations of the expected value
class IsEqualToVariationsOf(IAssertion):
    def __init__(self):
        super().__init__()

    def asserts(self, actual, expected):
        if actual.lower() == expected.lower():
            return True
        raises AssertionError

def test_google_search(setup_app):
    app = setup_app
    
    # The new assertion is used to check variations of 'All', like 'aLL' or 'ALL'
    app.at(home.Search, text="guara").asserts(IsEqualToVariationsOf, "All")

```

## Debugging

Errors in assertions are printed like this. Got the same example above. Notice the `actual` and `expected` values do not match.

```shell
_____________________________________________________________ test_google_search _____________________________________________________________

setup_app = <guara.transaction.Application object at 0x7f3c42bf6f90>

    def test_google_search(setup_app):
        app = setup_app
>       app.at(home.Search, text="guara").asserts(IsEqualToVariationsOf, "ALL")

test_tmp.py:30: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
venv/lib/python3.11/site-packages/guara/transaction.py:27: in asserts
    it().asserts(self._result, expected)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <test_tmp.IsEqualToVariationsOf object at 0x7f3c4349fc10>, actual = 'alls', expected = 'all'

    def asserts(self, actual, expected):
>       assert actual.lower() == expected.lower()
E       AssertionError: assert 'alls' == 'all'
E         
E         - alls
E         ?    -
E         + all

```

## Best practices
1. Add typing to `self._driver` in transactions to allow the autocomplete of IDEs
```python
class CloseBrowser(AbstractTransaction):
    def __init__(self, driver):
        self._driver : Chrome = driver
```
2. Add documentation of transactions in the class level describing all arguments and the returned value.
```python
class SaveFlightData(AbstractTransaction):
    """
    Saves flight data to a JSON file after filtering outdated data.

    Args:
        flights_data (list): The list of flight data to save.
        history_days (int): The number of days to retain in history.

    Returns:
        str: A message indicating the data was saved.
    """
    def do(self, flights_data, history_days):
        existing_data = read_json_file("flights_data.json", [])
        current_date = datetime.now().date()
```
3. Use the `app.result` attribute to return the result of the last transaction
```python
urls = app.at(GetURLs).result
for url in urls:
    print(url)
```
4. Use the `app.asserts` method directly to validate the result of the last transaction. Sometimes the user wants to get the result of the transaction to use it later.
```python
ids, data, has_more = app.at(GetArticleIDs, page=page).result
app.asserts(it.IsEqualTo, len(ids) > 0, True)  # Verify we got articles
```
5. Use the proper verb method of `app` to make the statements as natural speech
```python
app.at(home.OpenInfo, ...)
app.when(OpenInfo, ...).then(ChangeToEnglish, ...)
```
6. Use chained verb methods to build your statements in natural language
```python
app.at(home.OpenInfo, ...).then(ChangeToEnglish, ...).asserts(...)
app.when(OpenInfo, ...).then(ChangeToEnglish, ...).asserts(...)
app.at(home.OpenInfo, ...).at(info.ChangeToEnglish, ...).asserts(...)
```
7. Give good names to parameters of transactions to keep a smooth reading
```python
# do
app.at(home.Search, by_text="foo").at(home.CreateResource, with_name="bla")

# don't
app.at(home.Search, value="foo").at(home.CreateResource, value="bla")
```
8. (Required) Use named arguments of the transactions to keep the natural speech
```python
# do
app.at(home.Search, by_text="foo").at(home.CreateResource, named="bla")

# don't (the code will fail)
app.at(home.Search, "foo").at(home.CreateResource, "bla")
```
9. Use named arguments in the transaction's signature
```python
# recommended
class SaveFlightData(AbstractTransaction):
    def do(self, flights_data, history_days):
        existing_data = read_json_file(flights_data)
        current_date = timedelta(days=history_days)

# not recommended
class SaveFlightData(AbstractTransaction):
    def do(self, **kwargs):
        existing_data = read_json_file(kwargs.get(flights_data))
        current_date = timedelta(days=kwargs.get(history_days))
```

For a better readability of the code it is recommended to use a high-level tools instead of raw Selenium commands. In this [example](https://github.com/douglasdcm/guara/tree/main/examples/web_ui/selenium/browserist) there is the complete implementation of a test using [Browserist](https://github.com/jakob-bagterp/browserist). This is one of the transactions.

```python
from browserist import Browser
from guara.transaction import AbstractTransaction


class SubmitText(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._driver: Browser

    def do(self, text):
        TEXT = '//*[@id="input"]'
        BUTTON_TEST = '//*[@id="button"]'
        RESULT = '//*[@id="result"]'
        self._driver.input.value(TEXT, text)
        self._driver.click.button(BUTTON_TEST)
        return self._driver.get.text(RESULT)
```

Other interesting tool is [Helium](https://github.com/mherrmann/helium). More details in this [example](https://github.com/douglasdcm/guara/tree/main/examples/web_ui/selenium/helium). Here is a transaction implementation:

```
from helium import find_all, write, click, S, Text
from guara.transaction import AbstractTransaction


class SubmitText(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)

    def do(self, text):
        TEXT = '//*[@id="input"]'
        BUTTON_TEST = "button"
        text_field = find_all(S(TEXT))[0]
        write(text, text_field)
        click(find_all(S(BUTTON_TEST))[0])
        return Text("It works!").value
```

## Advanced
For more examples of implementations check the [examples](https://github.com/douglasdcm/guara/blob/main/examples) folder.
