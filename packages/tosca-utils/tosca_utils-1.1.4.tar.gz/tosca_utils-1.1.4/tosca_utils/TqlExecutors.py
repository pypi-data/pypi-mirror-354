import subprocess
import os

class TqlExecutors():
    def __init__(self,tws_path:str):
        self.tws_path=tws_path

    def runTqlForTestcases(self,tql_file:str)-> str:
        print('Executing the TQL for getting the Testcases...')
        result= ''
        try:
            result=subprocess.run(['TCSHELL.exe','-workspace',self.tws_path,str(os.getcwd())+"\\"+tql_file],capture_output=True, text=True)
            print('TQL Execution for Getting the Testcases is Completed!!')
            return result.stdout + result.stderr
        except Exception as e:
            print('TQL Execution Failed!!')
            result='FAIL'
            return result

    def runTqlForTestcasesInfo(self,tql_file:str)->str:
        print('Executing the TQL for getting the Testcases Info...')
        result= ''
        try:
            result=subprocess.run(['TCSHELL.exe','-workspace',self.tws_path,str(os.getcwd())+"\\"+tql_file], capture_output=True, text=True)
            print('TQL Execution for Getting the Testcases is Completed!!')
            return result.stdout + result.stderr
        except Exception as e:
            print('TQL Execution Failed!!')
            result='FAIL'
            return result

    def runTqlForExecuteEL(self,tql_file:str,execution_mode:bool=True)->str:
        print('Executing the TQL for running the Testcases...')
        try:
            if execution_mode:
                result=subprocess.run(['TCSHELL.exe','-workspace','-executionmode',self.tws_path,tql_file], capture_output=True, text=True)
            else:
                result=subprocess.run(['TCSHELL.exe','-workspace',self.tws_path,tql_file], capture_output=True, text=True)
            print('El Execution Completed!!')
            return result.stdout + result.stderr
        except Exception as e:
            print(e)
            print('TQL Execution Failed!!')
            result='FAIL'
            return result