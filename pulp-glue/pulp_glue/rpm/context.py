from typing import IO, Any, ClassVar, Optional

import click

from pulp_glue.common.context import (
    EntityDefinition,
    PluginRequirement,
    PulpACSContext,
    PulpContentContext,
    PulpDistributionContext,
    PulpEntityContext,
    PulpException,
    PulpPublicationContext,
    PulpRemoteContext,
    PulpRepositoryContext,
    PulpRepositoryVersionContext,
)
from pulp_glue.common.i18n import get_translation

translation = get_translation(__name__)
_ = translation.gettext


class PulpRpmACSContext(PulpACSContext):
    PLUGIN = "rpm"
    RESOURCE_TYPE = "rpm"
    ENTITY = _("rpm ACS")
    ENTITIES = _("rpm ACSes")
    HREF = "rpm_rpm_alternate_content_source_href"
    ID_PREFIX = "acs_rpm_rpm"
    NEEDS_PLUGINS = [PluginRequirement("rpm", specifier=">=3.18.0")]
    CAPABILITIES = {"roles": [PluginRequirement("rpm", specifier=">=3.19.0")]}


class PulpRpmCompsXmlContext(PulpEntityContext):
    UPLOAD_COMPS_ID: ClassVar[str] = "rpm_comps_upload"
    NEEDS_PLUGINS = [PluginRequirement("rpm", specifier=">=3.17.0")]

    def upload_comps(
        self, file: IO[bytes], repo_href: Optional[str], replace: Optional[bool]
    ) -> Any:
        click.echo(_("Uploading file {filename}").format(filename=file.name), err=True)
        file.seek(0)
        return self.call(
            "upload_comps",
            body={"repository": repo_href, "replace": replace, "file": file},
        )


class PulpRpmDistributionContext(PulpDistributionContext):
    PLUGIN = "rpm"
    RESOURCE_TYPE = "rpm"
    ENTITY = _("rpm distribution")
    ENTITIES = _("rpm distributions")
    HREF = "rpm_rpm_distribution_href"
    ID_PREFIX = "distributions_rpm_rpm"
    NEEDS_PLUGINS = [PluginRequirement("rpm", specifier=">=3.9.0")]
    CAPABILITIES = {"roles": [PluginRequirement("rpm", specifier=">=3.19.0")]}

    def preprocess_entity(self, body: EntityDefinition, partial: bool = False) -> EntityDefinition:
        body = super().preprocess_entity(body, partial=partial)
        if self.pulp_ctx.has_plugin(PluginRequirement("core", specifier=">=3.16.0")):
            if "repository" in body and "publication" not in body:
                body["publication"] = None
            if "repository" not in body and "publication" in body:
                body["repository"] = None
        if body.get("generate_repo_config") is False:
            self.pulp_ctx.needs_plugin(
                PluginRequirement(
                    "rpm",
                    specifier=">=3.23.0",
                    feature=_("configuring the generation of the config.repo file"),
                )
            )
        elif self.pulp_ctx.has_plugin(PluginRequirement("rpm", specifier="<3.23.0")):
            body.pop("generate_repo_config", None)
        return body


class PulpRpmPackageContext(PulpContentContext):
    PLUGIN = "rpm"
    RESOURCE_TYPE = "package"
    ENTITY = "rpm package"
    ENTITIES = "rpm packages"
    HREF = "rpm_package_href"
    ID_PREFIX = "content_rpm_packages"
    NEEDS_PLUGINS = [PluginRequirement("rpm", specifier=">=3.9.0")]
    CAPABILITIES = {"upload": []}

    def preprocess_entity(self, body: EntityDefinition, partial: bool = False) -> EntityDefinition:
        body = super().preprocess_entity(body, partial=partial)
        if partial is False:
            if body.get("relative_path") is None:
                self.pulp_ctx.needs_plugin(PluginRequirement("rpm", specifier=">=3.18.0"))
            else:
                PulpException(_("--relative-path must be provided"))
        return body


class PulpRpmAdvisoryContext(PulpContentContext):
    PLUGIN = "rpm"
    RESOURCE_TYPE = "update_record"
    ENTITY = "rpm advisory"
    ENTITIES = "rpm advisories"
    HREF = "rpm_update_record_href"
    ID_PREFIX = "content_rpm_advisories"
    NEEDS_PLUGINS = [PluginRequirement("rpm", specifier=">=3.9.0")]


