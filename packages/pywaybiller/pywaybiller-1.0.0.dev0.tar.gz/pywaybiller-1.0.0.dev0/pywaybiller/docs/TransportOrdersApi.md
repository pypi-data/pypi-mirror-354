# openapi_client.TransportOrdersApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**transport_orders_cancel_create**](TransportOrdersApi.md#transport_orders_cancel_create) | **POST** /external-api/transport-orders/{id}/cancel/ | Cancellation of a transport order
[**transport_orders_create**](TransportOrdersApi.md#transport_orders_create) | **POST** /external-api/transport-orders/ | Creation of a transport order
[**transport_orders_list**](TransportOrdersApi.md#transport_orders_list) | **GET** /external-api/transport-orders/ | Querying of transport orders
[**transport_orders_retrieve**](TransportOrdersApi.md#transport_orders_retrieve) | **GET** /external-api/transport-orders/{id}/ | Querying of a single transport order
[**transport_orders_update**](TransportOrdersApi.md#transport_orders_update) | **PUT** /external-api/transport-orders/{id}/ | Editing of a transport order


# **transport_orders_cancel_create**
> ExternalAPITransportOrderCancel transport_orders_cancel_create(id, external_api_transport_order_cancel_request)

Cancellation of a transport order

Cancels a transport order.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_transport_order_cancel import ExternalAPITransportOrderCancel
from openapi_client.models.external_api_transport_order_cancel_request import ExternalAPITransportOrderCancelRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.TransportOrdersApi(api_client)
    id = 56 # int | A unique integer value identifying this Transport order.
    external_api_transport_order_cancel_request = {"cancelling_reason":"Client requested cancellation","cancelled_by_user_id":123} # ExternalAPITransportOrderCancelRequest | 

    try:
        # Cancellation of a transport order
        api_response = api_instance.transport_orders_cancel_create(id, external_api_transport_order_cancel_request)
        print("The response of TransportOrdersApi->transport_orders_cancel_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransportOrdersApi->transport_orders_cancel_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this Transport order. | 
 **external_api_transport_order_cancel_request** | [**ExternalAPITransportOrderCancelRequest**](ExternalAPITransportOrderCancelRequest.md)|  | 

### Return type

[**ExternalAPITransportOrderCancel**](ExternalAPITransportOrderCancel.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**403** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **transport_orders_create**
> transport_orders_create(external_api_transport_order_request)

Creation of a transport order

Creates a new transport order.<br><br>
        **NB!** All posted IDs are IDs in your system and these are used to match objects in your system with objects in Waybiller.
        

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_transport_order_request import ExternalAPITransportOrderRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.TransportOrdersApi(api_client)
    external_api_transport_order_request = {"transport_order_id":"1","order_raw_id":1,"rows":[{"assortment_id":"1","assortment_name":"Construction sand","amount":"23.456"}],"organizer_user_id":1,"destination_id":"1","destination_name":"Waybiller OÜ","destination_address":"Mäealuse 2/1, Tallinn","destination_latitude":59.3962767,"destination_longitude":24.6566519,"destination_waybill_created_emails":["waybiller@waybiller.com"],"destination_waybill_reached_destination_emails":["waybiller@waybiller.com"],"destination_waybill_accepted_emails":["waybiller@waybiller.com"],"destination_transport_order_created_emails":["waybiller@waybiller.com"],"receiver_company_name":"Waybiller OÜ","receiver_company_reg_code":"14200010","origin_id":"1","origin_name":"Waybiller OÜ","origin_address":"Mäealuse 2/1, Tallinn","origin_latitude":59.3962767,"origin_longitude":24.6566519,"origin_waybill_created_emails":["waybiller@waybiller.com"],"origin_waybill_reached_destination_emails":["waybiller@waybiller.com"],"origin_waybill_accepted_emails":["waybiller@waybiller.com"],"origin_transport_order_created_emails":["waybiller@waybiller.com"],"shipper_company_name":"Waybiller OÜ","shipper_company_reg_code":"14200010","transportation_company_name":"Waybiller OÜ","transportation_company_reg_code":"14200010","truck_reg_number":"ABC123","trailer_reg_number":"XYZ789","driver_email":"driver@waybiller.com","driver_personal_code":"3891020xxxx","driver_name":"John Doe","driver_phone":"+372987654321","transport_date":"2025-01-01","transport_time":"14:15","additional_info":"Additional instructions for the driver","pallets_number":10} # ExternalAPITransportOrderRequest | 

    try:
        # Creation of a transport order
        api_instance.transport_orders_create(external_api_transport_order_request)
    except Exception as e:
        print("Exception when calling TransportOrdersApi->transport_orders_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_api_transport_order_request** | [**ExternalAPITransportOrderRequest**](ExternalAPITransportOrderRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**303** |  |  -  |
**403** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **transport_orders_list**
> PaginatedExternalAPITransportOrderListList transport_orders_list(destination_ids=destination_ids, end_date=end_date, limit=limit, number=number, number__contains=number__contains, number__icontains=number__icontains, number__iexact=number__iexact, number__in=number__in, offset=offset, origin_ids=origin_ids, raw_assortment_ids=raw_assortment_ids, raw_destination_ids=raw_destination_ids, raw_organizer_company_ids=raw_organizer_company_ids, raw_organizer_user_ids=raw_organizer_user_ids, raw_origin_ids=raw_origin_ids, raw_transportation_company_ids=raw_transportation_company_ids, raw_truck_ids=raw_truck_ids, start_date=start_date, status=status, status__contains=status__contains, status__icontains=status__icontains, status__iexact=status__iexact, status__in=status__in, truck__truck__reg_number=truck__truck__reg_number, truck__truck__reg_number__contains=truck__truck__reg_number__contains, truck__truck__reg_number__icontains=truck__truck__reg_number__icontains, truck__truck__reg_number__iexact=truck__truck__reg_number__iexact, truck__truck__reg_number__in=truck__truck__reg_number__in)

Querying of transport orders

Returns transport orders associated with your company, according to the specified filters.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.paginated_external_api_transport_order_list_list import PaginatedExternalAPITransportOrderListList
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.TransportOrdersApi(api_client)
    destination_ids = 'destination_ids_example' # str | Filters transport orders with a specified list of destination IDs from your system. Multiple values may be separated by commas. (optional)
    end_date = '2013-10-20T19:20:30+01:00' # datetime | Filters transport orders that have transport date on or before the specified date. (optional)
    limit = 30 # int | Maximum number of objects to return per page (optional) (default to 30)
    number = 'number_example' # str | Filters transport orders with specified number (case sensitive). (optional)
    number__contains = 'number__contains_example' # str | Filters transport orders of which numbers contain this keyword (case sensitive). (optional)
    number__icontains = 'number__icontains_example' # str | Filters transport orders of which numbers contain this keyword (case insensitive). (optional)
    number__iexact = 'number__iexact_example' # str | Filters transport orders with specified number (case insensitive). (optional)
    number__in = 'number__in_example' # str | Filters transport orders with specified list of transport order numbers. Multiple values may be separated by commas. (optional)
    offset = 0 # int | The initial index from which to return the results (optional) (default to 0)
    origin_ids = 'origin_ids_example' # str | Filters transport orders with a specified list of origin IDs from your system. Multiple values may be separated by commas. (optional)
    raw_assortment_ids = 'raw_assortment_ids_example' # str | Filters transport orders with a specified list of raw assortment IDs. Multiple values may be separated by commas. (optional)
    raw_destination_ids = 'raw_destination_ids_example' # str | Filters transport orders with a specified list of raw destination IDs. Multiple values may be separated by commas. (optional)
    raw_organizer_company_ids = 'raw_organizer_company_ids_example' # str | Filters transport orders with a specified list of raw organizer company IDs. Multiple values may be separated by commas. (optional)
    raw_organizer_user_ids = 'raw_organizer_user_ids_example' # str | Filters transport orders with a specified list of raw organizer user IDs. Multiple values may be separated by commas. (optional)
    raw_origin_ids = 'raw_origin_ids_example' # str | Filters transport orders with a specified list of raw origin IDs. Multiple values may be separated by commas. (optional)
    raw_transportation_company_ids = 'raw_transportation_company_ids_example' # str | Filters transport orders with a specified list of raw transportation company IDs. Multiple values may be separated by commas. (optional)
    raw_truck_ids = 'raw_truck_ids_example' # str | Filters transport orders with a specified list of raw truck IDs. Multiple values may be separated by commas. (optional)
    start_date = '2013-10-20T19:20:30+01:00' # datetime | Filters transport orders that have transport date on or after the specified date. (optional)
    status = 'status_example' # str | Filters transport orders with specified status (case sensitive). (optional)
    status__contains = 'status__contains_example' # str | Filters transport orders of which statuses contain this keyword (case sensitive). (optional)
    status__icontains = 'status__icontains_example' # str | Filters transport orders of which statuses contain this keyword (case insensitive). (optional)
    status__iexact = 'status__iexact_example' # str | Filters transport orders with specified status (case insensitive). (optional)
    status__in = 'status__in_example' # str | Filters transport orders with specified list of transport order statuses. Multiple values may be separated by commas. (optional)
    truck__truck__reg_number = 'truck__truck__reg_number_example' # str | Filters transport orders with specified truck reg number (case sensitive). (optional)
    truck__truck__reg_number__contains = 'truck__truck__reg_number__contains_example' # str | Filters transport orders of which truck reg numbers contain this keyword (case sensitive). (optional)
    truck__truck__reg_number__icontains = 'truck__truck__reg_number__icontains_example' # str | Filters transport orders of which truck reg numbers contain this keyword (case insensitive). (optional)
    truck__truck__reg_number__iexact = 'truck__truck__reg_number__iexact_example' # str | Filters transport orders with specified truck reg number (case insensitive). (optional)
    truck__truck__reg_number__in = 'truck__truck__reg_number__in_example' # str | Filters transport orders with specified list of transport order truck reg numbers. Multiple values may be separated by commas. (optional)

    try:
        # Querying of transport orders
        api_response = api_instance.transport_orders_list(destination_ids=destination_ids, end_date=end_date, limit=limit, number=number, number__contains=number__contains, number__icontains=number__icontains, number__iexact=number__iexact, number__in=number__in, offset=offset, origin_ids=origin_ids, raw_assortment_ids=raw_assortment_ids, raw_destination_ids=raw_destination_ids, raw_organizer_company_ids=raw_organizer_company_ids, raw_organizer_user_ids=raw_organizer_user_ids, raw_origin_ids=raw_origin_ids, raw_transportation_company_ids=raw_transportation_company_ids, raw_truck_ids=raw_truck_ids, start_date=start_date, status=status, status__contains=status__contains, status__icontains=status__icontains, status__iexact=status__iexact, status__in=status__in, truck__truck__reg_number=truck__truck__reg_number, truck__truck__reg_number__contains=truck__truck__reg_number__contains, truck__truck__reg_number__icontains=truck__truck__reg_number__icontains, truck__truck__reg_number__iexact=truck__truck__reg_number__iexact, truck__truck__reg_number__in=truck__truck__reg_number__in)
        print("The response of TransportOrdersApi->transport_orders_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransportOrdersApi->transport_orders_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **destination_ids** | **str**| Filters transport orders with a specified list of destination IDs from your system. Multiple values may be separated by commas. | [optional] 
 **end_date** | **datetime**| Filters transport orders that have transport date on or before the specified date. | [optional] 
 **limit** | **int**| Maximum number of objects to return per page | [optional] [default to 30]
 **number** | **str**| Filters transport orders with specified number (case sensitive). | [optional] 
 **number__contains** | **str**| Filters transport orders of which numbers contain this keyword (case sensitive). | [optional] 
 **number__icontains** | **str**| Filters transport orders of which numbers contain this keyword (case insensitive). | [optional] 
 **number__iexact** | **str**| Filters transport orders with specified number (case insensitive). | [optional] 
 **number__in** | **str**| Filters transport orders with specified list of transport order numbers. Multiple values may be separated by commas. | [optional] 
 **offset** | **int**| The initial index from which to return the results | [optional] [default to 0]
 **origin_ids** | **str**| Filters transport orders with a specified list of origin IDs from your system. Multiple values may be separated by commas. | [optional] 
 **raw_assortment_ids** | **str**| Filters transport orders with a specified list of raw assortment IDs. Multiple values may be separated by commas. | [optional] 
 **raw_destination_ids** | **str**| Filters transport orders with a specified list of raw destination IDs. Multiple values may be separated by commas. | [optional] 
 **raw_organizer_company_ids** | **str**| Filters transport orders with a specified list of raw organizer company IDs. Multiple values may be separated by commas. | [optional] 
 **raw_organizer_user_ids** | **str**| Filters transport orders with a specified list of raw organizer user IDs. Multiple values may be separated by commas. | [optional] 
 **raw_origin_ids** | **str**| Filters transport orders with a specified list of raw origin IDs. Multiple values may be separated by commas. | [optional] 
 **raw_transportation_company_ids** | **str**| Filters transport orders with a specified list of raw transportation company IDs. Multiple values may be separated by commas. | [optional] 
 **raw_truck_ids** | **str**| Filters transport orders with a specified list of raw truck IDs. Multiple values may be separated by commas. | [optional] 
 **start_date** | **datetime**| Filters transport orders that have transport date on or after the specified date. | [optional] 
 **status** | **str**| Filters transport orders with specified status (case sensitive). | [optional] 
 **status__contains** | **str**| Filters transport orders of which statuses contain this keyword (case sensitive). | [optional] 
 **status__icontains** | **str**| Filters transport orders of which statuses contain this keyword (case insensitive). | [optional] 
 **status__iexact** | **str**| Filters transport orders with specified status (case insensitive). | [optional] 
 **status__in** | **str**| Filters transport orders with specified list of transport order statuses. Multiple values may be separated by commas. | [optional] 
 **truck__truck__reg_number** | **str**| Filters transport orders with specified truck reg number (case sensitive). | [optional] 
 **truck__truck__reg_number__contains** | **str**| Filters transport orders of which truck reg numbers contain this keyword (case sensitive). | [optional] 
 **truck__truck__reg_number__icontains** | **str**| Filters transport orders of which truck reg numbers contain this keyword (case insensitive). | [optional] 
 **truck__truck__reg_number__iexact** | **str**| Filters transport orders with specified truck reg number (case insensitive). | [optional] 
 **truck__truck__reg_number__in** | **str**| Filters transport orders with specified list of transport order truck reg numbers. Multiple values may be separated by commas. | [optional] 

### Return type

[**PaginatedExternalAPITransportOrderListList**](PaginatedExternalAPITransportOrderListList.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**403** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **transport_orders_retrieve**
> ExternalAPITransportOrderRetrieve transport_orders_retrieve(id)

Querying of a single transport order

Returns a transport order with the specified ID. Only companies associated with the transport order can query it.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_transport_order_retrieve import ExternalAPITransportOrderRetrieve
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.TransportOrdersApi(api_client)
    id = 56 # int | A unique integer value identifying this Transport order.

    try:
        # Querying of a single transport order
        api_response = api_instance.transport_orders_retrieve(id)
        print("The response of TransportOrdersApi->transport_orders_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransportOrdersApi->transport_orders_retrieve: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this Transport order. | 

### Return type

[**ExternalAPITransportOrderRetrieve**](ExternalAPITransportOrderRetrieve.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**403** |  |  -  |
**404** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **transport_orders_update**
> transport_orders_update(id, external_api_transport_order_update_request=external_api_transport_order_update_request)

Editing of a transport order

Edits a transport order.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_api_transport_order_update_request import ExternalAPITransportOrderUpdateRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.TransportOrdersApi(api_client)
    id = 56 # int | A unique integer value identifying this Transport order.
    external_api_transport_order_update_request = {"origin_id":"1","origin_name":"Waybiller OÜ","origin_address":"Mäealuse 2/1, Tallinn","origin_latitude":59.3962767,"origin_longitude":24.6566519,"shipper_company_name":"Waybiller OÜ","shipper_company_reg_code":"14200010","origin_transport_order_created_emails":["waybiller@waybiller.com"],"origin_waybill_accepted_emails":["waybiller@waybiller.com"],"origin_waybill_created_emails":["waybiller@waybiller.com"],"origin_waybill_reached_destination_emails":["waybiller@waybiller.com"],"destination_id":"1","destination_name":"Waybiller OÜ","destination_address":"Mäealuse 2/1, Tallinn","destination_latitude":59.3962767,"destination_longitude":24.6566519,"receiver_company_name":"Waybiller OÜ","receiver_company_reg_code":"14200010","destination_transport_order_created_emails":["waybiller@waybiller.com"],"destination_waybill_accepted_emails":["waybiller@waybiller.com"],"destination_waybill_created_emails":["waybiller@waybiller.com"],"destination_waybill_reached_destination_emails":["waybiller@waybiller.com"],"truck_reg_number":"ABC123","trailer_reg_number":"XYZ789","pallets_number":1} # ExternalAPITransportOrderUpdateRequest |  (optional)

    try:
        # Editing of a transport order
        api_instance.transport_orders_update(id, external_api_transport_order_update_request=external_api_transport_order_update_request)
    except Exception as e:
        print("Exception when calling TransportOrdersApi->transport_orders_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this Transport order. | 
 **external_api_transport_order_update_request** | [**ExternalAPITransportOrderUpdateRequest**](ExternalAPITransportOrderUpdateRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**303** |  |  -  |
**403** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

