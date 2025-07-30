# ExternalAPITransportOrderList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transport_order_id** | **str** | Unique identifier of the transport order in your system | [readonly] 
**transport_date** | **date** | Date of transport | [readonly] 
**origin_id** | **str** | Unique identifier of the origin in your system | [readonly] 
**origin_name** | **str** | Name of the origin location | [readonly] 
**origin_address** | **str** | Address of the origin location | [readonly] 
**destination_id** | **str** | Unique identifier of the destination in your system | [readonly] 
**destination_name** | **str** | Name of the destination location | [readonly] 
**destination_address** | **str** | Address of the destination location | [readonly] 
**assortment_name** | **str** | Name of the assortment being transported | [readonly] 
**transportation_company_name** | **str** | Transportation company name | [readonly] 
**truck_reg_number** | **str** | Registration number of the truck | [readonly] 
**trailer_reg_number** | **str** | Registration number of the trailer | [readonly] 
**raw_data** | [**ExternalAPITransportOrderRawDataList**](ExternalAPITransportOrderRawDataList.md) | The IDs of the Waybiller internal objects | [readonly] 

## Example

```python
from openapi_client.models.external_api_transport_order_list import ExternalAPITransportOrderList

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPITransportOrderList from a JSON string
external_api_transport_order_list_instance = ExternalAPITransportOrderList.from_json(json)
# print the JSON string representation of the object
print(ExternalAPITransportOrderList.to_json())

# convert the object into a dict
external_api_transport_order_list_dict = external_api_transport_order_list_instance.to_dict()
# create an instance of ExternalAPITransportOrderList from a dict
external_api_transport_order_list_from_dict = ExternalAPITransportOrderList.from_dict(external_api_transport_order_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


