import ast
import json
from llm.llm_ops import query_llm
from agents.base_agent import Agent
from logger import log_message

class AgentOrchestrator:
    def __init__(self, agents: list[Agent]):
        self.agents = agents
        self.memory = []  # Stores the reasoning and action steps taken
        self.max_memory = 10

    def json_parser(self, input_string):

      print(type(input_string))

      python_dict = ast.literal_eval(input_string)
      json_string = json.dumps(python_dict)
      json_dict = json.loads(json_string)

      if isinstance(json_dict, dict) or isinstance(json_dict,list):
        return json_dict

      raise "Invalid JSON response"

    def orchestrate_task(self, user_input: str):        
        self.memory = self.memory[-self.max_memory:]

        context = "\n".join(self.memory)

        print(f"Context: {context}")

        response_format = {"action":"", "input":"", "next_action":""}
        
        def get_prompt(user_input):
            return f"""

                Use the context from memory to plan next steps.                
                Context:
                {context}

                You are an expert intent classifier.
                You need will use the context provided and the user's input to classify the intent select the appropriate agent.                
                You will rewrite the input for the agent so that the agent can efficiently execute the task.                                                

                Here are the available agents and their descriptions:
                {", ".join([f"- {agent.name}: {agent.description}" for agent in self.agents])}

                User Input:
                {user_input}              

                ###Guidelines###
                - Sometimes you might have to use multiple agent's to solve user's input. You have to do that in a loop.
                - The original userinput could have multiple tasks, you will use the context to understand the previous actions taken and the next steps you should take.
                - Read the context, take your time to understand, see if there were many tasks and if you executed them all
                - If there are no actions to be taken, then make the action "respond_to_user" with your final thoughts combining all previous responses as input.
                - Respond with "respond_to_user" only when there are no agents to select from or there is no next_action
                - You will return the agent name in the form of {response_format}
                - Always return valid JSON like {response_format} and nothing else.                

                """


        response = ""
        loop_count = 0
        self.memory = self.memory[-10:]        
        prompt = get_prompt(user_input)
        llm_response = query_llm(prompt)

        llm_response = self.json_parser(llm_response)
        print(f"LLM Response: {llm_response}")

        self.memory.append(f"Orchestrator: {llm_response}")
        

        action=  llm_response["action"]
        user_input = llm_response["input"]

        print(f"Action identified by LLM: {action}")
        
       
        if action == "respond_to_user":
            return llm_response
        for agent in self.agents:
            if agent.name == action:
                print("*******************Found Agent Name*******************************")
                agent_response = agent.process_input(user_input)
                print(f"{action} response: {agent_response}")
                self.memory.append(f"Agent Response for Task: {agent_response}")
                print(self.memory)
                return agent_response                
            

    def run(self):
        print("LLM Agent: Hello! How can I assist you today?")
        user_input = input("You: ")
        self.memory.append(f"User: {user_input}")

        while True:            
            if user_input.lower() in ["exit", "bye", "close"]:
                print("See you later!")
                break

            response = self.orchestrate_task(user_input)
            print(f"Final response of orchestrator {response}")
            if isinstance(response, dict) and response["action"] == "respond_to_user":                
                log_message(f"Reponse from Agent: {response["input"]}", "RESPONSE")
                user_input = input("You: ")
                self.memory.append(f"User: {user_input}")                
            elif response == "No action or agent needed":
                print("Reponse from Agent: ", response)
                user_input = input("You: ")
            else:
                user_input = response                
