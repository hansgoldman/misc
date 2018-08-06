################################################################################
# Filename: list_aws_instances.py
#
# Description: Prints a list of all EC2 instances with basic information for
#   each instance across all regions. Requires that you have set up a IAM user
#   with appropriate permissions and set your AWS Access Key ID and Secret
#   Access Key for that user in the .aws/credentials file.
#
# Author:             Hans Goldman
# Create Date:        08/05/2018
# Last Modified Date: 08/05/2018
# Last Modified by:   Hans Goldman
################################################################################

import boto3


def main():
    ec2_client  = boto3.client('ec2')
    ec2_regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

    for region in ec2_regions:
        ec2        = boto3.resource('ec2', region_name=region)
        instances  = ec2.instances.all()
        count      = 0

        for instance in instances:
            count        += 1
            instance_name = get_instance_name_from_tags(instance.tags)

            print('Instance #%s:'  % count)
            print('    Name:   %s' % instance_name)
            print('    Id:     %s' % instance.id)
            print('    Type:   %s' % instance.instance_type)
            print('    Region: %s' % region)
            print('    State:  %s' % instance.state["Name"])
            print()


def get_instance_name_from_tags(tags):
    """
    Returns the name of the instance from a given list of instance tags
    :param tags: A list of dictionaries containing tags for an AWS instance
    :return: The name of the instance or a default value is it is not found
    """
    instance_name = 'N/A'

    for tag in tags:
        if tag["Key"] == 'Name':
            instance_name = tag["Value"]
            break

    return instance_name


main()