class PulpRpmDistributionTreeContext(PulpContentContext):
    PLUGIN = "rpm"
    RESOURCE_TYPE = "distribution_tree"
    ENTITY = "rpm distribution tree"
    ENTITIES = "rpm distribution trees"
    HREF = "rpm_distribution_tree_href"
    ID_PREFIX = "content_rpm_distribution_trees"
    NEEDS_PLUGINS = [PluginRequirement("rpm", specifier=">=3.9.0")]


class PulpRpmModulemdDefaultsContext(PulpContentContext):
    PLUGIN = "rpm"
    RESOURCE_TYPE = "modulemd_defaults"
    ENTITY = "rpm modulemd defaults"
    ENTITIES = "rpm modulemd defaults"
    HREF = "rpm_modulemd_defaults_href"
    ID_PREFIX = "content_rpm_modulemd_defaults"
    NEEDS_PLUGINS = [PluginRequirement("rpm", specifier=">=3.9.0")]


class PulpRpmModulemdContext(PulpContentContext):
    PLUGIN = "rpm"
    RESOURCE_TYPE = "modulemd"
    ENTITY = "rpm modulemd"
    ENTITIES = "rpm modulemds"
    HREF = "rpm_modulemd_href"
    ID_PREFIX = "content_rpm_modulemds"
    NEEDS_PLUGINS = [PluginRequirement("rpm", specifier=">=3.9.0")]


class PulpRpmPackageCategoryContext(PulpContentContext):
    PLUGIN = "rpm"
    RESOURCE_TYPE = "package_category"
    ENTITY = "rpm package category"
    ENTITIES = "rpm package categories"
    HREF = "rpm_package_category_href"
    ID_PREFIX = "content_rpm_packagecategories"
    NEEDS_PLUGINS = [PluginRequirement("rpm", specifier=">=3.9.0")]


class PulpRpmPackageEnvironmentContext(PulpContentContext):
    PLUGIN = "rpm"
    RESOURCE_TYPE = "package_environment"
    ENTITY = "rpm package environment"
    ENTITIES = "rpm package environments"
    HREF = "rpm_package_environment_href"
    ID_PREFIX = "content_rpm_packageenvironments"
    NEEDS_PLUGINS = [PluginRequirement("rpm", specifier=">=3.9.0")]


class PulpRpmPackageGroupContext(PulpContentContext):
    PLUGIN = "rpm"
    RESOURCE_TYPE = "package_group"
    ENTITY = "rpm package group"
    ENTITIES = "rpm package groups"
    HREF = "rpm_package_group_href"
    ID_PREFIX = "content_rpm_packagegroups"
    NEEDS_PLUGINS = [PluginRequirement("rpm", specifier=">=3.9.0")]


class PulpRpmPackageLangpacksContext(PulpContentContext):
    PLUGIN = "rpm"
    RESOURCE_TYPE = "package_langpack"
    ENTITY = "rpm package langpack"
    ENTITIES = "rpm package langpacks"
    HREF = "rpm_package_langpacks_href"
    ID_PREFIX = "content_rpm_packagelangpacks"
    NEEDS_PLUGINS = [PluginRequirement("rpm", specifier=">=3.9.0")]


class PulpRpmRepoMetadataFileContext(PulpContentContext):
    PLUGIN = "rpm"
    RESOURCE_TYPE = "repo_metadata_file"
    ENTITY = "rpm repo metadata file"
    ENTITIES = "rpm repo metadata files"
    HREF = "rpm_repo_metadata_file_href"
    ID_PREFIX = "content_rpm_repo_metadata_files"
    NEEDS_PLUGINS = [PluginRequirement("rpm", specifier=">=3.9.0")]


