# API/models/schemas.py
from pydantic import BaseModel, Field
from enum import Enum

# Enum pour limiter les choix de `loan_type`
#class LoanTypeEnum(str, Enum):
#    short_term = "short_term"
#    long_term = "long_term"
#    microcredit = "microcredit"

# Enum pour `New_versus_Repeat`
#class NewRepeatEnum(str, Enum):
#    new = "new"
#    repeat = "repeat"

#class LoanProfile(BaseModel):
    #Total_Amount: float = Field(gt=0, description="Montant initial du prêt (>0)")
    #Total_Amount_to_Repay: float = Field(gt=0)
    #Amount_Funded_By_Lender: float = Field(ge=0)
    #duration: int = Field(gt=0, le=60, description="Durée en mois (max 60)")
    #Lender_portion_to_be_repaid: float = Field(ge=0)
    #loan_type: LoanTypeEnum
    #New_versus_Repeat: NewRepeatEnum
