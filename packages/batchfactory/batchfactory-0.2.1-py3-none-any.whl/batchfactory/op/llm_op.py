from ..core import *
from ..lib.llm_backend import LLMRequest, LLMMessage, LLMResponse, compute_llm_cost, get_provider_name
from ..lib.utils import get_format_keys, hash_texts
from ..brokers.concurrent_llm_call_broker import ConcurrentLLMCallBroker
from ..core.broker import BrokerJobRequest, BrokerJobResponse, BrokerJobStatus
from .common_op import RemoveField
from ..lib.utils import  _to_record, _to_BaseModel, _dict_to_dataclass, _to_list_2, _pick_field_or_value_strict
from .broker_op import BrokerOp, BrokerFailureBehavior
import copy
from typing import List, Dict, NamedTuple, Set, Tuple
from dataclasses import asdict



class GenerateLLMRequest(ApplyOp):
    """
    Generate a LLM query from a given prompt and save to entry.data["llm_request"]
    if the prompt is a string template, it will format according to entry.data 
    """
    def __init__(self,user_prompt,model,
                 max_completion_tokens=4096,
                 role="user",
                 output_field="llm_request",
                 system_prompt=None,
                 chat_history_field:str|bool|None=None, # if provided, will append the history to the prompt, if True, default to "chat_history"
                 after_prompt=None, # if provided, will append the after_prompt after the history
                 ):
        super().__init__()
        self.role = role
        self.user_prompt = user_prompt
        self.system_prompt = system_prompt
        if chat_history_field is True: 
            chat_history_field = "chat_history"
        self.history_field = chat_history_field
        self.after_prompt = after_prompt
        self.model = model
        self.max_completion_tokens = max_completion_tokens
        self.output_field = output_field
    def update(self, entry: Entry) -> None:
        messages = self._build_messages(entry)
        request_obj = LLMRequest(
            custom_id=self._generate_custom_id(messages, self.model, self.max_completion_tokens),
            messages=messages,
            model=self.model,
            max_completion_tokens=self.max_completion_tokens
        )
        entry.data[self.output_field] = request_obj.model_dump()
    
    def _build_messages(self,entry:Entry)->List[LLMMessage]:
        messages = []
        if self.system_prompt:
            system_str = self.system_prompt.format(**{k: entry.data[k] for k in get_format_keys(self.system_prompt)})
            messages.append(LLMMessage(role="system", content=system_str))
        if self.user_prompt:
            prompt_str = self.user_prompt.format(**{k: entry.data[k] for k in get_format_keys(self.user_prompt)})
            messages.append(LLMMessage(role=self.role, content=prompt_str))
        if self.history_field:
            history = entry.data.get(self.history_field, [])
            for msg in history:
                messages.append(LLMMessage(role=msg["role"], content=msg["content"]))
        if self.after_prompt:
            after_prompt_str = self.after_prompt.format(**{k: entry.data[k] for k in get_format_keys(self.after_prompt)})
            messages.append(LLMMessage(role=self.role, content=after_prompt_str))
        return messages

    @staticmethod
    def _generate_custom_id(messages,model,max_completion_tokens):
        texts=[model,str(max_completion_tokens)]
        for message in messages:
            texts.extend([message.role, message.content])
        return hash_texts(*texts)
    
class ExtractResponseMeta(ApplyOp):
    def __init__(self, 
                 input_response_field="llm_response", 
                 input_request_field="llm_request",
                 output_model_field="model",
                 accumulated_cost_field="api_cost",
                 ):
        super().__init__()
        self.input_response_field = input_response_field
        self.input_request_field = input_request_field
        self.output_model_field = output_model_field
        self.accumulated_cost_field = accumulated_cost_field
    def update(self, entry: Entry) -> None:
        llm_response = entry.data.get(self.input_response_field, None)
        llm_response:LLMResponse = LLMResponse.model_validate(llm_response)
        llm_request = entry.data.get(self.input_request_field, None)
        llm_request:LLMRequest = LLMRequest.model_validate(llm_request)
        if self.output_model_field:
            entry.data[self.output_model_field] = llm_request.model
        if self.accumulated_cost_field:
            cost = compute_llm_cost(llm_response,get_provider_name(llm_request.model))
            entry.data[self.accumulated_cost_field] = cost + entry.data.get(self.accumulated_cost_field, 0.0)

class ExtractResponseText(ApplyOp):
    def __init__(self, 
                 input_field="llm_response", 
                 output_field="text",
                 ):
        super().__init__()
        self.input_field = input_field
        self.output_field = output_field
    def update(self, entry: Entry) -> None:
        llm_response = entry.data.get(self.input_field, None)
        llm_response:LLMResponse = LLMResponse.model_validate(llm_response)
        entry.data[self.output_field] = llm_response.message.content
    
class UpdateChatHistory(ApplyOp):
    def __init__(self,
                    input_field="llm_response",
                    output_field="chat_history",
                    character_name:str=None, # e.g. "Timmy"
                    character_field:str=None, # e.g. "character_name"
    ):
        super().__init__()
        self.input_field = input_field
        self.output_field = output_field
        self.character_name = character_name
        self.character_field = character_field
    def update(self, entry: Entry) -> None:
        llm_response = entry.data.get(self.input_field, None)
        llm_response:LLMResponse = LLMResponse.model_validate(llm_response)
        chat_history = entry.data.setdefault(self.output_field, [])
        chat_history.append({
            "role": _pick_field_or_value_strict(entry.data, self.character_field, self.character_name, default=llm_response.message.role),
            "content": llm_response.message.content,
        })
        entry.data[self.output_field] = chat_history
    
