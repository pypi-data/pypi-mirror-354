# ExternalAPIOrderRetrieve


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**number** | **str** | Unique order reference number | [readonly] 
**status** | [**OrderStatusEnum**](OrderStatusEnum.md) | Current status of the order | [readonly] 
**order_id** | **str** | Unique identifier for this order in your system | [readonly] 
**period** | **List[date]** | Date range when the order is active | [readonly] 
**owner_raw_id** | **str** | Unique identifier of the company that owns this order | [readonly] 
**owner_company_name** | **str** | Name of the company that owns this order | [readonly] 
**client_id** | **str** | Unique identifier for the client company of this order in your system | [readonly] 
**destination_id** | **str** | Unique identifier for the destination of this order in your system | [readonly] 
**destination_name** | **str** | Name of the destination | [readonly] 
**destination_address** | **str** | Physical address of the delivery destination | [readonly] 
**destination_latitude** | **float** | Geographic latitude coordinate of the destination (decimal degrees) | [readonly] 
**destination_longitude** | **float** | Geographic longitude coordinate of the destination (decimal degrees) | [readonly] 
**origins** | [**List[ExternalAPIOrderOrigin]**](ExternalAPIOrderOrigin.md) | List of origins associated with this order | [readonly] 
**total_allowed_amount** | **decimal.Decimal** | Maximum total quantity allowed for this order | [readonly] 
**rows** | [**List[ExternalAPIOrderOriginsAssortments]**](ExternalAPIOrderOriginsAssortments.md) | Assortments associated with the origins of this order | [readonly] 
**transportation_companies** | [**List[ExternalAPIOrderTransportCompanies]**](ExternalAPIOrderTransportCompanies.md) | List of companies authorized to transport assortments for this order | [readonly] 
**cancel_transport_orders_on_allowed_amount_exceeding** | **bool** | Cancel transport orders and do not allow to create new transport orders if the order amount has been exceeded. | [readonly] 
**client_can_edit_transportation_values** | **bool** | Boolean flag indicating whether the client has permission to modify transportation details | [readonly] 
**vehicles** | [**List[ExternalAPIOrderVehicles]**](ExternalAPIOrderVehicles.md) | Specific vehicles approved for transporting materials in this order | [readonly] 
**extra_information** | **str** | Additional notes, special instructions, or requirements for this order | [readonly] 
**user_id** | **int** | Identifier of the user who created this order | [readonly] 
**raw_data** | [**ExternalAPIOrderRawData**](ExternalAPIOrderRawData.md) | The IDs of the Waybiller internal objects | [readonly] 

## Example

```python
from openapi_client.models.external_api_order_retrieve import ExternalAPIOrderRetrieve

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOrderRetrieve from a JSON string
external_api_order_retrieve_instance = ExternalAPIOrderRetrieve.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOrderRetrieve.to_json())

# convert the object into a dict
external_api_order_retrieve_dict = external_api_order_retrieve_instance.to_dict()
# create an instance of ExternalAPIOrderRetrieve from a dict
external_api_order_retrieve_from_dict = ExternalAPIOrderRetrieve.from_dict(external_api_order_retrieve_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


