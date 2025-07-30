import requests
import json
import os
import time


setHost = "172.24.2.66:8220/prod-api/s-n-validation"  # 默认地址 可通过autoNaviSystem.setHost设置
token = None
def login(userName,passWord):
    global setHost,token
    baseHost = setHost.rsplit('/', 1)[0] if '/' in setHost else setHost
    urlToken = f"http://{baseHost}/auth/getToken"
    query = {"username":userName,"password":passWord}
    payload = {
        "username": "CQDatHnnm3H/NYSe/EVHRtNomXMm5AacBYQuhvu+9J7o1Vbt2neTN5ln3Cjmf77h0D+paFAEqwKmbtjgO5XV1g==",
        "password": "nBkR7k/sWps7YgQjaETgbs6r+IyBbx03zhyCVb4zhDjeGWCcBKWF/dRFNmSFvt5dp0mtOixllVtFaWBweI54yA=="
    }
    headers = {}
    response = requests.request("POST", urlToken, json=payload, headers=headers, params=query)
    try:
        responseData = response.json()
        token = responseData.get('data', {}).get('access_token', '')
        return token
    except Exception as e:
        print("获取token失败：", e)
        print("响应内容：", response)
        return response
    

class scene:
    def __init__(self):  # 初始化http
        global setHost, token
        self.host = setHost  # 服务器地址 172.24.2.66:8220/prod-api/s-n-validation
        self.token = token  # 服务器地址 172.24.2.66:8220/prod-api/auth/getToken
        self.headers = {
            'Authorization': 'Bearer {}'.format(self.token)
        }
        

    def getSeneId(self):
        payload = {
            "ids": "0010101", #//场景ID
            "closeDescription": "关闭备注", #//0：代表编辑操作，1：代表新增操作
            "sceneEnable":0
        }
        urlGetSceneId = f"http://{self.host}/scenemanager/getSceneCode"
        try:
            response = requests.post(urlGetSceneId, json=payload, headers=self.headers)
            self.newSceneID = response.json().get('data', {})
            return self.newSceneID
        except requests.RequestException as e:
            print("网络请求失败：", e)
            return e
        except ValueError as e:
            print("解析 JSON 失败：", e)
            print("响应内容：", response.text if 'response' in locals() else '无响应')
            return response
    
    def queryShipModels(self):
        """
        查询船舶模型列表并打印‘模型名称’和‘船型类型’列，返回完整的数据列表
        """
        url =f"http://{self.host}/shipmodel/list"
        try:
            response = requests.post(url, json={}, headers=self.headers)
            response.raise_for_status()
            shipModelList =response.json()
             # 打印标题
            print(f"{'模型名称':<50}{'ModelCode':<50}")
            print("-" * 85)

            for model in shipModelList:
                modelName = model.get("modelName", "无")
                id = model.get("id", "无")
                print(f"{modelName:<50},{id:<50}")

            return shipModelList
        except Exception as e:
            print(" 获取船型列表失败：", e)
            print("响应内容：", response.text)
            return response

       
    
    def selectShipModel(self, testShipModel):
        """
        选择船型，返回船舶信息。
        :param testShipModel: 船舶模型列表（从查询结果获取）
        :return: 所选船舶模型的 JSON 数据

        """
        if not testShipModel:
            print("错误", "请选择要的测试的船舶")
            return "请选择要的测试的船舶"
        url = f"http://{self.host}/shipmodel/list"
        try:
            response = requests.post(url, json={}, headers=self.headers)
            response.raise_for_status()
            shipModelList =response.json()
            matched = [model for model in shipModelList if model.get("id") == testShipModel]
            if matched:
                selectedModel = matched[0]
                return selectedModel
            else:
                print("返回文本:没有找到合适的船模")
                return "没有找到合适的船模"
        except Exception as e:
            print("返回文本:", response.text)
            return response


    def save(self, sceneInfo, testShipModelCode,targetShipModelCode,sceneName):
        sceneTestShips = sceneInfo.get("sceneTestShips", [])
        sceneTargetShips = sceneInfo.get("sceneTargetShips", [])
        sceneInfo["ifAdd"] = '1'
        sceneInfo["sceneBaseInfo"]["sceneId"] = self.getSeneId()
        sceneInfo["sceneBaseInfo"]["sceneName"] = sceneName
        for i, modelCode in enumerate(testShipModelCode):
            modelInfo = self.selectShipModel(modelCode)
            modelInfo["sceneId"] = self.newSceneID
            sceneTestShips[i]["sceneId"] = self.newSceneID
            sceneTestShips[i]["shipModelCode"] = modelInfo["id"]
            sceneTestShips[i]["shipModelName"] = modelInfo["modelName"]
            sceneTestShips[i]["shipType"] = modelInfo["shipType"]
            sceneTestShips[i]["shipModelInfo"] = modelInfo.copy()

        for j, modelCode in enumerate(targetShipModelCode):
            modelInfo = self.selectShipModel(modelCode)
            modelInfo["sceneId"] = self.newSceneID
            sceneTargetShips[j]["sceneId"] = self.newSceneID
            sceneTargetShips[j]["shipModelCode"] = modelInfo["id"]
            sceneTargetShips[j]["shipModelName"] = modelInfo["modelName"]
            sceneTargetShips[j]["shipType"] = modelInfo["shipType"]
            sceneTargetShips[j]["shipModelInfo"] = modelInfo.copy()
        sceneInfo["sceneTestShips"] = sceneTestShips
        sceneInfo["sceneTargetShips"] =sceneTargetShips
        url = f"http://{self.host}/scenemanager/saveSceneInfo"
        
        # 解析响应内容
        
        try:
            response = requests.post(url, json=sceneInfo, headers=self.headers)
            print("返回结果:", response.json())
            print("新建场景id:", self.newSceneID)
            return {
                "response": response.json(),
                "scene_id": self.newSceneID
            }
        except Exception as e:
            print("返回文本:", response.text)
            return response

    def querySceneInfo(self, sceneId):
        url = f"http://{self.host}/scenemanager/selectSceneInfoById" #调用地址
        files = {
            "id": (None,sceneId)
        }
        try:
            response = requests.post(url, files=files, headers=self.headers)
            sceneInfo = response.json().get('data', {})
            sceneInfo = json.dumps(sceneInfo, indent=2, ensure_ascii=False)
            return sceneInfo
        except Exception as e:
            print("获取场景信息失败：", e)
            print("响应内容：", response.text)
            return response
        
    def deleteScene(self, deleteDescription,sceneIds):
        url = f"http://{self.host}/scenemanager/deleteSceneInfo"
        payload = {
            "deleteDescription": deleteDescription,
            "ids":sceneIds
        }
        try:
            response = requests.post(url, json=payload, headers=self.headers)
        # 解析响应内容
            print("状态码:", response.status_code)
            print("返回结果:", response.json())
            return response.json()
        except Exception as e:
            print("返回文本:", response.text)
            return response

    
    def edit(self, sceneInfo, testShipModelName,targetShipModelName,sceneName):
        sceneTestShips = sceneInfo.get("sceneTestShips", [])
        sceneTargetShips = sceneInfo.get("sceneTargetShips", [])
        sceneInfo["ifAdd"] = '0'
        sceneInfo["sceneBaseInfo"]["sceneName"] = sceneName
        sceneId = sceneInfo["sceneBaseInfo"]["sceneId"]
        for i, modelName in enumerate(testShipModelName):
            modelInfo = self.selectShipModel(modelName)
            modelInfo["sceneId"] = sceneId
            sceneTestShips[i]["sceneId"] = sceneId
            sceneTestShips[i]["shipModelCode"] = modelInfo["id"]
            sceneTestShips[i]["shipModelName"] = modelInfo["modelName"]
            sceneTestShips[i]["shipType"] = modelInfo["shipType"]
            sceneTestShips[i]["shipModelInfo"] = modelInfo.copy()

        for j, modelName in enumerate(targetShipModelName):
            modelInfo = self.selectShipModel(modelName)
            modelInfo["sceneId"] = sceneId
            sceneTargetShips[j]["sceneId"] = sceneId
            sceneTargetShips[j]["shipModelCode"] = modelInfo["id"]
            sceneTargetShips[j]["shipModelName"] = modelInfo["modelName"]
            sceneTargetShips[j]["shipType"] = modelInfo["shipType"]
            sceneTargetShips[j]["shipModelInfo"] = modelInfo.copy()
        sceneInfo["sceneTestShips"] = sceneTestShips
        sceneInfo["sceneTargetShips"] =sceneTargetShips
        url =f"http://{self.host}/scenemanager/saveSceneInfo"
        
        # 解析响应内容
        
        try:
            response = requests.post(url, json=sceneInfo, headers=self.headers)
            print("状态码:", response.status_code)
            print("返回结果:", response.json())
            return response.json()
        except Exception as e:
            print("返回文本:", response.text)
            return response
    
    def importScene(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                files = {
                    'file': (os.path.basename(file_path), f, 'application/json')
                }
                url = f"http://{self.host}/scenemanager/import"
                response = requests.post(url, files=files, headers=self.headers)
                response_data = response.json()
                jsonText = json.dumps(response_data, indent=2, ensure_ascii=False)
                print(jsonText)
                return jsonText
        except Exception as e:
            print("文件上传失败：", str(e))
            return "文件上传失败"


class Task:
    def __init__(self):
        global setHost, token
        self.host = setHost  # 服务地址 172.24.2.66:8220/prod-api/s-n-validation
        self.token = token  # 服务地址 172.24.2.66:8220/prod-api/auth/getToken
        self.headers = {
            'Authorization': 'Bearer {}'.format(self.token)
        }

    
    
    # 根据任务ID查询任务信息
    def queryTaskInfo(self, taskId):
        url = f"http://{self.host}/voyTaskInfo/queryById"
        files = {
            "id": (None,taskId)
        }

        try:
            response = requests.post(url, files=files, headers=self.headers)
            taskInfo = response.json()
            taskInfo = json.dumps(taskInfo, indent=2, ensure_ascii=False)
            return taskInfo
        except Exception as e:
            print("获取任务信息失败：", e)
            print("响应内容：", response.text)
            return response.text
    
    def queryTestObject(self, objectName):
        url = f"http://{self.host}/voyTaskInfo/paginListObjectInfo"
        params = {
            "objectName":objectName
        }

        try:
            response = requests.get(url, params=params, headers=self.headers)
            testObjectList = response.json().get('rows', {})
            testObjectList = json.dumps(testObjectList, indent=2, ensure_ascii=False)
            return testObjectList
        except Exception as e:
            print("获取测试对象列表失败：", e)
            print("响应内容：", response.text)
            return response
    #选择任务场景
    def selectTestScene(self, sceneId):
        url = f"http://{self.host}/voyTaskInfo/selectSceneByIds"
        payload =  [sceneId]        
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            taskSceneInfo = response.json()
            taskSceneInfo = json.dumps(taskSceneInfo, indent=2, ensure_ascii=False)
            return taskSceneInfo
        except Exception as e:
            print("获取任务场景信息失败：", e)
            print("响应内容：", response.text)
            return response
    #查询新建任务
    def searchNewTask(self, params):
        ##params入参示例
        # {
        #     "priority": "0" ,
        #     "pageNum": "1",
        #     "pageSize": "10",
        #     "taskStatus": "0",
        #     "creatorName": "admin2"
        # }
        url = f"http://{self.host}/voyTaskInfo/paginQuery"
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            newTask = response.json()
            newTask = json.dumps(newTask, indent=2, ensure_ascii=False)
            print("查询成功")
            return newTask
        except Exception as e:
            print("获取任务列表失败：", e)
            print("响应内容：", response.text)
            return response
    
    #提交新任务
    def submitNewTask(self, taskId):
        url = f"http://{self.host}/voyTaskInfo/submit"
        payload = {
            "id": taskId
        }
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            submitTask = response.json()
            submitTask = json.dumps(submitTask, indent=2, ensure_ascii=False)
            print("提交成功")
            return submitTask
        except Exception as e:
            print("提交任务失败：", e)
            print("响应内容：", response.text)
            return response
    
    #查询已提交任务信息（待审核）
    def querySubmittedTask(self, params):
        ##params入参示例
        # params = {
        # "priority": "0" ,
        # "pageNum": "1",
        # "pageSize": "10",
        # "taskStatus": "1",
        # "creatorName": "admin2"
        # }
        url = f"http://{self.host}/voyTaskInfo/paginQuery"
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            submittedTask = response.json()
            submittedTask = json.dumps(submittedTask, indent=2, ensure_ascii=False)
            print("查询成功")
            return submittedTask
        except Exception as e:
            print("获取已提交任务列表失败：", e)
            print("响应内容：", response.text)
            return response
        
    #审核任务
    def auditTask(self, payload):
        ##payload入参示例
        #payload = {
        # "approvalResults":"1",# 1（同意） 2（反驳）
        # "auditorName":"dev2test",
        # "remark":"同意",
        # "priority":"5",
        # "taskId":"1920399574724382720",#需要审核的任务id
        # "taskStatus":"1"   #任务的状态
        # }
        url = f"http://{self.host}/voyTaskInfo/addApprovalLog"
        
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            auditTaskResult = response.json()
            auditTaskResult = json.dumps(auditTaskResult, indent=2, ensure_ascii=False)
            print("审核完成")
            return auditTaskResult
        except Exception as e:
            print("审核任务失败：", e)
            print("响应内容：", response.text)
            return response
    
    # 查询已审核任务
    def queryAuditedTask(self, params):
        ##params入参示例
        # params = {
        # "priority": "0" ,
        # "pageNum": "1",
        # "pageSize": "10",
        # "taskStatus": "22",
        # "creatorName": "admin2"
        # }
        url =f"http://{self.host}/voyTaskInfo/paginQuery"
        
        try:    
            response = requests.get(url, params=params, headers=self.headers)
            auditedTaskList = response.json()
            auditedTaskList = json.dumps(auditedTaskList, indent=2, ensure_ascii=False)
            print("查询成功")
            return auditedTaskList
        except Exception as e:
            print("获取已审核任务列表失败：", e)
            print("响应内容：", response.text)
            return response
    # 根据任务ID查询实例化场景信息
    def querySceneInfo(self, taskId):
        url = f"http://{self.host}/voyTaskSceneInfo/listSceneInfoByTaskId"
        params = {
            "taskId": taskId
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            sceneBaseInfo = response.json()
            sceneBaseInfo = json.dumps(sceneBaseInfo, indent=2, ensure_ascii=False)
            print("查询成功",sceneBaseInfo)
            return sceneBaseInfo
        except Exception as e:
            print("获取实例化场景信息失败：", e)
            print("响应内容：", response.text)
            return response

    #任务执行前场景检查
    def taskSceneCheck(self, payload):
        ##payload入参示例
        # {
        #     "runNumber": "1", 
        #     "businessCode": "VOY", 
        #     "isVerification": "1", #是否校验 1代表检查 2代表执行
        #     "sceneIds": [
        #     "675423519055941"   #实例化场景id
        #     ] #场景id数组
        # }
        url = f"http://{self.host}/environmentapi/taskStartup"
        try:
            response = requests.post(url, json=payload, headers=self.headers)
        except Exception as e:
            print("任务执行前场景检查失败：", e)
            print("响应内容：", response)
            return response
        payloadCheck = {
            "isDelay": "0", #0:不延时，1：延时
            "ids": payload.get("sceneIds", []) #场景id集合
        }
            # 延迟 5 秒
        print("等待2秒后进行检查结果查询...")
        time.sleep(2)
        sceneCheckResult = self.querySceneCheckResult(payloadCheck)
        print("检查结果：",sceneCheckResult)
        return sceneCheckResult
    #任务执行前检查结果
    def querySceneCheckResult(self, payload):
        ##payload入参示例
        # {
        #     "isDelay": "0", #0:不延时，1：延时
        #     "ids": [
        #     "675423519055941"  # 实例化id
        #     ] #场景id集合
        # }
        url = f"http://{self.host}/voyTaskSceneInfo/listSceneStatusByIds"
        
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            responseResultJson = response.json()
            responseResult = json.dumps(responseResultJson, indent=2, ensure_ascii=False)
            checkValueList = responseResultJson.get("data", [])
            checkValue=str(checkValueList[0].get("sceneEnable",""))
            if checkValue == "0":
                checkResult = "试验完成"
            if checkValue == "1":
                checkResult = "执行中"
            if checkValue == "2":
                checkResult = "暂停"
            if checkValue == "3":
                checkResult = "执行失败"
            if checkValue == "11":
                checkResult = "未检查"
            if checkValue == "13":
                checkResult = "检查通过"
            if checkValue == "14":
                checkResult = "检查失败"
            if checkValue == "15":
                checkResult = "检查中"
            if checkValue == "20":
                checkResult = "报告生成中"
            if checkValue == "21":
                checkResult = "报告生成完成"
            if checkValue == "22":
                checkResult = "报告生成失败"
            if checkValue == "25":
                checkResult = "回放中"
            if checkValue == "30":
                checkResult = "回放暂停"
            print("检查结果：",checkResult)
            return {"response": responseResult,
                    "checkResult":checkResult
                    }
        except Exception as e:
            print("任务执行前检查结果失败：", e)
            print("响应内容：", response.text)
            return response
    #任务执行
    def execute(self, payload):
        ##payload入参示例
        # {
        #     "runNumber": "1", 
        #     "businessCode": "VOY", 
        #     "isVerification": "2", #是否校验 1代表检查 2代表执行
        #     "sceneIds": [
        #     "675423519055941"   #实例化场景id
        #     ] #场景id数组
        # }
        url = f"http://{self.host}/environmentapi/taskStartup"
        
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            responseData = response.json()
            responseData = json.dumps(responseData, indent=2, ensure_ascii=False)
            payloadCheck = {
            "isDelay": "0", #0:不延时，1：延时
            "ids": payload.get("sceneIds", []) #场景id集合
            }
            # 延迟 5 秒
            print("等待2秒后进行执行结果查询...")
            time.sleep(2)
            sceneExecuteResult = self.querySceneCheckResult(payloadCheck)
            print("执行结果：",sceneExecuteResult)
            print("response:",responseData)
            return {
                "response":responseData,
                "执行结果":sceneExecuteResult
                }
        except Exception as e:
            print("任务执行失败：", e)
            print("响应内容：", response.text)
            return {e,response}
    #任务结束结果
    def shutDown(self, ids):
        ##ids入参[675423519055941]
        # 
        url = f"http://{self.host}/environmentapi/shutdown"
        payload = ids
        
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            shutDownTaskResult = response.json()
            shutDownTaskResult = json.dumps(shutDownTaskResult, indent=2, ensure_ascii=False)
            print(shutDownTaskResult)
            return shutDownTaskResult
        except Exception as e:
            print("任务结束失败：", e)
            print("响应内容：", response.text)
            return response
    
    
    #导出CSV文件数据
    def exportCsvData(self, taskSceneId,version):
        url = f"http://{self.host}/environmentapi/exportProcessData"
        payload = {
            "sceneId": taskSceneId,
            "version": version
        }
        
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            fileNameId = payload.get("sceneId", "")
            fileNameVersion = payload.get("version", "")
            fileName = f"{fileNameId}_{fileNameVersion}数据.csv"                
            with open(fileName, "w", encoding="utf-8-sig", newline='') as f:
                f.write(response.text)
            print(f"导出CSV文件成功，文件名：{fileName}")
            return fileName
        except Exception as e:
            print("导出CSV文件失败：", e)
            return e
    
    # 查询过程数据
    def queryProcessData(self, params,payload):
        #params入参示例
        # {
        # "pageNum": "1",
        # "pageSize": "10"
        # }
            
        #payload入参示例
        # {
        #     "taskSceneId": "680310692708421", #任务场景id
        #     "shipModelObjectId": "680318676660317",#模型对象id
        #     "shipId": "680310692708422", #船舶id
        #     "version": "1", #执行数据版本号
        #     "startTime": "2025-05-26 11:17:24",#开始时间
        #     "endTime": "2025-05-26 11:21:26"#结束时间
        # }
        url = f"http://{self.host}/processData/listPage"
        
        try:
            response = requests.post(url, params=params, json=payload, headers=self.headers)
            processData = response.json()
            processData = json.dumps(processData, indent=2, ensure_ascii=False)
            return processData
        except Exception as e:
            print("查询过程数据失败：", e)
            print("响应内容：", response.text)
            return response
        
    ##查询模型类型及要素字段
    def queryModelTypeAndElement(self, payload):
        url = f"http://{self.host}/processData/getTableHeading"
        response = requests.post(url, json=payload, headers=self.headers)
        try:
            modelTypeAndElement = response.json()
            modelTypeAndElement = json.dumps(modelTypeAndElement, indent=2, ensure_ascii=False)
            print("查询成功：",modelTypeAndElement)
            return modelTypeAndElement
        except Exception as e:
            print("查询模型类型及要素字段失败：", e)
            print("响应内容：", response.text)
            return response
    
    #删除任务
    def delete(self, taskId):
        url = f"http://{self.host}/voyTaskInfo/deleteById"
        files = {
            "id": (None,taskId)
        }

        try:
            response = requests.post(url, files=files, headers=self.headers)
            taskInfo = response.json()
            taskInfo = json.dumps(taskInfo, indent=2, ensure_ascii=False)
            return taskInfo
        except Exception as e:
            print("删除任务失败：", e)
            print("响应内容：", response.text)
            return response


    def save(self, taskInfo):
        url = f"http://{self.host}/voyTaskInfo/add"
        payload = taskInfo
        response = requests.post(url, json=payload, headers=self.headers)
        try:
            addTaskResult = response.json()
            addTaskResult = json.dumps(addTaskResult, indent=2, ensure_ascii=False)
            print("状态码:", response.status_code)
            return addTaskResult
        except Exception as e:
            print("添加任务失败：", e)
            print("响应内容：", response.text)
            return response

def status(dictType):
    global setHost, token
    baseHost = setHost.rsplit('/', 1)[0] if '/' in setHost else setHost
    url = f"http://{baseHost}/system/dict/data/list"
    params = {
        "dictType": dictType
    }

    # 请求数据
    try:
        response = requests.get(url, params=params, headers={"Authorization": f"Bearer {token}"})
        status = response.json()
        statusList = json.dumps(status, indent=2, ensure_ascii=False)
        rows = status.get("rows", [])

        if not rows:
            print("没有查询到任何数据")
            return "没有查询到任何数据"

        # 定义列宽
        col_widths = [18, 12, 10, 10, 10]

        # 打印表头
        headers = ["字典编码", "字典标签", "字典键值", "字典排序", "状态"]
        header_row = "".join(f"{h:<{w}}" for h, w in zip(headers, col_widths))
        print(header_row)
        print("-" * sum(col_widths))

        # 打印数据行
        for row in rows:
            dict_code = str(row.get("id", ""))
            dict_label = str(row.get("dictLabel", ""))
            dict_value = str(row.get("dictValue", ""))
            dict_sort = str(row.get("dictSort", ""))
            status = "正常" if row.get("status") == "0" else "异常"

            print(f"{dict_code:<18}{dict_label:<12}{dict_value:<10}{dict_sort:<10}{status:<10}")
        return statusList
    except Exception as e:        
        print("获取字典数据失败：", e)
        print("响应内容：", response.text)
        return response