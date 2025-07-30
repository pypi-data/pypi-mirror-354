# server.py
import os
from mcp.server.fastmcp import FastMCP
from typing import Optional, Dict, Any
from mcp.types import Tool, TextContent
import mcp.types as types
import httpx
from datetime import datetime
import json

api_url = "https://report.hzzzwl.com"
api_key = os.getenv("KEY")

# Create an MCP server
mcp = FastMCP("hzzzwl-agriculture-mcp-x")


def post_form_request(url: str, form_data: Dict[str, Any], **kwargs) -> Optional[Dict[str, Any]]:
    """
    发送 x-www-form-urlencoded 格式的 POST 请求，并返回 JSON 响应
    
    :param url: 请求的目标 URL
    :param form_data: 表单参数字典（例如 {"key1": "value1"}）
    :param kwargs: 其他传递给 `httpx.post` 的参数（如 headers、timeout 等）
    :return: 解析后的 JSON 字典，请求失败时返回 None
    """
    try:
        # 发送 POST 请求
        response = httpx.post(
            url,
            data=form_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            **kwargs
        )
        response.raise_for_status()  # 检查 4xx/5xx 错误
        return response.json()
    
    except httpx.RequestError as e:
        print(f"请求失败: {e}")  # 网络问题（如 DNS 解析失败、连接超时）
    except httpx.HTTPStatusError as e:
        print(f"HTTP 错误: {e.response.status_code} {e.response.text}")  # 状态码非 2xx
    except (ValueError, TypeError) as e:
        print(f"JSON 解析失败: {e}")  # 响应内容不是有效 JSON
    
    return None


def get_now_time() -> list[TextContent]:
    """获取当前时间"""

    current_time = datetime.now()
    # 格式化时间（自定义输出格式）
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    return [TextContent(type="text", text=formatted_time)]



def getNyInfo(name:str,djzh:str) -> list[TextContent]:
    """根据农药名称：name和登记证号：djzh，获得该农药的基本信息,登记证号不必填。
    返回json格式数据，其中list为jsonarray，
    里面包含hzrq：核准日期，ccysff：储存和运输方法，shengCQY：登记证持有人(生产企业)，
    dux：毒性，description：备注，cpxn：产品性能，yxqz：有效期至，nylb：农药类别，
    zxhzrq：重新核准日期，name：农药名称，jix：剂型，zdjjcs：中毒急救措施，bzq：质量保证期，
    djzh：登记证号，zyxcfhl：总有效成分含量，zysx：注意事项，syjsyq：使用技术要求。
    """

    test_url = api_url+"/zzdata/api/zzdata/getNyInfo.do"
    test_data = {"name": name,"djzh":djzh,"token":api_key,"mdName":"getNyInfo"}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    jj = json.dumps(result, ensure_ascii=False, indent=4)

    return [TextContent(type="text", text=jj)]

def getNyChengF(name:str,djzh:str) -> list[TextContent]:
    """根据农药名称：name和登记证号：djzh，获得该农药的主要有效成分,登记证号不必填。
    返回json格式数据，其中list为jsonarray，
    里面包含name_cn：有效成分中文名，name_en：有效成分英文名，hanl：有效成分含量。"""

    test_url = api_url+"/zzdata/api/zzdata/getNyChengF.do"
    test_data = {"name": name,"djzh":djzh,"token":api_key,"mdName":"getNyChengF"}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    jj = json.dumps(result, ensure_ascii=False, indent=4)

    return [TextContent(type="text", text=jj)]

def getNyShengCQY(name:str,djzh:str) -> list[TextContent]:
    """根据农药名称：name和登记证号：djzh，获得该农药的生产企业信息,登记证号不必填。
    返回json格式数据，其中list为jsonarray，
    里面包含name：企业名称，province：企业所在省份，country：企业所在国家，county：企业所在县，
    postcode：邮编，tel：电话，fox：传真，contact：联系人，phone：手机号码，addr：单位地址，
    email：邮箱。"""

    test_url = api_url+"/zzdata/api/zzdata/getNyShengCQY.do"
    test_data = {"name": name,"djzh":djzh,"token":api_key,"mdName":"getNyShengCQY"}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    jj = json.dumps(result, ensure_ascii=False, indent=4)

    return [TextContent(type="text", text=jj)]

