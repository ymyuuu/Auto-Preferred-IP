import json
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.dnspod.v20210323 import dnspod_client, models

class QcloudApiV3:
    def __init__(self, secret_id, secret_key):
        # 初始化 QcloudApiV3 类，并传入腾讯云 API 的凭据。
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.cred = credential.Credential(secret_id, secret_key)
        self.client = dnspod_client.DnspodClient(self.cred, "")
        self.error_response = {"code": 0, "message": "None"}

    def _format_record(self, record):
        new_record = {}
        record["id"] = record['RecordId']
        for key in record:
            new_record[key.lower()] = record[key]
        return new_record

    def _get_domain_info(self, domain):
        req = models.DescribeDomainRequest()
        params = {"Domain": domain}
        req.from_json_string(json.dumps(params))
        resp = self.client.DescribeDomain(req)
        return json.loads(resp.to_json_string())

    def del_record(self, domain, record_id):
        # 删除 DNS 记录。
        try:
            req_model = models.DeleteRecordRequest()
            params = {"Domain": domain, "RecordId": record_id}
            req_model.from_json_string(json.dumps(params))
            resp = self.client.DeleteRecord(req_model)
            return json.loads(resp.to_json_string())
        except TencentCloudSDKException:
            return self.error_response

    def get_record(self, domain, length, sub_domain, record_type):
        try:
            req_model = models.DescribeRecordListRequest()
            params = {
                "Domain": domain,
                "Subdomain": sub_domain,
                "RecordType": record_type,
                "Limit": length
            }
            req_model.from_json_string(json.dumps(params))
            resp = self.client.DescribeRecordList(req_model)
            resp_data = {"code": 0, "data": {"records": []}}

            # 格式化每个记录并添加到响应中。
            for record in json.loads(resp.to_json_string())['RecordList']:
                resp_data["data"]["records"].append(self._format_record(record))

            resp_data["data"]["domain"] = {"grade": self._get_domain_info(domain)["DomainInfo"]["Grade"]}
            return resp_data
        except TencentCloudSDKException:
            return self.error_response

    def create_record(self, domain, sub_domain, value, record_type="A", line="默认", ttl=600):
        # 创建 DNS 记录。
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

        try:
            resp = self.client.CreateRecord(req)
            return json.loads(resp.to_json_string())
        except TencentCloudSDKException:
            return self.error_response

    def change_record(self, domain, record_id, sub_domain, value, record_type="A", line="默认", ttl=600):
        # 修改 DNS 记录。
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

        try:
            resp = self.client.ModifyRecord(req)
            return json.loads(resp.to_json_string())
        except TencentCloudSDKException:
            return self.error_response
