from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from finam_rest_py.models.account_models.position import Position
from finam_rest_py.models.converters import formatted_datetime
from finam_rest_py.models.money import MoneyModel


@dataclass
class Account:
    account_id: str
    type: str
    status: str
    equity: float
    unrealized_profit: float
    positions: list[Position]
    cash: list[MoneyModel]

    portfolio_mc_available_cash: float
    portfolio_mc_initial_margin: float
    portfolio_mc_maintenance_margin: float

    portfolio_mct: Optional[str]

    portfolio_forts_available_cash: Optional[float]
    portfolio_forts_money_reserved: Optional[float]

    open_account_date: Optional[datetime]
    first_trade_date: Optional[datetime]
    first_non_trade_date: Optional[datetime]

    @classmethod
    def from_dict(cls, account_dict: dict) -> Account:
        return Account(
            account_id=str(account_dict['account_id']) if 'account_id' in account_dict.keys()
            else str(account_dict['accountId']),
            type=str(account_dict['type']),
            status=str(account_dict['status']),
            equity=float(account_dict['equity']['value']),
            unrealized_profit=float(account_dict['unrealized_profit']['value']) if 'unrealized_profit' in account_dict.keys()
            else float(account_dict['unrealizedProfit']['value']),
            positions=[Position.from_dict(p) for p in account_dict['positions']],
            cash=[MoneyModel.from_dict(c) for c in account_dict['cash']],
            portfolio_mc_available_cash=float(account_dict['portfolio_mc']['available_cash']['value'])
            if 'portfolio_mc' in account_dict.keys()
            else float(account_dict['portfolioMc']['availableCash']['value']),
            portfolio_mc_initial_margin=float(account_dict['portfolio_mc']['initial_margin']['value'])
            if 'portfolio_mc' in account_dict.keys()
            else float(account_dict['portfolioMc']['initialMargin']['value']),
            portfolio_mc_maintenance_margin=float(account_dict['portfolio_mc']['maintenance_margin']['value'])
            if 'portfolio_mc' in account_dict.keys()
            else float(account_dict['portfolioMc']['maintenanceMargin']['value']),
            portfolio_mct=account_dict.get('portfolio_mct', account_dict.get('portfolioMct', None)),
            portfolio_forts_available_cash=account_dict['portfolio_forts']['available_cash']
            if 'portfolio_forts' in account_dict.keys() else account_dict['portfolioForts']['availableCash']
            if 'portfolioForts' in account_dict.keys() else None,
            portfolio_forts_money_reserved=account_dict['portfolio_forts']['money_reserved']
            if 'portfolio_forts' in account_dict.keys() else account_dict['portfolioForts']['moneyReserved']
            if 'portfolioForts' in account_dict.keys() else None,
            open_account_date=formatted_datetime(account_dict['open_account_date'])
            if 'open_account_date' in account_dict.keys() else formatted_datetime(account_dict['openAccountDate'])
            if 'openAccountDate' in account_dict.keys() else None,
            first_trade_date=formatted_datetime(account_dict['first_trade_date'])
            if 'first_trade_date' in account_dict.keys() else formatted_datetime(account_dict['firstTradeDate'])
            if 'firstTradeDate' in account_dict.keys() else None,
            first_non_trade_date=formatted_datetime(account_dict['first_non_trade_date'])
            if 'first_non_trade_date' in account_dict.keys() else formatted_datetime(account_dict['firstNonTradeDate'])
            if 'firstNonTradeDate' in account_dict.keys() else None,
        )