def getNyUseInfo(name:str,djzh:str) -> list[TextContent]:
    """根据农药名称：name和登记证号：djzh，获得该农药的使用范围和使用方法,登记证号不必填。
    返回json格式数据，其中list为jsonarray，
    里面包含crops：作物/场所，fzdx：防治对象，dosage：用药量（制剂量/亩），syff：施用方法。"""

    
    test_url = api_url+"/zzdata/api/zzdata/getNyUseInfo.do"
    test_data = {"name": name,"djzh":djzh,"token":api_key,"mdName":"getNyUseInfo"}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    jj = json.dumps(result, ensure_ascii=False, indent=4)

    return [TextContent(type="text", text=jj)]


def getNyInfoByScqy(scqy:str) -> list[TextContent]:
    """根据生产企业名称：scqy，获得该生产企业生产哪些农药。
    返回json格式数据，其中list为jsonarray，里面包含name：农药名称。"""

    
    test_url = api_url+"/zzdata/api/zzdata/getNyInfoByScqy.do"
    test_data = {"scqy": scqy,"token":api_key,"mdName":"getNyInfoByScqy"}

    # 发送请求
    result = post_form_request(test_url, test_data)
    jj = json.dumps(result, ensure_ascii=False, indent=4)

    return [TextContent(type="text", text=jj)]

def getFzffByCropFzdx(crop:str,fzdx:str) -> list[TextContent]:
    """根据农作物名称：crop和病虫害名称：fzdx，获得防治药物及使用方法。
    返回json格式数据，其中list为jsonarray，
    里面包含name：药物名称，dosage：用药量（制剂量/亩），syff：施用方法。"""

    
    test_url = api_url+"/zzdata/api/zzdata/getFzffByCropFzdx.do"
    test_data = {"crop": crop,"fzdx":fzdx,"token":api_key,"mdName":"getFzffByCropFzdx"}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    jj = json.dumps(result, ensure_ascii=False, indent=4)

    return [TextContent(type="text", text=jj)]

def getPlantWeather(plant:str) -> list[TextContent]:
    """根据农作物名称：plant，获得该农作物适合的种植气候以及包含城市。
    返回json格式数据，其中list为jsonarray，
    里面包含weather：气候，city：城市。"""

    
    test_url = api_url+"/zzdata/api/zzdata/getPlantWeather.do"
    test_data = {"plant": plant,"token":api_key,"mdName":"getPlantWeather"}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    jj = json.dumps(result, ensure_ascii=False, indent=4)

    return [TextContent(type="text", text=jj)]

def getCityWeather(city:str) -> list[TextContent]:
    """根据城市名称：city，获得该城市的气候以及适合种植的作物。
    返回json格式数据，其中list为jsonarray，
    里面包含weather：气候，plant：作物。"""

    
    test_url = api_url+"/zzdata/api/zzdata/getCityWeather.do"
    test_data = {"city": city,"token":api_key,"mdName":"getCityWeather"}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    jj = json.dumps(result, ensure_ascii=False, indent=4)

    return [TextContent(type="text", text=jj)]


def get_medication_value(productName:str,medicationName:str) -> list[TextContent]:
    """根据农产品名称：productName和药物名称：medicationName，获得该农产品上的该药物的检出限(检出上限)。
    返回json格式数据，其中list为jsonarray，里面包含unit：单位，pd：检出限，aname：药物名称，name：农产品名称
    ，value：检出限具体的值。"""

    
    test_url = api_url+"/mcp_server2/cellphone/getData.do?sysCmd=getJcx"
    test_data = {"cpname": productName,"ypname":medicationName,"token":api_key,"mdName":"get_medication_value"}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    jj = json.dumps(result, ensure_ascii=False, indent=4)

    return [TextContent(type="text", text=jj)]


def get_monitor_info(areaName: str,cpname:str,year:int) -> list[TextContent]:
    """根据区划：areaName，农产品名称：cpname，年度：year，获得该地区该农产品的检测合格率。其中年度不必填。
    返回json格式数据，其中list为jsonarray，里面包含year:年度,all_num:抽样批次数量，qualified_num：合格批次数量，qualified_rat：合格率，
    unqualified：不合格数量。"""

    
    test_url = api_url+"/mcp_server2/cellphone/getData.do?sysCmd=getHgl"
    test_data = {"areaName": areaName, "cpname": cpname,"year":year,"token":api_key,"mdName":"get_monitor_info"}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    jj = json.dumps(result, ensure_ascii=False, indent=4)

    return [TextContent(type="text", text=jj)]

