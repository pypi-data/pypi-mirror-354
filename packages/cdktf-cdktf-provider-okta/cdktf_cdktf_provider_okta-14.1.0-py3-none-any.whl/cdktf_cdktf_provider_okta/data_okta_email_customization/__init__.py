r'''
# `data_okta_email_customization`

Refer to the Terraform Registry for docs: [`data_okta_email_customization`](https://registry.terraform.io/providers/okta/okta/4.20.0/docs/data-sources/email_customization).
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


class DataOktaEmailCustomization(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.dataOktaEmailCustomization.DataOktaEmailCustomization",
):
    '''Represents a {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/data-sources/email_customization okta_email_customization}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        brand_id: builtins.str,
        customization_id: builtins.str,
        template_name: builtins.str,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/data-sources/email_customization okta_email_customization} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param brand_id: Brand ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/data-sources/email_customization#brand_id DataOktaEmailCustomization#brand_id}
        :param customization_id: The ID of the customization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/data-sources/email_customization#customization_id DataOktaEmailCustomization#customization_id}
        :param template_name: Template Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/data-sources/email_customization#template_name DataOktaEmailCustomization#template_name}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c984122af0d54771fdbf28fbbf7ce2af1e14b3e0a1b554a429412a459cae1c06)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataOktaEmailCustomizationConfig(
            brand_id=brand_id,
            customization_id=customization_id,
            template_name=template_name,
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
        '''Generates CDKTF code for importing a DataOktaEmailCustomization resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataOktaEmailCustomization to import.
        :param import_from_id: The id of the existing DataOktaEmailCustomization that should be imported. Refer to the {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/data-sources/email_customization#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataOktaEmailCustomization to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b33d85b9a6f1f3d72426881819cc50773ff11abffa55e126420e8cf1bf8d547)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

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
    @jsii.member(jsii_name="body")
    def body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "body"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="isDefault")
    def is_default(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isDefault"))

    @builtins.property
    @jsii.member(jsii_name="language")
    def language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "language"))

    @builtins.property
    @jsii.member(jsii_name="links")
    def links(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "links"))

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @builtins.property
    @jsii.member(jsii_name="brandIdInput")
    def brand_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "brandIdInput"))

    @builtins.property
    @jsii.member(jsii_name="customizationIdInput")
    def customization_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customizationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="templateNameInput")
    def template_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateNameInput"))

    @builtins.property
    @jsii.member(jsii_name="brandId")
    def brand_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "brandId"))

    @brand_id.setter
    def brand_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea3764e398e3ea33d30c75437a1eeee8ee56cb5585f663ed4a4ebbdc4ca43398)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "brandId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customizationId")
    def customization_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customizationId"))

    @customization_id.setter
    def customization_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fd429a32cf059e4eb560198d95926c2f98daacc033e8e75a1ac04fc986d9785)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customizationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="templateName")
    def template_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "templateName"))

    @template_name.setter
    def template_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b07f78cf6b59262e4cda3ef20e12f50da9d38f245d8cf4a2b9f1d6cc8ef9c2ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.dataOktaEmailCustomization.DataOktaEmailCustomizationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "brand_id": "brandId",
        "customization_id": "customizationId",
        "template_name": "templateName",
    },
)
class DataOktaEmailCustomizationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        brand_id: builtins.str,
        customization_id: builtins.str,
        template_name: builtins.str,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param brand_id: Brand ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/data-sources/email_customization#brand_id DataOktaEmailCustomization#brand_id}
        :param customization_id: The ID of the customization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/data-sources/email_customization#customization_id DataOktaEmailCustomization#customization_id}
        :param template_name: Template Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/data-sources/email_customization#template_name DataOktaEmailCustomization#template_name}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51196d15783823b1176d21517d6c785ce5683187bffde43a4516ce4771384d46)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument brand_id", value=brand_id, expected_type=type_hints["brand_id"])
            check_type(argname="argument customization_id", value=customization_id, expected_type=type_hints["customization_id"])
            check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "brand_id": brand_id,
            "customization_id": customization_id,
            "template_name": template_name,
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
    def brand_id(self) -> builtins.str:
        '''Brand ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/data-sources/email_customization#brand_id DataOktaEmailCustomization#brand_id}
        '''
        result = self._values.get("brand_id")
        assert result is not None, "Required property 'brand_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def customization_id(self) -> builtins.str:
        '''The ID of the customization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/data-sources/email_customization#customization_id DataOktaEmailCustomization#customization_id}
        '''
        result = self._values.get("customization_id")
        assert result is not None, "Required property 'customization_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template_name(self) -> builtins.str:
        '''Template Name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/data-sources/email_customization#template_name DataOktaEmailCustomization#template_name}
        '''
        result = self._values.get("template_name")
        assert result is not None, "Required property 'template_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOktaEmailCustomizationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataOktaEmailCustomization",
    "DataOktaEmailCustomizationConfig",
]

publication.publish()

def _typecheckingstub__c984122af0d54771fdbf28fbbf7ce2af1e14b3e0a1b554a429412a459cae1c06(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    brand_id: builtins.str,
    customization_id: builtins.str,
    template_name: builtins.str,
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

def _typecheckingstub__2b33d85b9a6f1f3d72426881819cc50773ff11abffa55e126420e8cf1bf8d547(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea3764e398e3ea33d30c75437a1eeee8ee56cb5585f663ed4a4ebbdc4ca43398(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fd429a32cf059e4eb560198d95926c2f98daacc033e8e75a1ac04fc986d9785(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b07f78cf6b59262e4cda3ef20e12f50da9d38f245d8cf4a2b9f1d6cc8ef9c2ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51196d15783823b1176d21517d6c785ce5683187bffde43a4516ce4771384d46(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    brand_id: builtins.str,
    customization_id: builtins.str,
    template_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
