import sys
import pytest
import botocore
import boto3
import json

def test_config_recorder():
    client = boto3.client('config')
    recorder_status = client.describe_configuration_recorder_status()
    recorder = client.describe_configuration_recorders()

    assert recorder_status['ConfigurationRecordersStatus'][0]['recording'] == True
    assert recorder['ConfigurationRecorders'][0]['recordingGroup']['allSupported'] == True


def test_delivery_channel():
    client = boto3.client('config')
    delivery_channels = client.describe_delivery_channels()
    delivery_channel_status = client.describe_delivery_channel_status()

    assert delivery_channels['ResponseMetadata']['HTTPStatusCode'] == 200
    assert delivery_channel_status['ResponseMetadata']['HTTPStatusCode'] == 200

def test_s3_public_read_rule_exists():
    client = boto3.client('config')
    response = client.describe_config_rules(
    ConfigRuleNames=[
        'S3_BUCKET_PUBLIC_READ_PROHIBITED',
        ]
    )
    print(response)

def test_s3_public_read_non_compliant():
    config_client = boto3.client('config')
    s3_client = boto3.client('s3')
    s3_client.create_bucket(Bucket='arctests3compliancepublicreadbucket')
    public_policy = {
        "Version":"2008-10-17",
        "Statement":[{
        "Sid":"AllowPublicRead",
            "Effect":"Allow",
            "Principal": {
                "AWS": "*"
                },
            "Action":["s3:GetObject"],
            "Resource":["arn:aws:s3:::arctests3compliancepublicreadbucket/*"
            ]
        }
        ]
    }
    response = s3_client.put_bucket_policy(
        Bucket='arctests3compliancepublicreadbucket',
        Policy = public_policy
    )

def create_s3_public_read():
    client = boto3.client('config')
    response = client.put_config_rule(
        ConfigRule={
            'ConfigRuleName': 'S3_BUCKET_PUBLIC_READ_PROHIBITED',
            'Description': 'Checks that your Amazon S3 buckets do not allow public read access.',
            'Scope': {
                'ComplianceResourceTypes': [
                    'AWS::S3::Bucket'
                ],
            },
            'Source': {
                'Owner': 'AWS',
                'SourceIdentifier': 'S3_BUCKET_PUBLIC_READ_PROHIBITED'
            },
            'ConfigRuleState': 'ACTIVE'
        }
    )
