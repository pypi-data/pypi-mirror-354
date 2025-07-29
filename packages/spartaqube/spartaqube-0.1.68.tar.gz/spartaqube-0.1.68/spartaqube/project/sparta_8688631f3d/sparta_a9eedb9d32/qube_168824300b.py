import hmac
import hashlib
import base64
import argparse
SMTP_REGIONS = ['us-east-2', 'us-east-1', 'us-west-2', 'ap-south-1',
    'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1',
    'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1',
    'us-gov-west-1']
DATE = '11111111'
SERVICE = 'ses'
MESSAGE = 'SendRawEmail'
TERMINAL = 'aws4_request'
VERSION = 4


def sparta_8428ea3f9e(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def sparta_563ee870a1(secret_access_key, region):
    if region not in SMTP_REGIONS:
        raise ValueError(f"The {region} Region doesn't have an SMTP endpoint.")
    signature = sparta_8428ea3f9e(('AWS4' + secret_access_key).encode('utf-8'), DATE)
    signature = sparta_8428ea3f9e(signature, region)
    signature = sparta_8428ea3f9e(signature, SERVICE)
    signature = sparta_8428ea3f9e(signature, TERMINAL)
    signature = sparta_8428ea3f9e(signature, MESSAGE)
    signature_and_version = bytes([VERSION]) + signature
    smtp_password = base64.b64encode(signature_and_version)
    return smtp_password.decode('utf-8')


def sparta_4efd6137a9():
    parser = argparse.ArgumentParser(description=
        'Convert a Secret Access Key for an IAM user to an SMTP password.')
    parser.add_argument('secret', help='The Secret Access Key to convert.')
    parser.add_argument('region', help=
        'The AWS Region where the SMTP password will be used.', choices=
        SMTP_REGIONS)
    args = parser.parse_args()
    print(sparta_563ee870a1(args.secret, args.region))


if __name__ == '__main__':
    sparta_4efd6137a9()

#END OF QUBE
