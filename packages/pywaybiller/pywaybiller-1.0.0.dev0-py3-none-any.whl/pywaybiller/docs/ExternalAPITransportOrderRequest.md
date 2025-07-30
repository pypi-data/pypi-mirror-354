# ExternalAPITransportOrderRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transport_order_id** | **str** | Unique identifier of the transport order in your system | 
**order_raw_id** | **int** | Unique identifier of the order in your system | [optional] 
**rows** | [**List[ExternalAPITransportOrderRowRequest]**](ExternalAPITransportOrderRowRequest.md) | List of assortments associated with the transport order | 
**organizer_user_id** | **int** | Organizer user ID. Required unless a default values has been set for the API key | [optional] 
**destination_raw_id** | **int** | Unique identifier of the destination in Waybiller. Either this field or destination_raw_id must be provided when creating a new transport order | [optional] 
**destination_id** | **str** | Unique identifier of the destination in your system. Either this field or destination_raw_id must be provided when creating a new transport order | [optional] 
**destination_name** | **str** | Name of the destination location | [optional] 
**destination_address** | **str** | Address of the destination location | [optional] 
**destination_latitude** | **float** | Latitude of the destination location | [optional] 
**destination_longitude** | **float** | Longitude of the destination location | [optional] 
**destination_waybill_created_emails** | **List[str]** | List of emails to notify when a waybill is created for this destination | [optional] 
**destination_waybill_reached_destination_emails** | **List[str]** | List of emails to notify when a waybill reaches this destination | [optional] 
**destination_waybill_accepted_emails** | **List[str]** | List of emails to notify when a waybill is accepted at this destination | [optional] 
**destination_transport_order_created_emails** | **List[str]** | List of emails to notify when a transport order is created for this destination | [optional] 
**receiver_company_name** | **str** | Name of the company that owns the destination location | [optional] 
**receiver_company_reg_code** | **str** | Registration code of the company that owns the destination location | [optional] 
**origin_raw_id** | **int** | Unique identifier of the origin in Waybiller. Either this field or origin_id must be provided when creating a new transport order | [optional] 
**origin_id** | **str** | Unique identifier of the origin in your system. Either this field or origin_raw_id must be provided when creating a new transport order | [optional] 
**origin_name** | **str** | Name of the origin location | [optional] 
**origin_address** | **str** | Address of the origin location | [optional] 
**origin_latitude** | **float** | Latitude of the origin location | [optional] 
**origin_longitude** | **float** | Longitude of the origin location | [optional] 
**origin_waybill_created_emails** | **List[str]** | List of emails to notify when a waybill is created from this origin | [optional] 
**origin_waybill_reached_destination_emails** | **List[str]** | List of emails to notify when a waybill from this origin reaches destination | [optional] 
**origin_waybill_accepted_emails** | **List[str]** | List of emails to notify when a waybill from this origin is accepted | [optional] 
**origin_transport_order_created_emails** | **List[str]** | List of emails to notify when a transport order is created from this origin | [optional] 
**shipper_company_name** | **str** | Name of the company that owns the origin location | [optional] 
**shipper_company_reg_code** | **str** | Registration code of the company that owns the origin location | [optional] 
**transportation_company_name** | **str** | Transportation company name | [optional] 
**transportation_company_reg_code** | **str** | Transportation company registration code | [optional] 
**truck_reg_number** | **str** | Registration number of the truck | [optional] 
**trailer_reg_number** | **str** | Registration number of the trailer | [optional] 
**driver_email** | **str** | Driver email | [optional] 
**driver_personal_code** | **str** | Driver personal code | [optional] 
**driver_name** | **str** | Driver name | [optional] 
**driver_phone** | **str** | Driver phone number | [optional] 
**transport_date** | **date** | Date of transport | 
**transport_time** | **str** | Time of transport | [optional] 
**additional_info** | **str** | Additional information for drivers | [optional] 
**pallets_number** | **int** | Number of pallets in the transport order | [optional] 

## Example

```python
from openapi_client.models.external_api_transport_order_request import ExternalAPITransportOrderRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPITransportOrderRequest from a JSON string
external_api_transport_order_request_instance = ExternalAPITransportOrderRequest.from_json(json)
# print the JSON string representation of the object
print(ExternalAPITransportOrderRequest.to_json())

# convert the object into a dict
external_api_transport_order_request_dict = external_api_transport_order_request_instance.to_dict()
# create an instance of ExternalAPITransportOrderRequest from a dict
external_api_transport_order_request_from_dict = ExternalAPITransportOrderRequest.from_dict(external_api_transport_order_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


