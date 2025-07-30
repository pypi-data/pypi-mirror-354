r'''
# `provider`

Refer to the Terraform Registry for docs: [`okta`](https://registry.terraform.io/providers/okta/okta/4.20.0/docs).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class OktaProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.provider.OktaProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs okta}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        access_token: typing.Optional[builtins.str] = None,
        alias: typing.Optional[builtins.str] = None,
        api_token: typing.Optional[builtins.str] = None,
        backoff: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        base_url: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        http_proxy: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[jsii.Number] = None,
        max_api_capacity: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        max_wait_seconds: typing.Optional[jsii.Number] = None,
        min_wait_seconds: typing.Optional[jsii.Number] = None,
        org_name: typing.Optional[builtins.str] = None,
        parallelism: typing.Optional[jsii.Number] = None,
        private_key: typing.Optional[builtins.str] = None,
        private_key_id: typing.Optional[builtins.str] = None,
        request_timeout: typing.Optional[jsii.Number] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs okta} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param access_token: Bearer token granting privileges to Okta API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#access_token OktaProvider#access_token}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#alias OktaProvider#alias}
        :param api_token: API Token granting privileges to Okta API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#api_token OktaProvider#api_token}
        :param backoff: Use exponential back off strategy for rate limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#backoff OktaProvider#backoff}
        :param base_url: The Okta url. (Use 'oktapreview.com' for Okta testing). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#base_url OktaProvider#base_url}
        :param client_id: API Token granting privileges to Okta API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#client_id OktaProvider#client_id}
        :param http_proxy: Alternate HTTP proxy of scheme://hostname or scheme://hostname:port format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#http_proxy OktaProvider#http_proxy}
        :param log_level: providers log level. Minimum is 1 (TRACE), and maximum is 5 (ERROR). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#log_level OktaProvider#log_level}
        :param max_api_capacity: Sets what percentage of capacity the provider can use of the total rate limit capacity while making calls to the Okta management API endpoints. Okta API operates in one minute buckets. See Okta Management API Rate Limits: https://developer.okta.com/docs/reference/rl-global-mgmt/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#max_api_capacity OktaProvider#max_api_capacity}
        :param max_retries: maximum number of retries to attempt before erroring out. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#max_retries OktaProvider#max_retries}
        :param max_wait_seconds: maximum seconds to wait when rate limit is hit. We use exponential backoffs when backoff is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#max_wait_seconds OktaProvider#max_wait_seconds}
        :param min_wait_seconds: minimum seconds to wait when rate limit is hit. We use exponential backoffs when backoff is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#min_wait_seconds OktaProvider#min_wait_seconds}
        :param org_name: The organization to manage in Okta. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#org_name OktaProvider#org_name}
        :param parallelism: Number of concurrent requests to make within a resource where bulk operations are not possible. Take note of https://developer.okta.com/docs/api/getting_started/rate-limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#parallelism OktaProvider#parallelism}
        :param private_key: API Token granting privileges to Okta API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#private_key OktaProvider#private_key}
        :param private_key_id: API Token Id granting privileges to Okta API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#private_key_id OktaProvider#private_key_id}
        :param request_timeout: Timeout for single request (in seconds) which is made to Okta, the default is ``0`` (means no limit is set). The maximum value can be ``300``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#request_timeout OktaProvider#request_timeout}
        :param scopes: API Token granting privileges to Okta API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#scopes OktaProvider#scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0808da6b083e2f9f99a310ae982044c5cce9f930ec458184ed0d591ca91e8007)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = OktaProviderConfig(
            access_token=access_token,
            alias=alias,
            api_token=api_token,
            backoff=backoff,
            base_url=base_url,
            client_id=client_id,
            http_proxy=http_proxy,
            log_level=log_level,
            max_api_capacity=max_api_capacity,
            max_retries=max_retries,
            max_wait_seconds=max_wait_seconds,
            min_wait_seconds=min_wait_seconds,
            org_name=org_name,
            parallelism=parallelism,
            private_key=private_key,
            private_key_id=private_key_id,
            request_timeout=request_timeout,
            scopes=scopes,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a OktaProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OktaProvider to import.
        :param import_from_id: The id of the existing OktaProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OktaProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51abd6d60d616dbc97a7bb26aafa91aa4440531aaca2984f18dd46c2b1e89c38)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAccessToken")
    def reset_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToken", []))

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetApiToken")
    def reset_api_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiToken", []))

    @jsii.member(jsii_name="resetBackoff")
    def reset_backoff(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackoff", []))

    @jsii.member(jsii_name="resetBaseUrl")
    def reset_base_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBaseUrl", []))

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetHttpProxy")
    def reset_http_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpProxy", []))

    @jsii.member(jsii_name="resetLogLevel")
    def reset_log_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogLevel", []))

    @jsii.member(jsii_name="resetMaxApiCapacity")
    def reset_max_api_capacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxApiCapacity", []))

    @jsii.member(jsii_name="resetMaxRetries")
    def reset_max_retries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRetries", []))

    @jsii.member(jsii_name="resetMaxWaitSeconds")
    def reset_max_wait_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxWaitSeconds", []))

    @jsii.member(jsii_name="resetMinWaitSeconds")
    def reset_min_wait_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinWaitSeconds", []))

    @jsii.member(jsii_name="resetOrgName")
    def reset_org_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrgName", []))

    @jsii.member(jsii_name="resetParallelism")
    def reset_parallelism(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelism", []))

    @jsii.member(jsii_name="resetPrivateKey")
    def reset_private_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateKey", []))

    @jsii.member(jsii_name="resetPrivateKeyId")
    def reset_private_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateKeyId", []))

    @jsii.member(jsii_name="resetRequestTimeout")
    def reset_request_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestTimeout", []))

    @jsii.member(jsii_name="resetScopes")
    def reset_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScopes", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenInput")
    def access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="apiTokenInput")
    def api_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="backoffInput")
    def backoff_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "backoffInput"))

    @builtins.property
    @jsii.member(jsii_name="baseUrlInput")
    def base_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="httpProxyInput")
    def http_proxy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpProxyInput"))

    @builtins.property
    @jsii.member(jsii_name="logLevelInput")
    def log_level_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "logLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="maxApiCapacityInput")
    def max_api_capacity_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxApiCapacityInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRetriesInput")
    def max_retries_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetriesInput"))

    @builtins.property
    @jsii.member(jsii_name="maxWaitSecondsInput")
    def max_wait_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxWaitSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="minWaitSecondsInput")
    def min_wait_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minWaitSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="orgNameInput")
    def org_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgNameInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelismInput")
    def parallelism_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "parallelismInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyIdInput")
    def private_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyInput")
    def private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="requestTimeoutInput")
    def request_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "requestTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="scopesInput")
    def scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopesInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e6d4b67aedcc0e8bae05fa446f17b047c0b5cba4e11b6b7a31e076ac950c31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97384be160dc39111d7579ed322eb92fd9e30057a81b7131b547d255276e0d7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiToken")
    def api_token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiToken"))

    @api_token.setter
    def api_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07fa7e60a80c2e5ee86d15a5bb1eec773afd17b818dbe22339e6a397ab81222a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backoff")
    def backoff(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "backoff"))

    @backoff.setter
    def backoff(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a2efb511f2eea65a6443a2843f2849f375c10359aae511a4bcefbb8c06b51df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backoff", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="baseUrl")
    def base_url(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseUrl"))

    @base_url.setter
    def base_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c3fe221116fa818079480b193405db75a8cb36d5937b182be5f9f6fddf87a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3852e89eb40ce1fd097eb1e37fdf1af3fa0b2e672666efe612f5f386e5e71e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpProxy")
    def http_proxy(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpProxy"))

    @http_proxy.setter
    def http_proxy(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16f485d30996cfe76676661fd4b4f89666efd7467358770eeac526d9fe14f348)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpProxy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "logLevel"))

    @log_level.setter
    def log_level(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__824238a8dc65639d3c07c656d9007ddcc1a51ad127ffec02ed20bd46348827d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxApiCapacity")
    def max_api_capacity(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxApiCapacity"))

    @max_api_capacity.setter
    def max_api_capacity(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f58b0fa38112bac5f723b72a8886918611ec6f47c64d41ec017cc93c751db1e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxApiCapacity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRetries")
    def max_retries(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetries"))

    @max_retries.setter
    def max_retries(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e87d41a2a7d444fe492057606056e9c8a7a673e0c4643e0e46877a0285fb20b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxWaitSeconds")
    def max_wait_seconds(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxWaitSeconds"))

    @max_wait_seconds.setter
    def max_wait_seconds(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20ddd950d51d4d3722c5af1222f8d20d5208be7f36a3010b0f6d2bd9d4e06162)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxWaitSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minWaitSeconds")
    def min_wait_seconds(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minWaitSeconds"))

    @min_wait_seconds.setter
    def min_wait_seconds(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b98daea3afef8d037c098df73aaacdb3165055e283fa79b946d4acbf1946f085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minWaitSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orgName")
    def org_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgName"))

    @org_name.setter
    def org_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bc910d954f91ee43c7de4fdd0ea5a119adb81df8a3200fafaf52968a0e5281e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parallelism")
    def parallelism(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "parallelism"))

    @parallelism.setter
    def parallelism(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54db927910a2cdf0c6953d083656468555e9feabd6a1ea0a2aa405be9b896b97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parallelism", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26972c05a93992b6107a08003a35c7510a1241f17751ebd6cacd312d9267f133)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKeyId")
    def private_key_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyId"))

    @private_key_id.setter
    def private_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac7742fe0b9942a7b6d92ec0d42c02cb5f8c281496ffedcfe875e9c5e52da3e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestTimeout")
    def request_timeout(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "requestTimeout"))

    @request_timeout.setter
    def request_timeout(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94dc4d32d89c93ac388701c844d8ee074ab3b88b4ef1b84618a1f44bf76cac3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c5643fe7360f0dda91ee51f1ccc2c4bc7ec96656ced2c1f6661aff5a4e4f09d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.provider.OktaProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "access_token": "accessToken",
        "alias": "alias",
        "api_token": "apiToken",
        "backoff": "backoff",
        "base_url": "baseUrl",
        "client_id": "clientId",
        "http_proxy": "httpProxy",
        "log_level": "logLevel",
        "max_api_capacity": "maxApiCapacity",
        "max_retries": "maxRetries",
        "max_wait_seconds": "maxWaitSeconds",
        "min_wait_seconds": "minWaitSeconds",
        "org_name": "orgName",
        "parallelism": "parallelism",
        "private_key": "privateKey",
        "private_key_id": "privateKeyId",
        "request_timeout": "requestTimeout",
        "scopes": "scopes",
    },
)
class OktaProviderConfig:
    def __init__(
        self,
        *,
        access_token: typing.Optional[builtins.str] = None,
        alias: typing.Optional[builtins.str] = None,
        api_token: typing.Optional[builtins.str] = None,
        backoff: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        base_url: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        http_proxy: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[jsii.Number] = None,
        max_api_capacity: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        max_wait_seconds: typing.Optional[jsii.Number] = None,
        min_wait_seconds: typing.Optional[jsii.Number] = None,
        org_name: typing.Optional[builtins.str] = None,
        parallelism: typing.Optional[jsii.Number] = None,
        private_key: typing.Optional[builtins.str] = None,
        private_key_id: typing.Optional[builtins.str] = None,
        request_timeout: typing.Optional[jsii.Number] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param access_token: Bearer token granting privileges to Okta API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#access_token OktaProvider#access_token}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#alias OktaProvider#alias}
        :param api_token: API Token granting privileges to Okta API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#api_token OktaProvider#api_token}
        :param backoff: Use exponential back off strategy for rate limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#backoff OktaProvider#backoff}
        :param base_url: The Okta url. (Use 'oktapreview.com' for Okta testing). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#base_url OktaProvider#base_url}
        :param client_id: API Token granting privileges to Okta API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#client_id OktaProvider#client_id}
        :param http_proxy: Alternate HTTP proxy of scheme://hostname or scheme://hostname:port format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#http_proxy OktaProvider#http_proxy}
        :param log_level: providers log level. Minimum is 1 (TRACE), and maximum is 5 (ERROR). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#log_level OktaProvider#log_level}
        :param max_api_capacity: Sets what percentage of capacity the provider can use of the total rate limit capacity while making calls to the Okta management API endpoints. Okta API operates in one minute buckets. See Okta Management API Rate Limits: https://developer.okta.com/docs/reference/rl-global-mgmt/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#max_api_capacity OktaProvider#max_api_capacity}
        :param max_retries: maximum number of retries to attempt before erroring out. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#max_retries OktaProvider#max_retries}
        :param max_wait_seconds: maximum seconds to wait when rate limit is hit. We use exponential backoffs when backoff is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#max_wait_seconds OktaProvider#max_wait_seconds}
        :param min_wait_seconds: minimum seconds to wait when rate limit is hit. We use exponential backoffs when backoff is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#min_wait_seconds OktaProvider#min_wait_seconds}
        :param org_name: The organization to manage in Okta. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#org_name OktaProvider#org_name}
        :param parallelism: Number of concurrent requests to make within a resource where bulk operations are not possible. Take note of https://developer.okta.com/docs/api/getting_started/rate-limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#parallelism OktaProvider#parallelism}
        :param private_key: API Token granting privileges to Okta API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#private_key OktaProvider#private_key}
        :param private_key_id: API Token Id granting privileges to Okta API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#private_key_id OktaProvider#private_key_id}
        :param request_timeout: Timeout for single request (in seconds) which is made to Okta, the default is ``0`` (means no limit is set). The maximum value can be ``300``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#request_timeout OktaProvider#request_timeout}
        :param scopes: API Token granting privileges to Okta API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#scopes OktaProvider#scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db2af804ca7d98e9e315bd0ff05a8444e2d8730b17bb1e9dae47ec495742e825)
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument api_token", value=api_token, expected_type=type_hints["api_token"])
            check_type(argname="argument backoff", value=backoff, expected_type=type_hints["backoff"])
            check_type(argname="argument base_url", value=base_url, expected_type=type_hints["base_url"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument http_proxy", value=http_proxy, expected_type=type_hints["http_proxy"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            check_type(argname="argument max_api_capacity", value=max_api_capacity, expected_type=type_hints["max_api_capacity"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            check_type(argname="argument max_wait_seconds", value=max_wait_seconds, expected_type=type_hints["max_wait_seconds"])
            check_type(argname="argument min_wait_seconds", value=min_wait_seconds, expected_type=type_hints["min_wait_seconds"])
            check_type(argname="argument org_name", value=org_name, expected_type=type_hints["org_name"])
            check_type(argname="argument parallelism", value=parallelism, expected_type=type_hints["parallelism"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument private_key_id", value=private_key_id, expected_type=type_hints["private_key_id"])
            check_type(argname="argument request_timeout", value=request_timeout, expected_type=type_hints["request_timeout"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_token is not None:
            self._values["access_token"] = access_token
        if alias is not None:
            self._values["alias"] = alias
        if api_token is not None:
            self._values["api_token"] = api_token
        if backoff is not None:
            self._values["backoff"] = backoff
        if base_url is not None:
            self._values["base_url"] = base_url
        if client_id is not None:
            self._values["client_id"] = client_id
        if http_proxy is not None:
            self._values["http_proxy"] = http_proxy
        if log_level is not None:
            self._values["log_level"] = log_level
        if max_api_capacity is not None:
            self._values["max_api_capacity"] = max_api_capacity
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if max_wait_seconds is not None:
            self._values["max_wait_seconds"] = max_wait_seconds
        if min_wait_seconds is not None:
            self._values["min_wait_seconds"] = min_wait_seconds
        if org_name is not None:
            self._values["org_name"] = org_name
        if parallelism is not None:
            self._values["parallelism"] = parallelism
        if private_key is not None:
            self._values["private_key"] = private_key
        if private_key_id is not None:
            self._values["private_key_id"] = private_key_id
        if request_timeout is not None:
            self._values["request_timeout"] = request_timeout
        if scopes is not None:
            self._values["scopes"] = scopes

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''Bearer token granting privileges to Okta API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#access_token OktaProvider#access_token}
        '''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#alias OktaProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_token(self) -> typing.Optional[builtins.str]:
        '''API Token granting privileges to Okta API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#api_token OktaProvider#api_token}
        '''
        result = self._values.get("api_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backoff(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use exponential back off strategy for rate limits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#backoff OktaProvider#backoff}
        '''
        result = self._values.get("backoff")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def base_url(self) -> typing.Optional[builtins.str]:
        '''The Okta url. (Use 'oktapreview.com' for Okta testing).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#base_url OktaProvider#base_url}
        '''
        result = self._values.get("base_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''API Token granting privileges to Okta API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#client_id OktaProvider#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_proxy(self) -> typing.Optional[builtins.str]:
        '''Alternate HTTP proxy of scheme://hostname or scheme://hostname:port format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#http_proxy OktaProvider#http_proxy}
        '''
        result = self._values.get("http_proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_level(self) -> typing.Optional[jsii.Number]:
        '''providers log level. Minimum is 1 (TRACE), and maximum is 5 (ERROR).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#log_level OktaProvider#log_level}
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_api_capacity(self) -> typing.Optional[jsii.Number]:
        '''Sets what percentage of capacity the provider can use of the total rate limit capacity while making calls to the Okta management API endpoints.

        Okta API operates in one minute buckets. See Okta Management API Rate Limits: https://developer.okta.com/docs/reference/rl-global-mgmt/

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#max_api_capacity OktaProvider#max_api_capacity}
        '''
        result = self._values.get("max_api_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''maximum number of retries to attempt before erroring out.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#max_retries OktaProvider#max_retries}
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_wait_seconds(self) -> typing.Optional[jsii.Number]:
        '''maximum seconds to wait when rate limit is hit. We use exponential backoffs when backoff is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#max_wait_seconds OktaProvider#max_wait_seconds}
        '''
        result = self._values.get("max_wait_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_wait_seconds(self) -> typing.Optional[jsii.Number]:
        '''minimum seconds to wait when rate limit is hit. We use exponential backoffs when backoff is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#min_wait_seconds OktaProvider#min_wait_seconds}
        '''
        result = self._values.get("min_wait_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def org_name(self) -> typing.Optional[builtins.str]:
        '''The organization to manage in Okta.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#org_name OktaProvider#org_name}
        '''
        result = self._values.get("org_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parallelism(self) -> typing.Optional[jsii.Number]:
        '''Number of concurrent requests to make within a resource where bulk operations are not possible. Take note of https://developer.okta.com/docs/api/getting_started/rate-limits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#parallelism OktaProvider#parallelism}
        '''
        result = self._values.get("parallelism")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''API Token granting privileges to Okta API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#private_key OktaProvider#private_key}
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key_id(self) -> typing.Optional[builtins.str]:
        '''API Token Id granting privileges to Okta API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#private_key_id OktaProvider#private_key_id}
        '''
        result = self._values.get("private_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_timeout(self) -> typing.Optional[jsii.Number]:
        '''Timeout for single request (in seconds) which is made to Okta, the default is ``0`` (means no limit is set).

        The maximum value can be ``300``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#request_timeout OktaProvider#request_timeout}
        '''
        result = self._values.get("request_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''API Token granting privileges to Okta API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs#scopes OktaProvider#scopes}
        '''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OktaProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "OktaProvider",
    "OktaProviderConfig",
]

publication.publish()

def _typecheckingstub__0808da6b083e2f9f99a310ae982044c5cce9f930ec458184ed0d591ca91e8007(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    access_token: typing.Optional[builtins.str] = None,
    alias: typing.Optional[builtins.str] = None,
    api_token: typing.Optional[builtins.str] = None,
    backoff: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    base_url: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    http_proxy: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[jsii.Number] = None,
    max_api_capacity: typing.Optional[jsii.Number] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    max_wait_seconds: typing.Optional[jsii.Number] = None,
    min_wait_seconds: typing.Optional[jsii.Number] = None,
    org_name: typing.Optional[builtins.str] = None,
    parallelism: typing.Optional[jsii.Number] = None,
    private_key: typing.Optional[builtins.str] = None,
    private_key_id: typing.Optional[builtins.str] = None,
    request_timeout: typing.Optional[jsii.Number] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51abd6d60d616dbc97a7bb26aafa91aa4440531aaca2984f18dd46c2b1e89c38(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e6d4b67aedcc0e8bae05fa446f17b047c0b5cba4e11b6b7a31e076ac950c31(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97384be160dc39111d7579ed322eb92fd9e30057a81b7131b547d255276e0d7b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07fa7e60a80c2e5ee86d15a5bb1eec773afd17b818dbe22339e6a397ab81222a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a2efb511f2eea65a6443a2843f2849f375c10359aae511a4bcefbb8c06b51df(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c3fe221116fa818079480b193405db75a8cb36d5937b182be5f9f6fddf87a4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3852e89eb40ce1fd097eb1e37fdf1af3fa0b2e672666efe612f5f386e5e71e9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16f485d30996cfe76676661fd4b4f89666efd7467358770eeac526d9fe14f348(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__824238a8dc65639d3c07c656d9007ddcc1a51ad127ffec02ed20bd46348827d0(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f58b0fa38112bac5f723b72a8886918611ec6f47c64d41ec017cc93c751db1e5(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e87d41a2a7d444fe492057606056e9c8a7a673e0c4643e0e46877a0285fb20b1(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ddd950d51d4d3722c5af1222f8d20d5208be7f36a3010b0f6d2bd9d4e06162(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b98daea3afef8d037c098df73aaacdb3165055e283fa79b946d4acbf1946f085(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bc910d954f91ee43c7de4fdd0ea5a119adb81df8a3200fafaf52968a0e5281e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54db927910a2cdf0c6953d083656468555e9feabd6a1ea0a2aa405be9b896b97(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26972c05a93992b6107a08003a35c7510a1241f17751ebd6cacd312d9267f133(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac7742fe0b9942a7b6d92ec0d42c02cb5f8c281496ffedcfe875e9c5e52da3e9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94dc4d32d89c93ac388701c844d8ee074ab3b88b4ef1b84618a1f44bf76cac3e(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c5643fe7360f0dda91ee51f1ccc2c4bc7ec96656ced2c1f6661aff5a4e4f09d(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db2af804ca7d98e9e315bd0ff05a8444e2d8730b17bb1e9dae47ec495742e825(
    *,
    access_token: typing.Optional[builtins.str] = None,
    alias: typing.Optional[builtins.str] = None,
    api_token: typing.Optional[builtins.str] = None,
    backoff: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    base_url: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    http_proxy: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[jsii.Number] = None,
    max_api_capacity: typing.Optional[jsii.Number] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    max_wait_seconds: typing.Optional[jsii.Number] = None,
    min_wait_seconds: typing.Optional[jsii.Number] = None,
    org_name: typing.Optional[builtins.str] = None,
    parallelism: typing.Optional[jsii.Number] = None,
    private_key: typing.Optional[builtins.str] = None,
    private_key_id: typing.Optional[builtins.str] = None,
    request_timeout: typing.Optional[jsii.Number] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
