# ExternalAPIOrderList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_id** | **str** | Unique identifier of the order in Waybiller | [readonly] 
**number** | **str** | Unique order reference number | [readonly] 
**status** | [**OrderStatusEnum**](OrderStatusEnum.md) | Current status of the order | [readonly] 
**period** | **List[date]** | Date range when the order is active | [readonly] 
**origins** | [**List[ExternalAPIOrderOrigin]**](ExternalAPIOrderOrigin.md) | List of origins associated with this order | [readonly] 
**owner_company_name** | **str** | Name of the company that owns this order | [readonly] 
**client_company_name** | **str** | Name of the client company for whom this order was created | [readonly] 
**destination_name** | **str** | Name of the destination | [readonly] [default to '']
**total_allowed_amount** | **decimal.Decimal** | Maximum total quantity allowed for this order | [readonly] 
**raw_data** | [**ExternalAPIOrderRawData**](ExternalAPIOrderRawData.md) | The IDs of the Waybiller internal objects | [readonly] 

## Example

```python
from openapi_client.models.external_api_order_list import ExternalAPIOrderList

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOrderList from a JSON string
external_api_order_list_instance = ExternalAPIOrderList.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOrderList.to_json())

# convert the object into a dict
external_api_order_list_dict = external_api_order_list_instance.to_dict()
# create an instance of ExternalAPIOrderList from a dict
external_api_order_list_from_dict = ExternalAPIOrderList.from_dict(external_api_order_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


