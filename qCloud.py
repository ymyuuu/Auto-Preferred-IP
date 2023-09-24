import json
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.dnspod.v20210323 import dnspod_client, models

class QcloudApiv3():
    def __init__(self, SECRETID, SECRETKEY):
        # 初始化 QcloudApiv3 类，并传入腾讯云 API 的凭据。
        self.SecretId = SECRETID
        self.secretKey = SECRETKEY
        self.cred = credential.Credential(SECRETID, SECRETKEY)

    def del_record(self, domain: str, record_id: int):
        # 删除 DNS 记录。
        client = dnspod_client.DnspodClient(self.cred, "")
        req_model = models.DeleteRecordRequest()
        params = {
            "Domain": domain,
            "RecordId": record_id
        }
        req_model.from_json_string(json.dumps(params))

        resp = client.DeleteRecord(req_model)

        # 将响应转换为 JSON 格式，并添加自定义的 code 和 message 字段。
        resp = json.loads(resp.to_json_string())
        resp["code"] = 0
        resp["message"] = "None"
        return resp

    def get_record(self, domain: str, length: int, sub_domain: str, record_type: str):
        def format_record(record: dict):
            new_record = {}
            record["id"] = record['RecordId']
            for key in record:
                new_record[key.lower()] = record[key]
            return new_record

        try:
            client = dnspod_client.DnspodClient(self.cred, "")

            req_model = models.DescribeRecordListRequest()
            params = {
                "Domain": domain,
                "Subdomain": sub_domain,
                "RecordType": record_type,
                "Limit": length
            }
            req_model.from_json_string(json.dumps(params))

            resp = client.DescribeRecordList(req_model)
            resp = json.loads(resp.to_json_string())

            temp_resp = {}
            temp_resp["code"] = 0
            temp_resp["data"] = {}
            temp_resp["data"]["records"] = []

            # 格式化每个记录并添加到响应中。
            for record in resp['RecordList']:
                temp_resp["data"]["records"].append(format_record(record))

            temp_resp["data"]["domain"] = {}
            temp_resp["data"]["domain"]["grade"] = self.get_domain(domain)["DomainInfo"]["Grade"]  # DP_Free
            return temp_resp

        except TencentCloudSDKException:
            temp_resp = {}
            temp_resp["code"] = 0
            temp_resp["data"] = {}
            temp_resp["data"]["records"] = {}
            temp_resp["data"]["domain"] = {}
            temp_resp["data"]["domain"]["grade"] = self.get_domain(domain)["DomainInfo"]["Grade"]  # DP_Free
            return temp_resp

    def create_record(self, domain: str, sub_domain: str, value: int, record_type: str = "A", line: str = "默认", ttl: int = 600):
        # 创建 DNS 记录。
        client = dnspod_client.DnspodClient(self.cred, "")
        req = models.CreateRecordRequest()
        params = {
            "Domain": domain,
            "SubDomain": sub_domain,
            "RecordType": record_type,
            "RecordLine": line,
            "Value": value,
            "ttl": ttl
        }
        req.from_json_string(json.dumps(params))

        resp = client.CreateRecord(req)

        # 将响应转换为 JSON 格式，并添加自定义的 code 和 message 字段。
        resp = json.loads(resp.to_json_string())
        resp["code"] = 0
        resp["message"] = "None"
        return resp

    def change_record(self, domain: str, record_id: int, sub_domain: str, value: str, record_type: str = "A", line: str = "默认", ttl: int = 600):
        # 修改 DNS 记录。
        client = dnspod_client.DnspodClient(self.cred, "")
        req = models.ModifyRecordRequest()
        params = {
            "Domain": domain,
            "SubDomain": sub_domain,
            "RecordType": record_type,
            "RecordLine": line,
            "Value": value,
            "TTL": ttl,
            "RecordId": record_id
        }
        req.from_json_string(json.dumps(params))

        resp = client.ModifyRecord(req)

        # 将响应转换为 JSON 格式，并添加自定义的 code 和 message 字段。
        resp = json.loads(resp.to_json_string())
        resp["code"] = 0
        resp["message"] = "None"
        return resp

    def get_domain(self, domain: str):
        # 获取域名信息。
        client = dnspod_client.DnspodClient(self.cred, "")
        req = models.DescribeDomainRequest()
        params = {
            "Domain": domain
        }
        req.from_json_string(json.dumps(params))

        resp = client.DescribeDomain(req)
        resp = json.loads(resp.to_json_string())
        return resp
