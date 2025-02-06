from datetime import datetime

from maihem import Maihem


maihem_client = Maihem(env="local")

target_agent_name = "sanity_check"
try:
    target_agent = maihem_client.add_target_agent(
        name=target_agent_name,  # + str(datetime.now().strftime("%Y%m%d_%H%M%S")),
        role="Airbnb customer support agent",
        description="Airbnb customer support agent that can help with questions about the platform",
    )
except Exception as e:
    print(e)
    target_agent = maihem_client.get_target_agent(name=target_agent_name)
print(target_agent)

# data = [
#     {
#         "input_payload": {
#             "message": "I want to book a stay in London",
#         },
#         "output_payload_expected": {
#             "entity": "London",
#         },
#     },
#     {
#         "input_payload": {
#             "message": "I want to book a stay in San Francisco",
#         },
#         "output_payload_expected": {
#             "entity": "San Francisco",
#         },
#     },
# ]

# maihem_client.upload_dataset(
#     name="dataset_sanity_check_",  # + str(datetime.now().strftime("%Y%m%d_%H%M%S")),
#     data=data,
# )

test = maihem_client.create_workflow_test(
    name="test_sanity_check",
    target_agent_name=target_agent_name,
    dataset_name="dataset_sanity_check_",
    label="Sanity check 1",
)
print(test)
