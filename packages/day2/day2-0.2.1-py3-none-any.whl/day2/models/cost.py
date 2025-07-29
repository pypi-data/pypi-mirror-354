import re
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field, root_validator


# Utility function to convert camelCase or PascalCase to snake_case
def to_snake_case(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


class GetCostByChargeTypeOutput(BaseModel):
    """Details of cost breakdown by charge type."""

    total_cost: Optional[float] = Field(None, alias="TotalCost")
    usage: Optional[float] = Field(None, alias="Usage")
    bundled_discount: Optional[float] = Field(None, alias="BundledDiscount")
    credit: Optional[float] = Field(None, alias="Credit")
    discount: Optional[float] = Field(None, alias="Discount")
    discounted_usage: Optional[float] = Field(None, alias="DiscountedUsage")
    fee: Optional[float] = Field(None, alias="Fee")
    refund: Optional[float] = Field(None, alias="Refund")
    ri_fee: Optional[float] = Field(None, alias="RIFee")
    tax: Optional[float] = Field(None, alias="Tax")
    savings_plan_upfront_fee: Optional[float] = Field(
        None, alias="SavingsPlanUpfrontFee"
    )
    savings_plan_recurring_fee: Optional[float] = Field(
        None, alias="SavingsPlanRecurringFee"
    )
    savings_plan_covered_usage: Optional[float] = Field(
        None, alias="SavingsPlanCoveredUsage"
    )
    savings_plan_negation: Optional[float] = Field(None, alias="SavingsPlanNegation")
    spp_discount: Optional[float] = Field(None, alias="SPPDiscount")
    distributor_discount: Optional[float] = Field(None, alias="DistributorDiscount")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")

    @root_validator(pre=True)
    @classmethod
    def handle_dynamic_extra_fields(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Handle dynamic extra fields by converting them to snake_case."""
        known_fields = {
            field.alias or field_name for field_name, field in cls.model_fields.items()
        }
        # Dynamically handle all extra fields
        for key in list(values.keys()):
            if key not in known_fields:
                # Convert the extra field to snake_case and map it
                snake_case_key = to_snake_case(key)
                values[snake_case_key] = values.pop(key)
        return values