def get_monitor_task_info(areaName: str,taskName:str) -> list[TextContent]:
    """根据区划：areaName和任务：taskName，获得该地区该监测任务的完成情况，并给出下一年的任务安排建议。
    返回json格式的数据，详细内容都在message字段中。"""

    
    test_url = api_url+"/mcp_server2/cellphone/getData.do?sysCmd=getJcQ4"
    test_data = {"areaName": areaName, "taskName": taskName,"token":api_key,"mdName":"get_monitor_task_info"}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    jj = json.dumps(result, ensure_ascii=False, indent=4)

    return [TextContent(type="text", text=jj)]

def get_monitor_predictions_data(areaName: str,cpname:str) -> list[TextContent]:
    """根据区划：areaName，农产品名称：cpname，预测该地区该农产品未来几年的检测合格率。
    返回json格式数据，其中history_data为jsonarray，里面包含历史检测数据：year:年度,all_num:抽样批次数量，qualified_num：合格批次数量，qualified_rat：合格率，
    unqualified：不合格数量。predictions_data为jsonarray，里面包含预测的检测合格率：year:年度，qualified_rat_predicted：预测的合格率。"""

    
    test_url = api_url+"/getBccbContent"
    test_data = {"areaName": areaName, "cpname": cpname,"token":api_key,"mdName":"get_monitor_predictions_data"}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    jj = json.dumps(result, ensure_ascii=False, indent=4)

    return [TextContent(type="text", text=jj)]

def get_risk_agricultural_products(areaName: str,year:int) -> list[TextContent]:
    """根据区划：areaName，年度：year，获得该地区检测合格率较低的农产品(风险农产品)。
    返回json格式数据，其中list为jsonarray，里面包含sampid:产品id,name:产品名称，zcs：抽检数量，cs：不合格数量。"""

    
    test_url = api_url+"/mcp_server2/cellphone/getData.do?sysCmd=getFxpz"
    test_data = {"areaName": areaName, "year":year,"token":api_key,"mdName":"get_risk_agricultural_products"}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    jj = json.dumps(result, ensure_ascii=False, indent=4)

    return [TextContent(type="text", text=jj)]

def get_hgz_num(areaName: str,year:int,cpname:str) -> list[TextContent]:
    """根据区划：areaName，年度：year，cpname:产品名称，获得该地区合格证开具批次数量。其中：年度和产品名称不必填。
    返回json格式数据，其中list为jsonarray，里面包含year:年度,num:批次，dyzs：打印张数。"""

    
    test_url = api_url+"/mcp_server2/cellphone/getData.do?sysCmd=getHgzNum"
    test_data = {"areaName": areaName, "year":year,"cpname":cpname,"token":api_key,"mdName":"get_hgz_num"}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    jj = json.dumps(result, ensure_ascii=False, indent=4)

    return [TextContent(type="text", text=jj)]



def get_sale_buy_num(areaName: str,name:str,year:int) -> list[TextContent]:
    """根据区划：areaName和农资产品名称或者分类：name，年度：year,获得该地区该农资产品的进货量和销售量。其中年度不必填。
    返回json格式数据，其中list为jsonarray，里面包含year：年份,totalBuy：进货量kg，totalSale：销售量kg。"""

    
    test_url = api_url+"/mcp_server1/api/zzchat/sale_buy_num.do"
    test_data = {"areaName": areaName, "name": name,"year":year,"token":api_key,"mdName":"get_sale_buy_num"}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    jj = json.dumps(result, ensure_ascii=False, indent=4)

    return [TextContent(type="text", text=jj)]

def getNzdByYpName(areaName: str,name:str,lon:str,lat:str) -> list[TextContent]:
    """根据区划：areaName(如：浙江省或金华市或义乌市或上溪镇，最小区划到乡镇级)，
    农资产品名称：name，
    经度：lon(如：120.111111)，纬度：lat(如：30.111111)
    获得该地区售卖该农资产品的农资店信息，农资产品信息，以及根据提供的经纬度和农资店的距离信息。
    比如：用户想知道哪里可以购买到某某农资产品，可以使用该工具。
    返回json格式数据，其中list为jsonarray，里面包含nzdname：农资店名称,nzdaddress：农资店地址，
    nzdlxdh：农资店联系电话，name：农资产品名称，guig：农资产品规格，price：农资产品价格，
    xl：农资产品销量，kc：农资产品库存，
    longitude：农资店所在地经度,latitude：农资店所在地纬度,jl：距离(km)。
    """
    
    test_url = api_url+"/mcp_server1/api/zzchat/getNzdByYpName.do"
    test_data = {"areaName": areaName, "name": name,"lon":lon,"lat":lat,"token":api_key,"mdName":"getNzdByYpName"}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    jj = json.dumps(result, ensure_ascii=False, indent=4)

    return [TextContent(type="text", text=jj)]

