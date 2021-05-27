import os
import shutil
import time
import re
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import FirefoxProfile
from constants import Constants


class FirefoxBrowserFactory:
    def __create_ff_profile(self):
        ff_profile = FirefoxProfile()
        ff_profile.set_preference('browser.download.folderList', 2)  # custom location
        ff_profile.set_preference('browser.download.dir', Constants.OUTPUT_DIR)
        ff_profile.set_preference('browser.download.manager.showWhenStarting', False)
        ff_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', "application/pdf")
        ff_profile.set_preference("pdfjs.disabled", True)
        return ff_profile

    def create_headless_browser(self):
        ff_profile = self.__create_ff_profile()
        opts = Options()
        opts.headless = True
        browser = Firefox(firefox_profile=ff_profile, options=opts)
        return browser

    def create_browser(self):
        ff_profile = self.__create_ff_profile()
        browser = Firefox(firefox_profile=ff_profile)
        return browser


class Astm:
    def __init__(self, browser):
        self.browser = browser
        self.main_page_url = "http://astm/"
        self.sub_directories = [
            # "A.htm",
            # "B.htm",
            # "C.htm",
            # "D.htm",
            # "E.htm",
            # "F.htm",
            "G.htm"
        ]

    def goto_subdirectories(self):
        for sub_dir in self.sub_directories:
            sub_direcrtory_url = "{}/{}".format(self.main_page_url, sub_dir)
            self.browser.get(sub_direcrtory_url)
            yield sub_dir.split(".")[0]

    def get_standard_links(self):
        links = self.browser.find_elements_by_class_name("bluenolinelinks")
        for link in links:
            if link.get_attribute("innerHTML").startswith("Standard"):
                yield link


class DownloadMngr:
    def __init__(self, browser):
        self.browser = browser

    def get_downloaded_file_name(self, wait_time):
        self.browser.execute_script("window.open()")
        self.browser.switch_to.window(self.browser.window_handles[-1])
        self.browser.get("about:downloads")

        end_time = time.time() + wait_time
        while True:
            try:
                file_name = self.browser.execute_script("return document.querySelector('#contentAreaDownloadsView \
                .downloadMainArea .downloadContainer description:nth-of-type(1)').value")
                if file_name:
                    self.browser.close()
                    self.browser.switch_to.window(self.browser.window_handles[0])
                    return file_name
            except Exception as e:
                print(str(e))

            time.sleep(1)
            if time.time() > end_time:
                return None


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    to_print = f'\r{prefix} |{bar}| ({iteration}/{total}) {percent}% {suffix}'
    print(to_print, end="", flush=True)
    # Print New Line on Complete
    if iteration == total:
        print()


def main():
    ff_factory = FirefoxBrowserFactory()
    browser = ff_factory.create_browser()
    dl_mngr = DownloadMngr(browser)
    astm = Astm(browser)
    for letter in astm.goto_subdirectories():
        astm_file_name_pairs = []
        # download all the PDF then save some data.
        print("Downloading PDFs in Group {}...".format(letter))
        for link in astm.get_standard_links():
            link.click()
            # time.sleep(3)
            # wait 10 seconds
            file_name = dl_mngr.get_downloaded_file_name(5)
            name_of_standard = "{}.pdf".format(link.get_attribute("innerHTML"))
            # remove invalid symbols to make a valid windows file name
            name_of_standard = re.sub(r"[\\/:*?\"<>|]", '', name_of_standard)
            if file_name and name_of_standard:
                astm_file_name_pairs.append({"old_file_name": file_name, "new_file_name": name_of_standard})

        total_pairs = len(astm_file_name_pairs)
        print_progress_bar(0, total_pairs,
                           prefix="Renaming PDFs in Group {}".format(letter),
                           suffix="Completed",
                           length=50)
        for i, file_name_pair in enumerate(astm_file_name_pairs):
            old_file_name = file_name_pair["old_file_name"]
            new_file_name = file_name_pair["new_file_name"]
            fp_old_file_name = os.path.join(Constants.OUTPUT_DIR, old_file_name)
            fp_new_file_name = os.path.join(Constants.OUTPUT_DIR, letter, new_file_name)

            if os.path.exists(fp_old_file_name):
                os.rename(fp_old_file_name, fp_new_file_name)
            print_progress_bar(i + 1, total_pairs,
                               prefix="Renaming PDFs in Group {}".format(letter),
                               suffix="Completed",
                               length=50)


if __name__ == "__main__":
    main()
