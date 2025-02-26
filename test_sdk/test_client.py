from datetime import datetime

from maihem import Maihem

from data import data_e2e, data_reranking


target_agent_name = "target-deco-names"
test_name = "test_reranking_2602_2"


maihem_client = Maihem(env="local")
try:
    target_agent = maihem_client.add_target_agent(
        name=target_agent_name,
        role="Airbnb customer support agent",
        description="Airbnb customer support agent that can help with questions about the platform",
    )
except Exception as e:
    print(e)
    target_agent = maihem_client.get_target_agent(name=target_agent_name)
print(target_agent)


##################################################################
######################### WORKFLOW STEPS #########################
##################################################################

# maihem_client.upload_dataset(
#     name="dataset_reranking_2",  # + str(datetime.now().strftime("%Y%m%d_%H%M%S")),
#     data=data_reranking,
#     target_agent_name=target_agent_name,
#     workflow_step_name="reranking_function",
# )

# test = maihem_client.create_test_uploaded_data(
#     name=test_name,
#     workflow_step_name="reranking_function",
#     target_agent_name=target_agent_name,
#     dataset_name="dataset_reranking_2",
# )
# print(test)

# maihem_client.generate_wrapper_function(test_name=test_name)

# revision = maihem_client._create_agent_target_revision(
#     name="revision_2602_5",
#     target_agent_id=target_agent.id,
# )
# print(revision)

# test_run = maihem_client.run_test(
#     name="test_run_reranking_" + datetime.now().strftime("%Y%m%d_%H%M%S"),
#     test_name=test_name,
# )
# print(test_run)


##################################################################
######################### WORKFLOW (ALL) #########################
##################################################################

# maihem_client.upload_dataset(
#     name="dataset_e2e_1",  # + str(datetime.now().strftime("%Y%m%d_%H%M%S")),
#     data=data_e2e,
#     target_agent_name=target_agent_name,
#     workflow_step_name="generate_message",
# )

# test = maihem_client.create_test_uploaded_data(
#     name=test_name,
#     workflow_step_name="generate_message",
#     target_agent_name=target_agent_name,
#     dataset_name="dataset_e2e_1",
# )
# print(test)

# test_run = maihem_client.run_test(
#     name="test_run_" + datetime.now().strftime("%Y%m%d_%H%M%S"),
#     test_name=test_name,
#     concurrent_interactions=1,
# )
# print(test_run)


# test = maihem_client.create_workflow_test(
#     name=test_name,
#     target_agent_name=target_agent_name,
#     dataset_name="dataset_sanity_check_e2e_dict",
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
#     test_name=test_name,
#     concurrent_conversations=1,
# )
# print(test_run)