def getZtfp(areaName: str,year:int) -> list[TextContent]:
    """根据区划：areaName和年度：year,获得该地区主推配方肥流通量。其中年度不必填。
    返回json格式数据，其中list为jsonarray，里面包含year：年份,at：流通量(吨)。"""
    
    test_url = api_url+"/mcp_server1/api/zzchat/getZtfp.do"
    test_data = {"areaName": areaName, "year":year,"token":api_key,"mdName":"getZtfp"}
    # 发送请求
    result = post_form_request(test_url, test_data)
    jj = json.dumps(result, ensure_ascii=False, indent=4)

    return [TextContent(type="text", text=jj)]


def get_agricultural_guidance_vector(text: str) -> list[TextContent]:
    """根据用户的问题：text从农事指导的向量库中查找出几段最近似的内容，需要你归纳总结形成答案给用户。
    返回json格式数据，其中data为jsonarray，里面包含content：近似的内容。
    从content中选取跟用户的问题相关的内容总结后返回给用户，无关的舍弃不要。
    """

    test_url = api_url+"/getNszdContent"
    test_data = {"text": text,"token":api_key,"tag":"nszd","mdName":"get_agricultural_guidance_vector"}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    jj = json.dumps(result, ensure_ascii=False, indent=4)

    return [TextContent(type="text", text=jj)]

def get_agricultural_disease_vector(text: str) -> list[TextContent]:
    """根据用户的问题：text从病虫测报的向量库中查找出几段最近似的内容，需要你归纳总结形成答案给用户。
    返回json格式数据，其中data为jsonarray，里面包含content：近似的内容。
    从content中选取跟用户的问题相关的内容总结后返回给用户，无关的舍弃不要。
    """


    test_url = api_url+"/getNszdContent"
    test_data = {"text": text,"token":api_key,"tag":"bccb","mdName":"get_agricultural_disease_vector"}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    jj = json.dumps(result, ensure_ascii=False, indent=4)

    return [TextContent(type="text", text=jj)]

def get_agricultural_case_vector(text: str) -> list[TextContent]:
    """根据用户的问题：text从农业典型案件的向量库中查找出几段最近似的内容，需要你归纳总结形成答案给用户。
    返回json格式数据，其中data为jsonarray，里面包含content：近似的内容。
    从content中选取跟用户的问题相关的内容总结后返回给用户，无关的舍弃不要。
    """

    test_url = api_url+"/getNszdContent"
    test_data = {"text": text,"token":api_key,"tag":"nydxal","mdName":"get_agricultural_case_vector"}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    jj = json.dumps(result, ensure_ascii=False, indent=4)

    return [TextContent(type="text", text=jj)]


def get_agricultural_growth_vector(text: str) -> list[TextContent]:
    """根据用户的问题：text从农作物生长模式(如：生长环境选择，品种选择，生长期注意事项等)的向量库中查找出几段最近似的内容，需要你归纳总结形成答案给用户。
    返回json格式数据，其中data为jsonarray，里面包含content：近似的内容。
    从content中选取跟用户的问题相关的内容总结后返回给用户，无关的舍弃不要。
    """

    test_url = api_url+"/getNszdContent"
    test_data = {"text": text,"token":api_key,"tag":"szms","mdName":"get_agricultural_growth_vector"}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    jj = json.dumps(result, ensure_ascii=False, indent=4)

    return [TextContent(type="text", text=jj)]

