#!/usr/bin/python

import boto3

client = boto3.client('ec2')
response=client.describe_vpn_connections(DryRun=False)

primaryPeerIP='52.17.130.149'
secondaryPeerIP='54.154.27.148'

for peer in response['VpnConnections'][0]['VgwTelemetry']:
	if peer['OutsideIpAddress'] == primaryPeerIP:
		primaryPeerStatus=peer['Status']
		primaryPeerStatusMessage=peer['StatusMessage']
	if peer['OutsideIpAddress'] == secondaryPeerIP:
		secondaryPeerStatus=peer['Status']
		secondaryPeerStatusMessage=peer['StatusMessage']

if primaryPeerStatus == 'UP' and secondaryPeerStatus == 'DOWN': 
	print("Statistic.VPNpeerStatus: 0")
	print("Message.VPNpeerStatus: {0}:{1}[{2}], {3}:{4}[{5}], OK -> preferred configutration".format(primaryPeerIP,primaryPeerStatus,primaryPeerStatusMessage,secondaryPeerIP,secondaryPeerStatus,secondaryPeerStatusMessage))

elif primaryPeerStatus == 'DOWN' and secondaryPeerStatus == 'UP': 
	print("Statistic.VPNpeerStatus: 1")
	print("Message.VPNpeerStatus: {0}:{1}[{2}], {3}:{4}[{5}], WARN -> preferred peer not active".format(primaryPeerIP,primaryPeerStatus,primaryPeerStatusMessage,secondaryPeerIP,secondaryPeerStatus,secondaryPeerStatusMessage))

elif primaryPeerStatus == 'DOWN' and secondaryPeerStatus == 'DOWN': 
	print("Statistic.VPNpeerStatus: 2")
	print("Message.VPNpeerStatus: {0}:{1}[{2}], {3}:{4}[{5}], CRIT -> all peers are DOWN".format(primaryPeerIP,primaryPeerStatus,primaryPeerStatusMessage,secondaryPeerIP,secondaryPeerStatus,secondaryPeerStatusMessage))

elif primaryPeerStatus == 'UP' and secondaryPeerStatus == 'UP': 
	print("Statistic.VPNpeerStatus: 1")
	print("Message.VPNpeerStatus: {0}:{1}[{2}], {3}:{4}[{5}], WARN -> both peers are UP, it shouldn't happen".format(primaryPeerIP,primaryPeerStatus,primaryPeerStatusMessage,secondaryPeerIP,secondaryPeerStatus,secondaryPeerStatusMessage))

