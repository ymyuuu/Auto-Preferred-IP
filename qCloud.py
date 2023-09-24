import json
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.dnspod.v20210323 import dnspod_client, models

class QcloudApiv3():
    def __init__(self, SECRETID, SECRETKEY):
        # 初始化对象时设置SecretId和SecretKey
        self.SecretId = SECRETID
        self.SecretKey = SECRETKEY
        # 创建Tencent Cloud Credential对象
        self.cred = credential.Credential(SECRETID, SECRETKEY)
        # 创建Tencent Cloud DnspodClient对象
        self.client = dnspod_client.DnspodClient(self.cred, "")

    def _handle_exception(self, domain):
        try:
            # 获取域名信息，如果发生异常则返回一个默认的域名信息
            domain_info = self.get_domain(domain)
        except TencentCloudSDKException:
            domain_info = {"DomainInfo": {"Grade": "DP_Free"}}
        return domain_info

    def del_record(self, domain: str, record_id: int):
        # 创建删除记录请求对象
        req_model = models.DeleteRecordRequest(Domain=domain, RecordId=record_id)
        try:
            # 发送删除记录请求
            resp = self.client.DeleteRecord(req_model)
        except TencentCloudSDKException:
            # 如果发生异常，返回一个默认的响应
            return {"code": 0, "message": "None"}

        # 返回成功响应
        return {"code": 0, "message": "None"}

    def get_record(self, domain: str, length: int, sub_domain: str, record_type: str):
        def format_record(record: dict):
            return {key.lower(): record[key] for key in record}

        # 创建获取记录列表请求对象
        req_model = models.DescribeRecordListRequest(Domain=domain, Subdomain=sub_domain,
                                                     RecordType=record_type, Limit=length)

        try:
            # 发送获取记录列表请求
            resp = self.client.DescribeRecordList(req_model)
        except TencentCloudSDKException:
            # 如果发生异常，获取默认的域名信息
            domain_info = self._handle_exception(domain)
            # 返回一个默认的响应
            return {"code": 0, "data": {"records": [], "domain": domain_info["DomainInfo"]["Grade"]}}

        # 格式化记录列表并获取域名信息
        records = [format_record(record) for record in resp.RecordList]
        domain_info = self._handle_exception(domain)
        # 返回成功响应
        return {"code": 0, "data": {"records": records, "domain": domain_info["DomainInfo"]["Grade"]}}

    def create_record(self, domain: str, sub_domain: str, value: int, record_type: str = "A", line: str = "默认", ttl: int = 600):
        # 创建创建记录请求对象
        req = models.CreateRecordRequest(Domain=domain, SubDomain=sub_domain, RecordType=record_type,
                                         RecordLine=line, Value=value, TTL=ttl)

        try:
            # 发送创建记录请求
            resp = self.client.CreateRecord(req)
        except TencentCloudSDKException:
            # 如果发生异常，返回一个默认的响应
            return {"code": 0, "message": "None"}

        # 返回成功响应
        return {"code": 0, "message": "None"}

    def change_record(self, domain: str, record_id: int, sub_domain: str, value: str, record_type: str = "A", line: str = "默认", ttl: int = 600):
        # 创建修改记录请求对象
        req = models.ModifyRecordRequest(Domain=domain, SubDomain=sub_domain, RecordType=record_type,
                                         RecordLine=line, Value=value, TTL=ttl, RecordId=record_id)

        try:
            # 发送修改记录请求
            resp = self.client.ModifyRecord(req)
        except TencentCloudSDKException:
            # 如果发生异常，返回一个默认的响应
            return {"code": 0, "message": "None"}

        # 返回成功响应
        return {"code": 0, "message": "None"}

    def get_domain(self, domain: str):
        # 创建获取域名信息请求对象
        req = models.DescribeDomainRequest(Domain=domain)

        try:
            # 发送获取域名信息请求
            resp = self.client.DescribeDomain(req)
        except TencentCloudSDKException:
            # 如果发生异常，返回一个空字典
            return {}

        # 返回域名信息
        return resp
