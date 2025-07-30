# ExternalAPIOrderRawData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_id** | **int** | Unique identifier of the order | [readonly] 
**number** | **str** | Unique order reference number | [readonly] 
**status** | [**ExternalAPIOrderRawDataStatusEnum**](ExternalAPIOrderRawDataStatusEnum.md) | Numeric status code of the order | [readonly] 
**origins** | **List[int]** | List of origin IDs associated with this order | [readonly] 
**owner_company_id** | **str** | Unique identifier of the company that owns this order | [readonly] 
**client_id** | **str** | Unique identifier of the client company for whom this order was created | [readonly] 
**origins_assortment** | **List[int]** | IDs of origin assortments that can be used for this order | [readonly] 
**transportation_companies** | **List[int]** | The transportation companies the &#x60;client&#x60; is using for transporting assortments from &#x60;origins&#x60;to &#x60;destination&#x60; | [readonly] 
**vehicles** | **List[int]** | The vehicles that the &#x60;transportation_companies&#x60; are allowed to use for this order. | [readonly] 
**destination** | **int** | ID of the delivery destination | [readonly] 

## Example

```python
from openapi_client.models.external_api_order_raw_data import ExternalAPIOrderRawData

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOrderRawData from a JSON string
external_api_order_raw_data_instance = ExternalAPIOrderRawData.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOrderRawData.to_json())

# convert the object into a dict
external_api_order_raw_data_dict = external_api_order_raw_data_instance.to_dict()
# create an instance of ExternalAPIOrderRawData from a dict
external_api_order_raw_data_from_dict = ExternalAPIOrderRawData.from_dict(external_api_order_raw_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


