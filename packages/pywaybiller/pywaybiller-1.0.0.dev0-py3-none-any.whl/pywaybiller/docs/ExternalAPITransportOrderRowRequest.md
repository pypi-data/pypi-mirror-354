# ExternalAPITransportOrderRowRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**assortment_id** | **str** | Unique identifier of the assortment in your system | 
**assortment_name** | **str** | Name of the assortment | 
**amount** | **decimal.Decimal** | Amount of the assortment | 

## Example

```python
from openapi_client.models.external_api_transport_order_row_request import ExternalAPITransportOrderRowRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPITransportOrderRowRequest from a JSON string
external_api_transport_order_row_request_instance = ExternalAPITransportOrderRowRequest.from_json(json)
# print the JSON string representation of the object
print(ExternalAPITransportOrderRowRequest.to_json())

# convert the object into a dict
external_api_transport_order_row_request_dict = external_api_transport_order_row_request_instance.to_dict()
# create an instance of ExternalAPITransportOrderRowRequest from a dict
external_api_transport_order_row_request_from_dict = ExternalAPITransportOrderRowRequest.from_dict(external_api_transport_order_row_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


