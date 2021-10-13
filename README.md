# connector-azure-kubernetes-services

Deploy and manage containerized applications with a fully managed Kubernetes. This connector facilitates the automated operations related to managed cluster.

## API Documentation Link:  https://docs.microsoft.com/en-us/rest/api/aks/

## Azure Kubernetes Services Version: 2021-05-01

# Accessing the Azure Kubernetes Services API

Your application needs to be both authenticated and authorized to access the Azure Kubernetes Services API. The REST APIs of Azure Kubernetes Services allows you to deploy and manage containerized applications.The following configuration parameters are required to authenticate the Azure Kubernetes Services Connector with the Azure Kubernetes Services API.


*  Client ID
*  Client Secret
*  Tenant ID
*  Redirect URI

The following configuration parameter is required to authorize the Azure Kubernetes Services Connector with the Azure Kubernetes Services API.

* Authorization Code

You can follow the steps below to secure the authentication and authorization codes in order to access the Azure Kubernetes Services API:

1.    Register your client application with Azure AD. See Register your client application for more information.
2.    Now that you have registered the application in Azure AD, you will have access to the following authentication codes: client ID, tenant ID, redirect URI, and client secret (after registering the app in Azure AD, you can generate the client secret.) Make a note of these authentication codes. In the Configurations tab of the connector, enter the authentication details in the following fields in order to authenticate the Azure Kubernetes Services Connector with the Azure Kubernetes Services API.

* In the Client ID field, enter the client ID
* In the Client Secret field, enter the client secret
* In the Tenant ID field, enter the tenant ID
* In the Redirect URL field, enter the redirect URI. By default, the redirect URI is set to https://localhost/myapp

Now that you have the authentication codes, you can use them to generate the authorization code.

3.    Ensure that the registered application has Azure Service Management listed in the API Permissions list with Delegated permissions for user_impersonation.
4.    Copy the following URL into a browser and replace the TENANT_ID, CLIENT_ID, and REDIRECT_URI with the tenant ID, client ID, and redirect URI that are generated at the time of registering the application: https://login.microsoftonline.com/TENANT_ID/oauth2/v2.0/authorize?response_type=code&scope=https://management.azure.com/user_impersonation offline_access user.read&client_id=CLIENT_ID&redirect_uri=REDIRECT_URI
5.    In the event you have not granted the required permissions to your registered application, the link you entered in the preceding step will prompt you to grant Delegated permissions for user_impersonation in the Azure Service Management API. If you have already granted the permissions, you will not be prompted again.
6.    Next, you will be automatically redirected to a link with the following structure: REDIRECT_URI?code=AUTH_CODE&session_state=SESSION_STATE. Copy the AUTH_CODE, and in the Configurations tab of the connector, paste the AUTH_CODE in the Authorization Code field.

The process to access the Azure Kubernetes Services API is now complete.
