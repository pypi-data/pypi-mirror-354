from typing import TYPE_CHECKING

import torch
import torch.nn.functional as F

from saefarer.analysis.feature_analysis import get_display_tokens
from saefarer.analysis.types import FeatureTokenSequence

if TYPE_CHECKING:
    from transformers import PreTrainedModel

    from saefarer import sae
    from saefarer.analysis import AnalysisConfig
    from saefarer.analysis.types import InferenceInput
    from saefarer.protocols import TokenizerProtocol


def inference(
    inference_input: "InferenceInput",
    model: "PreTrainedModel",
    tokenizer: "TokenizerProtocol",
    sae: "sae.SAE",
    cfg: "AnalysisConfig",
) -> "FeatureTokenSequence":
    tokenize_results = tokenizer.encode(
        inference_input["sequence"], max_length=cfg.model_sequence_length
    )

    input_ids = tokenize_results["token_ids"]
    token_ids = torch.tensor(input_ids, device=sae.device).unsqueeze(0)

    attention_mask = torch.tensor(
        tokenize_results["attention_mask"], device=sae.device
    ).unsqueeze(0)

    model_results = model(
        token_ids,
        attention_mask=attention_mask,
        output_hidden_states=True,
    )
    pred_probs = F.softmax(model_results.logits, dim=1).flatten()
    pred_label: int = pred_probs.argmax().item()  # type: ignore

    model_acts = model_results.hidden_states[cfg.hidden_state_index]
    sae_acts, _ = sae.encode(model_acts)
    feature_acts = sae_acts[0, :, inference_input["feature_index"]]

    display_tokens, max_token_index = get_display_tokens(
        tokenizer=tokenizer,
        input_ids=input_ids,
        activations=feature_acts.tolist(),
        sequence_index=-1,
        token_index=feature_acts.argmax().item(),  # type: ignore
        token_extras={},
        n_context_tokens=-1,
    )

    return FeatureTokenSequence(
        feature_index=inference_input["feature_index"],
        sequence_index=-1,
        display_tokens=display_tokens,
        max_token_index=max_token_index,
        label=-1,
        pred_label=pred_label,
        pred_probs=pred_probs.tolist(),
        extras={},
    )
