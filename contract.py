"""
CSC148, Winter 2025
Assignment 1

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2025 Bogdan Simion, Diane Horton, Jacqueline Smith
"""
import datetime
from math import ceil
from typing import Optional
from bill import Bill
from call import Call


# Constants for the month-to-month contract monthly fee and term deposit
MTM_MONTHLY_FEE = 50.00
TERM_MONTHLY_FEE = 20.00
TERM_DEPOSIT = 300.00

# Constants for the included minutes and SMSs in the term contracts (per month)
TERM_MINS = 100

# Cost per minute and per SMS in the month-to-month contract
MTM_MINS_COST = 0.05

# Cost per minute and per SMS in the term contract
TERM_MINS_COST = 0.1

# Cost per minute and per SMS in the prepaid contract
PREPAID_MINS_COST = 0.025


class Contract:
    """ A contract for a phone line

    This is an abstract class and should not be directly instantiated.

    Only subclasses should be instantiated.

    === Public Attributes ===
    start:
         starting date for the contract
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
    """
    start: datetime.date
    bill: Optional[Bill]

    def __init__(self, start: datetime.date) -> None:
        """ Create a new Contract with the <start> date, starts as inactive
        """
        self.start = start
        self.bill = None

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.

        DO NOT CHANGE THIS METHOD
        """
        raise NotImplementedError

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        self.start = None
        return self.bill.get_cost()


class TermContract (Contract):
    """
        A Term based contract for a phoneline
    === Public Attributes ===
    start:
         Same as parent class
    bill:
         Same as parent class
    current:
         tracks the current month every time new month is called
    end:
         end date for the contract

    """
    current: datetime.date
    end: datetime.date

    def __init__(self, start: datetime.date, end: datetime.date) -> None:
        Contract.__init__(self, start)
        self.end = end
        self.current = start

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.

        """
        self.bill = bill
        bill.free_min = 0
        if self.start.month == month and self.start.year == year:
            bill.add_fixed_cost(TERM_DEPOSIT)
        bill.set_rates('TERM', TERM_MINS_COST)
        bill.add_fixed_cost(TERM_MONTHLY_FEE)
        self.current = datetime.date(year, month, 1)

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill, properly handling free minutes. """

        call_time = ceil(call.duration / 60.0)
        excess = call_time - (TERM_MINS - self.bill.free_min)

        if (self.bill.free_min + call_time) < TERM_MINS:
            self.bill.free_min += call_time
        elif (self.bill.free_min - TERM_MINS) != 0:
            self.bill.free_min += call_time - excess
            self.bill.add_free_minutes(self.bill.free_min)
            self.bill.add_billed_minutes(excess)
        else:
            self.bill.add_billed_minutes(excess)

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        if self.end <= self.current:
            return 0.0
        else:
            return TERM_DEPOSIT - TERM_MONTHLY_FEE


class MTMContract(Contract):
    """
    A month-to-month contract for a phoneline
    === Public Attributes ===
    start:
         Same as parent class
    bill:
         Same as parent class
    """
    def __init__(self, start: datetime.datetime) -> None:
        Contract.__init__(self, start)

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.

        """
        self.bill = bill
        bill.set_rates('MTM', MTM_MINS_COST)
        bill.add_fixed_cost(MTM_MONTHLY_FEE)


class PrepaidContract(Contract):
    """
        A prepaid contract for a phoneline
        === Public Attributes ===
        start:
             Same as parent class
        bill:
             Same as parent class
    """
    balance: int

    def __init__(self, start: datetime.datetime, balance: int) -> None:
        Contract.__init__(self, start)
        self.balance = -balance

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.

        """
        self.bill = bill
        bill.add_fixed_cost(self.balance)

        if self.balance > -10:
            self.balance -= 25
            bill.add_fixed_cost(25)
        bill.set_rates('PREPAID', PREPAID_MINS_COST)

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        self.balance += ((ceil(call.duration / 60.0)) * PREPAID_MINS_COST)
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """

        if self.balance <= 0:
            return 0.0
        else:
            return self.balance


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'datetime', 'bill', 'call', 'math'
        ],
        'disable': ['R0902', 'R0913'],
        'generated-members': 'pygame.*'
    })
