#! /usr/bin/env nix-shell
#! nix-shell -i python3 -p python3Packages.boto3 -p python3Packages.botocore -I channel:nixos-unstable
import datetime
import botocore
import boto3
import argparse
import time


def connect_boto3(region):
    _conn = boto3.session.Session().client('service-quotas', region_name=region)
    return _conn

def quota_increase_request(_conn, service_code, quota_code, desired_value):
    quotas = ""
    try:
        quotas = _conn.request_service_quota_increase(ServiceCode=service_code,QuotaCode=quota_code,
                                                        DesiredValue=desired_value)
    except botocore.exceptions.ClientError as error:
        print(error.response['Error']['Code'])
    print("--- Request Quota Id", quotas['RequestedQuota']['Id'], " -- State: ", quotas['RequestedQuota']['Status'])
    print("----------------------------------------------------------------------------------------------------")

def main():
    
    parser = argparse.ArgumentParser(
    description='Increase service quota limit')

    parser.add_argument( '-r', '--region', dest='region', metavar='', action='append', default=[],
        required=False, help='aws region')
    parser.add_argument( '-s', '--service-code', dest='service_code',  metavar='', required=True,
                        help='aws service code for which to increase quota (ex: vpc).')
    parser.add_argument( '-q', '--quota-code', dest='quota_code', metavar='', required=True,
                        help='service to which to increase quota')
    parser.add_argument( '-d', '--desired-value', dest='desired_value', metavar='', required=True, help='Quota increase desired value')
    args = parser.parse_args()

    regions = args.region
    service_code = args.service_code
    quota_code = args.quota_code
    desired_value = int(args.desired_value)

    if regions == []:
        # all regions
        regions = ["eu-north-1" ,"ap-south-1" ,"eu-west-3" ,"eu-west-2" ,"eu-west-1" ,"ap-northeast-2" ,"ap-northeast-1" ,"sa-east-1" ,"ca-central-1" ,"ap-southeast-1" ,"ap-southeast-2" ,"eu-central-1" ,"us-east-1" ,"us-east-2" ,"us-west-1" ,"us-west-2"]
    print("----------------------------------------------------------------------------------------------------")
    for region in regions:
        _conn = connect_boto3(region)
        print("--- Requesting Quota increase for service {}, in the {} region".format(service_code, region))
        quota_increase_request(_conn, service_code, quota_code, desired_value)  
if __name__ == '__main__':

    main()
