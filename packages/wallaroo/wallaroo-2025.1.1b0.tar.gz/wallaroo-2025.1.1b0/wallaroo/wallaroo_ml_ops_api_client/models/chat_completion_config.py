from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import (
    define as _attrs_define,
    field as _attrs_field,
)

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chat_completion_config_logit_bias_type_0 import (
        ChatCompletionConfigLogitBiasType0,
    )
    from ..models.chat_completion_config_metadata_type_0 import (
        ChatCompletionConfigMetadataType0,
    )
    from ..models.chat_completion_function_definition import (
        ChatCompletionFunctionDefinition,
    )
    from ..models.chat_completion_response_format import ChatCompletionResponseFormat
    from ..models.venice_parameters import VeniceParameters


T = TypeVar("T", bound="ChatCompletionConfig")


@_attrs_define
class ChatCompletionConfig:
    """
    Attributes:
        frequency_penalty (Union[None, Unset, float]):
        function_call (Union[Unset, Any]):
        functions (Union[List['ChatCompletionFunctionDefinition'], None, Unset]):
        logit_bias (Union['ChatCompletionConfigLogitBiasType0', None, Unset]):
        logprobs (Union[None, Unset, int]):
        max_completion_tokens (Union[None, Unset, int]):
        max_tokens (Union[None, Unset, int]):
        metadata (Union['ChatCompletionConfigMetadataType0', None, Unset]):
        n (Union[None, Unset, int]):
        presence_penalty (Union[None, Unset, float]):
        response_format (Union['ChatCompletionResponseFormat', None, Unset]):
        seed (Union[None, Unset, int]):
        stop (Union[List[str], None, Unset]):
        store (Union[None, Unset, bool]):
        temperature (Union[None, Unset, float]):
        top_logprobs (Union[None, Unset, int]):
        top_p (Union[None, Unset, float]):
        user (Union[None, Unset, str]):
        venice_parameters (Union['VeniceParameters', None, Unset]):
    """

    frequency_penalty: Union[None, Unset, float] = UNSET
    function_call: Union[Unset, Any] = UNSET
    functions: Union[List["ChatCompletionFunctionDefinition"], None, Unset] = UNSET
    logit_bias: Union["ChatCompletionConfigLogitBiasType0", None, Unset] = UNSET
    logprobs: Union[None, Unset, int] = UNSET
    max_completion_tokens: Union[None, Unset, int] = UNSET
    max_tokens: Union[None, Unset, int] = UNSET
    metadata: Union["ChatCompletionConfigMetadataType0", None, Unset] = UNSET
    n: Union[None, Unset, int] = UNSET
    presence_penalty: Union[None, Unset, float] = UNSET
    response_format: Union["ChatCompletionResponseFormat", None, Unset] = UNSET
    seed: Union[None, Unset, int] = UNSET
    stop: Union[List[str], None, Unset] = UNSET
    store: Union[None, Unset, bool] = UNSET
    temperature: Union[None, Unset, float] = UNSET
    top_logprobs: Union[None, Unset, int] = UNSET
    top_p: Union[None, Unset, float] = UNSET
    user: Union[None, Unset, str] = UNSET
    venice_parameters: Union["VeniceParameters", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.chat_completion_config_logit_bias_type_0 import (
            ChatCompletionConfigLogitBiasType0,
        )
        from ..models.chat_completion_config_metadata_type_0 import (
            ChatCompletionConfigMetadataType0,
        )
        from ..models.chat_completion_response_format import (
            ChatCompletionResponseFormat,
        )
        from ..models.venice_parameters import VeniceParameters

        frequency_penalty: Union[None, Unset, float]
        if isinstance(self.frequency_penalty, Unset):
            frequency_penalty = UNSET
        else:
            frequency_penalty = self.frequency_penalty

        function_call = self.function_call

        functions: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.functions, Unset):
            functions = UNSET
        elif isinstance(self.functions, list):
            functions = []
            for functions_type_0_item_data in self.functions:
                functions_type_0_item = functions_type_0_item_data.to_dict()
                functions.append(functions_type_0_item)

        else:
            functions = self.functions

        logit_bias: Union[Dict[str, Any], None, Unset]
        if isinstance(self.logit_bias, Unset):
            logit_bias = UNSET
        elif isinstance(self.logit_bias, ChatCompletionConfigLogitBiasType0):
            logit_bias = self.logit_bias.to_dict()
        else:
            logit_bias = self.logit_bias

        logprobs: Union[None, Unset, int]
        if isinstance(self.logprobs, Unset):
            logprobs = UNSET
        else:
            logprobs = self.logprobs

        max_completion_tokens: Union[None, Unset, int]
        if isinstance(self.max_completion_tokens, Unset):
            max_completion_tokens = UNSET
        else:
            max_completion_tokens = self.max_completion_tokens

        max_tokens: Union[None, Unset, int]
        if isinstance(self.max_tokens, Unset):
            max_tokens = UNSET
        else:
            max_tokens = self.max_tokens

        metadata: Union[Dict[str, Any], None, Unset]
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, ChatCompletionConfigMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        n: Union[None, Unset, int]
        if isinstance(self.n, Unset):
            n = UNSET
        else:
            n = self.n

        presence_penalty: Union[None, Unset, float]
        if isinstance(self.presence_penalty, Unset):
            presence_penalty = UNSET
        else:
            presence_penalty = self.presence_penalty

        response_format: Union[Dict[str, Any], None, Unset]
        if isinstance(self.response_format, Unset):
            response_format = UNSET
        elif isinstance(self.response_format, ChatCompletionResponseFormat):
            response_format = self.response_format.to_dict()
        else:
            response_format = self.response_format

        seed: Union[None, Unset, int]
        if isinstance(self.seed, Unset):
            seed = UNSET
        else:
            seed = self.seed

        stop: Union[List[str], None, Unset]
        if isinstance(self.stop, Unset):
            stop = UNSET
        elif isinstance(self.stop, list):
            stop = self.stop

        else:
            stop = self.stop

        store: Union[None, Unset, bool]
        if isinstance(self.store, Unset):
            store = UNSET
        else:
            store = self.store

        temperature: Union[None, Unset, float]
        if isinstance(self.temperature, Unset):
            temperature = UNSET
        else:
            temperature = self.temperature

        top_logprobs: Union[None, Unset, int]
        if isinstance(self.top_logprobs, Unset):
            top_logprobs = UNSET
        else:
            top_logprobs = self.top_logprobs

        top_p: Union[None, Unset, float]
        if isinstance(self.top_p, Unset):
            top_p = UNSET
        else:
            top_p = self.top_p

        user: Union[None, Unset, str]
        if isinstance(self.user, Unset):
            user = UNSET
        else:
            user = self.user

        venice_parameters: Union[Dict[str, Any], None, Unset]
        if isinstance(self.venice_parameters, Unset):
            venice_parameters = UNSET
        elif isinstance(self.venice_parameters, VeniceParameters):
            venice_parameters = self.venice_parameters.to_dict()
        else:
            venice_parameters = self.venice_parameters

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if frequency_penalty is not UNSET:
            field_dict["frequency_penalty"] = frequency_penalty
        if function_call is not UNSET:
            field_dict["function_call"] = function_call
        if functions is not UNSET:
            field_dict["functions"] = functions
        if logit_bias is not UNSET:
            field_dict["logit_bias"] = logit_bias
        if logprobs is not UNSET:
            field_dict["logprobs"] = logprobs
        if max_completion_tokens is not UNSET:
            field_dict["max_completion_tokens"] = max_completion_tokens
        if max_tokens is not UNSET:
            field_dict["max_tokens"] = max_tokens
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if n is not UNSET:
            field_dict["n"] = n
        if presence_penalty is not UNSET:
            field_dict["presence_penalty"] = presence_penalty
        if response_format is not UNSET:
            field_dict["response_format"] = response_format
        if seed is not UNSET:
            field_dict["seed"] = seed
        if stop is not UNSET:
            field_dict["stop"] = stop
        if store is not UNSET:
            field_dict["store"] = store
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if top_logprobs is not UNSET:
            field_dict["top_logprobs"] = top_logprobs
        if top_p is not UNSET:
            field_dict["top_p"] = top_p
        if user is not UNSET:
            field_dict["user"] = user
        if venice_parameters is not UNSET:
            field_dict["venice_parameters"] = venice_parameters

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.chat_completion_config_logit_bias_type_0 import (
            ChatCompletionConfigLogitBiasType0,
        )
        from ..models.chat_completion_config_metadata_type_0 import (
            ChatCompletionConfigMetadataType0,
        )
        from ..models.chat_completion_function_definition import (
            ChatCompletionFunctionDefinition,
        )
        from ..models.chat_completion_response_format import (
            ChatCompletionResponseFormat,
        )
        from ..models.venice_parameters import VeniceParameters

        d = src_dict.copy()

        def _parse_frequency_penalty(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        frequency_penalty = _parse_frequency_penalty(d.pop("frequency_penalty", UNSET))

        function_call = d.pop("function_call", UNSET)

        def _parse_functions(
            data: object,
        ) -> Union[List["ChatCompletionFunctionDefinition"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                functions_type_0 = []
                _functions_type_0 = data
                for functions_type_0_item_data in _functions_type_0:
                    functions_type_0_item = ChatCompletionFunctionDefinition.from_dict(
                        functions_type_0_item_data
                    )

                    functions_type_0.append(functions_type_0_item)

                return functions_type_0
            except:  # noqa: E722
                pass
            return cast(
                Union[List["ChatCompletionFunctionDefinition"], None, Unset], data
            )

        functions = _parse_functions(d.pop("functions", UNSET))

        def _parse_logit_bias(
            data: object,
        ) -> Union["ChatCompletionConfigLogitBiasType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                logit_bias_type_0 = ChatCompletionConfigLogitBiasType0.from_dict(data)

                return logit_bias_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ChatCompletionConfigLogitBiasType0", None, Unset], data)

        logit_bias = _parse_logit_bias(d.pop("logit_bias", UNSET))

        def _parse_logprobs(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        logprobs = _parse_logprobs(d.pop("logprobs", UNSET))

        def _parse_max_completion_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_completion_tokens = _parse_max_completion_tokens(
            d.pop("max_completion_tokens", UNSET)
        )

        def _parse_max_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_tokens = _parse_max_tokens(d.pop("max_tokens", UNSET))

        def _parse_metadata(
            data: object,
        ) -> Union["ChatCompletionConfigMetadataType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = ChatCompletionConfigMetadataType0.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ChatCompletionConfigMetadataType0", None, Unset], data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        def _parse_n(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        n = _parse_n(d.pop("n", UNSET))

        def _parse_presence_penalty(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        presence_penalty = _parse_presence_penalty(d.pop("presence_penalty", UNSET))

        def _parse_response_format(
            data: object,
        ) -> Union["ChatCompletionResponseFormat", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_format_type_1 = ChatCompletionResponseFormat.from_dict(data)

                return response_format_type_1
            except:  # noqa: E722
                pass
            return cast(Union["ChatCompletionResponseFormat", None, Unset], data)

        response_format = _parse_response_format(d.pop("response_format", UNSET))

        def _parse_seed(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        seed = _parse_seed(d.pop("seed", UNSET))

        def _parse_stop(data: object) -> Union[List[str], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                stop_type_0 = cast(List[str], data)

                return stop_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None, Unset], data)

        stop = _parse_stop(d.pop("stop", UNSET))

        def _parse_store(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        store = _parse_store(d.pop("store", UNSET))

        def _parse_temperature(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        temperature = _parse_temperature(d.pop("temperature", UNSET))

        def _parse_top_logprobs(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        top_logprobs = _parse_top_logprobs(d.pop("top_logprobs", UNSET))

        def _parse_top_p(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        top_p = _parse_top_p(d.pop("top_p", UNSET))

        def _parse_user(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user = _parse_user(d.pop("user", UNSET))

        def _parse_venice_parameters(
            data: object,
        ) -> Union["VeniceParameters", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                venice_parameters_type_1 = VeniceParameters.from_dict(data)

                return venice_parameters_type_1
            except:  # noqa: E722
                pass
            return cast(Union["VeniceParameters", None, Unset], data)

        venice_parameters = _parse_venice_parameters(d.pop("venice_parameters", UNSET))

        chat_completion_config = cls(
            frequency_penalty=frequency_penalty,
            function_call=function_call,
            functions=functions,
            logit_bias=logit_bias,
            logprobs=logprobs,
            max_completion_tokens=max_completion_tokens,
            max_tokens=max_tokens,
            metadata=metadata,
            n=n,
            presence_penalty=presence_penalty,
            response_format=response_format,
            seed=seed,
            stop=stop,
            store=store,
            temperature=temperature,
            top_logprobs=top_logprobs,
            top_p=top_p,
            user=user,
            venice_parameters=venice_parameters,
        )

        chat_completion_config.additional_properties = d
        return chat_completion_config

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