class PulpRpmPublicationContext(PulpPublicationContext):
    PLUGIN = "rpm"
    RESOURCE_TYPE = "rpm"
    ENTITY = _("rpm publication")
    ENTITIES = _("rpm publications")
    HREF = "rpm_rpm_publication_href"
    ID_PREFIX = "publications_rpm_rpm"
    NEEDS_PLUGINS = [PluginRequirement("rpm", specifier=">=3.9.0")]
    CAPABILITIES = {"roles": [PluginRequirement("rpm", specifier=">=3.19.0")]}

    def preprocess_entity(self, body: EntityDefinition, partial: bool = False) -> EntityDefinition:
        body = super().preprocess_entity(body, partial=partial)
        version = body.pop("version", None)
        if version is not None:
            repository_href = body.pop("repository")
            body["repository_version"] = f"{repository_href}versions/{version}/"
        if "repo_config" in body:
            self.pulp_ctx.needs_plugin(
                PluginRequirement(
                    "rpm",
                    specifier=">=3.24.0",
                    feature=_("customization of the config.repo file"),
                )
            )
        return body


class PulpRpmRemoteContext(PulpRemoteContext):
    PLUGIN = "rpm"
    RESOURCE_TYPE = "rpm"
    ENTITY = _("rpm remote")
    ENTITIES = _("rpm remotes")
    HREF = "rpm_rpm_remote_href"
    ID_PREFIX = "remotes_rpm_rpm"
    NULLABLES = {
        "ca_cert",
        "client_cert",
        "client_key",
        "username",
        "password",
        "proxy_url",
        "proxy_username",
        "proxy_password",
        "sles_auth_token",
    }
    NEEDS_PLUGINS = [PluginRequirement("rpm", specifier=">=3.9.0")]
    CAPABILITIES = {"roles": [PluginRequirement("rpm", specifier=">=3.19.0")]}


class PulpUlnRemoteContext(PulpRemoteContext):
    PLUGIN = "rpm"
    RESOURCE_TYPE = "uln"
    ENTITY = _("uln remote")
    ENTITIES = _("uln remotes")
    HREF = "rpm_uln_remote_href"
    ID_PREFIX = "remotes_rpm_uln"
    NULLABLES = PulpRemoteContext.NULLABLES | {"uln-server-base-url"}
    NEEDS_PLUGINS = [PluginRequirement("rpm", specifier=">=3.12.0")]
    CAPABILITIES = {"roles": [PluginRequirement("rpm", specifier=">=3.19.0")]}


class PulpRpmRepositoryVersionContext(PulpRepositoryVersionContext):
    HREF = "rpm_rpm_repository_version_href"
    ID_PREFIX = "repositories_rpm_rpm_versions"
    NEEDS_PLUGINS = [PluginRequirement("rpm", specifier=">=3.9.0")]


class PulpRpmRepositoryContext(PulpRepositoryContext):
    PLUGIN = "rpm"
    RESOURCE_TYPE = "rpm"
    HREF = "rpm_rpm_repository_href"
    ID_PREFIX = "repositories_rpm_rpm"
    ENTITY = _("rpm repository")
    ENTITIES = _("rpm repositories")
    VERSION_CONTEXT = PulpRpmRepositoryVersionContext
    CAPABILITIES = {
        "sync": [],
        "pulpexport": [],
        "roles": [PluginRequirement("rpm", specifier=">=3.19.0")],
    }
    NEEDS_PLUGINS = [PluginRequirement("rpm", specifier=">=3.9.0")]

    def preprocess_entity(self, body: EntityDefinition, partial: bool = False) -> EntityDefinition:
        body = super().preprocess_entity(body, partial=partial)
        if "autopublish" in body:
            self.pulp_ctx.needs_plugin(PluginRequirement("rpm", specifier=">=3.12.0"))
        if "repo_config" in body:
            self.pulp_ctx.needs_plugin(
                PluginRequirement(
                    "rpm",
                    specifier=">=3.24.0",
                    feature=_("customization of the config.repo file"),
                )
            )
        return body

    def sync(self, href: Optional[str] = None, body: Optional[EntityDefinition] = None) -> Any:
        if body:
            if body.get("optimize") is not None:
                self.pulp_ctx.needs_plugin(PluginRequirement("rpm", specifier=">=3.3.0"))
            if body.get("sync_policy") is not None:
                self.pulp_ctx.needs_plugin(PluginRequirement("rpm", specifier=">=3.16.0"))
            if "treeinfo" in body.get("skip_types", ""):
                self.pulp_ctx.needs_plugin(
                    PluginRequirement("rpm", specifier=">=3.18.10", feature="--skip-type treeinfo")
                )

        return super().sync(href, body)
