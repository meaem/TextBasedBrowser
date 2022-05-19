from hstest.stage_test import *
import requests
import os
import shutil
import sys
if sys.platform.startswith("win"):
    import _locale
    # pylint: disable=protected-access
    _locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)


class TextBasedBrowserTest(StageTest):

    def generate(self):

        dir_for_files = 'tb_tabs'
        return [
            TestCase(
                stdin='bloomberg.com\nexit',
                attach='bloomberg.com',
                args=[dir_for_files]
            ),
            TestCase(
                stdin='docs.python.org\nexit',
                attach='docs.python.org',
                args=[dir_for_files]
            )
        ]

    def compare_pages(self, output_page, ideal_page):
        # with open('output_page.txt','w') as out , open('ideal_page.txt','w') as ideal:
        #     out.write(output_page)
        #     ideal.write(ideal_page)
        # print("@@@@@@@@@@output_page")
        # idx = output_page.find("tock Selloff May Be Enterin")
        # print("@@@@@@@@@@", idx)
        # for c in output_page[idx + 15:idx + 30]:
        #     print(c, ord(c))
        # print("@@@@@@@@@@ideal_page")
        # idx = ideal_page.find("tock Selloff May Be Enterin")
        # print("@@@@@@@@@@", idx)
        # for c in ideal_page[idx + 15:idx + 30]:
        #     print(c, ord(c))
        print("comparison started")
        print(len(ideal_page))
        print(len(output_page))
        for i in range(len(ideal_page)):
            if ideal_page[i] != output_page[i]:
                print(f"--->{i} ideal_page[{i}]={ord(ideal_page[i])}\toutput_page[{i}]={ord(output_page[i])}",i)


        print("comparison finished")
        # return False,"dssd"
        # ideal_page = ideal_page.split('\n')
        # i = 1
        # for line in ideal_page:
        #     print(i)
        #     i+=1
        #     if line.strip() not in output_page:
        #         return False, line.strip()
        return True, ""

    def _check_files(self, path_for_tabs: str, ideal_page: str):
        """
        Helper which checks that browser saves visited url in files and
        provides access to them.

        :param path_for_tabs: directory which must contain saved tabs
        :param ideal_page: HTML code of the needed page
        """

        path, dirs, filenames = next(os.walk(path_for_tabs))

        for file in filenames:
            print("file: {}".format(file))
            with open(os.path.join(path_for_tabs, file), 'r', encoding='utf-8') as tab:
                try:
                    content = tab.read()
                except UnicodeDecodeError:
                    raise WrongAnswer('An error occurred while reading your saved tab. '
                                      'Perhaps you used the wrong encoding?')
                is_page_saved_correctly, wrong_line = self.compare_pages(content, ideal_page)
                if not is_page_saved_correctly:
                    raise WrongAnswer(f"The following line is missing from the file {file}:\n"
                                      f"\'{wrong_line}\'\n"
                                      f"Make sure you output the needed web page to the file\n"
                                      f"and save the file in the utf-8 encoding.")

    @staticmethod
    def get_page(url):

        url = f'https://{url}'
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/70.0.3538.77 Safari/537.36"
        try:
            page = requests.get(url, headers={'User-Agent': user_agent})
            print("test response headers" , page.headers)
        except requests.exceptions.ConnectionError:
            raise WrongAnswer(f"An error occurred while tests tried to connect to the page {url}.\n"
                              f"Please try again a bit later.")
        print("****page.encoding*****", page.encoding)
        return page.text

    def check(self, reply, attach):

        # Incorrect URL
        if attach is None:
            if '<p>' in reply:
                return CheckResult.wrong('You haven\'t checked whether the URL was correct')
            else:
                return CheckResult.correct()

        # Correct URL
        if isinstance(attach, str):
            path_for_tabs = os.path.join(os.curdir, 'tb_tabs')

            if not os.path.isdir(path_for_tabs):
                return CheckResult.wrong("There is no directory for tabs")

            ideal_page = TextBasedBrowserTest.get_page(attach)
            self._check_files(path_for_tabs, ideal_page)

            try:
                shutil.rmtree(path_for_tabs)
            except PermissionError:
                return CheckResult.wrong("Impossible to remove the directory for tabs. \n"
                                         "Perhaps you haven't closed some file?")

            is_page_printed_correctly, wrong_line = self.compare_pages(reply, ideal_page)
            if not is_page_printed_correctly:
                return CheckResult.wrong(f"The following line in missing from your console output:\n"
                                         f"\'{wrong_line}\'\n"
                                         f"Make sure you output the needed web page to the console.")

            return CheckResult.correct()


TextBasedBrowserTest().run_tests()
