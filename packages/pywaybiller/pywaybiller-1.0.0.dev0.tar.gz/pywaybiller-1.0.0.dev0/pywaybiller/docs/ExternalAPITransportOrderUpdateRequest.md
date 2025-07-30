# ExternalAPITransportOrderUpdateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**origin_id** | **str** | Unique identifier of the origin in your system. Either this field or origin_raw_id must be provided when creating a new transport order | [optional] 
**origin_raw_id** | **int** | Unique identifier of the origin in Waybiller. Either this field or origin_id must be provided when creating a new transport order | [optional] 
**origin_name** | **str** | Name of the origin location | [optional] 
**origin_address** | **str** | Address of the origin location | [optional] 
**origin_latitude** | **float** | Latitude of the origin location | [optional] 
**origin_longitude** | **float** | Longitude of the origin location | [optional] 
**shipper_company_name** | **str** | Name of the company that owns the origin location | [optional] 
**shipper_company_reg_code** | **str** | Registration code of the company that owns the origin location | [optional] 
**origin_transport_order_created_emails** | **List[str]** | List of emails to notify when a transport order is created from this origin | [optional] 
**origin_waybill_accepted_emails** | **List[str]** | List of emails to notify when a waybill from this origin is accepted | [optional] 
**origin_waybill_created_emails** | **List[str]** | List of emails to notify when a waybill is created from this origin | [optional] 
**origin_waybill_reached_destination_emails** | **List[str]** | List of emails to notify when a waybill from this origin reaches destination | [optional] 
**destination_id** | **str** | Unique identifier of the destination in your system. Either this field or destination_raw_id must be provided when creating a new transport order | [optional] 
**destination_raw_id** | **int** | Unique identifier of the destination in Waybiller. Either this field or destination_raw_id must be provided when creating a new transport order | [optional] 
**destination_name** | **str** | Name of the destination location | [optional] 
**destination_address** | **str** | Address of the destination location | [optional] 
**destination_latitude** | **float** | Latitude of the destination location | [optional] 
**destination_longitude** | **float** | Longitude of the destination location | [optional] 
**receiver_company_name** | **str** | Name of the company that owns the destination location | [optional] 
**receiver_company_reg_code** | **str** | Registration code of the company that owns the destination location | [optional] 
**destination_transport_order_created_emails** | **List[str]** | List of emails to notify when a transport order is created for this destination | [optional] 
**destination_waybill_accepted_emails** | **List[str]** | List of emails to notify when a waybill is accepted at this destination | [optional] 
**destination_waybill_created_emails** | **List[str]** | List of emails to notify when a waybill is created for this destination | [optional] 
**destination_waybill_reached_destination_emails** | **List[str]** | List of emails to notify when a waybill reaches this destination | [optional] 
**truck_reg_number** | **str** | Registration number of the truck | [optional] 
**trailer_reg_number** | **str** | Registration number of the trailer | [optional] 
**pallets_number** | **int** | Number of pallets in the transport order | [optional] 

## Example

```python
from openapi_client.models.external_api_transport_order_update_request import ExternalAPITransportOrderUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPITransportOrderUpdateRequest from a JSON string
external_api_transport_order_update_request_instance = ExternalAPITransportOrderUpdateRequest.from_json(json)
# print the JSON string representation of the object
print(ExternalAPITransportOrderUpdateRequest.to_json())

# convert the object into a dict
external_api_transport_order_update_request_dict = external_api_transport_order_update_request_instance.to_dict()
# create an instance of ExternalAPITransportOrderUpdateRequest from a dict
external_api_transport_order_update_request_from_dict = ExternalAPITransportOrderUpdateRequest.from_dict(external_api_transport_order_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


