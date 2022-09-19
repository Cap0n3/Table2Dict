import unittest
import os
import sys
import re
import inspect
from bs4 import BeautifulSoup
import requests
import json

# Go to parent folder to find modules (it's so stupid to have to do that ...)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

# Import class & functions
from BandAPI.BandWiki import BandWiki
from BandAPI.CustomPackage.ExtractTableMod import ExtractTable

#================#
#=== Settings ===#
#================#

PATH = os.path.dirname(os.path.realpath(__file__))

#===========================#
#=== Test Data reference ===#
#===========================#

BAND_LIST = ["Nirvana", "Queens of the stone age", "Knocked Loose", "Korn", "Mastodon", "Melvins", "Pearl jam", "Graveyard"]

TEST_MAIN_DICT = {
    'Origin': 'Aberdeen, Washington, U.S.', 
    'Genres': ['Grunge', 'alternative rock', 'punk rock', 'hard rock'], 
    'Years active': '1987–1994', 
    'Labels': ['Sub Pop', 'DGC'], 
    'Associated acts': ['Foo Fighters', 'Fecal Matter', 'Melvins', 'Scream', 'Sweet 75', 'Giants in the Trees'], 
    'Website': 'nirvana.com', 
    'Past members': ['Kurt Cobain', 'Krist Novoselic', 'Dave Grohl'], 
    'Discography': ['Bleach (1989)', 'Nevermind (1991)', 'In Utero (1993)']
}

TEST_DISCO_LIST = ['Bleach (1989)', 'Nevermind (1991)', 'In Utero (1993)']

#===========================#
#========= Testing =========#
#===========================#

@unittest.skip("Comment here to test")
class test_BandWiki(unittest.TestCase):
    # Setting Up
    def setUp(self):
        self.bandDataObj = BandWiki("Nirvana")
    
    def tearDown(self):
        self.bandDataObj = None
    
    # === Testing === #
    def test_getUlDiscography(self):
        html = requests.get("https://en.wikipedia.org/wiki/Nirvana_(band)").content
        self.testSoup = BeautifulSoup(html, "html.parser")
        resultList = self.bandDataObj.getUlDiscography(self.testSoup)
        self.assertListEqual(resultList, TEST_DISCO_LIST)

    def test_getAllInfos(self):
        resultDict = self.bandDataObj.getAllInfos()
        self.assertDictEqual(resultDict, TEST_MAIN_DICT)

    #@unittest.skip("To check dictionnaries, comment this line")
    def test_OutputDict(self):
        '''
        This test method is not regular, I just need it to test outputs for several
        bands dictionnaries (a sort of parametrization) but without the need of assert.

        If needed, it'll print all output dictionnaries in a file named 'dictToReview.txt' 
        to review later in order to check if resulting wikipedia scrap is clean or not.
        '''
        fileExists = os.path.exists(f"{PATH}/dictToReview.txt")
        if fileExists :
            os.remove(f"{PATH}/dictToReview.txt")
        
        for band in BAND_LIST:
            with open(f"{PATH}/dictToReview.txt", "a") as file:
                wikiObj = BandWiki(band).getAllInfos()
                prettyDict = json.dumps(wikiObj, indent=4, ensure_ascii=False)
                file.write(f"### (DICT START) ###\n\n")
                file.write(f"# ================= {band} ================= #\n\n")
                file.write(prettyDict)
                file.write(f"\n\n### (DICT END) ###\n\n")

