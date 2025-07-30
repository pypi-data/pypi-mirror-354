# ExternalAPITransportOrderCancel


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cancelling_reason** | **str** | Reason for cancelling the transport order | 
**cancelled_by_user_id** | **int** | ID of the user who cancelled the transport order. Required unless a default values has been set for the API key. | [optional] 

## Example

```python
from openapi_client.models.external_api_transport_order_cancel import ExternalAPITransportOrderCancel

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPITransportOrderCancel from a JSON string
external_api_transport_order_cancel_instance = ExternalAPITransportOrderCancel.from_json(json)
# print the JSON string representation of the object
print(ExternalAPITransportOrderCancel.to_json())

# convert the object into a dict
external_api_transport_order_cancel_dict = external_api_transport_order_cancel_instance.to_dict()
# create an instance of ExternalAPITransportOrderCancel from a dict
external_api_transport_order_cancel_from_dict = ExternalAPITransportOrderCancel.from_dict(external_api_transport_order_cancel_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


