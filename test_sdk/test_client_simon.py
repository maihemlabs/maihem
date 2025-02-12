from datetime import datetime

from maihem import Maihem

from data import data_e2e


maihem_client = Maihem(env="local")

target_agent_name = "agent-colin-local"
# try:
#     target_agent = maihem_client.add_target_agent(
#         name=target_agent_name,  # + str(datetime.now().strftime("%Y%m%d_%H%M%S")),
#         role="Airbnb customer support agent",
#         description="Airbnb customer support agent that can help with questions about the platform",
#     )
# except Exception as e:
#     print(e)
# target_agent = maihem_client.get_target_agent(name=target_agent_name)
# print(target_agent)


# maihem_client.upload_dataset(
#     name="dataset_sanity_check_e2e-3",  # + str(datetime.now().strftime("%Y%m%d_%H%M%S")),
#     data=data_e2e,
# )

# test = maihem_client.create_workflow_test(
#     name="test_sanity_check_e2e_v2-3",
#     target_agent_name=target_agent_name,
#     dataset_name="dataset_sanity_check_e2e-3",
#     label="Sanity check 2",
# )
# print(test)

# test = maihem_client.autogenerate_workflow_test(
#     name="test_sanity_check_e2e_gen_v1",
#     target_agent_name=target_agent_name,
#     label="Autogen sanity check 1",
#     modules=["cx"],
#     number_conversations=5,
# )
# print(test)

test_run = maihem_client.run_workflow_test(
    name="test_run" + datetime.now().strftime("%Y%m%d_%H%M%S"),
    test_name="test_sanity_check_e2e_gen_v1",
    concurrent_conversations=1,
)
print(test_run)
