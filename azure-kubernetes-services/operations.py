""" Copyright start
  Copyright (C) 2008 - 2021 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """

from requests import request, exceptions as req_exceptions
from .microsoft_api_auth import *

logger = get_logger('azure-kubernetes-services')

kubernetes_api_endpoint = 'https://management.azure.com'

managed_cluster_action = {
    "Start Managed Cluster": "start",
    "Stop Managed Cluster": "stop",
    "Rotate Cluster Certificates": "rotateClusterCertificates"
}


def api_request(method, endpoint, connector_info, config, params=None, data=None, headers={}):
    try:
        ms = MicrosoftAuth(config)
        token = ms.validate_token(config, connector_info)
        headers['Authorization'] = token
        headers['Content-Type'] = 'application/json'
        logger.debug("Endpoint: {0}".format(endpoint))
        try:
            response = request(method, endpoint, headers=headers, params=params, json=data, verify=ms.verify_ssl)
            logger.debug("Response Status Code: {0}".format(response.status_code))
            logger.debug("Response: {0}".format(response.text))
            logger.debug("API Header: {0}".format(response.headers))
            if response.status_code in [200, 201, 204]:
                if response.text != "":
                    return response.json()
                else:
                    return True
            else:
                if response.text != "":
                    err_resp = response.json()
                    failure_msg = err_resp['error']['message']
                    error_msg = 'Response [{0}:{1} Details: {2}]'.format(response.status_code, response.reason,
                                                                         failure_msg if failure_msg else '')
                else:
                    error_msg = 'Response [{0}:{1}]'.format(response.status_code, response.reason)
                logger.error(error_msg)
                raise ConnectorError(error_msg)
        except req_exceptions.SSLError:
            logger.error('An SSL error occurred')
            raise ConnectorError('An SSL error occurred')
        except req_exceptions.ConnectionError:
            logger.error('A connection error occurred')
            raise ConnectorError('A connection error occurred')
        except req_exceptions.Timeout:
            logger.error('The request timed out')
            raise ConnectorError('The request timed out')
        except req_exceptions.RequestException:
            logger.error('There was an error while handling the request')
            raise ConnectorError('There was an error while handling the request')
        except Exception as err:
            raise ConnectorError(str(err))
    except Exception as err:
        raise ConnectorError(str(err))


def check_payload(payload):
    final_payload = {}
    for key, value in payload.items():
        if isinstance(value, dict):
            nested = check_payload(value)
            if len(nested.keys()) > 0:
                final_payload[key] = nested
        elif value:
            final_payload[key] = value
    return final_payload


def list_managed_clusters(config, params, connector_info):
    try:
        endpoint = kubernetes_api_endpoint + '/subscriptions/{0}/providers/Microsoft.ContainerService/managedClusters?api-version=2021-05-01'.format(
            params.get('subscriptionId'))
        response = api_request("GET", endpoint, connector_info, config)
        return response
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def get_managed_cluster(config, params, connector_info):
    try:
        endpoint = kubernetes_api_endpoint + '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.ContainerService/managedClusters/{2}?api-version=2021-05-01'.format(
            params.get('subscriptionId'), params.get('resourceGroupName'), params.get('resourceName'))
        response = api_request("GET", endpoint, connector_info, config)
        return response
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def create_managed_cluster(config, params, connector_info):
    try:
        endpoint = kubernetes_api_endpoint + '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.ContainerService/managedClusters/{2}?api-version=2021-05-01'.format(
            params.get('subscriptionId'), params.get('resourceGroupName'), params.get('resourceName'),
            params.get('savedSearchId'))
        additional_fields = params.get('additional_fields')
        payload = {
            "location": params.get('location')
        }
        if additional_fields:
            payload.update(additional_fields)
        payload = check_payload(payload)
        logger.debug("Payload: {0}".format(payload))
        response = api_request("PUT", endpoint, connector_info, config, data=payload)
        return response
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def update_managed_cluster(config, params, connector_info):
    try:
        endpoint = kubernetes_api_endpoint + '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.ContainerService/managedClusters/{2}?api-version=2021-05-01'.format(
            params.get('subscriptionId'), params.get('resourceGroupName'), params.get('resourceName'),
            params.get('savedSearchId'))
        additional_fields = params.get('additional_fields')
        payload = {
            "location": params.get('location')
        }
        if additional_fields:
            payload.update(additional_fields)
        payload = check_payload(payload)
        logger.debug("Payload: {0}".format(payload))
        response = api_request("PUT", endpoint, connector_info, config, data=payload)
        return response
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def delete_managed_cluster(config, params, connector_info):
    try:
        endpoint = kubernetes_api_endpoint + '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.ContainerService/managedClusters/{2}?api-version=2021-05-01'.format(
            params.get('subscriptionId'), params.get('resourceGroupName'), params.get('resourceName'))
        response = api_request("DELETE", endpoint, connector_info, config)
        return {'result': 'Deleted Managed Cluster {0} successfully'.format(params.get('resourceName'))}
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def managed_cluster_actions(config, params, connector_info):
    try:
        endpoint = kubernetes_api_endpoint + '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.ContainerService/managedClusters/{2}/{3}?api-version=2021-05-01'.format(
            params.get('subscriptionId'), params.get('resourceGroupName'), params.get('resourceName'), managed_cluster_action.get(params.get('action')))
        response = api_request("POST", endpoint, connector_info, config)
        return {'result': 'Successfully {0}'.format(params.get('action'))}
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def run_command(config, params, connector_info):
    try:
        endpoint = kubernetes_api_endpoint + '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.ContainerService/managedClusters/{2}/runCommand?api-version=2021-05-01'.format(
            params.get('subscriptionId'), params.get('resourceGroupName'), params.get('resourceName'))
        additional_fields = params.get('additional_fields')
        payload = {
            'command': params.get('command')
        }
        if additional_fields:
            payload.update(additional_fields)
        payload = check_payload(payload)
        logger.debug("Payload: {0}".format(payload))
        response = api_request("POST", endpoint, connector_info, config, data=payload)
        return response
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def get_command_details(config, params, connector_info):
    try:
        endpoint = kubernetes_api_endpoint + '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.ContainerService/managedClusters/{2}/commandResults/{3}?api-version=2021-05-01'.format(
            params.get('subscriptionId'), params.get('resourceGroupName'), params.get('resourceName'), params.get('commandId'))
        response = api_request("GET", endpoint, connector_info, config)
        return response
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def _check_health(config, connector_info):
    try:
        return check(config, connector_info)
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


operations = {
    'create_managed_cluster': create_managed_cluster,
    'list_managed_clusters': list_managed_clusters,
    'get_managed_cluster': get_managed_cluster,
    'update_managed_cluster': update_managed_cluster,
    'delete_managed_cluster': delete_managed_cluster,
    'managed_cluster_actions': managed_cluster_actions,
    'run_command': run_command,
    'get_command_details': get_command_details
}
