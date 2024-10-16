#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk.cdk_stack import CdkStack

app = cdk.App()

CdkStack(app, "hlb-cdk-dynamodb-develop",)

app.synth()
