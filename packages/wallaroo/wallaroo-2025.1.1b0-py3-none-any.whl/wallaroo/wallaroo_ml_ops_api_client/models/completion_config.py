from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import (
    define as _attrs_define,
    field as _attrs_field,
)

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.completion_config_logit_bias_type_0 import (
        CompletionConfigLogitBiasType0,
    )


T = TypeVar("T", bound="CompletionConfig")


@_attrs_define
class CompletionConfig:
    """
    Attributes:
        best_of (Union[None, Unset, int]):
        echo (Union[None, Unset, bool]):
        frequency_penalty (Union[None, Unset, float]):
        logit_bias (Union['CompletionConfigLogitBiasType0', None, Unset]):
        logprobs (Union[None, Unset, int]):
        max_tokens (Union[None, Unset, int]):
        n (Union[None, Unset, int]):
        presence_penalty (Union[None, Unset, float]):
        seed (Union[None, Unset, int]):
        stop (Union[List[str], None, Unset]):
        suffix (Union[None, Unset, str]):
        temperature (Union[None, Unset, float]):
        top_p (Union[None, Unset, float]):
        user (Union[None, Unset, str]):
    """

    best_of: Union[None, Unset, int] = UNSET
    echo: Union[None, Unset, bool] = UNSET
    frequency_penalty: Union[None, Unset, float] = UNSET
    logit_bias: Union["CompletionConfigLogitBiasType0", None, Unset] = UNSET
    logprobs: Union[None, Unset, int] = UNSET
    max_tokens: Union[None, Unset, int] = UNSET
    n: Union[None, Unset, int] = UNSET
    presence_penalty: Union[None, Unset, float] = UNSET
    seed: Union[None, Unset, int] = UNSET
    stop: Union[List[str], None, Unset] = UNSET
    suffix: Union[None, Unset, str] = UNSET
    temperature: Union[None, Unset, float] = UNSET
    top_p: Union[None, Unset, float] = UNSET
    user: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.completion_config_logit_bias_type_0 import (
            CompletionConfigLogitBiasType0,
        )

        best_of: Union[None, Unset, int]
        if isinstance(self.best_of, Unset):
            best_of = UNSET
        else:
            best_of = self.best_of

        echo: Union[None, Unset, bool]
        if isinstance(self.echo, Unset):
            echo = UNSET
        else:
            echo = self.echo

        frequency_penalty: Union[None, Unset, float]
        if isinstance(self.frequency_penalty, Unset):
            frequency_penalty = UNSET
        else:
            frequency_penalty = self.frequency_penalty

        logit_bias: Union[Dict[str, Any], None, Unset]
        if isinstance(self.logit_bias, Unset):
            logit_bias = UNSET
        elif isinstance(self.logit_bias, CompletionConfigLogitBiasType0):
            logit_bias = self.logit_bias.to_dict()
        else:
            logit_bias = self.logit_bias

        logprobs: Union[None, Unset, int]
        if isinstance(self.logprobs, Unset):
            logprobs = UNSET
        else:
            logprobs = self.logprobs

        max_tokens: Union[None, Unset, int]
        if isinstance(self.max_tokens, Unset):
            max_tokens = UNSET
        else:
            max_tokens = self.max_tokens

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

        suffix: Union[None, Unset, str]
        if isinstance(self.suffix, Unset):
            suffix = UNSET
        else:
            suffix = self.suffix

        temperature: Union[None, Unset, float]
        if isinstance(self.temperature, Unset):
            temperature = UNSET
        else:
            temperature = self.temperature

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

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if best_of is not UNSET:
            field_dict["best_of"] = best_of
        if echo is not UNSET:
            field_dict["echo"] = echo
        if frequency_penalty is not UNSET:
            field_dict["frequency_penalty"] = frequency_penalty
        if logit_bias is not UNSET:
            field_dict["logit_bias"] = logit_bias
        if logprobs is not UNSET:
            field_dict["logprobs"] = logprobs
        if max_tokens is not UNSET:
            field_dict["max_tokens"] = max_tokens
        if n is not UNSET:
            field_dict["n"] = n
        if presence_penalty is not UNSET:
            field_dict["presence_penalty"] = presence_penalty
        if seed is not UNSET:
            field_dict["seed"] = seed
        if stop is not UNSET:
            field_dict["stop"] = stop
        if suffix is not UNSET:
            field_dict["suffix"] = suffix
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if top_p is not UNSET:
            field_dict["top_p"] = top_p
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.completion_config_logit_bias_type_0 import (
            CompletionConfigLogitBiasType0,
        )

        d = src_dict.copy()

        def _parse_best_of(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        best_of = _parse_best_of(d.pop("best_of", UNSET))

        def _parse_echo(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        echo = _parse_echo(d.pop("echo", UNSET))

        def _parse_frequency_penalty(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        frequency_penalty = _parse_frequency_penalty(d.pop("frequency_penalty", UNSET))

        def _parse_logit_bias(
            data: object,
        ) -> Union["CompletionConfigLogitBiasType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                logit_bias_type_0 = CompletionConfigLogitBiasType0.from_dict(data)

                return logit_bias_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CompletionConfigLogitBiasType0", None, Unset], data)

        logit_bias = _parse_logit_bias(d.pop("logit_bias", UNSET))

        def _parse_logprobs(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        logprobs = _parse_logprobs(d.pop("logprobs", UNSET))

        def _parse_max_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_tokens = _parse_max_tokens(d.pop("max_tokens", UNSET))

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

        def _parse_suffix(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        suffix = _parse_suffix(d.pop("suffix", UNSET))

        def _parse_temperature(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        temperature = _parse_temperature(d.pop("temperature", UNSET))

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

        completion_config = cls(
            best_of=best_of,
            echo=echo,
            frequency_penalty=frequency_penalty,
            logit_bias=logit_bias,
            logprobs=logprobs,
            max_tokens=max_tokens,
            n=n,
            presence_penalty=presence_penalty,
            seed=seed,
            stop=stop,
            suffix=suffix,
            temperature=temperature,
            top_p=top_p,
            user=user,
        )

        completion_config.additional_properties = d
        return completion_config

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
