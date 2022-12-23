from seleniumwire import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from seleniumwire.utils import decode
import re
from time import sleep


class WebdriverFirefox(webdriver.Firefox):
    @staticmethod
    def recomended_conf(path_to_profile):
        """Returns the configured driver.
        Мaybe will be updated for better hiding from detection"""

        # need for pars https
        proxy = r'localhost:8080'
        # auto install actual version of geckodriver
        driver_path = GeckoDriverManager().install()

        service = FirefoxService(driver_path)
        service.start()

        options = Options()
        options.set_preference('profile', path_to_profile)
        options.add_argument(f'--proxy-server=%s{proxy}')

        options.headless = True

        return WebdriverFirefox(service=service, options=options)

    def find_all_elements(self, pattern: str) -> list:
        """
        The method receives a pattern of regular expression, and with the help of Seleniumwire Webdriver, 
        it checks for all the coincidences in all requests and response that were sent by the browser.\n
        """

        result = []

        for request in self.requests:

            # Check the requests
            re_request = request.__repr__()
            rec_result = re.findall(pattern, re_request)
            for res in rec_result:
                if res != [] and res not in result:
                    result.append(res)

            # Check the response
            if request.response:
                re_response = request.url + request.response.headers.__repr__() + \
                    request.response.__repr__()
                response_body = decode(request.response.body, request.response.headers.get(
                    'Content-Encoding', 'identity'))
                try:
                    response_body = response_body.decode("utf-8")
                    res_result = re.findall(
                        pattern, re_response) + re.findall(pattern, response_body)
                    for res in res_result:
                        if res != [] and res not in result:
                            result.append(res)
                except Exception as ex:
                    print(ex)
        return result


def main():
    # regex pattern
    regex_pattern = r""

    # pass to Firefox profile
    path_to_profile = r""

    # target link
    link = r""

    with WebdriverFirefox.recomended_conf(path_to_profile) as driver:
        driver.get(link)
        sleep(7)
        result = driver.find_all_elements(regex_pattern)
        print(result)

if __name__ == "__main__":
    main()
