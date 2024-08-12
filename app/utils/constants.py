from enum import Enum


class APIResponses(Enum):
    SUCCESS = "SUCCESS"
    FAIL = "FAILED"


class WorkFlows(Enum):
    pnl = "PNL"
    balance_sheet = "BALANCE_SHEET"
    contracts = "CONTRACTS"


class DocumentActivityStage(Enum):
    NEW = "NEW"
    EXTRACTION = "EXTRACTION"
    DONE = "DONE"


class DocumentActivityStatus(Enum):
    NEW = "NEW"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"


class DocumentCategory(Enum):
    FINANCIAL_STATEMENT = "FINANCIAL_STATEMENT"
    CONTRACTS = "CONTRACTS"


class ReportTypes(Enum):
    PNL = "PNL"
    BALANCE_SHEET = "BALANCE_SHEET"
    CHART_OF_ACCOUNTS = "CHART_OF_ACCOUNTS"
    TRAIL_BALANCE = "TRAIL_BALANCE"
    GENERAL_LEDGER = "GENERAL_LEDGER"
    CONTRACTS = "CONTRACTS"