def get_agricultural_encyclopedia(text: str) -> list[TextContent]:
    """根据用户的问题：text从农业百科（包含：兽医,植物病理学,养蜂,土壤,水利,水产业,蔬菜,生物学,森林工业,农作物,农业气象,农业历史,农业经济,
    农业机械化,农业化学,农业工程,农药,林业,昆虫,果树,观赏园艺,畜牧业,茶业,蚕业等）的向量库中查找出几段最近似的内容，需要你归纳总结形成答案给用户。
    返回json格式数据，其中data为jsonarray，里面包含content：近似的内容。
    从content中选取跟用户的问题相关的内容总结后返回给用户，无关的舍弃不要。
    注意：在使用其他工具无法很好的回答用户提出的关于农业方面的问题，可使用该工具。
    """

    test_url = api_url+"/getNszdContent"
    test_data = {"text": text,"token":api_key,"tag":"bkqs","mdName":"get_agricultural_encyclopedia"}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    jj = json.dumps(result, ensure_ascii=False, indent=4)

    return [TextContent(type="text", text=jj)]


async def list_tools() -> list[types.Tool]:
    """
    列出所有可用的工具。
    
    Args:
        None.
    
    Returns:
        list (types.Tool): 包含了所有可用的工具, 每个工具都包含了名称、描述、输入schema三个属性.
    """
    return [

        types.Tool(
            name="getNyInfo",
            description="根据农药名称：name和登记证号：djzh，获得该农药的基本信息,登记证号不必填。返回json格式数据，其中list为jsonarray，里面包含hzrq：核准日期，ccysff：储存和运输方法，shengCQY：登记证持有人(生产企业)，dux：毒性，description：备注，cpxn：产品性能，yxqz：有效期至，nylb：农药类别，zxhzrq：重新核准日期，name：农药名称，jix：剂型，zdjjcs：中毒急救措施，bzq：质量保证期，djzh：登记证号，zyxcfhl：总有效成分含量，zysx：注意事项，syjsyq：使用技术要求。",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "农药名称"},
                    "djzh": {"type": "string", "description": "登记证号"}
                },
                "required": ["name"],
            },
        ),
        types.Tool(
            name="getNyChengF",
            description="根据农药名称：name和登记证号：djzh，获得该农药的主要有效成分,登记证号不必填。返回json格式数据，其中list为jsonarray，里面包含name_cn：有效成分中文名，name_en：有效成分英文名，hanl：有效成分含量。",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "农药名称"},
                    "djzh": {"type": "string", "description": "登记证号"}
                },
                "required": ["name"],
            },
        ),
        types.Tool(
            name="getNyShengCQY",
            description="根据农药名称：name和登记证号：djzh，获得该农药的生产企业信息,登记证号不必填。返回json格式数据，其中list为jsonarray，里面包含name：企业名称，province：企业所在省份，country：企业所在国家，county：企业所在县，postcode：邮编，tel：电话，fox：传真，contact：联系人，phone：手机号码，addr：单位地址，email：邮箱。",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "农药名称"},
                    "djzh": {"type": "string", "description": "登记证号"}
                },
                "required": ["name"],
            },
        ),
        types.Tool(
            name="getNyUseInfo",
            description="根据农药名称：name和登记证号：djzh，获得该农药的使用范围和使用方法,登记证号不必填。返回json格式数据，其中list为jsonarray，里面包含crops：作物/场所，fzdx：防治对象，dosage：用药量（制剂量/亩），syff：施用方法。",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "农药名称"},
                    "djzh": {"type": "string", "description": "登记证号"}
                },
                "required": ["name"],
            },
        ),

        types.Tool(
            name="getNyInfoByScqy",
            description="根据生产企业名称：scqy，获得该生产企业生产哪些农药。返回json格式数据，其中list为jsonarray，里面包含name：农药名称。",
            inputSchema={
                "type": "object",
                "properties": {
                    "scqy": {"type": "string", "description": "生产企业"}
                },
                "required": ["scqy"],
            },
        ),

        types.Tool(
            name="getFzffByCropFzdx",
            description="根据农作物名称：crop和病虫害名称：fzdx，获得防治药物及使用方法。返回json格式数据，其中list为jsonarray，里面包含name：药物名称，dosage：用药量（制剂量/亩），syff：施用方法。",
            inputSchema={
                "type": "object",
                "properties": {
                    "crop": {"type": "string", "description": "农作物名称"},
                    "fzdx": {"type": "string", "description": "病虫害名称"}
                },
                "required": ["crop","fzdx"],
            },
        ),

        types.Tool(
            name="getPlantWeather",
            description="根据农作物名称：plant，获得该农作物适合的种植气候以及包含城市。返回json格式数据，其中list为jsonarray，里面包含weather：气候，city：城市。",
            inputSchema={
                "type": "object",
                "properties": {
                    "plant": {"type": "string", "description": "农作物名称"}
                },
                "required": ["plant"],
            },
        ),

        types.Tool(
            name="getCityWeather",
            description="根据城市名称：city，获得该城市的气候以及适合种植的作物。返回json格式数据，其中list为jsonarray，里面包含weather：气候，plant：作物。",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称"}
                },
                "required": ["city"],
            },
        ),

        types.Tool(
            name="get_medication_value",
            description="根据农产品名称：productName和药物名称：medicationName，获得该农产品上的该药物的检出限(检出上限)。返回json格式数据，其中list为jsonarray，里面包含unit：单位，pd：检出限，aname：药物名称，name：农产品名称，value：检出限具体的值。",
            inputSchema={
                "type": "object",
                "properties": {
                    "productName": {"type": "string", "description": "农产品名称"},
                    "medicationName": {"type": "string", "description": "药物名称"}
                },
                "required": ["productName","medicationName"],
            },
        ),


        types.Tool(
            name="get_monitor_info",
            description="根据区划：areaName，农产品名称：cpname，年度：year，获得该地区该农产品的检测合格率。其中年度不必填。返回json格式数据，其中list为jsonarray，里面包含year:年度,all_num:抽样批次数量，qualified_num：合格批次数量，qualified_rat：合格率，unqualified：不合格数量。",
            inputSchema={
                "type": "object",
                "properties": {
                    "areaName": {"type": "string", "description": "区划"},
                    "cpname": {"type": "string", "description": "农产品名称"},
                    "year": {"type": "integer", "description": "年度"}
                },
                "required": ["areaName","cpname"],
            },
        ),

        types.Tool(
            name="get_monitor_task_info",
            description="根据区划：areaName和任务：taskName，获得该地区该监测任务的完成情况，并给出下一年的任务安排建议。返回json格式的数据，详细内容都在message字段中。",
            inputSchema={
                "type": "object",
                "properties": {
                    "areaName": {"type": "string", "description": "区划"},
                    "taskName": {"type": "string", "description": "任务"}
                },
                "required": ["areaName","taskName"],
            },
        ),

        types.Tool(
            name="get_monitor_predictions_data",
            description="根据区划：areaName，农产品名称：cpname，预测该地区该农产品未来几年的检测合格率。返回json格式数据，其中history_data为jsonarray，里面包含历史检测数据：year:年度,all_num:抽样批次数量，qualified_num：合格批次数量，qualified_rat：合格率，unqualified：不合格数量。predictions_data为jsonarray，里面包含预测的检测合格率：year:年度，qualified_rat_predicted：预测的合格率。",
            inputSchema={
                "type": "object",
                "properties": {
                    "areaName": {"type": "string", "description": "区划"},
                    "cpname": {"type": "string", "description": "农产品名称"}
                },
                "required": ["areaName","cpname"],
            },
        ),

        types.Tool(
            name="get_risk_agricultural_products",
            description="根据区划：areaName，年度：year，获得该地区检测合格率较低的农产品(风险农产品)。返回json格式数据，其中list为jsonarray，里面包含sampid:产品id,name:产品名称，zcs：抽检数量，cs：不合格数量。",
            inputSchema={
                "type": "object",
                "properties": {
                    "areaName": {"type": "string", "description": "区划"},
                    "year": {"type": "integer", "description": "年度"}
                },
                "required": ["areaName","year"],
            },
        ),
        types.Tool(
            name="get_hgz_num",
            description="根据区划：areaName，年度：year，cpname:产品名称，获得该地区合格证开具批次数量。其中：年度和产品名称不必填。返回json格式数据，其中list为jsonarray，里面包含year:年度,num:批次，dyzs：打印张数。",
            inputSchema={
                "type": "object",
                "properties": {
                    "areaName": {"type": "string", "description": "区划"},
                    "year": {"type": "integer", "description": "年度"},
                    "cpname": {"type": "string", "description": "农产品名称"}
                },
                "required": ["areaName"],
            },
        ),
        types.Tool(
            name="get_sale_buy_num",
            description="根据区划：areaName和农资产品名称或者分类：name，年度：year,获得该地区该农资产品的进货量和销售量。其中年度不必填。返回json格式数据，其中list为jsonarray，里面包含year：年份,totalBuy：进货量kg，totalSale：销售量kg。",
            inputSchema={
                "type": "object",
                "properties": {
                    "areaName": {"type": "string", "description": "区划"},
                    "name": {"type": "string", "description": "农资产品名称"},
                    "year": {"type": "integer", "description": "年度"}
                },
                "required": ["areaName","name"],
            },
        ),
        types.Tool(
            name="getNzdByYpName",
            description="根据区划：areaName(如：浙江省或金华市或义乌市或上溪镇，最小区划到乡镇级)，农资产品名称：name，经度：lon(如：120.111111)，纬度：lat(如：30.111111)获得该地区售卖该农资产品的农资店信息，农资产品信息，以及根据提供的经纬度和农资店的距离信息。比如：用户想知道哪里可以购买到某某农资产品，可以使用该工具。返回json格式数据，其中list为jsonarray，里面包含nzdname：农资店名称,nzdaddress：农资店地址，nzdlxdh：农资店联系电话，name：农资产品名称，guig：农资产品规格，price：农资产品价格，xl：农资产品销量，kc：农资产品库存，longitude：农资店所在地经度,latitude：农资店所在地纬度,jl：距离(km)。",
            inputSchema={
                "type": "object",
                "properties": {
                    "areaName": {"type": "string", "description": "区划"},
                    "name": {"type": "string", "description": "农资产品名称"},
                    "lon": {"type": "string", "description": "用户提供地址的经度"},
                    "lat": {"type": "string", "description": "用户提供地址的纬度"}
                },
                "required": ["areaName","name"],
            },
        ),

        types.Tool(
            name="getZtfp",
            description="根据区划：areaName和年度：year,获得该地区主推配方肥流通量。其中年度不必填。返回json格式数据，其中list为jsonarray，里面包含year：年份,at：流通量(吨)。",
            inputSchema={
                "type": "object",
                "properties": {
                    "areaName": {"type": "string", "description": "区划"},
                    "year": {"type": "integer", "description": "年度"}
                },
                "required": ["areaName"],
            },
        ),
        
        types.Tool(
            name="get_agricultural_guidance_vector",
            description="根据用户的问题：text从农事指导的向量库中查找出几段最近似的内容，需要你归纳总结形成答案给用户。返回json格式数据，其中data为jsonarray，里面包含content：近似的内容。从content中选取跟用户的问题相关的内容总结后返回给用户，无关的舍弃不要。",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "用户的问题"}
                },
                "required": ["text"],
            },
        ),
        types.Tool(
            name="get_agricultural_disease_vector",
            description="根据用户的问题：text从病虫测报的向量库中查找出几段最近似的内容，需要你归纳总结形成答案给用户。返回json格式数据，其中data为jsonarray，里面包含content：近似的内容。从content中选取跟用户的问题相关的内容总结后返回给用户，无关的舍弃不要。",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "用户的问题"}
                },
                "required": ["text"],
            },
        ),

        types.Tool(
            name="get_agricultural_case_vector",
            description="根据用户的问题：text从农业典型案件的向量库中查找出几段最近似的内容，需要你归纳总结形成答案给用户。返回json格式数据，其中data为jsonarray，里面包含content：近似的内容。从content中选取跟用户的问题相关的内容总结后返回给用户，无关的舍弃不要。",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "用户的问题"}
                },
                "required": ["text"],
            },
        ),
        types.Tool(
            name="get_agricultural_growth_vector",
            description="根据用户的问题：text从农作物生长模式(如：生长环境选择，品种选择，生长期注意事项等)的向量库中查找出几段最近似的内容，需要你归纳总结形成答案给用户。返回json格式数据，其中data为jsonarray，里面包含content：近似的内容。从content中选取跟用户的问题相关的内容总结后返回给用户，无关的舍弃不要。",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "用户的问题"}
                },
                "required": ["text"],
            },
        ),

        types.Tool(
            name="get_agricultural_encyclopedia",
            description="根据用户的问题：text从农业百科（包含：兽医,植物病理学,养蜂,土壤,水利,水产业,蔬菜,生物学,森林工业,农作物,农业气象,农业历史,农业经济,农业机械化,农业化学,农业工程,农药,林业,昆虫,果树,观赏园艺,畜牧业,茶业,蚕业等）的向量库中查找出几段最近似的内容，需要你归纳总结形成答案给用户。返回json格式数据，其中data为jsonarray，里面包含content：近似的内容。从content中选取跟用户的问题相关的内容总结后返回给用户，无关的舍弃不要。注意：在使用其他工具无法很好的回答用户提出的关于农业方面的问题，可使用该工具。",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "用户的问题"}
                },
                "required": ["text"],
            },
        ),
        
        types.Tool(
            name="get_now_time",
            description="获取当前时间",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
    ]


