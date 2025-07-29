import os
class TqlGenerators():
    def __init__(self,el_path:str):
        self.el_path=el_path

    def generateTqlForTestcases(self,attribute_files:list,tql_file:str):
        print('Generating TQL for getting Testcases...')
        try:
            tcs_file=open(tql_file, 'w')
            tcs_file.write('UpdateAll')
            tcs_file.write('\n')
            tcs_file.write('JumpToNode "'+self.el_path+'"\n')
            line='For "=>SUBPARTS:ExecutionEntry" CallOnEach '+'"'
            line=line+str(os.getcwd()).replace('\\','\\\\')+'\\\\'+attribute_files[0]+'"\n'
            tcs_file.write(line)
            tcs_file.write("CheckinAll")
            tcs_file.write("\n")
            tcs_file.close()
            print('TQL Generation for Testcases is completed!!')
        except Exception as e:
            print('TQL Generation Failed!!')

    def generateTqlForTestcaseInfo(self,attribute_files:list,testcase_name:str,file_path:str):
        line='For "=>SUBPARTS:ExecutionEntry[Name==\\"'+testcase_name+'\\"]->ActualLog"'+" "+'CallOnEach'+" "+'"'+file_path+'\\\\'+attribute_files[1]+'"\n'
        line=line+'For "=>SUBPARTS:ExecutionEntry[Name==\\"'+testcase_name+'\\"]->ActualLog=>SUBPARTS:ExecutionTestStepValueLog[Detail!=\\"\\" and Detail =i? \\".txt\\"]"'
        line=line+" "+'CallOnEach'+" "+'"'+file_path+'\\\\'+attribute_files[2]+'"\n'

        line=line+'For "=>SUBPARTS:ExecutionEntry[Name==\\"'+testcase_name+'\\"]->ActualLog=>SUBPARTS:ExecutionTestStepLog[Detail!=\\"\\" and Detail =i? \\".txt\\"]"'
        line=line+" "+'CallOnEach'+" "+'"'+file_path+'\\\\'+attribute_files[2]+'"\n'

        line=line+'For "->SELF" CallOnEach '+'"'+file_path+'\\\\'+attribute_files[0]+'"\n'
        return line

    def generateTqlForTestcasesInfo(self,testcases:list,attribute_files:list,tql_file:str):
        try:
            tcs_file=open(tql_file, 'w')
            tcs_file.write('UpdateAll')
            tcs_file.write('\n')
            line='JumpToNode "'+self.el_path+'"\n'
            tcs_file.write(line)
            tcs_file.write('For "->SELF" CallOnEach '+'"'+str(os.getcwd()).replace('\\','\\\\')+'\\\\'+attribute_files[0]+'"\n')
            for i in testcases:
                tcs_file.write(self.generateTqlForTestcaseInfo(attribute_files,i,str(os.getcwd()).replace('\\','\\\\')))
            tcs_file.write("CheckinAll")
            tcs_file.write("\n")
            tcs_file.close()
        except Exception as e:
            print('TQL Generation Failed!!')

    def generateTqlForExecuteEL(self,tql_file:str):
        tql=f'''UpdateAll
JumpToNode "{self.el_path}"
task "Checkout Tree"
task "run"
CheckinAll
'''
        try:
            tcs_file=open(tql_file, 'w')
            tcs_file.write(tql)
            tcs_file.close()
        except Exception as e:
            print('TQL Generation Failed!!')