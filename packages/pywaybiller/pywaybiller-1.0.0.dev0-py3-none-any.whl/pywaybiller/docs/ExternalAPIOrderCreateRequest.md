# ExternalAPIOrderCreateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_id** | **str** | Unique identifier for this order in your system | 
**period** | **List[date]** | The date range when the order is active | 
**client_id** | **str** | Unique identifier for the client company of this order in your system | [optional] 
**client_company_reg_code** | **str** | The company reg code for whom the order is created for. Used as raw id to match the company, if it exists. Required if the &#x60;client_id&#x60; is not provided | [optional] 
**client_company_name** | **str** | Name of the company for whom the order is created for. Only used if a company with the given &#x60;client_company_reg_code&#x60; does not exist | [optional] 
**destination_raw_id** | **int** | Unique identifier of the destination | [optional] 
**destination_id** | **str** | Unique identifier of the destination in your system | [optional] 
**destination_name** | **str** | Name of the destination. Ignored if existing &#x60;destination_id&#x60; or &#x60;destination_raw_id&#x60; is provided | [optional] 
**destination_address** | **str** | Address of the destination. Ignored if existing &#x60;destination_id&#x60; or &#x60;destination_raw_id&#x60; is provided | [optional] 
**destination_latitude** | **float** | Geographic latitude coordinate of the destination (decimal degrees). Ignored if existing &#x60;destination_id&#x60; or &#x60;destination_raw_id&#x60; is provided | [optional] 
**destination_longitude** | **float** | Geographic longitude coordinate of the destination (decimal degrees). Ignored if existing &#x60;destination_id&#x60; or &#x60;destination_raw_id&#x60; is provided | [optional] 
**origins** | [**List[ExternalAPIOrderOriginRequest]**](ExternalAPIOrderOriginRequest.md) | The origins for which the order is created | [optional] 
**total_allowed_amount** | **decimal.Decimal** | Maximum total quantity allowed for this order | [optional] 
**rows** | [**List[ExternalAPIOrderOriginsAssortmentsRequest]**](ExternalAPIOrderOriginsAssortmentsRequest.md) | Assortments associated with the origins of this order | [optional] 
**transportation_companies** | [**List[ExternalAPIOrderTransportCompaniesRequest]**](ExternalAPIOrderTransportCompaniesRequest.md) | The transportation companies the client is using for transporting assortments from origins to destination | [optional] 
**cancel_transport_orders_on_allowed_amount_exceeding** | **bool** | Cancel transport orders and do not allow to create new transport orders if the order amount has been exceeded. | [optional] 
**client_can_edit_transportation_values** | **bool** | Boolean flag indicating whether the client has permission to modify transportation details | [optional] [default to False]
**vehicles** | [**List[ExternalAPIOrderVehiclesRequest]**](ExternalAPIOrderVehiclesRequest.md) | The vehicles that the transportation companies are allowed to use for this order | [optional] 
**extra_information** | **str** | Additional notes, special instructions, or requirements for this order | [optional] 
**user_id** | **int** | Unique identifier of the user who created this order | 

## Example

```python
from openapi_client.models.external_api_order_create_request import ExternalAPIOrderCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOrderCreateRequest from a JSON string
external_api_order_create_request_instance = ExternalAPIOrderCreateRequest.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOrderCreateRequest.to_json())

# convert the object into a dict
external_api_order_create_request_dict = external_api_order_create_request_instance.to_dict()
# create an instance of ExternalAPIOrderCreateRequest from a dict
external_api_order_create_request_from_dict = ExternalAPIOrderCreateRequest.from_dict(external_api_order_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


