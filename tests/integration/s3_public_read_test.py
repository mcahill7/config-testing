import sys
import pytest
import botocore
import boto3
import json
import time

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
    assert response['ConfigRules'][0]['Source']['SourceIdentifier'] == 'S3_BUCKET_PUBLIC_READ_PROHIBITED'

def test_s3_public_read_non_compliant():
    create_s3_public_bucket()
    time.sleep(5)
    client = boto3.client('config')

    response = client.get_compliance_details_by_resource(
        ResourceType = 'AWS::S3::Bucket',
        ResourceId = 'arctests3compliancepublicreadbucket',
        ComplianceTypes = ['NON_COMPLIANT']
    )

    assert response['EvaluationResults'][0]['ComplianceType'] == 'NON_COMPLIANT'

    delete_s3_public_bucket()
    time.sleep(5)


def create_s3_public_bucket():
    s3_client = boto3.client('s3')
    s3_client.create_bucket(Bucket='arctests3compliancepublicreadbucket')
    public_policy = """{
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
    }"""
    response = s3_client.put_bucket_policy(
        Bucket='arctests3compliancepublicreadbucket',
        Policy = public_policy
    )

def delete_s3_public_bucket():
    s3_client = boto3.client('s3')
    s3_client.delete_bucket(Bucket='arctests3compliancepublicreadbucket')


