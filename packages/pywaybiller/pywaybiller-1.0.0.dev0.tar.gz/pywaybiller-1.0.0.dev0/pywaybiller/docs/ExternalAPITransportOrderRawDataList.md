# ExternalAPITransportOrderRawDataList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transport_order_id** | **int** | Unique identifier of the transport order in the Waybiller system | [readonly] 
**status** | [**TransportOrderStatusEnum**](TransportOrderStatusEnum.md) | Current status of the transport order | [readonly] 
**number** | **str** | Unique number of the transport order in the Waybiller system | [readonly] 
**origin_id** | **int** | Unique identifier of the origin in the Waybiller system | [readonly] 
**destination_id** | **int** | Unique identifier of the destination in the Waybiller system | [readonly] 
**entity_code** | **str** | Entity code of the transport order, if applicable | [readonly] 
**truck_id** | **int** | Unique identifier of the truck associated with the transport order | [readonly] 
**waybills_ids** | **List[int]** | List of waybill IDs associated with the transport order | [readonly] 

## Example

```python
from openapi_client.models.external_api_transport_order_raw_data_list import ExternalAPITransportOrderRawDataList

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPITransportOrderRawDataList from a JSON string
external_api_transport_order_raw_data_list_instance = ExternalAPITransportOrderRawDataList.from_json(json)
# print the JSON string representation of the object
print(ExternalAPITransportOrderRawDataList.to_json())

# convert the object into a dict
external_api_transport_order_raw_data_list_dict = external_api_transport_order_raw_data_list_instance.to_dict()
# create an instance of ExternalAPITransportOrderRawDataList from a dict
external_api_transport_order_raw_data_list_from_dict = ExternalAPITransportOrderRawDataList.from_dict(external_api_transport_order_raw_data_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


