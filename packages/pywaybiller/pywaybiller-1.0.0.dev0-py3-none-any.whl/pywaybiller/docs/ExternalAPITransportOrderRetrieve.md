# ExternalAPITransportOrderRetrieve


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transport_order_id** | **str** | Unique identifier of the transport order in your system | [readonly] 
**number** | **str** | Unique transport order reference number | [readonly] 
**status** | [**TransportOrderStatusEnum**](TransportOrderStatusEnum.md) | Status of the transport order | [readonly] 
**rows** | [**List[ExternalAPITransportOrderRow]**](ExternalAPITransportOrderRow.md) | List of assortments associated with the transport order | [readonly] 
**organizer_user_id** | **int** | Organizer user ID. Required unless a default values has been set for the API key | [readonly] 
**destination_id** | **str** | Unique identifier of the destination in your system | [readonly] 
**destination_name** | **str** | Name of the destination location | [readonly] 
**destination_address** | **str** | Address of the destination location | [readonly] 
**destination_latitude** | **float** | Latitude of the destination location | [readonly] 
**destination_longitude** | **float** | Longitude of the destination location | [readonly] 
**destination_waybill_created_emails** | **List[str]** | List of emails to notify when a waybill is created for this destination | [readonly] 
**destination_waybill_reached_destination_emails** | **List[str]** | List of emails to notify when a waybill reaches this destination | [readonly] 
**destination_waybill_accepted_emails** | **List[str]** | List of emails to notify when a waybill is accepted at this destination | [readonly] 
**destination_transport_order_created_emails** | **List[str]** | List of emails to notify when a transport order is created for this destination | [readonly] 
**receiver_company_name** | **str** | Name of the company that owns the destination location | [readonly] 
**receiver_company_reg_code** | **str** | Registration code of the company that owns the destination location | [readonly] 
**origin_id** | **str** | Unique identifier of the origin in your system | [readonly] 
**origin_name** | **str** | Name of the origin location | [readonly] 
**origin_address** | **str** | Address of the origin location | [readonly] 
**origin_latitude** | **float** | Latitude of the origin location | [readonly] 
**origin_longitude** | **float** | Longitude of the origin location | [readonly] 
**origin_waybill_created_emails** | **List[str]** | List of emails to notify when a waybill is created from this origin | [readonly] 
**origin_waybill_reached_destination_emails** | **List[str]** | List of emails to notify when a waybill from this origin reaches destination | [readonly] 
**origin_waybill_accepted_emails** | **List[str]** | List of emails to notify when a waybill from this origin is accepted | [readonly] 
**origin_transport_order_created_emails** | **List[str]** | List of emails to notify when a transport order is created from this origin | [readonly] 
**shipper_company_name** | **str** | Name of the company that owns the origin location | [readonly] 
**shipper_company_reg_code** | **str** | Registration code of the company that owns the origin location | [readonly] 
**transportation_company_name** | **str** | Transportation company name | [readonly] 
**transportation_company_reg_code** | **str** | Transportation company registration code | [readonly] 
**truck_reg_number** | **str** | Registration number of the truck | [readonly] 
**trailer_reg_number** | **str** | Registration number of the trailer | [readonly] 
**driver_email** | **str** | Driver email | [readonly] 
**driver_personal_code** | **str** | Driver personal code | [readonly] 
**driver_name** | **str** | Driver name | [readonly] 
**driver_phone** | **str** | Driver phone number | [readonly] 
**transport_date** | **date** | Date of transport | [readonly] 
**transport_time** | **str** | Time of transport | [readonly] 
**additional_info** | **str** | Additional information for drivers | [readonly] 
**waybill_pdf_urls** | **List[str]** | List of links to waybill PDFs | [readonly] 
**pallets_number** | **int** | Number of pallets in the transport order | [readonly] 
**raw_data** | [**ExternalAPITransportOrderRawData**](ExternalAPITransportOrderRawData.md) | Raw data from the transport order | [readonly] 

## Example

```python
from openapi_client.models.external_api_transport_order_retrieve import ExternalAPITransportOrderRetrieve

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalAPITransportOrderRetrieve from a JSON string
external_api_transport_order_retrieve_instance = ExternalAPITransportOrderRetrieve.from_json(json)
# print the JSON string representation of the object
print(ExternalAPITransportOrderRetrieve.to_json())

# convert the object into a dict
external_api_transport_order_retrieve_dict = external_api_transport_order_retrieve_instance.to_dict()
# create an instance of ExternalAPITransportOrderRetrieve from a dict
external_api_transport_order_retrieve_from_dict = ExternalAPITransportOrderRetrieve.from_dict(external_api_transport_order_retrieve_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


