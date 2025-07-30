from functools import cached_property
from typing import Optional, Literal, Any, Union, Callable

from pydantic import BaseModel, Field, model_validator

from ipf_dynamic_attributes.configs.rules import InventoryRule, DefaultRule, ConfigRule, Rule, DefaultConfigRule


class IPFabric(BaseModel):
    base_url: Optional[str] = Field(
        None,
        description="The IP Fabric Base URL to fetch data from (env: 'IPF_URL').",
        title="IP Fabric URL",
        examples=["https://demo.ipfabric.com"],
    )
    auth: Optional[str] = Field(
        None,
        description="The IP Fabric API token to use for authentication (env: 'IPF_TOKEN'). "
        "Username and password can be used by setting Environment Variables (IPF_USERNAME, IPF_PASSWORD).",
        title="IP Fabric API Token",
    )
    timeout: Optional[Union[int, tuple, float, None]] = Field(
        5,
        description="The timeout for the API requests; default 5 seconds (env: 'IPF_TIMEOUT').",
        title="IP Fabric Timeout",
    )
    verify: Union[bool, str] = Field(
        True, description="Verify SSL Certificates; default True (env: 'IPF_VERIFY').", title="SSL Verification"
    )
    snapshot_id: str = Field(
        "$last",
        description="The snapshot ID to use for the API endpoint; defaults to '$last'.",
        title="Snapshot ID",
        examples=["$last", "$prev", "$lastLocked", "d03a89d3-911b-4e2d-868b-8b8103771801"],
    )


class Config(BaseModel):
    ipfabric: Optional[IPFabric] = Field(
        default_factory=IPFabric, description="IP Fabric connection configuration.", title="IP Fabric Connection"
    )
    dry_run: bool = Field(
        True, description="Defaults to run in dry-run mode and not apply any updates.", title="Dry Run"
    )
    overwrite: bool = Field(
        False,
        description="Overwrite existing Global Attribute values; default False.",
        title="Overwrite Global Attribute",
    )
    update_snapshot: bool = Field(
        True,
        description="Update Local Attributes on the selected snapshot; default True.",
        title="Update Snapshot Attributes",
    )
    inventory: InventoryRule = Field(
        default_factory=InventoryRule,
        description="Optional: Filters to limit the inventory of devices based on Inventory > Devices table.",
        title="Inventory Filters",
    )
    default: Optional[DefaultRule] = Field(
        None,
        description="Optional: Default configuration to merge into all other Table Rules.",
        title="Default Table Rule",
    )
    default_config: Optional[DefaultConfigRule] = Field(
        None,
        description="Optional: Default configuration to merge into all other Configuration Rules.",
        title="Default Configuration Rule",
    )
    rules: list[Union[ConfigRule, Rule]] = Field(
        description="List of Table or Configuration Rules which are processed in order; at least 1 rule is required.",
        title="Dynamic Attribute Rules",
    )

    @model_validator(mode="after")
    def _validate(self):
        if not self.rules:
            raise ValueError("At least one rule must be provided.")
        if len({_.name for _ in self.rules}) != len(self.rules):
            raise ValueError("Duplicate Rule Names found.")
        if False in {bool(_.value) for _ in self.rules} and not self.default.value:
            raise ValueError("All Rules must have a value set or 'default[value]' can be used for Table Rules.")
        if False in {bool(_.attribute) for _ in self.rules if isinstance(_, Rule)} and not self.default.attribute:
            raise ValueError(
                "An Attribute Name must be set in 'default[attribute]' or all Table rules must have it defined."
            )
        if (
            False in {bool(_.attribute) for _ in self.rules if isinstance(_, ConfigRule)}
            and not self.default_config.attribute
        ):
            raise ValueError(
                "An Attribute Name must be set in 'default_config[attribute]' "
                "or all Configuration Rules must have it defined."
            )
        return self

    @cached_property
    def merged_rules(self) -> list[Union[ConfigRule, Rule]]:
        """Copy Defaults to rules"""
        return [
            rule.merge_default(self.default if isinstance(rule, Rule) else self.default_config) for rule in self.rules
        ]

    def model_dump_merged(
        self,
        *,
        mode: Literal["json", "python"] = "python",
        context: Optional[Any] = None,
        by_alias: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: Union[bool, Literal["none", "warn", "error"]] = True,
        fallback: Optional[Callable[[Any], Any]] = None,
        serialize_as_any: bool = False,
    ) -> dict[str, Any]:
        """Dump the full config with all default rules merged."""
        config = self.model_copy(deep=True)
        config.rules = self.merged_rules
        return config.model_dump(
            mode=mode,
            exclude={"default", "default_config"},
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            fallback=fallback,
            serialize_as_any=serialize_as_any,
        )
