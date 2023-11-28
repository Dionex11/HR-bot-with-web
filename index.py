import os
from secret import OPENAI_API_KEY
from langchain.llms import OpenAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.chains.conversation.memory import ConversationBufferMemory


dataset = "dataset\Employee.csv"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY 


def app():
    # conversation memory
    memory = ConversationBufferMemory()

    while True:
        # Create CSV agent
        agent = create_csv_agent(
            OpenAI(temperature=0),
            dataset,
            memory=memory,
            verbose=False
        )
        # user query
        print("Enter Query: ")
        query = input()

        prompt = (
            """
                For the following query, if it requires drawing a table, reply as follows:
                {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}

                If the query requires creating a bar chart, reply as follows:
                {"bar": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

                If the query requires creating a line chart, reply as follows:
                {"line": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

                If the query requires creating a pie chart, reply as follows:
                {"pie": {"columns": ["A", "B", "C", ...], "data": [25%, 24%, 10%, ...]}}

                There can only be three types of chart, "pie", "bar" and "line".

                If it is just asking a question that requires none, reply as follows:
                {"answer": "answer"}
                Example:
                {"answer": "The title with the highest rating is 'Gilead'"}

                If you do not know the answer, reply as follows:
                {"answer": "I do not know."}

                Return all output as a string.

                All strings in "columns" list and data list, should be in double quotes,

                For example: {"columns": ["title", "ratings_count"], "data": [["Gilead", 361], ["Spider's Web", 5164]]}

                Lets think step by step.

                Below is the query.
                Query: 
                """
            + query
        )

        
        # Run the prompt through the agent.
        response = agent.run(prompt)

        # Convert the response to a string.
        print(response.__str__())



if __name__ == "__main__":
    app()