class test_ExtractTable(unittest.TestCase):
    '''
    Test for prototypes methods in ExtractTable class.
    '''
    def setUp(self):
        # =========== INIT - HERE TO FINE TUNE TEST ============ #
        # Put to "ALL" to test all cases OR give case to test a particular file (ex : "case1" or "case5")
        self.testAllTableHeaders = "ALL"     # To test table headers
        self.testAllTableBodies = "ALL"     # To test table bodies
        self.testAllTables = "ALL"     # To test full tables
        # ====================================================== #
        # Get current folder
        self.dirname = os.path.dirname(__file__)
        # ============== ADD CUSTOM FOLDERS HERE =============== #
        # Set folder path to test table headers
        self.tableHeaderFilesFolder = os.path.join(self.dirname, "Test_Wiki_Table/Test_Table_Header")
        # Set folder path to test table body
        self.tableBodyFilesFolder = os.path.join(self.dirname, "Test_Wiki_Table/Test_Table_Body")
        # Set folder path to test full tables
        self.tablesFilesFolder = os.path.join(self.dirname, "Test_Wiki_Table/Test_Tables")
    
    # ======================================== #
    # ============ UTILITY METHODS =========== #
    # ======================================== #
    @staticmethod
    def sortFilesAndCases(targetDir, testCases):
        '''
        This utility method do several things (besides help staying DRY). 
        
        1. First, it puts files in given directory in a list and then adds full path to files. 
        For instance `tableHeader_case0.html` would become :
        ```txt
        /Users/kim0n0/myDev/1_PROJECTS/BandAPI_Project/Testing/Test_Wiki_Table/Test_Table_Header/tableHeader_case0.html
        ````
        2. Second, it sort files by case in created list and returns it.
        3. It creates another list containing all cases like this `['case0', 'case1', 'case3']` and returns it.

        Parameters
        ----------
        `targetDir` : `<class 'str'>`
            String representing target directory (where files to be sorted are)
        
        `testCases` : `<class 'dict'>`
            Dictionnary of cases (`{"case0" : [['Year'], ['Album'], ['Label'], ['Note']], etc...}`)
     
        Returns
        -------
        `tuple[list, list]`
            List of files sorted by cases and list of cases.
        '''
        # === Utility function === #
        def sortByCase(element):
            '''
            Utility function to sort files by case number in a list of files. First it'll isolate string case with a number beside like "case12" 
            in string "/Users/kim/BandAPI_Project/Testing/Test_Wiki_Table/Test_Table_Header/12_tableHeader_case12.html".
            
            Then it'll return only an int representing it's number, for "case12" it would be 12. Can be useful to then sort alist by key 
            thanks to `sort()` like this :
            
            ```python
            allFiles.sort(key=test_Functions.sortByCase)
            ```
            '''
            res = re.findall(r'case\d+', element)
            num = re.findall(r'\d+', res[0])
            return int(num[0])
        # ======================== #
        files = [f for f in sorted(os.listdir(targetDir))]
        # Add complete path for all file in list
        _allFiles = map(lambda file: os.path.join(targetDir, file), files)
        # Filter out folders from list
        filteredObj = filter(lambda file: os.path.isfile(file), _allFiles)
        _allFiles = list(filteredObj)
        # Sort files by case in list (they aren't sorted properly by sorted() above)
        _allFiles.sort(key=sortByCase)
        # Get keys (case number) in list
        _allCasesList = list(testCases.keys())

        return (_allFiles, _allCasesList)

    def oneOrAllCases(self, caseToTest, srcFolder, params, methodToUse):
        '''
        Utility method that gives the possibility of testing one OR all the cases in parameters for each testing methods. It'll assert 
        every cases or one particular case. This function was writtent to allow a DRYer code and more re-usability in different tests.

        > Note : If a new method in ExtractTable is created and have to be tested, don't forget to update the condition tree in returnResults()
        to include the new method.

        Parameters
        ----------
        `caseToTest` : `<class 'str'>`
            String representing case to test. Can be set to `ALL` or any particular case like `case0`, `case1`, etc ...
        
        `srcFolder` : `<class 'str'>`
            Absolute path of folder containing all tables to test.
        
        `params` : `<class 'dict'>`
            Dictonnary of results expected for tables (parametrization)

        `methodToUse` : `<class 'dict'>`
            Method to use for the testing (one of ExtractTable methods)
        '''

        # ======= UTILS METHODS ====== #
        def returnResults(_tableObj, _methodToUse):
            '''
            Function to select which method will be used for testing. It can be edited to include new methods if needed.
            > Note : Mostly created to stay DRY.

            Parameters
            ----------
            `_tableObj` : `<class 'ExtractTable'>`
                ExtractTable object
            
            `_methodToUse` : `<class 'str'>`
                Method to use for testing
            
            Returns
            -------
            `<class 'str'>`
                First portion of file name (before the underscore)
            '''
            # PLEASE UPDATE HERE IF NEW METHOD IS CREATED !
            if _methodToUse == "getTableHeader":
                res = _tableObj.getTableHeader()
            elif _methodToUse == "getTableBody":
                res = _tableObj.getTableBody()
            elif _methodToUse == "getTableList":
                res = _tableObj.getTableList()
            elif _methodToUse == "getTableDict":
                res = _tableObj.getTableDict()
            else:
                raise AttributeError("Method not recognized ! Please verify entered method or update condition in testOneOrAllCases() to include a new method !")
            return res

        def extractFilename(pathStr):
            '''
            Utility function to dynamically get the beginning of file name from an absolute path.
            For instance, if we pass this string to function : `/Users/kim/myDev/Testing/Test_Wiki_Table/Test_Tables/debugTable_case0.html`
            It would only return `debugTable`.
 
            Parameters
            ----------
            `pathStr` : `<class 'str'>`
                String representing absolute path.

            Returns
            -------
            `<class 'str'>`
                First portion of file name (before the underscore)
            '''
            # Split last portion of path
            fileName = pathStr.split("/")[-1]
            # Extract matching part and position in string
            pattern = r'_case\d\.html'
            match = re.search(pattern, fileName)
            # Return only first part of file name
            return fileName[:match.start()]

        allFiles, allCasesList = test_ExtractTable.sortFilesAndCases(srcFolder, params)
        # CHOICE A) Test ALL header tables
        if caseToTest == "ALL":
            for file, case in zip(allFiles, params):
                with self.subTest(msg=f"ERROR ! An error occured with test '{case}'", case_table=params[case], tested_file=file):
                    # Print tested case to console
                    print(f"TESTING '{case}' with file '{file}'")
                    # Open file in read mode
                    with open(file, 'r') as htmlTestFile:
                        soup = BeautifulSoup(htmlTestFile, "html.parser")
                    # Extract table from soup
                    table = soup.find('table')
                    # Create object for test
                    tableObj = ExtractTable(table)
                    # === Test object === #
                    result = returnResults(tableObj, methodToUse)
                    self.assertEqual(result, params[case])
        # CHOICE B) Test a particular case
        elif caseToTest in allCasesList:
            # Give any file path in allFiles to get first part of file name
            fileNamePart = extractFilename(allFiles[0])
            filename = os.path.join(self.dirname, f'{srcFolder}/{fileNamePart}_{caseToTest}.html')
            with open(filename, 'r') as htmlTestFile:
                soup = BeautifulSoup(htmlTestFile, "html.parser")
            # Print tested case to console
            print(f"TESTING '{caseToTest}' with file '{filename}'")
            # Extract table from soup
            table = soup.find('table')
            # Test function
            tableObj = ExtractTable(table)
            result = returnResults(tableObj, methodToUse)
            self.assertEqual(result, params[caseToTest])
        else:
            raise AttributeError(f"{caseToTest} is not a valid choice. Choose 'ALL' or one of the following :\n{allCasesList}")
    
    # ================================= #
    # ============ TESTING ============ #
    # ================================= #
    
    @unittest.SkipTest
    def test_getTableHeader(self):
        # ========= PARAMS ========= # 
        # Test cases (expected results), all files in Test_Table_Header folder should be here !
        testTableHeaders = {
            "case0" : [['Year'], ['Album'], ['Label'], ['Note']],
            "case1" : [['Year', 'Year'], ['Album', 'Album'], ['Label', 'Label'], ['Note', 'About']],
            "case2" : [['Year', 'Year'], ['Album', 'Release'], ['Label', 'Label'], ['Note', 'About']],
            "case3" : [['Album', 'Release'], ['Year', 'Year'], ['Label', 'Label'], ['Note', 'About']],
            "case4" : [['Year', 'Year', 'Period'], ['Album', 'Album', 'Release'], ['Label', 'Label', 'Label'], ['Note', 'About', 'Facts']],
            "case5" : [['Year', 'Year', 'Period'], ['Album', 'Release', 'Record'], ['Label', 'Label', 'Company'], ['Note', 'About', 'Facts']],
            "case6" : [['Album', 'Album'], ['Details', 'Details'], ['Charts', 'USA'], ['Charts', 'EU'], ['Certifications', 'Certifications']],
            "case7" : [['Album', 'Release'], ['Details', 'Details'], ['Charts', 'USA'], ['Charts', 'EU'], ['Certifications', 'Awards']],
            "case8" : [['Album', 'Release', 'CD'], ['Details', 'Details', 'Details'], ['Charts', 'USA', 'USA'], ['Charts', 'EU', 'Germany'], ['Certifications', 'Awards', 'Awards']],
            "case9" : [['Album', 'Release', 'CD'], ['Details', 'Details', 'Details'], ['Charts', 'Charts', 'USA'], ['Charts', 'Charts', 'EU'], ['Certifications', 'Awards', 'Awards']],
            "case10" : [['Album', 'Release'], ['Details', 'Details'], ['CD Sales', 'EU'], ['Vinyl Sales', 'EU'], ['Certifications', 'Awards']],
            "case11" : [['Album', 'Album', 'Album'], ['Details', 'Details', 'Infos'], ['CD Sales', 'EU', 'SKU1'], ['Vinyl Sales', 'EU', 'SKU2'], ['Certifications', 'Awards', 'Awards']],
            "case12" : [['Album', 'Album', 'Album'], ['Details', 'Details', 'Infos'], ['CD Sales', 'EU', 'EU'], ['Vinyl Sales', 'EU', 'EU'], ['Certifications', 'Awards', 'Rewards']],
        }
        # ========= TEST ========== #
        self.oneOrAllCases(self.testAllTableHeaders, self.tableHeaderFilesFolder, testTableHeaders, "getTableHeader")

    @unittest.SkipTest
    def test_getTableBody(self):
        # ========= PARAMS ========= # 
        # Test cases (expected results), all files in Test_Table_Body folder should be here !
        testTableBody = {
            "case0" : [['1991', '1992', '1993'], ['Bullhead', 'Eggog', 'Houdini'], ['Whatever Records', 'Boner Record', 'Atlantic Records']],
            "case1" : [['1991', '1991', '1992'], ['Bullhead', 'Eggog', 'Houdini'], ['Whatever Records', 'Boner Record', 'Atlantic Records']],
            "case2" : [['1991', '1991', '1991'], ['Bullhead', 'Eggog', 'Lysol'], ['Whatever Records', 'Whatever Records', 'Atlantic Records']],
            "case3" : [['1991', '1991', '1992'], ['Bullhead', 'Eggog', 'Lysol'], ['Whatever Records', 'Boner Record', 'Boner Record']],
            "case4" : [['1991', '1992', '1992'], ['Bullhead', 'Bullhead', 'Lysol'], ['Whatever Records', 'Boner Record', 'Atlantic Records']],
            "case5" : [['1991', '1992', '1992'], ['Bullhead', 'Bullhead', 'Lysol'], ['Whatever Records', 'Whatever Records', 'Whatever Records']],
        }
        # ========= TEST ========== #
        self.oneOrAllCases(self.testAllTableBodies, self.tableBodyFilesFolder, testTableBody, "getTableBody")

    @unittest.SkipTest
    def test_getTableList(self):
        testTables = {
            "case0" : [['Year', '1990', '1991', '1992'], ['Album', 'Bullhead', 'Eggog', 'Lysol'], ['Label', 'Whatever Records', 'Boner Record', 'Atlantic Records']],
            "case1" : [['Year', '1991', '1991', '1992'], ['Album', 'Bullhead', 'Eggog', 'Lysol'], ['Label', 'Boner Record', 'Phyllis Record', 'Atlantic Records']],
            "case2" : [['Year', '1991', '1991', '1992'], ['Album', 'Bullhead', 'Eggog', 'Lysol'], ['Label', 'Boner Record', 'Boner Record', 'Atlantic Records']],
            "case3" : [['Year', '1991', '1991', '1992'], ['Album', 'Bullhead', 'Eggog', 'Lysol'], ['Label', 'Boner Record', 'Boner Record', 'Atlantic Records'], ['Note', '2.3', '3.5', '5']],
            "case4" : [['Year', '1991', '1991', '1992'], ['Album', 'Bullhead', 'Eggog', 'Lysol'], ['Label', 'Boner Record', 'Boner Record', 'Atlantic Records'], ['Note', '2.3', '3.5', '3.5']],
            "case5" : [['Year', 'Year', '1991', '1991', '1992'], ['Album', 'Album', 'Bullhead', 'Eggog', 'Lysol'], ['Label', 'Label', 'Boner Record', 'Boner Record', 'Atlantic Records'], ['Note', 'Sku', '2.3', '3.5', '3.5']],
            "case6" : [['Year', 'Year', 'Year', '1991', '1991', '1992'], ['Album', 'Sku1', 'Sku3', 'Bullhead', 'Eggog', 'Lysol'], ['Label', 'Label', 'Label', 'Boner Record', 'Boner Record', 'Atlantic Records'], ['Note', 'Sku2', 'Sku4', '2.3', '3.5', '3.5']],
            "case7" : [['Title', 'Title', 'Down Below', 'This Is Not the Way Home', 'The Honeymoon is Over', 'Three Legged Dog', 'Over Easy', "Where There's Smoke"], ['Year', 'Year', '1990', '1991', '1993', '1995', '1998', '2001'], ['Peak chart positions', 'AUS', '133', '62', '4', '1', '13', '25'], ['Peak chart positions', 'NZ', '-', '-', '33', '20', '-', '-'], ['Label', 'Label', 'Red Eye Records', 'Red Eye Records', 'Red Eye Records', 'Red Eye Records', 'Polydor Records', 'Polydor Records']],            
            "case8" : [['Title', 'Name', 'Down Below', 'This Is Not the Way Home', 'The Honeymoon is Over', 'Three Legged Dog', 'Over Easy', "Where There's Smoke"], ['Year', 'Year', '1990', '1991', '1993', '1995', '1998', '2001'], ['Peak chart positions', 'AUS', '133', '62', '4', '1', '13', '25'], ['Peak chart positions', 'NZ', '-', '-', '33', '20', '-', '-'], ['Label', 'Company', 'Red Eye Records', 'Red Eye Records', 'Red Eye Records', 'Red Eye Records', 'Polydor Records', 'Polydor Records']],            
            "case9" : [['Title', 'Title', 'Down Below', 'This Is Not the Way Home', 'The Honeymoon is Over', 'Three Legged Dog', 'Over Easy', "Where There's Smoke"], ['Year', 'Year', '1990', '1991', '1993', '1995', '1998', '2001'], ['Peak chart positions', 'AUS', '133', '62', '4', '1', '13', '25'], ['Peak chart positions', 'NZ', '-', '-', '33', '20', '-', '-'], ['Label', 'Label', 'Red Eye Records', 'Red Eye Records', 'Red Eye Records', 'Red Eye Records', 'Polydor Records', 'Polydor Records']],            
            "case10" : [['Title', 'Title', 'Down Below', 'This Is Not the Way Home', 'The Honeymoon is Over', 'Three Legged Dog', 'Over Easy', "Where There's Smoke"], ['Album details', 'Album details', 'Released: 3 December 1990Formats: CD, LPLabel: Records', 'Released: 28 October 1991Formats: CD, LPLabel: Red Eye Records', 'Released: 31 May 1993Formats: CD, LP, CassetteLabel: Red Eye Records', 'Released: April 1995Formats: CD, LP, CassetteLabel: Red Eye Records', 'Released: July 1998Formats: CDLabel: Polydor Records', 'Released: September 2001Formats: CDLabel: Polydor Records'], ['Peak chart positions', 'AUS', '133', '62', '4', '1', '13', '25'], ['Peak chart positions', 'NZ', '-', '-', '33', '20', '-', '-'], ['Certifications', 'Certifications', '', 'AUS: Platinum', 'AUS: 3× Platinum', 'AUS: Platinum', '', '']],            
        }
        # ========= TEST ========== #
        self.oneOrAllCases(self.testAllTables, self.tablesFilesFolder, testTables, "getTableList")

    #@unittest.SkipTest
    def test_getTableDict(self):
        testTables = {
            "case0" : {'Year': ['1990', '1991', '1992'], 'Album': ['Bullhead', 'Eggog', 'Lysol'], 'Label': ['Whatever Records', 'Boner Record', 'Atlantic Records']},
            "case1" : {'Year': ['1991', '1991', '1992'], 'Album': ['Bullhead', 'Eggog', 'Lysol'], 'Label': ['Boner Record', 'Phyllis Record', 'Atlantic Records']},
            "case2" : {'Year': ['1991', '1991', '1992'], 'Album': ['Bullhead', 'Eggog', 'Lysol'], 'Label': ['Boner Record', 'Boner Record', 'Atlantic Records']},
            "case3" : {'Year': ['1991', '1991', '1992'], 'Album': ['Bullhead', 'Eggog', 'Lysol'], 'Label': ['Boner Record', 'Boner Record', 'Atlantic Records'], 'Note': ['2.3', '3.5', '5']},
            "case4" : {'Year': ['1991', '1991', '1992'], 'Album': ['Bullhead', 'Eggog', 'Lysol'], 'Label': ['Boner Record', 'Boner Record', 'Atlantic Records'], 'Note': ['2.3', '3.5', '3.5']},
            "case5" : {'Year': ['1991', '1991', '1992'], 'Album': ['Bullhead', 'Eggog', 'Lysol'], 'Label': ['Boner Record', 'Boner Record', 'Atlantic Records'], 'Note (Sku)': ['2.3', '3.5', '3.5']},
            "case6" : {'Year': ['1991', '1991', '1992'], 'Album (Sku1, Sku3)': ['Bullhead', 'Eggog', 'Lysol'], 'Label': ['Boner Record', 'Boner Record', 'Atlantic Records'], 'Note (Sku2, Sku4)': ['2.3', '3.5', '3.5']},
            "case7" : {'Title': ['Down Below', 'This Is Not the Way Home', 'The Honeymoon is Over', 'Three Legged Dog', 'Over Easy', "Where There's Smoke"], 'Year': ['1990', '1991', '1993', '1995', '1998', '2001'], 'Peak chart positions (AUS)': ['133', '62', '4', '1', '13', '25'], 'Peak chart positions (NZ)': ['-', '-', '33', '20', '-', '-'], 'Label': ['Red Eye Records', 'Red Eye Records', 'Red Eye Records', 'Red Eye Records', 'Polydor Records', 'Polydor Records']},
            "case8" : {'Title (Name)': ['Down Below', 'This Is Not the Way Home', 'The Honeymoon is Over', 'Three Legged Dog', 'Over Easy', "Where There's Smoke"], 'Year': ['1990', '1991', '1993', '1995', '1998', '2001'], 'Peak chart positions (AUS)': ['133', '62', '4', '1', '13', '25'], 'Peak chart positions (NZ)': ['-', '-', '33', '20', '-', '-'], 'Label (Company)': ['Red Eye Records', 'Red Eye Records', 'Red Eye Records', 'Red Eye Records', 'Polydor Records', 'Polydor Records']},
            "case9" : {'Down Below': {'Year': '1990', 'Peak chart positions (AUS)': '133', 'Peak chart positions (NZ)': '-', 'Label': 'Red Eye Records'}, 'This Is Not the Way Home': {'Year': '1991', 'Peak chart positions (AUS)': '62', 'Peak chart positions (NZ)': '-', 'Label': 'Red Eye Records'}, 'The Honeymoon is Over': {'Year': '1993', 'Peak chart positions (AUS)': '4', 'Peak chart positions (NZ)': '33', 'Label': 'Red Eye Records'}, 'Three Legged Dog': {'Year': '1995', 'Peak chart positions (AUS)': '1', 'Peak chart positions (NZ)': '20', 'Label': 'Red Eye Records'}, 'Over Easy': {'Year': '1998', 'Peak chart positions (AUS)': '13', 'Peak chart positions (NZ)': '-', 'Label': 'Polydor Records'}, "Where There's Smoke": {'Year': '2001', 'Peak chart positions (AUS)': '25', 'Peak chart positions (NZ)': '-', 'Label': 'Polydor Records'}},
            "case10" : {'Down Below': {'Album details': 'Released: 3 December 1990Formats: CD, LPLabel: Records', 'Peak chart positions (AUS)': '133', 'Peak chart positions (NZ)': '-', 'Certifications': ''}, 'This Is Not the Way Home': {'Album details': 'Released: 28 October 1991Formats: CD, LPLabel: Red Eye Records', 'Peak chart positions (AUS)': '62', 'Peak chart positions (NZ)': '-', 'Certifications': 'AUS: Platinum'}, 'The Honeymoon is Over': {'Album details': 'Released: 31 May 1993Formats: CD, LP, CassetteLabel: Red Eye Records', 'Peak chart positions (AUS)': '4', 'Peak chart positions (NZ)': '33', 'Certifications': 'AUS: 3× Platinum'}, 'Three Legged Dog': {'Album details': 'Released: April 1995Formats: CD, LP, CassetteLabel: Red Eye Records', 'Peak chart positions (AUS)': '1', 'Peak chart positions (NZ)': '20', 'Certifications': 'AUS: Platinum'}, 'Over Easy': {'Album details': 'Released: July 1998Formats: CDLabel: Polydor Records', 'Peak chart positions (AUS)': '13', 'Peak chart positions (NZ)': '-', 'Certifications': ''}, "Where There's Smoke": {'Album details': 'Released: September 2001Formats: CDLabel: Polydor Records', 'Peak chart positions (AUS)': '25', 'Peak chart positions (NZ)': '-', 'Certifications': ''}},
        }
        # ========= TEST ========== #
        self.oneOrAllCases(self.testAllTables, self.tablesFilesFolder, testTables, "getTableDict")

if __name__ == "__main__":
  unittest.main()