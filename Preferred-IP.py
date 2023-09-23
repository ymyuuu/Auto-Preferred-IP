import random
import time
import json
import requests
import os
import traceback
from qCloud import QcloudApiv3
import sys
import logging
import base64  

# 配置参数
CONFIG = {
    "KEY": base64.b64decode("bzF6cm1IQUY=").decode('utf-8'),  
    "DOMAINS": json.loads(os.environ.get("DOMAINS", "{}")),
    "SECRETID": os.environ.get("SECRETID"),
    "SECRETKEY": os.environ.get("SECRETKEY"),
    "AFFECT_NUM": 2,
    "TTL": 600,
    "RECORD_TYPE": sys.argv[1] if len(sys.argv) >= 2 else "A",
}

logging.basicConfig(level=logging.INFO, format="%(message)s")
successful_domains = set()

# 获取优选IP的函数
def get_optimization_ip():
    try:
        headers = {'Content-Type': 'application/json'}
        data = {"key": CONFIG["KEY"], "type": "v4" if CONFIG["RECORD_TYPE"] == "A" else "v6"}
        response = requests.post(base64.b64decode("aHR0cHM6Ly9hcGkuaG9zdG1vbml0LmNvbS9nZXRfb3B0aW1pemF0aW9uX2lw").decode('utf-8'), json=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error("获取优选IP错误: 请求状态码不为200")
            return None
    except Exception as e:
        logging.error("获取优选IP错误: " + str(e))
        return None

# 修改DNS的函数
def change_dns(cloud, line, s_info, c_info, domain, sub_domain):
    lines = {"CM": "移动", "CU": "联通", "CT": "电信", "AB": "境外", "DEF": "默认"}
    line = lines[line]

    try:
        create_num = CONFIG["AFFECT_NUM"] - len(s_info)
        if create_num == 0:
            for info in s_info:
                if len(c_info) == 0:
                    break
                cf_ip = c_info.pop(random.randint(0, len(c_info) - 1))["ip"]
                if cf_ip in str(s_info):
                    continue
                ret = cloud.change_record(domain, info["recordId"], sub_domain, cf_ip, CONFIG["RECORD_TYPE"], line, CONFIG["TTL"])
                if ret["code"] == 0:
                    logging.info("成功更新DNS记录——时间:%s, 解析线路=%s, 记录ID=%s, 值=%s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 8 * 3600)), line, info["recordId"], cf_ip))
                    successful_domains.add(domain)
                else:
                    logging.error("更新DNS记录失败——时间:%s, 解析线路=%s, 记录ID=%s, 值=%s, 错误信息=%s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 8 * 3600)), line, info["recordId"], cf_ip, ret["message"]))
        elif create_num > 0:
            for i in range(create_num):
                if len(c_info) == 0:
                    break
                cf_ip = c_info.pop(random.randint(0, len(c_info) - 1))["ip"]
                if cf_ip in str(s_info):
                    continue
                ret = cloud.create_record(domain, sub_domain, cf_ip, CONFIG["RECORD_TYPE"], line, CONFIG["TTL"])
                if ret["code"] == 0:
                    logging.info("成功创建DNS记录——时间:%s, 解析线路=%s, 值=%s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 8 * 3600)), line, cf_ip))
                    successful_domains.add(domain)
                else:
                    logging.error("创建DNS记录失败——时间:%s, 解析线路=%s, 值=%s, 错误信息=%s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 8 * 3600)), line, cf_ip, ret["message"]))
        else:
            for info in s_info:
                if create_num == 0 or len(c_info) == 0:
                    break
                cf_ip = c_info.pop(random.randint(0, len(c_info) - 1))["ip"]
                if cf_ip in str(s_info):
                    create_num += 1
                    continue
                ret = cloud.change_record(domain, info["recordId"], sub_domain, cf_ip, CONFIG["RECORD_TYPE"], line, CONFIG["TTL"])
                if ret["code"] == 0:
                    logging.info("成功更新DNS记录——时间:%s, 解析线路=%s, 记录ID=%s, 值=%s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 8 * 3600)), line, info["recordId"], cf_ip))
                    successful_domains.add(domain)
                else:
                    logging.error("更新DNS记录失败——时间:%s, 解析线路=%s, 记录ID=%s, 值=%s, 错误信息=%s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 8 * 3600)), line, info["recordId"], cf_ip, ret["message"]))
                create_num += 1
    except Exception as e:
        logging.error("操作DNS记录失败——时间:%s, 错误信息=%s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 8 * 3600)), str(traceback.print_exc())))

# 主函数
def main(cloud):
    if len(CONFIG["DOMAINS"]) > 0:
        try:
            cfips = get_optimization_ip()
            if cfips is None or cfips["code"] != 200:
                logging.error("获取优选IP错误——时间:%s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 8 * 3600)))
                return
            cf_cmips = cfips["info"]["CM"]
            cf_cuips = cfips["info"]["CU"]
            cf_ctips = cfips["info"]["CT"]
            for domain, sub_domains in CONFIG["DOMAINS"].items():
                for sub_domain, lines in sub_domains.items():
                    temp_cf_cmips = cf_cmips.copy()
                    temp_cf_cuips = cf_cuips.copy()
                    temp_cf_ctips = cf_ctips.copy()
                    ret = cloud.get_record(domain, 20, sub_domain, "CNAME")
                    if ret["code"] == 0:
                        for record in ret["data"]["records"]:
                            if record["line"] in ["移动", "联通", "电信"]:
                                retMsg = cloud.del_record(domain, record["id"])
                                if retMsg["code"] == 0:
                                    logging.info("成功删除DNS记录——时间:%s, 解析线路=%s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 8 * 3600)), record["line"]))
                                else:
                                    logging.error("删除DNS记录失败——时间:%s, 解析线路=%s, 错误信息=%s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 8 * 3600)), record["line"], retMsg["message"]))
                    ret = cloud.get_record(domain, 100, sub_domain, CONFIG["RECORD_TYPE"])
                    if ret["code"] == 0:
                        if "Free" in ret["data"]["domain"]["grade"] and CONFIG["AFFECT_NUM"] > 2:
                            CONFIG["AFFECT_NUM"] = 2
                        cm_info = []
                        cu_info = []
                        ct_info = []
                        for record in ret["data"]["records"]:
                            if record["line"] == "移动":
                                info = {"recordId": record["id"], "value": record["value"]}
                                cm_info.append(info)
                            if record["line"] == "联通":
                                info = {"recordId": record["id"], "value": record["value"]}
                                cu_info.append(info)
                            if record["line"] == "电信":
                                info = {"recordId": record["id"], "value": record["value"]}
                                ct_info.append(info)
                        for line in lines:
                            if line == "CM":
                                change_dns(cloud, "CM", cm_info, temp_cf_cmips, domain, sub_domain)
                            elif line == "CU":
                                change_dns(cloud, "CU", cu_info, temp_cf_cuips, domain, sub_domain)
                            elif line == "CT":
                                change_dns(cloud, "CT", ct_info, temp_cf_ctips, domain, sub_domain)
        except Exception as e:
            logging.error("操作DNS记录失败——时间:%s, 错误信息=%s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 8 * 3600)), str(traceback.print_exc())))

    logging.info("\n优选IP已成功推送到:")
    for domain in successful_domains:
        obfuscated_domain = domain[:3] + '*' * (len(domain) - 6) + domain[-3:]  # 使用星号替换中间字符
        logging.info("域名：%s" % obfuscated_domain)

if __name__ == '__main__':
    cloud = QcloudApiv3(CONFIG["SECRETID"], CONFIG["SECRETKEY"])
    main(cloud)
