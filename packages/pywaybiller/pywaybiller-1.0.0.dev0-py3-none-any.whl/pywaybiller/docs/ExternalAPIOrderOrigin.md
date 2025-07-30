# ExternalAPIOrderOrigin


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**origin_name** | **str** | Name of the origin | [readonly] 
**origin_address** | **str** | Physical address of the origin | [readonly] 
**origin_latitude** | **float** | Geographic latitude coordinate of the origin (decimal degrees) | [readonly] 
**origin_longitude** | **float** | Geographic longitude coordinate of the origin (decimal degrees) | [readonly] 
**shipper_company_name** | **str** | Name of the company that owns the origin | [readonly] 
**shipper_company_reg_code** | **str** | Official registration number of the origin company | [readonly] 

## Example

```python
from openapi_client.models.external_api_order_origin import ExternalAPIOrderOrigin

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPIOrderOrigin from a JSON string
external_api_order_origin_instance = ExternalAPIOrderOrigin.from_json(json)
# print the JSON string representation of the object
print(ExternalAPIOrderOrigin.to_json())

# convert the object into a dict
external_api_order_origin_dict = external_api_order_origin_instance.to_dict()
# create an instance of ExternalAPIOrderOrigin from a dict
external_api_order_origin_from_dict = ExternalAPIOrderOrigin.from_dict(external_api_order_origin_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


