from eme.entities import loadHandlers


class TestApp():

    def __init__(self, directory='testapp/'):
        super().__init__()
        self.tests = loadHandlers(self, "Test", directory)

    def run(self, testCase=None, testName=None):
        if testCase is None:
            for testCase in self.tests:
                self.runTestCase(testCase)
        else:
            self.runTestCase(testCase, testName)

    def runTestCase(self, testCase, testName=None):
        if not testName:
            for testName in dir(self.tests[testCase.title()]):
                if testName[:5] == 'test_':
                    self.runTest(testCase, testName[5:])
        else:
            self.runTest(testCase, testName)

    def runTest(self, testCase, testName):
        getattr(self.tests[testCase.title()], "test_" + testName)()