class ChatHistoryToText(ApplyOp):
    def __init__(self, 
                 input_field="chat_history",
                 output_field="text",
                 template="**{role}**: {content}\n\n",
                 exclude_roles:List[str]|None=None, # e.g. ["system"]
    ):
        super().__init__()
        self.input_field = input_field
        self.output_field = output_field
        self.template = template
        self.exclude_roles = _to_list_2(exclude_roles)
    def update(self, entry: Entry) -> None:
        text=""
        chat_history = entry.data[self.input_field]
        for message in chat_history:
            if message["role"] in self.exclude_roles:
                continue
            text += self.template.format(role=message["role"], content=message["content"])
        entry.data[self.output_field] = text

        
class TransformCharacterDialogueForLLM(ApplyOp):
    def __init__(self, 
                 character_name:str|None=None, # e.g. "Timmy"
                 character_field:str|None=None, # e.g. "character_name"
                 prompt_template="{name}: {content}\n",
                 input_field="llm_request",
    ):
        super().__init__()
        self.character_name = character_name
        self.character_field = character_field
        self.input_field = input_field
        self.allowed_roles=["user","assistant","system"]
        self.prompt_template = prompt_template
    def update(self, entry: Entry) -> None:
        llm_request = entry.data.get(self.input_field, None)
        llm_request:LLMRequest = LLMRequest.model_validate(llm_request)
        input_messages = llm_request.messages
        output_messages = []
        assistant_character_name = _pick_field_or_value_strict(entry.data, self.character_field, self.character_name, default="assistant")
        for input_message in input_messages:
            if input_message.role in self.allowed_roles:
                output_messages.append(input_message)
                continue
            if input_message.role == assistant_character_name:
                role = "assistant"
            else:
                role = "user"
            context = self.prompt_template.format(name=input_message.role, content=input_message.content)
            if len(output_messages)>0 and output_messages[-1].role == role:
                output_messages[-1].content += context
            else:
                output_messages.append(LLMMessage(role=role, content=context))
        llm_request.messages = output_messages
        entry.data[self.input_field] = llm_request.model_dump()

    
class PrintTotalCost(OutputOp):
    def __init__(self, accumulated_cost_field="api_cost"):
        super().__init__()
        self.accumulated_cost_field = accumulated_cost_field
    def output_batch(self,batch:Dict[str,Entry])->None:
        total_cost = sum(entry.data.get(self.accumulated_cost_field, 0.0) for entry in batch.values())
        if total_cost<0.05:
            print(f"Total API cost for the output: {total_cost: .6f} USD")
        else:
            print(f"Total API cost for the output: ${total_cost:.2f} USD")
    

class ConcurrentLLMCall(BrokerOp):
    def __init__(self,
                    cache_path: str,
                    broker: ConcurrentLLMCallBroker,
                    input_field="llm_request",
                    output_field="llm_response",
                    status_field="status",
                    job_idx_field="job_idx",
                    keep_all_rev: bool = True,
                    failure_behavior:BrokerFailureBehavior = BrokerFailureBehavior.STAY
    ):
        super().__init__(
            cache_path=cache_path,
            broker=broker,
            keep_all_rev=keep_all_rev,
            status_field=status_field,
            job_idx_field=job_idx_field,
            failure_behavior=failure_behavior
        )
        self.input_field = input_field
        self.output_field = output_field

    def generate_job_idx(self, entry):
        return entry.data[self.input_field]["custom_id"]

    def get_request_object(self, entry: Entry)->Dict:
        return LLMRequest.model_validate(entry.data[self.input_field])
        
    def dispatch_broker(self, mock:bool=False)->None:
        if self.failure_behavior == BrokerFailureBehavior.RETRY:
            allowed_status = [BrokerJobStatus.FAILED, BrokerJobStatus.QUEUED]
        else:
            allowed_status = [BrokerJobStatus.QUEUED]
        requests = self.broker.get_job_requests(allowed_status)
        if not requests:
            return
        self.broker.process_jobs(requests, mock=mock)


class CleanupLLMData(RemoveField):
    def __init__(self,fields=["llm_request","llm_response","status"]):
        super().__init__(*fields)

class SplitCot(ApplyOp):
    def __init__(self, input_field="llm_response", cot_field="cot", label = "</think>", start_label = "<think>"):
        super().__init__()
        self.input_field = input_field
        self.cot_field = cot_field
        self.label = label
        self.start_label = start_label
    def update(self, entry: Entry) -> None:
        llm_response = entry.data.get(self.input_field, None)
        llm_response:LLMResponse = LLMResponse.model_validate(llm_response)
        content = llm_response.message.content
        cot = ""
        if self.label in content:
            cot, content = content.split(self.label,1)
            if self.start_label and cot.strip().startswith(self.start_label):
                cot = cot.strip()[len(self.start_label):]
        if self.cot_field:
            entry.data[self.cot_field] = cot.strip()
        llm_response.message.content = content
        entry.data[self.input_field] = llm_response.model_dump()
        




__all__ = [
    "GenerateLLMRequest",
    "ExtractResponseText",
    "ExtractResponseMeta",
    "UpdateChatHistory",
    "TransformCharacterDialogueForLLM",
    "ConcurrentLLMCall",
    "PrintTotalCost",
    "CleanupLLMData",
    "ChatHistoryToText",
    "SplitCot",
]





