r'''
# `okta_brand`

Refer to the Terraform Registry for docs: [`okta_brand`](https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand).
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


class Brand(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.brand.Brand",
):
    '''Represents a {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand okta_brand}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        agree_to_custom_privacy_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        brand_id: typing.Optional[builtins.str] = None,
        custom_privacy_policy_url: typing.Optional[builtins.str] = None,
        default_app_app_instance_id: typing.Optional[builtins.str] = None,
        default_app_app_link_name: typing.Optional[builtins.str] = None,
        default_app_classic_application_uri: typing.Optional[builtins.str] = None,
        locale: typing.Optional[builtins.str] = None,
        remove_powered_by_okta: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand okta_brand} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the brand. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#name Brand#name}
        :param agree_to_custom_privacy_policy: Is a required input flag with when changing custom_privacy_url, shouldn't be considered as a readable property. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#agree_to_custom_privacy_policy Brand#agree_to_custom_privacy_policy}
        :param brand_id: Brand ID - Note: Okta API for brands only reads and updates therefore the okta_brand resource needs to act as a quasi data source. Do this by setting brand_id. ``DEPRECATED``: Okta has fully support brand creation, this attribute is a no op and will be removed Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#brand_id Brand#brand_id}
        :param custom_privacy_policy_url: Custom privacy policy URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#custom_privacy_policy_url Brand#custom_privacy_policy_url}
        :param default_app_app_instance_id: Default app app instance id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#default_app_app_instance_id Brand#default_app_app_instance_id}
        :param default_app_app_link_name: Default app app link name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#default_app_app_link_name Brand#default_app_app_link_name}
        :param default_app_classic_application_uri: Default app classic application uri. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#default_app_classic_application_uri Brand#default_app_classic_application_uri}
        :param locale: The language specified as an IETF BCP 47 language tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#locale Brand#locale}
        :param remove_powered_by_okta: Removes "Powered by Okta" from the Okta-hosted sign-in page and "© 2021 Okta, Inc." from the Okta End-User Dashboard. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#remove_powered_by_okta Brand#remove_powered_by_okta}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d7e18230a9679bcb2d8a4bbb20ecd6c5e549abeb5b80dc2a6b55e3908bbda9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = BrandConfig(
            name=name,
            agree_to_custom_privacy_policy=agree_to_custom_privacy_policy,
            brand_id=brand_id,
            custom_privacy_policy_url=custom_privacy_policy_url,
            default_app_app_instance_id=default_app_app_instance_id,
            default_app_app_link_name=default_app_app_link_name,
            default_app_classic_application_uri=default_app_classic_application_uri,
            locale=locale,
            remove_powered_by_okta=remove_powered_by_okta,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
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
        '''Generates CDKTF code for importing a Brand resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Brand to import.
        :param import_from_id: The id of the existing Brand that should be imported. Refer to the {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Brand to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cb9e70d5e73139b39575bc1a1095b613fd003a1ed67bd5863e88ae7e6b681e0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAgreeToCustomPrivacyPolicy")
    def reset_agree_to_custom_privacy_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgreeToCustomPrivacyPolicy", []))

    @jsii.member(jsii_name="resetBrandId")
    def reset_brand_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBrandId", []))

    @jsii.member(jsii_name="resetCustomPrivacyPolicyUrl")
    def reset_custom_privacy_policy_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomPrivacyPolicyUrl", []))

    @jsii.member(jsii_name="resetDefaultAppAppInstanceId")
    def reset_default_app_app_instance_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultAppAppInstanceId", []))

    @jsii.member(jsii_name="resetDefaultAppAppLinkName")
    def reset_default_app_app_link_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultAppAppLinkName", []))

    @jsii.member(jsii_name="resetDefaultAppClassicApplicationUri")
    def reset_default_app_classic_application_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultAppClassicApplicationUri", []))

    @jsii.member(jsii_name="resetLocale")
    def reset_locale(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocale", []))

    @jsii.member(jsii_name="resetRemovePoweredByOkta")
    def reset_remove_powered_by_okta(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemovePoweredByOkta", []))

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
    @jsii.member(jsii_name="emailDomainId")
    def email_domain_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailDomainId"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="isDefault")
    def is_default(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isDefault"))

    @builtins.property
    @jsii.member(jsii_name="links")
    def links(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "links"))

    @builtins.property
    @jsii.member(jsii_name="agreeToCustomPrivacyPolicyInput")
    def agree_to_custom_privacy_policy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "agreeToCustomPrivacyPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="brandIdInput")
    def brand_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "brandIdInput"))

    @builtins.property
    @jsii.member(jsii_name="customPrivacyPolicyUrlInput")
    def custom_privacy_policy_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customPrivacyPolicyUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultAppAppInstanceIdInput")
    def default_app_app_instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultAppAppInstanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultAppAppLinkNameInput")
    def default_app_app_link_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultAppAppLinkNameInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultAppClassicApplicationUriInput")
    def default_app_classic_application_uri_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultAppClassicApplicationUriInput"))

    @builtins.property
    @jsii.member(jsii_name="localeInput")
    def locale_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="removePoweredByOktaInput")
    def remove_powered_by_okta_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "removePoweredByOktaInput"))

    @builtins.property
    @jsii.member(jsii_name="agreeToCustomPrivacyPolicy")
    def agree_to_custom_privacy_policy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "agreeToCustomPrivacyPolicy"))

    @agree_to_custom_privacy_policy.setter
    def agree_to_custom_privacy_policy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a188989f1e2e1a421b119f34b3755fa4cbbdf28ee4bdbf022bf334dbfab994)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agreeToCustomPrivacyPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="brandId")
    def brand_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "brandId"))

    @brand_id.setter
    def brand_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a01a0159a0126332e6826636dd10ceb76194ff7b2f42e67f6090e3ef270efc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "brandId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customPrivacyPolicyUrl")
    def custom_privacy_policy_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customPrivacyPolicyUrl"))

    @custom_privacy_policy_url.setter
    def custom_privacy_policy_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d340b3c630f3f9dcc058631e47292e4b46f1fade342f4eab5001597e0dbe5df3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customPrivacyPolicyUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultAppAppInstanceId")
    def default_app_app_instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultAppAppInstanceId"))

    @default_app_app_instance_id.setter
    def default_app_app_instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30020ee5e4d402c4417611354ba5208492110d4d3e46ade78f2579694d7083ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultAppAppInstanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultAppAppLinkName")
    def default_app_app_link_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultAppAppLinkName"))

    @default_app_app_link_name.setter
    def default_app_app_link_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1113da733a42c93485016bd948d778954b112e6742ccd054e170eb02556b484f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultAppAppLinkName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultAppClassicApplicationUri")
    def default_app_classic_application_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultAppClassicApplicationUri"))

    @default_app_classic_application_uri.setter
    def default_app_classic_application_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02062a3e1322906d8765eb0faaa05916dda8498f1c74295c4a3d555fa8bb09d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultAppClassicApplicationUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="locale")
    def locale(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "locale"))

    @locale.setter
    def locale(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b89603539dc45a70c40a18bfd565d028d02484a99ea0c777018ad5950af1d7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locale", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0622446aa3dd15cc5daf64316edcbae22574259f68791efd485d00beedd519db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="removePoweredByOkta")
    def remove_powered_by_okta(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "removePoweredByOkta"))

    @remove_powered_by_okta.setter
    def remove_powered_by_okta(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42f9c7af21a10a5e0e69b1de043527cde1622f8eadcf459f5f6d0f1e60ca1b8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "removePoweredByOkta", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.brand.BrandConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "agree_to_custom_privacy_policy": "agreeToCustomPrivacyPolicy",
        "brand_id": "brandId",
        "custom_privacy_policy_url": "customPrivacyPolicyUrl",
        "default_app_app_instance_id": "defaultAppAppInstanceId",
        "default_app_app_link_name": "defaultAppAppLinkName",
        "default_app_classic_application_uri": "defaultAppClassicApplicationUri",
        "locale": "locale",
        "remove_powered_by_okta": "removePoweredByOkta",
    },
)
class BrandConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        name: builtins.str,
        agree_to_custom_privacy_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        brand_id: typing.Optional[builtins.str] = None,
        custom_privacy_policy_url: typing.Optional[builtins.str] = None,
        default_app_app_instance_id: typing.Optional[builtins.str] = None,
        default_app_app_link_name: typing.Optional[builtins.str] = None,
        default_app_classic_application_uri: typing.Optional[builtins.str] = None,
        locale: typing.Optional[builtins.str] = None,
        remove_powered_by_okta: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the brand. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#name Brand#name}
        :param agree_to_custom_privacy_policy: Is a required input flag with when changing custom_privacy_url, shouldn't be considered as a readable property. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#agree_to_custom_privacy_policy Brand#agree_to_custom_privacy_policy}
        :param brand_id: Brand ID - Note: Okta API for brands only reads and updates therefore the okta_brand resource needs to act as a quasi data source. Do this by setting brand_id. ``DEPRECATED``: Okta has fully support brand creation, this attribute is a no op and will be removed Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#brand_id Brand#brand_id}
        :param custom_privacy_policy_url: Custom privacy policy URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#custom_privacy_policy_url Brand#custom_privacy_policy_url}
        :param default_app_app_instance_id: Default app app instance id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#default_app_app_instance_id Brand#default_app_app_instance_id}
        :param default_app_app_link_name: Default app app link name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#default_app_app_link_name Brand#default_app_app_link_name}
        :param default_app_classic_application_uri: Default app classic application uri. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#default_app_classic_application_uri Brand#default_app_classic_application_uri}
        :param locale: The language specified as an IETF BCP 47 language tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#locale Brand#locale}
        :param remove_powered_by_okta: Removes "Powered by Okta" from the Okta-hosted sign-in page and "© 2021 Okta, Inc." from the Okta End-User Dashboard. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#remove_powered_by_okta Brand#remove_powered_by_okta}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdaa068f352d0f9814bd9f7105de41a5097c77622ef2727ebe72bb393e61d86d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument agree_to_custom_privacy_policy", value=agree_to_custom_privacy_policy, expected_type=type_hints["agree_to_custom_privacy_policy"])
            check_type(argname="argument brand_id", value=brand_id, expected_type=type_hints["brand_id"])
            check_type(argname="argument custom_privacy_policy_url", value=custom_privacy_policy_url, expected_type=type_hints["custom_privacy_policy_url"])
            check_type(argname="argument default_app_app_instance_id", value=default_app_app_instance_id, expected_type=type_hints["default_app_app_instance_id"])
            check_type(argname="argument default_app_app_link_name", value=default_app_app_link_name, expected_type=type_hints["default_app_app_link_name"])
            check_type(argname="argument default_app_classic_application_uri", value=default_app_classic_application_uri, expected_type=type_hints["default_app_classic_application_uri"])
            check_type(argname="argument locale", value=locale, expected_type=type_hints["locale"])
            check_type(argname="argument remove_powered_by_okta", value=remove_powered_by_okta, expected_type=type_hints["remove_powered_by_okta"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if agree_to_custom_privacy_policy is not None:
            self._values["agree_to_custom_privacy_policy"] = agree_to_custom_privacy_policy
        if brand_id is not None:
            self._values["brand_id"] = brand_id
        if custom_privacy_policy_url is not None:
            self._values["custom_privacy_policy_url"] = custom_privacy_policy_url
        if default_app_app_instance_id is not None:
            self._values["default_app_app_instance_id"] = default_app_app_instance_id
        if default_app_app_link_name is not None:
            self._values["default_app_app_link_name"] = default_app_app_link_name
        if default_app_classic_application_uri is not None:
            self._values["default_app_classic_application_uri"] = default_app_classic_application_uri
        if locale is not None:
            self._values["locale"] = locale
        if remove_powered_by_okta is not None:
            self._values["remove_powered_by_okta"] = remove_powered_by_okta

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the brand.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#name Brand#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agree_to_custom_privacy_policy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Is a required input flag with when changing custom_privacy_url, shouldn't be considered as a readable property.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#agree_to_custom_privacy_policy Brand#agree_to_custom_privacy_policy}
        '''
        result = self._values.get("agree_to_custom_privacy_policy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def brand_id(self) -> typing.Optional[builtins.str]:
        '''Brand ID - Note: Okta API for brands only reads and updates therefore the okta_brand resource needs to act as a quasi data source.

        Do this by setting brand_id. ``DEPRECATED``: Okta has fully support brand creation, this attribute is a no op and will be removed

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#brand_id Brand#brand_id}
        '''
        result = self._values.get("brand_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_privacy_policy_url(self) -> typing.Optional[builtins.str]:
        '''Custom privacy policy URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#custom_privacy_policy_url Brand#custom_privacy_policy_url}
        '''
        result = self._values.get("custom_privacy_policy_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_app_app_instance_id(self) -> typing.Optional[builtins.str]:
        '''Default app app instance id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#default_app_app_instance_id Brand#default_app_app_instance_id}
        '''
        result = self._values.get("default_app_app_instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_app_app_link_name(self) -> typing.Optional[builtins.str]:
        '''Default app app link name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#default_app_app_link_name Brand#default_app_app_link_name}
        '''
        result = self._values.get("default_app_app_link_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_app_classic_application_uri(self) -> typing.Optional[builtins.str]:
        '''Default app classic application uri.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#default_app_classic_application_uri Brand#default_app_classic_application_uri}
        '''
        result = self._values.get("default_app_classic_application_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def locale(self) -> typing.Optional[builtins.str]:
        '''The language specified as an IETF BCP 47 language tag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#locale Brand#locale}
        '''
        result = self._values.get("locale")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remove_powered_by_okta(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Removes "Powered by Okta" from the Okta-hosted sign-in page and "© 2021 Okta, Inc." from the Okta End-User Dashboard.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/brand#remove_powered_by_okta Brand#remove_powered_by_okta}
        '''
        result = self._values.get("remove_powered_by_okta")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BrandConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Brand",
    "BrandConfig",
]

publication.publish()

def _typecheckingstub__f2d7e18230a9679bcb2d8a4bbb20ecd6c5e549abeb5b80dc2a6b55e3908bbda9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    agree_to_custom_privacy_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    brand_id: typing.Optional[builtins.str] = None,
    custom_privacy_policy_url: typing.Optional[builtins.str] = None,
    default_app_app_instance_id: typing.Optional[builtins.str] = None,
    default_app_app_link_name: typing.Optional[builtins.str] = None,
    default_app_classic_application_uri: typing.Optional[builtins.str] = None,
    locale: typing.Optional[builtins.str] = None,
    remove_powered_by_okta: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb9e70d5e73139b39575bc1a1095b613fd003a1ed67bd5863e88ae7e6b681e0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a188989f1e2e1a421b119f34b3755fa4cbbdf28ee4bdbf022bf334dbfab994(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a01a0159a0126332e6826636dd10ceb76194ff7b2f42e67f6090e3ef270efc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d340b3c630f3f9dcc058631e47292e4b46f1fade342f4eab5001597e0dbe5df3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30020ee5e4d402c4417611354ba5208492110d4d3e46ade78f2579694d7083ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1113da733a42c93485016bd948d778954b112e6742ccd054e170eb02556b484f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02062a3e1322906d8765eb0faaa05916dda8498f1c74295c4a3d555fa8bb09d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b89603539dc45a70c40a18bfd565d028d02484a99ea0c777018ad5950af1d7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0622446aa3dd15cc5daf64316edcbae22574259f68791efd485d00beedd519db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42f9c7af21a10a5e0e69b1de043527cde1622f8eadcf459f5f6d0f1e60ca1b8b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdaa068f352d0f9814bd9f7105de41a5097c77622ef2727ebe72bb393e61d86d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    agree_to_custom_privacy_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    brand_id: typing.Optional[builtins.str] = None,
    custom_privacy_policy_url: typing.Optional[builtins.str] = None,
    default_app_app_instance_id: typing.Optional[builtins.str] = None,
    default_app_app_link_name: typing.Optional[builtins.str] = None,
    default_app_classic_application_uri: typing.Optional[builtins.str] = None,
    locale: typing.Optional[builtins.str] = None,
    remove_powered_by_okta: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
