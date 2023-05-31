from typing import Any, Dict, List
from pydantic import BaseModel
from langchain.chains.base import Chain
from langchain.base_language import BaseLanguageModel
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks.base import BaseCallbackHandler
from langchain.prompts import PromptTemplate
from chatmof.tools import load_chatmof_tools
from chatmof.agents.prompt import PROMPT


class ChatMOF(Chain):
    llm: BaseLanguageModel
    agent: BaseModel
    verbose: bool = False
    input_key: str = "query"
    output_key: str = "output"
    
    @property
    def input_keys(self) -> list[str]:
        return [self.input_key]
    
    @property
    def output_keys(self) -> list[str]:
        return [self.output_key]
    
    def _call(
            self,
            query: str,
            callbacks: List[BaseCallbackHandler] or None = None
    ) -> Dict[str, Any]:
        
        print ("\n" + "#"*10 + ' Question ' + "#"*30)
        print (query['query'])
        
        prompt = PromptTemplate(template=PROMPT, input_variables=[self.input_key])
        output = self.agent.run(
            prompt.format(**{self.input_key: query}),
                callbacks=callbacks
        )

        print ('\n')
        print ("#"*10 + ' Output ' + "#" * 30)
        print (output)
        print ('\n')
        print ('Thanks for using CHATMOF!')

        return {
            self.output_key: output
        }
    
    async def _acall(
            self,
            query: str,
    ) -> Dict[str, Any]:
        prompt = PromptTemplate(template=PROMPT, input_variables=[self.input_key])
        output = await self.agent.arun(prompt.format(**{self.input_key: query}))

        return {
            self.output_key: output
        }

    @classmethod
    def from_llm(
        cls: BaseModel,
        llm: BaseLanguageModel,
        verbose: bool = False,
        ):

        tools = load_chatmof_tools(llm, verbose=verbose)
        agent = initialize_agent(
            tools,
            llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=verbose,
        )
        
        return cls(agent=agent, llm=llm, verbose=verbose)
