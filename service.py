# -*- coding: utf-8 -*-
import datetime
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    """
    Check usage of Stiki APIs for quota limits.

    Look up api usage plans, and then looks at yesterday's usage for
    each of those. If yesterday's usage brings the limit too close,
    send a notification.
    """
    apigw = boto3.client('apigateway')
    notifier = boto3.client('sns')

    plan_data = apigw.get_usage_plans()
    for plan in plan_data['items']:
        limit = plan['quota']['limit']
        key_data = apigw.get_usage_plan_keys(usagePlanId=plan['id'])
        for key in key_data['items']:
            logger.info(f"Checking {key['id']} for plan {plan['id']}.")
            yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
            usage_data = apigw.get_usage(
                usagePlanId=plan['id'],
                keyId=key['id'],
                startDate=yesterday.strftime('%Y-%m-%d'),
                endDate=yesterday.strftime('%Y-%m-%d'),
            )
            try:
                use_yesterday, remaining = usage_data['items'][key['id']][0]
            except KeyError as e:
                continue
            usage_info_string = (f"Key id {key['id']} used {use_yesterday} "
                                 f"invocations out of {limit}. They have "
                                 f"{remaining} left.")
            usage_info_warning = None
            logger.info(usage_info_string)
            if remaining < (5 * use_yesterday):
                usage_info_warning = (f" At this usage rate, they have "
                                      f"{remaining // use_yesterday} days "
                                      f"before the quota is exhausted.")
            if remaining < (.1 * limit):
                usage_info_warning = " Less than 10 percent of quota remains."
            if usage_info_warning:
                logger.info(usage_info_warning)
                response = notifier.publish(
                    TargetArn=os.environ['notifier_arn'],
                    Message=usage_info_string + usage_info_warning,
                )
