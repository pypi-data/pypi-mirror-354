import pandas as pd
import json

class ToscaReports():

    def reportTestcasesToExcel(self,testcases:list,file_path:str):
        try:
            df=pd.DataFrame({'S.No':list(range(1,len(testcases)+1)),'TestCases':testcases})
            df.to_excel(file_path,index=False)
        except Exception as e:
            print(e)
            print(f'Error in writing testcases to excel file - {file_path} !!')

    def reportTestcasesToJSON(self,testcases:list,file_path:str):
        try:
            with open(file_path, 'w', encoding='utf-8', errors='ignore') as json_file:
                json.dump({'testcases':testcases}, json_file, indent=4)
        except Exception as e:
            print(e)
            print(f'Error in writing testcases to JSON file - {file_path} !!')

    def reportTestcasesInfoToExcel(self,textcases_info:list,file_path:str):
        try:
            df=pd.DataFrame(textcases_info)
            df.columns=[str(i).title() for i in df.columns]
            df.to_excel(file_path,index=False)
        except Exception as e:
            print(e)
            print(f'Error in writing testcases info to excel file - {file_path}!!')

    def reportTestcasesInfoToJSON(self,textcases_info:list,file_path:str):
        try:
            with open(file_path, 'w', encoding='utf-8', errors='ignore') as json_file:
                json.dump({'testcases_info': textcases_info}, json_file, indent=4)
        except Exception as e:
            print(e)
            print(f'Error in writing testcases info to JSON file - {file_path} !!')