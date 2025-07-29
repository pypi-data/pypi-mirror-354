from typing import List, Optional, Tuple, Union

from huggingface_hub import hf_hub_download
from transformers.models.auto.tokenization_auto import AutoTokenizer
from transformers.tokenization_utils import PreTrainedTokenizer
from transformers.tokenization_utils_fast import PreTrainedTokenizerFast

from vajra._native.core.tokenizer import Tokenizer
from vajra.logger import init_logger

logger = init_logger(__name__)


def get_tokenizer_path(
    tokenizer_name: str,
    *args,
    **kwargs,
):
    path = hf_hub_download(tokenizer_name, filename="tokenizer.json", *args, **kwargs)
    return path


def get_tokenizer(
    tokenizer_name: str,
    *args,
    **kwargs,
):
    """Returns a Vajra tokenizer object backed by C++"""
    path = get_tokenizer_path(tokenizer_name, *args, **kwargs)
    tokenizer = Tokenizer.from_path(path)
    return tokenizer


def get_hf_tokenizer(
    tokenizer_name: str,
    tokenizer_mode: str = "auto",
    trust_remote_code: bool = False,
    *args,
    **kwargs,
) -> Union[PreTrainedTokenizer, PreTrainedTokenizerFast]:
    """Gets a tokenizer for the given model name via Huggingface."""
    if tokenizer_mode == "slow":
        if kwargs.get("use_fast", False):
            raise ValueError("Cannot use the fast tokenizer in slow tokenizer mode.")
        kwargs["use_fast"] = False

    try:
        tokenizer = AutoTokenizer.from_pretrained(
            tokenizer_name, *args, trust_remote_code=trust_remote_code, **kwargs
        )
    except TypeError as e:
        # The LLaMA tokenizer causes a protobuf error in some environments.
        err_msg = "Failed to load the tokenizer."
        raise RuntimeError(err_msg) from e
    except ValueError as e:
        # If the error pertains to the tokenizer class not existing or not
        # currently being imported, suggest using the --trust-remote-code flag.
        if not trust_remote_code and (
            "does not exist or is not currently imported." in str(e)
            or "requires you to execute the tokenizer file" in str(e)
        ):
            err_msg = (
                "Failed to load the tokenizer. If the tokenizer is a custom "
                "tokenizer not yet available in the HuggingFace transformers "
                "library, consider setting `trust_remote_code=True` in LLM "
                "or using the `--trust-remote-code` flag in the CLI."
            )
            raise RuntimeError(err_msg) from e
        else:
            raise e

    if not isinstance(tokenizer, PreTrainedTokenizerFast):
        logger.warning(
            "Using a slow tokenizer. This might cause a significant "
            "slowdown. Consider using a fast tokenizer instead."
        )
    return tokenizer


def get_eos_token_id(
    tokenizer_name: str,
    tokenizer_mode: str = "auto",
    trust_remote_code: bool = False,
    *args,
    **kwargs,
):
    """Returns the eos token id for a tokenizer"""

    # Do the simple thing here... use AutoTokenizer and extract eos_token_id
    # The alternative involves looking at different config files
    # ('config.json', 'generation_config.json', 'tokenizer_config.json') to
    # look for an `eos_token_id`, some of which may not exist. It's better to
    # let HF deal with this to protect from future changes in file format.

    tok = get_hf_tokenizer(
        tokenizer_name, *args, tokenizer_mode, trust_remote_code, **kwargs
    )
    return tok.eos_token_id


