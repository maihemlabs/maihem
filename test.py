import src.maihem as maihem
import os


os.environ['MAIHEM_API_KEY'] = 'maihem-20240308-}:Sx^c4B&$NNvjLg?9bZCJgiZ!O;CPKv'


metrics_chatbot = {
    "Empathy": "The chatbot was able to understand and empathize with the persona's feelings",
    "Politeness": "The chatbot used polite language and tone to communicate with the persona",
    "On topic": "The chatbot stayed on topic and anwered the persona's request",
}

metrics_persona = {
    "Mood improvement": "The persona's mood improved",
    "Goal completion": "The goal of the persona was achieved",
    "Frustration avoidance": "The persona was not fustrated",
    "Question answering": "The persona's questions were answered successfully."
}


df_eval = maihem.evaluate(
    test_name="Puppeteer_Test_03042024",
    test_run_name="03042024_run_1_hr",
    metrics_chatbot=metrics_chatbot, 
    metrics_persona=metrics_persona
)

print(df_eval)

# maihem.create_test(
#     test_name="Puppeteer_Test_03042024",       # Choose a unique name for your test
#     chatbot_role="health care advisor", # Role of chatbot, e.g. "education tutor", "customer service agent"
#     industry="health care",         # Industry of chatbot
#     n=5,                          # Number of AI personas in test
#     topic="sleep disorders",               # Optional
#     # language="<language>"          # Optional
# ) 


