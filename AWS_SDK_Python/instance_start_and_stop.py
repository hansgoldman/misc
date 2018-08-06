################################################################################
# Filename: instance_start_and_stop.py
#
# Description: Start or stop AWS EC2 instances. Requires that you have set up
#   an IAM user with appropriate permissions and set your AWS Access Key ID and
#   Secret Access Key for that user in the .aws/credentials file and the
#   instance's region must match what is in your .aws/config file.
#
# Usage: python instance_start_and_stop.py start <EC2 instance ID>
#        or
#        python instance_start_and_stop.py stop <EC2 instance ID>
#
# More Info: 
# https://boto3.readthedocs.io/en/latest/guide/ec2-example-managing-instances.html
#
# Author:             Hans Goldman
# Create Date:        08/05/2018
# Last Modified Date: 08/05/2018
# Last Modified by:   Hans Goldman
################################################################################

import boto3
import sys

from botocore.exceptions import ClientError


def main():
    action      = sys.argv[1].upper()
    instance_id = sys.argv[2]
    ec2         = boto3.client('ec2')

    # Verify user input
    if action not in ['START', 'STOP']:
        raise Exception('Unknown action: "%s". No action taken. Please use "STOP" or "START".' % action)

    # Assign either stop or start method calls to a single variable to eliminate duplicate code
    ec2_function_pointer = ec2.start_instances

    if action == 'STOP':
        ec2_function_pointer = ec2.stop_instances

    # Do a dry run first to verify permissions
    try:
        ec2_function_pointer(InstanceIds=[instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, now lets do it without the dry run
    try:
        ec2_function_pointer(InstanceIds=[instance_id], DryRun=False)
        print('Successfully ran %s command on instance: %s' % (action, instance_id))
    except ClientError as e:
        print(e)


main()
