r'''
# `okta_idp_social`

Refer to the Terraform Registry for docs: [`okta_idp_social`](https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social).
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


class IdpSocial(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.idpSocial.IdpSocial",
):
    '''Represents a {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social okta_idp_social}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        scopes: typing.Sequence[builtins.str],
        type: builtins.str,
        account_link_action: typing.Optional[builtins.str] = None,
        account_link_group_include: typing.Optional[typing.Sequence[builtins.str]] = None,
        apple_kid: typing.Optional[builtins.str] = None,
        apple_private_key: typing.Optional[builtins.str] = None,
        apple_team_id: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        deprovisioned_action: typing.Optional[builtins.str] = None,
        groups_action: typing.Optional[builtins.str] = None,
        groups_assignment: typing.Optional[typing.Sequence[builtins.str]] = None,
        groups_attribute: typing.Optional[builtins.str] = None,
        groups_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        issuer_mode: typing.Optional[builtins.str] = None,
        max_clock_skew: typing.Optional[jsii.Number] = None,
        profile_master: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        protocol_type: typing.Optional[builtins.str] = None,
        provisioning_action: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        subject_match_attribute: typing.Optional[builtins.str] = None,
        subject_match_type: typing.Optional[builtins.str] = None,
        suspended_action: typing.Optional[builtins.str] = None,
        username_template: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social okta_idp_social} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the IdP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#name IdpSocial#name}
        :param scopes: The scopes of the IdP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#scopes IdpSocial#scopes}
        :param type: Identity Provider Types: https://developer.okta.com/docs/reference/api/idps/#identity-provider-type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#type IdpSocial#type}
        :param account_link_action: Specifies the account linking action for an IdP user. Default: ``AUTO``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#account_link_action IdpSocial#account_link_action}
        :param account_link_group_include: Group memberships to determine link candidates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#account_link_group_include IdpSocial#account_link_group_include}
        :param apple_kid: The Key ID that you obtained from Apple when you created the private key for the client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#apple_kid IdpSocial#apple_kid}
        :param apple_private_key: The Key ID that you obtained from Apple when you created the private key for the client. PrivateKey is required when resource is first created. For all consecutive updates, it can be empty/omitted and keeps the existing value if it is empty/omitted. PrivateKey isn't returned when importing this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#apple_private_key IdpSocial#apple_private_key}
        :param apple_team_id: The Team ID associated with your Apple developer account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#apple_team_id IdpSocial#apple_team_id}
        :param client_id: Unique identifier issued by AS for the Okta IdP instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#client_id IdpSocial#client_id}
        :param client_secret: Client secret issued by AS for the Okta IdP instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#client_secret IdpSocial#client_secret}
        :param deprovisioned_action: Action for a previously deprovisioned IdP user during authentication. Can be ``NONE`` or ``REACTIVATE``. Default: ``NONE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#deprovisioned_action IdpSocial#deprovisioned_action}
        :param groups_action: Provisioning action for IdP user's group memberships. It can be ``NONE``, ``SYNC``, ``APPEND``, or ``ASSIGN``. Default: ``NONE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#groups_action IdpSocial#groups_action}
        :param groups_assignment: List of Okta Group IDs to add an IdP user as a member with the ``ASSIGN`` ``groups_action``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#groups_assignment IdpSocial#groups_assignment}
        :param groups_attribute: IdP user profile attribute name (case-insensitive) for an array value that contains group memberships. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#groups_attribute IdpSocial#groups_attribute}
        :param groups_filter: Whitelist of Okta Group identifiers that are allowed for the ``APPEND`` or ``SYNC`` ``groups_action``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#groups_filter IdpSocial#groups_filter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#id IdpSocial#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param issuer_mode: Indicates whether Okta uses the original Okta org domain URL, or a custom domain URL. It can be ``ORG_URL`` or ``CUSTOM_URL``. Default: ``ORG_URL`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#issuer_mode IdpSocial#issuer_mode}
        :param max_clock_skew: Maximum allowable clock-skew when processing messages from the IdP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#max_clock_skew IdpSocial#max_clock_skew}
        :param profile_master: Determines if the IdP should act as a source of truth for user profile attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#profile_master IdpSocial#profile_master}
        :param protocol_type: The type of protocol to use. It can be ``OIDC`` or ``OAUTH2``. Default: ``OAUTH2``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#protocol_type IdpSocial#protocol_type}
        :param provisioning_action: Provisioning action for an IdP user during authentication. Default: ``AUTO``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#provisioning_action IdpSocial#provisioning_action}
        :param status: Default to ``ACTIVE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#status IdpSocial#status}
        :param subject_match_attribute: Okta user profile attribute for matching transformed IdP username. Only for matchType ``CUSTOM_ATTRIBUTE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#subject_match_attribute IdpSocial#subject_match_attribute}
        :param subject_match_type: Determines the Okta user profile attribute match conditions for account linking and authentication of the transformed IdP username. By default, it is set to ``USERNAME``. It can be set to ``USERNAME``, ``EMAIL``, ``USERNAME_OR_EMAIL`` or ``CUSTOM_ATTRIBUTE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#subject_match_type IdpSocial#subject_match_type}
        :param suspended_action: Action for a previously suspended IdP user during authentication. Can be ``NONE`` or ``REACTIVATE``. Default: ``NONE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#suspended_action IdpSocial#suspended_action}
        :param username_template: Okta EL Expression to generate or transform a unique username for the IdP user. Default: ``idpuser.email``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#username_template IdpSocial#username_template}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__281f61eb0a6909884735ce5eb8686bf9b41bd2dc13ca18c3263015cab4ca377b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IdpSocialConfig(
            name=name,
            scopes=scopes,
            type=type,
            account_link_action=account_link_action,
            account_link_group_include=account_link_group_include,
            apple_kid=apple_kid,
            apple_private_key=apple_private_key,
            apple_team_id=apple_team_id,
            client_id=client_id,
            client_secret=client_secret,
            deprovisioned_action=deprovisioned_action,
            groups_action=groups_action,
            groups_assignment=groups_assignment,
            groups_attribute=groups_attribute,
            groups_filter=groups_filter,
            id=id,
            issuer_mode=issuer_mode,
            max_clock_skew=max_clock_skew,
            profile_master=profile_master,
            protocol_type=protocol_type,
            provisioning_action=provisioning_action,
            status=status,
            subject_match_attribute=subject_match_attribute,
            subject_match_type=subject_match_type,
            suspended_action=suspended_action,
            username_template=username_template,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a IdpSocial resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IdpSocial to import.
        :param import_from_id: The id of the existing IdpSocial that should be imported. Refer to the {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IdpSocial to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e085f698a4a605e56b549b0a249750c229041d12eaa68d5d1924452ddf87671)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAccountLinkAction")
    def reset_account_link_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountLinkAction", []))

    @jsii.member(jsii_name="resetAccountLinkGroupInclude")
    def reset_account_link_group_include(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountLinkGroupInclude", []))

    @jsii.member(jsii_name="resetAppleKid")
    def reset_apple_kid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppleKid", []))

    @jsii.member(jsii_name="resetApplePrivateKey")
    def reset_apple_private_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplePrivateKey", []))

    @jsii.member(jsii_name="resetAppleTeamId")
    def reset_apple_team_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppleTeamId", []))

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetDeprovisionedAction")
    def reset_deprovisioned_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeprovisionedAction", []))

    @jsii.member(jsii_name="resetGroupsAction")
    def reset_groups_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupsAction", []))

    @jsii.member(jsii_name="resetGroupsAssignment")
    def reset_groups_assignment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupsAssignment", []))

    @jsii.member(jsii_name="resetGroupsAttribute")
    def reset_groups_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupsAttribute", []))

    @jsii.member(jsii_name="resetGroupsFilter")
    def reset_groups_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupsFilter", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIssuerMode")
    def reset_issuer_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuerMode", []))

    @jsii.member(jsii_name="resetMaxClockSkew")
    def reset_max_clock_skew(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxClockSkew", []))

    @jsii.member(jsii_name="resetProfileMaster")
    def reset_profile_master(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProfileMaster", []))

    @jsii.member(jsii_name="resetProtocolType")
    def reset_protocol_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocolType", []))

    @jsii.member(jsii_name="resetProvisioningAction")
    def reset_provisioning_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisioningAction", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetSubjectMatchAttribute")
    def reset_subject_match_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectMatchAttribute", []))

    @jsii.member(jsii_name="resetSubjectMatchType")
    def reset_subject_match_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectMatchType", []))

    @jsii.member(jsii_name="resetSuspendedAction")
    def reset_suspended_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuspendedAction", []))

    @jsii.member(jsii_name="resetUsernameTemplate")
    def reset_username_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsernameTemplate", []))

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
    @jsii.member(jsii_name="authorizationBinding")
    def authorization_binding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationBinding"))

    @builtins.property
    @jsii.member(jsii_name="authorizationUrl")
    def authorization_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationUrl"))

    @builtins.property
    @jsii.member(jsii_name="tokenBinding")
    def token_binding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenBinding"))

    @builtins.property
    @jsii.member(jsii_name="tokenUrl")
    def token_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenUrl"))

    @builtins.property
    @jsii.member(jsii_name="trustAudience")
    def trust_audience(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trustAudience"))

    @builtins.property
    @jsii.member(jsii_name="trustIssuer")
    def trust_issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trustIssuer"))

    @builtins.property
    @jsii.member(jsii_name="trustKid")
    def trust_kid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trustKid"))

    @builtins.property
    @jsii.member(jsii_name="trustRevocation")
    def trust_revocation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trustRevocation"))

    @builtins.property
    @jsii.member(jsii_name="trustRevocationCacheLifetime")
    def trust_revocation_cache_lifetime(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "trustRevocationCacheLifetime"))

    @builtins.property
    @jsii.member(jsii_name="accountLinkActionInput")
    def account_link_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountLinkActionInput"))

    @builtins.property
    @jsii.member(jsii_name="accountLinkGroupIncludeInput")
    def account_link_group_include_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accountLinkGroupIncludeInput"))

    @builtins.property
    @jsii.member(jsii_name="appleKidInput")
    def apple_kid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appleKidInput"))

    @builtins.property
    @jsii.member(jsii_name="applePrivateKeyInput")
    def apple_private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applePrivateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="appleTeamIdInput")
    def apple_team_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appleTeamIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="deprovisionedActionInput")
    def deprovisioned_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deprovisionedActionInput"))

    @builtins.property
    @jsii.member(jsii_name="groupsActionInput")
    def groups_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupsActionInput"))

    @builtins.property
    @jsii.member(jsii_name="groupsAssignmentInput")
    def groups_assignment_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupsAssignmentInput"))

    @builtins.property
    @jsii.member(jsii_name="groupsAttributeInput")
    def groups_attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupsAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="groupsFilterInput")
    def groups_filter_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupsFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerModeInput")
    def issuer_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerModeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxClockSkewInput")
    def max_clock_skew_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxClockSkewInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="profileMasterInput")
    def profile_master_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "profileMasterInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolTypeInput")
    def protocol_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="provisioningActionInput")
    def provisioning_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "provisioningActionInput"))

    @builtins.property
    @jsii.member(jsii_name="scopesInput")
    def scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopesInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectMatchAttributeInput")
    def subject_match_attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectMatchAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectMatchTypeInput")
    def subject_match_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectMatchTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="suspendedActionInput")
    def suspended_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "suspendedActionInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameTemplateInput")
    def username_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="accountLinkAction")
    def account_link_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountLinkAction"))

    @account_link_action.setter
    def account_link_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e04876352cacdad7085404c55889ab8d1ca2782ec3e488996b7d7faf63482af0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountLinkAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accountLinkGroupInclude")
    def account_link_group_include(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accountLinkGroupInclude"))

    @account_link_group_include.setter
    def account_link_group_include(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c863b402c423a672a5de0f55f84b458fc6f6cd8c60a7c5da1c0c8dc18d0736ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountLinkGroupInclude", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appleKid")
    def apple_kid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appleKid"))

    @apple_kid.setter
    def apple_kid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e16795d318f5a1b8aa0635feb04f791e30a52c5f38c06a890dad3d3f0474fe0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appleKid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applePrivateKey")
    def apple_private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applePrivateKey"))

    @apple_private_key.setter
    def apple_private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__951c068bb0a72d3327216f2eee180bd81a64a18c6514ce35b4332e6e1127b9e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applePrivateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appleTeamId")
    def apple_team_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appleTeamId"))

    @apple_team_id.setter
    def apple_team_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab18b61263651c196fd8f3f3b4f6c86a1a66a823a75bdb7b1386a9ae7aff030)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appleTeamId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d31a87775c5d7f00225fcd6cd814aa67c15591ecb993f581dfa84b4e920cd35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__444691c77fe36cf7bce83c07dba2cbf8e1e5ac67fb7647dbb5ec83bd382c4490)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deprovisionedAction")
    def deprovisioned_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deprovisionedAction"))

    @deprovisioned_action.setter
    def deprovisioned_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be944781e723e0dfeb37aaa5cab24831f095b1985eb776636ff71c8fd752581f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deprovisionedAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupsAction")
    def groups_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupsAction"))

    @groups_action.setter
    def groups_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac2456675e44103b4a741290d645e160eea592db6f2b757be75e40d88b41f819)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupsAssignment")
    def groups_assignment(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupsAssignment"))

    @groups_assignment.setter
    def groups_assignment(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e517b323dc683733752d5e6372c24d9561ae75a2df84a6c9493b81c9de248c81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsAssignment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupsAttribute")
    def groups_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupsAttribute"))

    @groups_attribute.setter
    def groups_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c10c050df7bec68cf864fa6c20bd4df23b9c9fe55e846bd539369cf2cf14cda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupsFilter")
    def groups_filter(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupsFilter"))

    @groups_filter.setter
    def groups_filter(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba1f4b2a2e5a3a0799b856a22357e4ae377063ee362acb6c680a4c41632d01a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdbbf03e37013d5a275fff3f7a9656acee5b1fff1bf33afdc41442e5e3625bac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuerMode")
    def issuer_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerMode"))

    @issuer_mode.setter
    def issuer_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92d18680990f5b30f5fdbccd40523611847679e65d5187f2f82943c8031c82fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxClockSkew")
    def max_clock_skew(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxClockSkew"))

    @max_clock_skew.setter
    def max_clock_skew(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d87a1f77c60ca28877bb1fc88ab0ae9a55a285370edfec1700ed94ce51c2bb5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxClockSkew", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e72c64e3c594499a010f327d4ea330bc9027cab40b8486cf97821334e36a4e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="profileMaster")
    def profile_master(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "profileMaster"))

    @profile_master.setter
    def profile_master(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__719e515922117f9a0dce2a78906387762017658889cd7cd11698849920f04505)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profileMaster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocolType")
    def protocol_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocolType"))

    @protocol_type.setter
    def protocol_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9a63e2deaf9707c9390829e3d13d24ae86bec60b3a56539ea80b22ede8af0bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocolType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisioningAction")
    def provisioning_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "provisioningAction"))

    @provisioning_action.setter
    def provisioning_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a4513f91e30b16850b79fe8c4b07efeb17a2309e69ea9cb1267d692d65211b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisioningAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dd586d58ef17654750c903f568a2c8cf5c01b94412c6a4dcc6c524394977120)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c8eef61b36d40e24a13786262878f0a3e107f1222f42fc4bf859d11a18a62d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subjectMatchAttribute")
    def subject_match_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subjectMatchAttribute"))

    @subject_match_attribute.setter
    def subject_match_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43381c24107881a080aba8179c0401a0c7adeb6913506cf3d08cbd5dbff007be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectMatchAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subjectMatchType")
    def subject_match_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subjectMatchType"))

    @subject_match_type.setter
    def subject_match_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6482dc9d1f9e275bce52baf016581180d3ad52c10adced0cd3c2dce43a15a964)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectMatchType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suspendedAction")
    def suspended_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suspendedAction"))

    @suspended_action.setter
    def suspended_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__497ac8ee32c8dbb385448f9d7bc88ee1bdacc1547e63e8f0ae191fa28f6fb0b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspendedAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3437a8409412f84b10ffe5dce6b1d9e5fd58fa534b1eb06edb314e2413cf0a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="usernameTemplate")
    def username_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usernameTemplate"))

    @username_template.setter
    def username_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2068615a1decffabc828cb37804fed4e3fbd90c92f0a108e61c5f0220302924)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usernameTemplate", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.idpSocial.IdpSocialConfig",
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
        "scopes": "scopes",
        "type": "type",
        "account_link_action": "accountLinkAction",
        "account_link_group_include": "accountLinkGroupInclude",
        "apple_kid": "appleKid",
        "apple_private_key": "applePrivateKey",
        "apple_team_id": "appleTeamId",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "deprovisioned_action": "deprovisionedAction",
        "groups_action": "groupsAction",
        "groups_assignment": "groupsAssignment",
        "groups_attribute": "groupsAttribute",
        "groups_filter": "groupsFilter",
        "id": "id",
        "issuer_mode": "issuerMode",
        "max_clock_skew": "maxClockSkew",
        "profile_master": "profileMaster",
        "protocol_type": "protocolType",
        "provisioning_action": "provisioningAction",
        "status": "status",
        "subject_match_attribute": "subjectMatchAttribute",
        "subject_match_type": "subjectMatchType",
        "suspended_action": "suspendedAction",
        "username_template": "usernameTemplate",
    },
)
class IdpSocialConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        scopes: typing.Sequence[builtins.str],
        type: builtins.str,
        account_link_action: typing.Optional[builtins.str] = None,
        account_link_group_include: typing.Optional[typing.Sequence[builtins.str]] = None,
        apple_kid: typing.Optional[builtins.str] = None,
        apple_private_key: typing.Optional[builtins.str] = None,
        apple_team_id: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        deprovisioned_action: typing.Optional[builtins.str] = None,
        groups_action: typing.Optional[builtins.str] = None,
        groups_assignment: typing.Optional[typing.Sequence[builtins.str]] = None,
        groups_attribute: typing.Optional[builtins.str] = None,
        groups_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        issuer_mode: typing.Optional[builtins.str] = None,
        max_clock_skew: typing.Optional[jsii.Number] = None,
        profile_master: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        protocol_type: typing.Optional[builtins.str] = None,
        provisioning_action: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        subject_match_attribute: typing.Optional[builtins.str] = None,
        subject_match_type: typing.Optional[builtins.str] = None,
        suspended_action: typing.Optional[builtins.str] = None,
        username_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the IdP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#name IdpSocial#name}
        :param scopes: The scopes of the IdP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#scopes IdpSocial#scopes}
        :param type: Identity Provider Types: https://developer.okta.com/docs/reference/api/idps/#identity-provider-type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#type IdpSocial#type}
        :param account_link_action: Specifies the account linking action for an IdP user. Default: ``AUTO``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#account_link_action IdpSocial#account_link_action}
        :param account_link_group_include: Group memberships to determine link candidates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#account_link_group_include IdpSocial#account_link_group_include}
        :param apple_kid: The Key ID that you obtained from Apple when you created the private key for the client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#apple_kid IdpSocial#apple_kid}
        :param apple_private_key: The Key ID that you obtained from Apple when you created the private key for the client. PrivateKey is required when resource is first created. For all consecutive updates, it can be empty/omitted and keeps the existing value if it is empty/omitted. PrivateKey isn't returned when importing this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#apple_private_key IdpSocial#apple_private_key}
        :param apple_team_id: The Team ID associated with your Apple developer account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#apple_team_id IdpSocial#apple_team_id}
        :param client_id: Unique identifier issued by AS for the Okta IdP instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#client_id IdpSocial#client_id}
        :param client_secret: Client secret issued by AS for the Okta IdP instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#client_secret IdpSocial#client_secret}
        :param deprovisioned_action: Action for a previously deprovisioned IdP user during authentication. Can be ``NONE`` or ``REACTIVATE``. Default: ``NONE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#deprovisioned_action IdpSocial#deprovisioned_action}
        :param groups_action: Provisioning action for IdP user's group memberships. It can be ``NONE``, ``SYNC``, ``APPEND``, or ``ASSIGN``. Default: ``NONE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#groups_action IdpSocial#groups_action}
        :param groups_assignment: List of Okta Group IDs to add an IdP user as a member with the ``ASSIGN`` ``groups_action``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#groups_assignment IdpSocial#groups_assignment}
        :param groups_attribute: IdP user profile attribute name (case-insensitive) for an array value that contains group memberships. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#groups_attribute IdpSocial#groups_attribute}
        :param groups_filter: Whitelist of Okta Group identifiers that are allowed for the ``APPEND`` or ``SYNC`` ``groups_action``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#groups_filter IdpSocial#groups_filter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#id IdpSocial#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param issuer_mode: Indicates whether Okta uses the original Okta org domain URL, or a custom domain URL. It can be ``ORG_URL`` or ``CUSTOM_URL``. Default: ``ORG_URL`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#issuer_mode IdpSocial#issuer_mode}
        :param max_clock_skew: Maximum allowable clock-skew when processing messages from the IdP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#max_clock_skew IdpSocial#max_clock_skew}
        :param profile_master: Determines if the IdP should act as a source of truth for user profile attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#profile_master IdpSocial#profile_master}
        :param protocol_type: The type of protocol to use. It can be ``OIDC`` or ``OAUTH2``. Default: ``OAUTH2``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#protocol_type IdpSocial#protocol_type}
        :param provisioning_action: Provisioning action for an IdP user during authentication. Default: ``AUTO``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#provisioning_action IdpSocial#provisioning_action}
        :param status: Default to ``ACTIVE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#status IdpSocial#status}
        :param subject_match_attribute: Okta user profile attribute for matching transformed IdP username. Only for matchType ``CUSTOM_ATTRIBUTE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#subject_match_attribute IdpSocial#subject_match_attribute}
        :param subject_match_type: Determines the Okta user profile attribute match conditions for account linking and authentication of the transformed IdP username. By default, it is set to ``USERNAME``. It can be set to ``USERNAME``, ``EMAIL``, ``USERNAME_OR_EMAIL`` or ``CUSTOM_ATTRIBUTE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#subject_match_type IdpSocial#subject_match_type}
        :param suspended_action: Action for a previously suspended IdP user during authentication. Can be ``NONE`` or ``REACTIVATE``. Default: ``NONE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#suspended_action IdpSocial#suspended_action}
        :param username_template: Okta EL Expression to generate or transform a unique username for the IdP user. Default: ``idpuser.email``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#username_template IdpSocial#username_template}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae4a924937328ddddf15a8a52207f3512cf87180b82dc9c95f84250fb7e6853c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument account_link_action", value=account_link_action, expected_type=type_hints["account_link_action"])
            check_type(argname="argument account_link_group_include", value=account_link_group_include, expected_type=type_hints["account_link_group_include"])
            check_type(argname="argument apple_kid", value=apple_kid, expected_type=type_hints["apple_kid"])
            check_type(argname="argument apple_private_key", value=apple_private_key, expected_type=type_hints["apple_private_key"])
            check_type(argname="argument apple_team_id", value=apple_team_id, expected_type=type_hints["apple_team_id"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument deprovisioned_action", value=deprovisioned_action, expected_type=type_hints["deprovisioned_action"])
            check_type(argname="argument groups_action", value=groups_action, expected_type=type_hints["groups_action"])
            check_type(argname="argument groups_assignment", value=groups_assignment, expected_type=type_hints["groups_assignment"])
            check_type(argname="argument groups_attribute", value=groups_attribute, expected_type=type_hints["groups_attribute"])
            check_type(argname="argument groups_filter", value=groups_filter, expected_type=type_hints["groups_filter"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument issuer_mode", value=issuer_mode, expected_type=type_hints["issuer_mode"])
            check_type(argname="argument max_clock_skew", value=max_clock_skew, expected_type=type_hints["max_clock_skew"])
            check_type(argname="argument profile_master", value=profile_master, expected_type=type_hints["profile_master"])
            check_type(argname="argument protocol_type", value=protocol_type, expected_type=type_hints["protocol_type"])
            check_type(argname="argument provisioning_action", value=provisioning_action, expected_type=type_hints["provisioning_action"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument subject_match_attribute", value=subject_match_attribute, expected_type=type_hints["subject_match_attribute"])
            check_type(argname="argument subject_match_type", value=subject_match_type, expected_type=type_hints["subject_match_type"])
            check_type(argname="argument suspended_action", value=suspended_action, expected_type=type_hints["suspended_action"])
            check_type(argname="argument username_template", value=username_template, expected_type=type_hints["username_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "scopes": scopes,
            "type": type,
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
        if account_link_action is not None:
            self._values["account_link_action"] = account_link_action
        if account_link_group_include is not None:
            self._values["account_link_group_include"] = account_link_group_include
        if apple_kid is not None:
            self._values["apple_kid"] = apple_kid
        if apple_private_key is not None:
            self._values["apple_private_key"] = apple_private_key
        if apple_team_id is not None:
            self._values["apple_team_id"] = apple_team_id
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if deprovisioned_action is not None:
            self._values["deprovisioned_action"] = deprovisioned_action
        if groups_action is not None:
            self._values["groups_action"] = groups_action
        if groups_assignment is not None:
            self._values["groups_assignment"] = groups_assignment
        if groups_attribute is not None:
            self._values["groups_attribute"] = groups_attribute
        if groups_filter is not None:
            self._values["groups_filter"] = groups_filter
        if id is not None:
            self._values["id"] = id
        if issuer_mode is not None:
            self._values["issuer_mode"] = issuer_mode
        if max_clock_skew is not None:
            self._values["max_clock_skew"] = max_clock_skew
        if profile_master is not None:
            self._values["profile_master"] = profile_master
        if protocol_type is not None:
            self._values["protocol_type"] = protocol_type
        if provisioning_action is not None:
            self._values["provisioning_action"] = provisioning_action
        if status is not None:
            self._values["status"] = status
        if subject_match_attribute is not None:
            self._values["subject_match_attribute"] = subject_match_attribute
        if subject_match_type is not None:
            self._values["subject_match_type"] = subject_match_type
        if suspended_action is not None:
            self._values["suspended_action"] = suspended_action
        if username_template is not None:
            self._values["username_template"] = username_template

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
        '''Name of the IdP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#name IdpSocial#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scopes(self) -> typing.List[builtins.str]:
        '''The scopes of the IdP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#scopes IdpSocial#scopes}
        '''
        result = self._values.get("scopes")
        assert result is not None, "Required property 'scopes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Identity Provider Types: https://developer.okta.com/docs/reference/api/idps/#identity-provider-type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#type IdpSocial#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_link_action(self) -> typing.Optional[builtins.str]:
        '''Specifies the account linking action for an IdP user. Default: ``AUTO``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#account_link_action IdpSocial#account_link_action}
        '''
        result = self._values.get("account_link_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def account_link_group_include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Group memberships to determine link candidates.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#account_link_group_include IdpSocial#account_link_group_include}
        '''
        result = self._values.get("account_link_group_include")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def apple_kid(self) -> typing.Optional[builtins.str]:
        '''The Key ID that you obtained from Apple when you created the private key for the client.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#apple_kid IdpSocial#apple_kid}
        '''
        result = self._values.get("apple_kid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def apple_private_key(self) -> typing.Optional[builtins.str]:
        '''The Key ID that you obtained from Apple when you created the private key for the client.

        PrivateKey is required when resource is first created. For all consecutive updates, it can be empty/omitted and keeps the existing value if it is empty/omitted. PrivateKey isn't returned when importing this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#apple_private_key IdpSocial#apple_private_key}
        '''
        result = self._values.get("apple_private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def apple_team_id(self) -> typing.Optional[builtins.str]:
        '''The Team ID associated with your Apple developer account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#apple_team_id IdpSocial#apple_team_id}
        '''
        result = self._values.get("apple_team_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Unique identifier issued by AS for the Okta IdP instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#client_id IdpSocial#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''Client secret issued by AS for the Okta IdP instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#client_secret IdpSocial#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deprovisioned_action(self) -> typing.Optional[builtins.str]:
        '''Action for a previously deprovisioned IdP user during authentication. Can be ``NONE`` or ``REACTIVATE``. Default: ``NONE``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#deprovisioned_action IdpSocial#deprovisioned_action}
        '''
        result = self._values.get("deprovisioned_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups_action(self) -> typing.Optional[builtins.str]:
        '''Provisioning action for IdP user's group memberships. It can be ``NONE``, ``SYNC``, ``APPEND``, or ``ASSIGN``. Default: ``NONE``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#groups_action IdpSocial#groups_action}
        '''
        result = self._values.get("groups_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups_assignment(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of Okta Group IDs to add an IdP user as a member with the ``ASSIGN`` ``groups_action``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#groups_assignment IdpSocial#groups_assignment}
        '''
        result = self._values.get("groups_assignment")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def groups_attribute(self) -> typing.Optional[builtins.str]:
        '''IdP user profile attribute name (case-insensitive) for an array value that contains group memberships.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#groups_attribute IdpSocial#groups_attribute}
        '''
        result = self._values.get("groups_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Whitelist of Okta Group identifiers that are allowed for the ``APPEND`` or ``SYNC`` ``groups_action``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#groups_filter IdpSocial#groups_filter}
        '''
        result = self._values.get("groups_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#id IdpSocial#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issuer_mode(self) -> typing.Optional[builtins.str]:
        '''Indicates whether Okta uses the original Okta org domain URL, or a custom domain URL.

        It can be ``ORG_URL`` or ``CUSTOM_URL``. Default: ``ORG_URL``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#issuer_mode IdpSocial#issuer_mode}
        '''
        result = self._values.get("issuer_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_clock_skew(self) -> typing.Optional[jsii.Number]:
        '''Maximum allowable clock-skew when processing messages from the IdP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#max_clock_skew IdpSocial#max_clock_skew}
        '''
        result = self._values.get("max_clock_skew")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def profile_master(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines if the IdP should act as a source of truth for user profile attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#profile_master IdpSocial#profile_master}
        '''
        result = self._values.get("profile_master")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def protocol_type(self) -> typing.Optional[builtins.str]:
        '''The type of protocol to use. It can be ``OIDC`` or ``OAUTH2``. Default: ``OAUTH2``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#protocol_type IdpSocial#protocol_type}
        '''
        result = self._values.get("protocol_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioning_action(self) -> typing.Optional[builtins.str]:
        '''Provisioning action for an IdP user during authentication. Default: ``AUTO``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#provisioning_action IdpSocial#provisioning_action}
        '''
        result = self._values.get("provisioning_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Default to ``ACTIVE``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#status IdpSocial#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_match_attribute(self) -> typing.Optional[builtins.str]:
        '''Okta user profile attribute for matching transformed IdP username. Only for matchType ``CUSTOM_ATTRIBUTE``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#subject_match_attribute IdpSocial#subject_match_attribute}
        '''
        result = self._values.get("subject_match_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_match_type(self) -> typing.Optional[builtins.str]:
        '''Determines the Okta user profile attribute match conditions for account linking and authentication of the transformed IdP username.

        By default, it is set to ``USERNAME``. It can be set to ``USERNAME``, ``EMAIL``, ``USERNAME_OR_EMAIL`` or ``CUSTOM_ATTRIBUTE``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#subject_match_type IdpSocial#subject_match_type}
        '''
        result = self._values.get("subject_match_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suspended_action(self) -> typing.Optional[builtins.str]:
        '''Action for a previously suspended IdP user during authentication. Can be ``NONE`` or ``REACTIVATE``. Default: ``NONE``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#suspended_action IdpSocial#suspended_action}
        '''
        result = self._values.get("suspended_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username_template(self) -> typing.Optional[builtins.str]:
        '''Okta EL Expression to generate or transform a unique username for the IdP user. Default: ``idpuser.email``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.20.0/docs/resources/idp_social#username_template IdpSocial#username_template}
        '''
        result = self._values.get("username_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdpSocialConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IdpSocial",
    "IdpSocialConfig",
]

publication.publish()

def _typecheckingstub__281f61eb0a6909884735ce5eb8686bf9b41bd2dc13ca18c3263015cab4ca377b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    scopes: typing.Sequence[builtins.str],
    type: builtins.str,
    account_link_action: typing.Optional[builtins.str] = None,
    account_link_group_include: typing.Optional[typing.Sequence[builtins.str]] = None,
    apple_kid: typing.Optional[builtins.str] = None,
    apple_private_key: typing.Optional[builtins.str] = None,
    apple_team_id: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    deprovisioned_action: typing.Optional[builtins.str] = None,
    groups_action: typing.Optional[builtins.str] = None,
    groups_assignment: typing.Optional[typing.Sequence[builtins.str]] = None,
    groups_attribute: typing.Optional[builtins.str] = None,
    groups_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    issuer_mode: typing.Optional[builtins.str] = None,
    max_clock_skew: typing.Optional[jsii.Number] = None,
    profile_master: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    protocol_type: typing.Optional[builtins.str] = None,
    provisioning_action: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    subject_match_attribute: typing.Optional[builtins.str] = None,
    subject_match_type: typing.Optional[builtins.str] = None,
    suspended_action: typing.Optional[builtins.str] = None,
    username_template: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__1e085f698a4a605e56b549b0a249750c229041d12eaa68d5d1924452ddf87671(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e04876352cacdad7085404c55889ab8d1ca2782ec3e488996b7d7faf63482af0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c863b402c423a672a5de0f55f84b458fc6f6cd8c60a7c5da1c0c8dc18d0736ea(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e16795d318f5a1b8aa0635feb04f791e30a52c5f38c06a890dad3d3f0474fe0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__951c068bb0a72d3327216f2eee180bd81a64a18c6514ce35b4332e6e1127b9e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab18b61263651c196fd8f3f3b4f6c86a1a66a823a75bdb7b1386a9ae7aff030(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d31a87775c5d7f00225fcd6cd814aa67c15591ecb993f581dfa84b4e920cd35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__444691c77fe36cf7bce83c07dba2cbf8e1e5ac67fb7647dbb5ec83bd382c4490(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be944781e723e0dfeb37aaa5cab24831f095b1985eb776636ff71c8fd752581f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac2456675e44103b4a741290d645e160eea592db6f2b757be75e40d88b41f819(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e517b323dc683733752d5e6372c24d9561ae75a2df84a6c9493b81c9de248c81(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c10c050df7bec68cf864fa6c20bd4df23b9c9fe55e846bd539369cf2cf14cda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba1f4b2a2e5a3a0799b856a22357e4ae377063ee362acb6c680a4c41632d01a0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdbbf03e37013d5a275fff3f7a9656acee5b1fff1bf33afdc41442e5e3625bac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92d18680990f5b30f5fdbccd40523611847679e65d5187f2f82943c8031c82fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87a1f77c60ca28877bb1fc88ab0ae9a55a285370edfec1700ed94ce51c2bb5f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e72c64e3c594499a010f327d4ea330bc9027cab40b8486cf97821334e36a4e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__719e515922117f9a0dce2a78906387762017658889cd7cd11698849920f04505(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9a63e2deaf9707c9390829e3d13d24ae86bec60b3a56539ea80b22ede8af0bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a4513f91e30b16850b79fe8c4b07efeb17a2309e69ea9cb1267d692d65211b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd586d58ef17654750c903f568a2c8cf5c01b94412c6a4dcc6c524394977120(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c8eef61b36d40e24a13786262878f0a3e107f1222f42fc4bf859d11a18a62d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43381c24107881a080aba8179c0401a0c7adeb6913506cf3d08cbd5dbff007be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6482dc9d1f9e275bce52baf016581180d3ad52c10adced0cd3c2dce43a15a964(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__497ac8ee32c8dbb385448f9d7bc88ee1bdacc1547e63e8f0ae191fa28f6fb0b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3437a8409412f84b10ffe5dce6b1d9e5fd58fa534b1eb06edb314e2413cf0a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2068615a1decffabc828cb37804fed4e3fbd90c92f0a108e61c5f0220302924(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae4a924937328ddddf15a8a52207f3512cf87180b82dc9c95f84250fb7e6853c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    scopes: typing.Sequence[builtins.str],
    type: builtins.str,
    account_link_action: typing.Optional[builtins.str] = None,
    account_link_group_include: typing.Optional[typing.Sequence[builtins.str]] = None,
    apple_kid: typing.Optional[builtins.str] = None,
    apple_private_key: typing.Optional[builtins.str] = None,
    apple_team_id: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    deprovisioned_action: typing.Optional[builtins.str] = None,
    groups_action: typing.Optional[builtins.str] = None,
    groups_assignment: typing.Optional[typing.Sequence[builtins.str]] = None,
    groups_attribute: typing.Optional[builtins.str] = None,
    groups_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    issuer_mode: typing.Optional[builtins.str] = None,
    max_clock_skew: typing.Optional[jsii.Number] = None,
    profile_master: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    protocol_type: typing.Optional[builtins.str] = None,
    provisioning_action: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    subject_match_attribute: typing.Optional[builtins.str] = None,
    subject_match_type: typing.Optional[builtins.str] = None,
    suspended_action: typing.Optional[builtins.str] = None,
    username_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