def _convert_tokens_to_string_with_added_encoders(
    tokenizer: Union[PreTrainedTokenizer, PreTrainedTokenizerFast],
    output_tokens: List[str],
    skip_special_tokens: bool,
) -> str:
    # Adapted from
    # https://github.com/huggingface/transformers/blob/v4.28.0/src/transformers/tokenization_utils.py#L921
    # NOTE(woosuk): The following code is slow because it runs a for loop over
    # the output_tokens. In Python, running a for loop over a list can be slow
    # even when the loop body is very simple.
    sub_texts = []
    current_sub_text: List[str] = []
    all_special_tokens = set(tokenizer.all_special_tokens)
    for token in output_tokens:
        if skip_special_tokens and token in all_special_tokens:
            continue
        if token in tokenizer.get_added_vocab():
            if current_sub_text:
                sub_text = tokenizer.convert_tokens_to_string(current_sub_text)
                sub_texts.append(sub_text)
                current_sub_text = []
            sub_texts.append(token)
        else:
            current_sub_text.append(token)
    if current_sub_text:
        sub_text = tokenizer.convert_tokens_to_string(current_sub_text)
        sub_texts.append(sub_text)
    return " ".join(sub_texts)


# Based on
# https://github.com/huggingface/text-generation-inference/blob/v0.9.4/server/text_generation_server/models/model.py#L62C9-L62C15
# under Apache 2.0 license
def detokenize_incrementally(
    tokenizer: Union[PreTrainedTokenizer, PreTrainedTokenizerFast],
    last_five_input_ids: List[int],
    prev_tokens: Optional[List[str]],
    prefix_offset: int = 0,
    read_offset: int = 0,
    skip_special_tokens: bool = False,
) -> Tuple[List[str], str, int, int]:
    new_token_id = last_five_input_ids[-1]

    # This is the first iteration for this sequence
    if prev_tokens is None:
        new_tokens: List[str]

        try:
            _new_tokens = tokenizer.convert_ids_to_tokens(
                last_five_input_ids[-6:], skip_special_tokens=skip_special_tokens
            )
            if type(_new_tokens) == str:
                new_tokens = [_new_tokens]
            else:
                assert isinstance(_new_tokens, list)
                new_tokens = _new_tokens
        except ValueError as e:
            new_tokens = ["[UNK]"] * 6
            logger.warning(f"Warning: {e}")

        output_tokens = new_tokens
        # 5 is an arbitrary value that should work for all
        # tokenizers (bigger = more conservative).
        # Subtract 1 extra to account for the generated token.
        prefix_offset = max(len(output_tokens) - 6, 0)
        read_offset = max(len(output_tokens) - 1, 0)
    else:
        new_tokens: List[str]

        # Put new_token_id in a list so skip_special_tokens is respected
        try:
            _new_tokens = tokenizer.convert_ids_to_tokens(
                [new_token_id], skip_special_tokens=skip_special_tokens
            )
            if type(_new_tokens) == str:
                new_tokens = [_new_tokens]
            else:
                assert isinstance(_new_tokens, list)
                new_tokens = _new_tokens
        except ValueError as e:
            new_tokens = [prev_tokens[-1]]
            logger.warning(f"Warning: {e}")

        output_tokens = prev_tokens + new_tokens

    # The prefix text is necessary only to defeat cleanup algorithms in
    # the decode which decide to add a space or not depending on the
    # surrounding ids.
    if tokenizer.is_fast or not tokenizer.get_added_vocab():
        prefix_text = tokenizer.convert_tokens_to_string(
            output_tokens[prefix_offset:read_offset]
        )
        new_text = tokenizer.convert_tokens_to_string(output_tokens[prefix_offset:])
    else:
        prefix_text = _convert_tokens_to_string_with_added_encoders(
            tokenizer,
            output_tokens[prefix_offset:read_offset],
            skip_special_tokens=skip_special_tokens,
        )
        new_text = _convert_tokens_to_string_with_added_encoders(
            tokenizer,
            output_tokens[prefix_offset:],
            skip_special_tokens=skip_special_tokens,
        )

    if len(new_text) > len(prefix_text) and not new_text.endswith("�"):
        # utf-8 char at the end means it's a potential unfinished byte sequence
        # from byte fallback tokenization.
        # If it's in the middle, it's probably a real invalid id generated
        # by the model
        new_text = new_text[len(prefix_text) :]
        return new_tokens, new_text, read_offset, len(output_tokens)
    else:
        return new_tokens, "", prefix_offset, read_offset
