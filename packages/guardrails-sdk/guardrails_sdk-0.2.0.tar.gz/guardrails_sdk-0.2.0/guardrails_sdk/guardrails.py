from pydantic import BaseModel
from typing import List, Dict, Optional,Literal

from guardrails_sdk.pii.pii import analyze_and_mask_text
from guardrails_sdk.toxicity.toxic_bert import detect_toxicity
from guardrails_sdk.prompt_secure.prompt_break import classify_prompt_injection
from guardrails_sdk.compitator_banned_words.block_words import moderate_text
import asyncio


class ToxiRequest(BaseModel):
    content: str
    treshold: float = 0.5


class Prompt(BaseModel):
    content: str


class TransformRequest(BaseModel):
    content: str
    guardrails: List[str]
    treshold: float = 0.5
    custom_entities: Optional[List[Dict]] = None
    action: Optional[Literal["mask", "block"]] = None
    compitator_loc: Optional[str] = None
    block_loc: Optional[str] = None

class Compitator(BaseModel):
    content: str
    action: Literal["mask", "block"]
    compitator_loc: Optional[str] = None
    block_loc: Optional[str] = None

class GuardrailsClient:
    def __init__(self):
        pass

    async def validate_content(self, request: ToxiRequest):
        result = await detect_toxicity(request.content, request.treshold)
        return result

    async def transform_content(self, request: TransformRequest):
        res = await analyze_and_mask_text(
            request.content, request.guardrails, request.custom_entities, request.treshold)
        return res

    async def prompt_injection(self, request: Prompt):
        result = await classify_prompt_injection(request.content)
        return result

    async def run_all_guardrails(self, request: TransformRequest):
        pii_result, toxicity_result, prompt_injection_result,moderate_result = await asyncio.gather(
            analyze_and_mask_text(
                request.content, request.guardrails, request.custom_entities, request.treshold),
            detect_toxicity(request.content, request.treshold),
            classify_prompt_injection(request.content),
            moderate_text(request.content,request.block_loc,request.compitator_loc,request.action)
        )
        return {
            "pii": pii_result,
            "toxicity": toxicity_result,
            "prompt_injection": prompt_injection_result,
            "moderate_result":moderate_result
        }
    
    async def compitator_banned(self, request: Compitator):
        response = await moderate_text(
            text=request.content,
            banned_words_file=request.block_loc,
            competitor_words_file=request.compitator_loc,
            action=request.action
        )
        return response
