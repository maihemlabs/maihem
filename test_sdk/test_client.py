from datetime import datetime

from maihem import Maihem

from data import data_e2e, data_reranking


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

##################################################################
######################### WORKFLOW E2E ###########################
##################################################################

# maihem_client.upload_dataset(
#     name="dataset_sanity_check_e2e_2",  # + str(datetime.now().strftime("%Y%m%d_%H%M%S")),
#     data=data_e2e,
# )

# test = maihem_client.create_workflow_test(
#     name="test_5",
#     target_agent_name=target_agent_name,
#     dataset_name="dataset_sanity_check_e2e_2",
# )
# print(test)

# test = maihem_client.autogenerate_workflow_test(
#     name="test_autogen_sanity_check",
#     target_agent_name=target_agent_name,
#     label="Autogen sanity check 1",
#     modules=["cx"],
#     number_conversations=5,
# )
# print(test)

# test_run = maihem_client.run_workflow_test(
#     name="test_run" + datetime.now().strftime("%Y%m%d_%H%M%S"),
#     test_name="test_5",
# )
# print(test_run)


##################################################################
######################### WORKFLOW STEPS #########################
##################################################################

# maihem_client.upload_step_dataset(
#     name="dataset_step_reranking",  # + str(datetime.now().strftime("%Y%m%d_%H%M%S")),
#     data=data_reranking,
#     target_agent_name=target_agent_name,
#     step_name="reranking",
# )

test = maihem_client.create_step_test(
    name="test_reranking_3",
    step_name="reranking",
    target_agent_name=target_agent_name,
    dataset_name="dataset_step_reranking",
)
print(test)
