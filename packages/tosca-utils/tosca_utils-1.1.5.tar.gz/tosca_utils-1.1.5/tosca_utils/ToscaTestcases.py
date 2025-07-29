import datetime
class ToscaTestcases():
    def getTestcases(self,tql_output:str)->list:
        tc_content = tql_output.encode('utf-8',errors='ignore').decode('utf-8', errors='ignore')
        tc_names=[]
        if "Name:" in tc_content:
            tc_content=tc_content[tc_content.index("Name:"):]
            tc_content=tc_content.split("\n")
            for line in tc_content:
                if line.startswith("Name:"):
                    tc_names.append(line.split("Name:")[1].strip())
                elif line.startswith('Checkin all:'):
                    break
        return tc_names

    def getTestcasesInfo(self,tql_output:str)->list:
        try:
            tql_output=tql_output.encode('utf-8',errors='ignore').decode('utf-8', errors='ignore')
            tql_output=tql_output.split('\n')
            tcs_info=['']
            for i in tql_output:
                if(i.startswith("UniqueId:")):
                    tcs_info.append('')
                    tcs_info[-1]=tcs_info[-1]+i+'\n'
                elif(i.startswith("Checkin all:")):
                    break
                else:
                    tcs_info[-1]=tcs_info[-1]+i+'\n'
            tcs_info=tcs_info[1:-1]
            tc_names=[]
            tc_durations=[]
            tc_results=[]
            tc_req_res_paths=[]
            for tc_info in tcs_info:
                tc_names.append(" ")
                tc_durations.append(" ")
                tc_results.append(" ")
                tc_req_res_paths.append(" ")
                if "Name:" in tc_info:
                    tc_names[-1]=tc_info[tc_info.index("Name:"):].split("\n")[0].split("Name:")[1].strip()
                    print(tc_names[-1])
                if "Duration:" in tc_info:
                    tc_durations[-1]=tc_info[tc_info.index("Duration:"):].split("\n")[0].split("Duration:")[1].strip()
                    print(tc_durations[-1])
                if "Result:" in tc_info:
                    tc_results[-1]=tc_info[tc_info.index("Result:"):].split("\n")[0].split("Result:")[1].strip()
                    print(tc_results[-1])
                if "Detail:" in tc_info:
                    paths_start_end=[line.split("Detail:")[1].strip() for line in tc_info[tc_info.index("Detail:"):].split('\n') if line.startswith("Detail:")]
                    tc_req_res_paths[-1]="::".join(paths_start_end)
                    if "::" not in tc_req_res_paths[-1]:
                        tc_req_res_paths[-1]=tc_req_res_paths[-1]+"::"
            exec_date=datetime.datetime.now().strftime("%Y-%m-%d")
            tc_exec_dates=[str(exec_date) for i in tc_results]
            tc_durations=[float(i) if len(str(i).strip())>0 else 0 for i in tc_durations]
            return [{'S.No':i+1,'testcase':tc_names[i],'duration':tc_durations[i],'result':tc_results[i],'date of execution':tc_exec_dates[i],'paths':tc_req_res_paths[i]} for i in range(len(tc_names))]
        except Exception as e:
            print("Couldn't get the Testcases Info!!")