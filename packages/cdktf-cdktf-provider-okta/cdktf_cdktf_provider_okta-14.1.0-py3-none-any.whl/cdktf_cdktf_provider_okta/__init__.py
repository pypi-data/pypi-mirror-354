r'''
# CDKTF prebuilt bindings for okta/okta provider version 4.20.0

This repo builds and publishes the [Terraform okta provider](https://registry.terraform.io/providers/okta/okta/4.20.0/docs) bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-okta](https://www.npmjs.com/package/@cdktf/provider-okta).

`npm install @cdktf/provider-okta`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-okta](https://pypi.org/project/cdktf-cdktf-provider-okta).

`pipenv install cdktf-cdktf-provider-okta`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Okta](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Okta).

`dotnet add package HashiCorp.Cdktf.Providers.Okta`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-okta](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-okta).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-okta</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-okta-go`](https://github.com/cdktf/cdktf-provider-okta-go) package.

`go get github.com/cdktf/cdktf-provider-okta-go/okta/<version>`

Where `<version>` is the version of the prebuilt provider you would like to use e.g. `v11`. The full module name can be found
within the [go.mod](https://github.com/cdktf/cdktf-provider-okta-go/blob/main/okta/go.mod#L1) file.

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-okta).

## Versioning

This project is explicitly not tracking the Terraform okta provider version 1:1. In fact, it always tracks `latest` of `~> 4.0` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by [generating the provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [CDK for Terraform](https://cdk.tf)
* [Terraform okta provider](https://registry.terraform.io/providers/okta/okta/4.20.0)
* [Terraform Engine](https://terraform.io)

If there are breaking changes (backward incompatible) in any of the above, the major version of this project will be bumped.

## Features / Issues / Bugs

Please report bugs and issues to the [CDK for Terraform](https://cdk.tf) project:

* [Create bug report](https://cdk.tf/bug)
* [Create feature request](https://cdk.tf/feature)

## Contributing

### Projen

This is mostly based on [Projen](https://github.com/projen/projen), which takes care of generating the entire repository.

### cdktf-provider-project based on Projen

There's a custom [project builder](https://github.com/cdktf/cdktf-provider-project) which encapsulate the common settings for all `cdktf` prebuilt providers.

### Provider Version

The provider version can be adjusted in [./.projenrc.js](./.projenrc.js).

### Repository Management

The repository is managed by [CDKTF Repository Manager](https://github.com/cdktf/cdktf-repository-manager/).
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

from ._jsii import *

__all__ = [
    "admin_role_custom",
    "admin_role_custom_assignments",
    "admin_role_targets",
    "app_access_policy_assignment",
    "app_auto_login",
    "app_basic_auth",
    "app_bookmark",
    "app_group_assignment",
    "app_group_assignments",
    "app_oauth",
    "app_oauth_api_scope",
    "app_oauth_post_logout_redirect_uri",
    "app_oauth_redirect_uri",
    "app_oauth_role_assignment",
    "app_saml",
    "app_saml_app_settings",
    "app_secure_password_store",
    "app_shared_credentials",
    "app_signon_policy",
    "app_signon_policy_rule",
    "app_swa",
    "app_three_field",
    "app_user",
    "app_user_base_schema_property",
    "app_user_schema_property",
    "auth_server",
    "auth_server_claim",
    "auth_server_claim_default",
    "auth_server_default",
    "auth_server_policy",
    "auth_server_policy_rule",
    "auth_server_scope",
    "authenticator",
    "behavior",
    "brand",
    "captcha",
    "captcha_org_wide_settings",
    "customized_signin_page",
    "data_okta_app",
    "data_okta_app_group_assignments",
    "data_okta_app_metadata_saml",
    "data_okta_app_oauth",
    "data_okta_app_saml",
    "data_okta_app_signon_policy",
    "data_okta_app_user_assignments",
    "data_okta_apps",
    "data_okta_auth_server",
    "data_okta_auth_server_claim",
    "data_okta_auth_server_claims",
    "data_okta_auth_server_policy",
    "data_okta_auth_server_scopes",
    "data_okta_authenticator",
    "data_okta_behavior",
    "data_okta_behaviors",
    "data_okta_brand",
    "data_okta_brands",
    "data_okta_default_policy",
    "data_okta_default_signin_page",
    "data_okta_device_assurance_policy",
    "data_okta_domain",
    "data_okta_email_customization",
    "data_okta_email_customizations",
    "data_okta_email_smtp_server",
    "data_okta_email_template",
    "data_okta_email_templates",
    "data_okta_everyone_group",
    "data_okta_group",
    "data_okta_group_rule",
    "data_okta_groups",
    "data_okta_idp_metadata_saml",
    "data_okta_idp_oidc",
    "data_okta_idp_saml",
    "data_okta_idp_social",
    "data_okta_log_stream",
    "data_okta_network_zone",
    "data_okta_org_metadata",
    "data_okta_policy",
    "data_okta_role_subscription",
    "data_okta_theme",
    "data_okta_themes",
    "data_okta_trusted_origins",
    "data_okta_user",
    "data_okta_user_profile_mapping_source",
    "data_okta_user_security_questions",
    "data_okta_user_type",
    "data_okta_users",
    "domain",
    "domain_certificate",
    "domain_verification",
    "email_customization",
    "email_domain",
    "email_domain_verification",
    "email_sender",
    "email_sender_verification",
    "email_smtp_server",
    "email_template_settings",
    "event_hook",
    "event_hook_verification",
    "factor",
    "factor_totp",
    "group",
    "group_memberships",
    "group_owner",
    "group_role",
    "group_rule",
    "group_schema_property",
    "idp_oidc",
    "idp_saml",
    "idp_saml_key",
    "idp_social",
    "inline_hook",
    "link_definition",
    "link_value",
    "log_stream",
    "network_zone",
    "org_configuration",
    "org_support",
    "policy_device_assurance_android",
    "policy_device_assurance_chromeos",
    "policy_device_assurance_ios",
    "policy_device_assurance_macos",
    "policy_device_assurance_windows",
    "policy_mfa",
    "policy_mfa_default",
    "policy_password",
    "policy_password_default",
    "policy_profile_enrollment",
    "policy_profile_enrollment_apps",
    "policy_rule_idp_discovery",
    "policy_rule_mfa",
    "policy_rule_password",
    "policy_rule_profile_enrollment",
    "policy_rule_signon",
    "policy_signon",
    "preview_signin_page",
    "profile_mapping",
    "provider",
    "rate_limiting",
    "resource_set",
    "role_subscription",
    "security_notification_emails",
    "template_sms",
    "theme",
    "threat_insight_settings",
    "trusted_origin",
    "trusted_server",
    "user",
    "user_admin_roles",
    "user_base_schema_property",
    "user_factor_question",
    "user_group_memberships",
    "user_schema_property",
    "user_type",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import admin_role_custom
from . import admin_role_custom_assignments
from . import admin_role_targets
from . import app_access_policy_assignment
from . import app_auto_login
from . import app_basic_auth
from . import app_bookmark
from . import app_group_assignment
from . import app_group_assignments
from . import app_oauth
from . import app_oauth_api_scope
from . import app_oauth_post_logout_redirect_uri
from . import app_oauth_redirect_uri
from . import app_oauth_role_assignment
from . import app_saml
from . import app_saml_app_settings
from . import app_secure_password_store
from . import app_shared_credentials
from . import app_signon_policy
from . import app_signon_policy_rule
from . import app_swa
from . import app_three_field
from . import app_user
from . import app_user_base_schema_property
from . import app_user_schema_property
from . import auth_server
from . import auth_server_claim
from . import auth_server_claim_default
from . import auth_server_default
from . import auth_server_policy
from . import auth_server_policy_rule
from . import auth_server_scope
from . import authenticator
from . import behavior
from . import brand
from . import captcha
from . import captcha_org_wide_settings
from . import customized_signin_page
from . import data_okta_app
from . import data_okta_app_group_assignments
from . import data_okta_app_metadata_saml
from . import data_okta_app_oauth
from . import data_okta_app_saml
from . import data_okta_app_signon_policy
from . import data_okta_app_user_assignments
from . import data_okta_apps
from . import data_okta_auth_server
from . import data_okta_auth_server_claim
from . import data_okta_auth_server_claims
from . import data_okta_auth_server_policy
from . import data_okta_auth_server_scopes
from . import data_okta_authenticator
from . import data_okta_behavior
from . import data_okta_behaviors
from . import data_okta_brand
from . import data_okta_brands
from . import data_okta_default_policy
from . import data_okta_default_signin_page
from . import data_okta_device_assurance_policy
from . import data_okta_domain
from . import data_okta_email_customization
from . import data_okta_email_customizations
from . import data_okta_email_smtp_server
from . import data_okta_email_template
from . import data_okta_email_templates
from . import data_okta_everyone_group
from . import data_okta_group
from . import data_okta_group_rule
from . import data_okta_groups
from . import data_okta_idp_metadata_saml
from . import data_okta_idp_oidc
from . import data_okta_idp_saml
from . import data_okta_idp_social
from . import data_okta_log_stream
from . import data_okta_network_zone
from . import data_okta_org_metadata
from . import data_okta_policy
from . import data_okta_role_subscription
from . import data_okta_theme
from . import data_okta_themes
from . import data_okta_trusted_origins
from . import data_okta_user
from . import data_okta_user_profile_mapping_source
from . import data_okta_user_security_questions
from . import data_okta_user_type
from . import data_okta_users
from . import domain
from . import domain_certificate
from . import domain_verification
from . import email_customization
from . import email_domain
from . import email_domain_verification
from . import email_sender
from . import email_sender_verification
from . import email_smtp_server
from . import email_template_settings
from . import event_hook
from . import event_hook_verification
from . import factor
from . import factor_totp
from . import group
from . import group_memberships
from . import group_owner
from . import group_role
from . import group_rule
from . import group_schema_property
from . import idp_oidc
from . import idp_saml
from . import idp_saml_key
from . import idp_social
from . import inline_hook
from . import link_definition
from . import link_value
from . import log_stream
from . import network_zone
from . import org_configuration
from . import org_support
from . import policy_device_assurance_android
from . import policy_device_assurance_chromeos
from . import policy_device_assurance_ios
from . import policy_device_assurance_macos
from . import policy_device_assurance_windows
from . import policy_mfa
from . import policy_mfa_default
from . import policy_password
from . import policy_password_default
from . import policy_profile_enrollment
from . import policy_profile_enrollment_apps
from . import policy_rule_idp_discovery
from . import policy_rule_mfa
from . import policy_rule_password
from . import policy_rule_profile_enrollment
from . import policy_rule_signon
from . import policy_signon
from . import preview_signin_page
from . import profile_mapping
from . import provider
from . import rate_limiting
from . import resource_set
from . import role_subscription
from . import security_notification_emails
from . import template_sms
from . import theme
from . import threat_insight_settings
from . import trusted_origin
from . import trusted_server
from . import user
from . import user_admin_roles
from . import user_base_schema_property
from . import user_factor_question
from . import user_group_memberships
from . import user_schema_property
from . import user_type
