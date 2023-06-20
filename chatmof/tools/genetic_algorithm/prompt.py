PLAN_PROMPT = """Create a plan to generate material based on the following question. 
Use the following format:

Question: the input question you must to answer
Thought: you should always think about what to do
Search look-up table: plan to extract 200 material for the purpose from the look-up table where the property is pre-calculated.
Genetic algorithm: plan to create a new materials using the 200 extracted mateirals.

Begin!
Question: generate a material with a porosity of 0.5
Thought: I need to generate a material with a porosity value of 0.5. 
Search look-up table: extract name and porosity of 200 materials with porosity close to 0.5 from look-up tables. 
Genetic algorithm: create a new material with a porosity close to 0.5 from 200 materials

Question: generate a material with a highest band-gap
Thought: I need to generate a material with a highest band-gap.
Search look-up table: extract name and band-gap of 200 materials with high band-gap value from look-up tables. 
Genetic algorithm: generate 200 new materials with the highest band gap from the 200 materials.

Question: {question}"""


GENETIC_PROMPT = (
    "You should act as a generator to find the optimal material. "
    "A substance consists of a block1, block2, and must maintain the order. "
    "I will give you 200 parent materials with value. "
    "Based on these, you must answer as many new children as you expect to answer the question. "
    "You output children only and nothing else."
    "\n\n"
    "Begin.\n"
    "Question: {question}\n"
    "Parent:\n"
    "V1+T1 (value: 1.0)\n"
    "V2+T2 (value: 0.0)\n"
    "2 new Children:\n"
    "V2+T1, V1+T2\n"
    "Parent:\n"
    "{parents}"
    "200 new Children:\n"
)


if __name__ == '__main__':
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain
    from langchain.chat_models import ChatOpenAI

    llm = ChatOpenAI(temperature=0.0)
    prompt = PromptTemplate(template=PLAN_PROMPT, input_variables=['question'])
    chain = LLMChain(llm=llm, prompt=prompt)
    output = chain.run('Generate a material with surface area near 0.2')
    print (output)