async def call_tool_x(name: str, arguments: dict) -> list[TextContent]:

    if name == "getNyInfo":
        name = arguments.get("name")
        djzh = arguments.get("djzh")
        return getNyInfo(name,djzh)
    elif name == "getNyChengF":
        name = arguments.get("name")
        djzh = arguments.get("djzh")
        return getNyChengF(name,djzh)
    elif name == "getNyShengCQY":
        name = arguments.get("name")
        djzh = arguments.get("djzh")
        return getNyShengCQY(name,djzh)
    elif name == "getNyUseInfo":
        name = arguments.get("name")
        djzh = arguments.get("djzh")
        return getNyUseInfo(name,djzh)
    elif name == "getNyInfoByScqy":
        scqy = arguments.get("scqy")
        return getNyInfoByScqy(scqy)
    elif name == "getFzffByCropFzdx":
        crop = arguments.get("crop")
        fzdx = arguments.get("fzdx")
        return getFzffByCropFzdx(crop,fzdx)
    elif name == "getPlantWeather":
        plant = arguments.get("plant")
        return getPlantWeather(plant)
    elif name == "getFzffByCropFzdx":
        city = arguments.get("city")
        return getFzffByCropFzdx(city)
    elif name == "get_medication_value":
        productName = arguments.get("productName")
        medicationName = arguments.get("medicationName")
        return get_medication_value(productName,medicationName)
    elif name == "get_monitor_info":
        areaName = arguments.get("areaName")
        cpname = arguments.get("cpname")
        year = arguments.get("year")
        return get_monitor_info(areaName,cpname,year)
    elif name == "get_monitor_task_info":
        areaName = arguments.get("areaName")
        taskName = arguments.get("taskName")
        return get_monitor_task_info(areaName,taskName)
    elif name == "get_monitor_predictions_data":
        areaName = arguments.get("areaName")
        cpname = arguments.get("cpname")
        return get_monitor_predictions_data(areaName,cpname)
    elif name == "get_risk_agricultural_products":
        areaName = arguments.get("areaName")
        year = arguments.get("year")
        return get_risk_agricultural_products(areaName,year)
    elif name == "get_hgz_num":
        areaName = arguments.get("areaName")
        year = arguments.get("year")
        cpname = arguments.get("cpname")
        return get_hgz_num(areaName,year,cpname)
    elif name == "get_sale_buy_num":
        areaName = arguments.get("areaName")
        name = arguments.get("name")
        year = arguments.get("year")
        return get_sale_buy_num(areaName,name,year)
    elif name == "getNzdByYpName":
        areaName = arguments.get("areaName")
        name = arguments.get("name")
        lon = arguments.get("lon")
        lat = arguments.get("lat")
        return getNzdByYpName(areaName,name,lon,lat)
    elif name == "getZtfp":
        areaName = arguments.get("areaName")
        year = arguments.get("year")
        return getZtfp(areaName,year)
    elif name == "get_agricultural_guidance_vector":
        text = arguments.get("text")
        return get_agricultural_guidance_vector(text)
    elif name == "get_agricultural_disease_vector":
        text = arguments.get("text")
        return get_agricultural_disease_vector(text)
    elif name == "get_agricultural_case_vector":
        text = arguments.get("text")
        return get_agricultural_case_vector(text)
    elif name == "get_agricultural_growth_vector":
        text = arguments.get("text")
        return get_agricultural_growth_vector(text)
    elif name == "get_agricultural_encyclopedia":
        text = arguments.get("text")
        return get_agricultural_encyclopedia(text)
    elif name == "get_now_time":
        return get_now_time()
    
    raise ValueError(f"未知的工具: {name}")

# 注册list_tools方法
mcp._mcp_server.list_tools()(list_tools)
# 注册call_tool_x方法
mcp._mcp_server.call_tool()(call_tool_x)

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()