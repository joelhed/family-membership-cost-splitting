from collections import defaultdict
from itertools import tee
from typing import Tuple, List, Dict, NamedTuple
import datetime as dt




# One person, the Payer, pays for one year of family membership.

# The cost for every day of membership is shared equally across all family members at that date.
# When a new family member joins, they pay for their part of the rest of the year to the Payer. 
# At the end of the year, the Payer will have some surplus money,
# given that new family members joined within the year.
# You cannot stop being a member until the end of the family membership.

# The model of this program includes every family member and the date they joined, and
# calculates what payments every person should have made and received for the entire year,
# and in the end, what they owe and are owed.

CURRENCY = "kr"
FAMILY_MEMBERSHIP_PRICE = 350
FAMILY_MEMBERSHIP_DURATION = dt.timedelta(days=365)


FamilyMember = Tuple[str, dt.date]


class Period(NamedTuple):
    start: dt.date
    last: dt.date
    days: int
    num_members: int
    cost_per_member: float
    members: List[str]


class Family:

    def __init__(self, payer, members):
        self.payer: str = payer
        # Make sure that the payer is at the top of the list!!!!
        self.members: List[FamilyMember] = sorted(members, key=lambda member: member[1])

    def calculate_costs(self):
        # in the end, i want to see all price periods, their durations in days, the members in each period, price
        # per member for the period and the cost for every member of the period.
        # the results here should be able to be printed, and used in calculate_events
        member_names_at_date = defaultdict(list)
        i = 0
        while i < len(self.members):
            date = self.members[i][1]
            while (i + 1 < len(self.members)) and date == self.members[i+1][1]:
                i += 1

            member_names_at_date[date] = [name for name, date in self.members[:i+1]]
            i += 1

        dates = sorted(member_names_at_date.keys())
        dates.append(dates[0] + FAMILY_MEMBERSHIP_DURATION)
        assert (dates[-2] < dates[-1] if len(dates) > 1 else True), "last new member is past past the family membership end."

        periods = []
        for period_start, period_end in pairwise(dates):
            # period_end  is up until but not including
            days = (period_end - period_start).days
            members = member_names_at_date[period_start]
            num_members = len(members)
            price_per_member = (
                FAMILY_MEMBERSHIP_PRICE
                / FAMILY_MEMBERSHIP_DURATION.days
                / num_members
            )
            cost_per_member = days * price_per_member 

            periods.append(Period(
                period_start,
                period_end - dt.timedelta(days=1),
                days,
                num_members,
                cost_per_member, #cost_per_member,
                members,
            ))

        return periods

    def calculate_events(self) -> Dict[str, List[Tuple[dt.date, str, float]]]:
        events = defaultdict(list)

        start_date = None
        end_date = None
        num_members = 0
        for name, date in self.members:
            if name == self.payer:
                start_date = date
                end_date = start_date + FAMILY_MEMBERSHIP_DURATION
                days = (end_date - date).days
                num_members += 1

                events[name].append((date, f"Payed Nintendo for {days} days membership", FAMILY_MEMBERSHIP_PRICE))
            else:
                num_members += 1
                days = (end_date - date).days
                price = (
                    days
                    * FAMILY_MEMBERSHIP_PRICE
                    / FAMILY_MEMBERSHIP_DURATION.days
                    / num_members
                )
                num_members
                events[name].append((date, f"Payed {self.payer} for {days} days membership", price))
                events[self.payer].append((date, f"Received from {name}", -price))

        return events


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def transform_family_members_date(members: List[Tuple[str, str]]) -> List[FamilyMember]:
    return [(name, dt.date.fromisoformat(date)) for name, date in members]


def print_events(events):
    for name in events:
        print(name)
        for date, event_text, amount in events[name]:
            print(f"{date.isoformat()} {event_text:50}  {amount:.2f}")

        print()


def print_costs(periods):
    cost_per_person = defaultdict(int)
    for period in periods:
        print(f"{period.start.isoformat()} - {period.last.isoformat()}: {period.days:3} days, {period.num_members} members, {period.cost_per_member:.2f} {CURRENCY} per member")
        print("Members: ", ", ".join(period.members))
        print()


def print_individual_reports(family):
    periods = family.calculate_costs()
    events = family.calculate_events()
    
    for name, start_date in family.members:
        print(name)
        print("=" * 15)
        # print actual costs (i.e. the periods where the person was a member)
        costs = 0.0
        print("Costs:")
        print(f"{'Period':23}  Days  Members  Cost/member  {'Sum':>7}")
        for period in periods:
            if period.last < start_date:
                continue

            costs += period.cost_per_member
            print(f"{period.start.isoformat()} - {period.last.isoformat()}  "
                  f"{period.days:4}  "
                  f"{period.num_members:7}  "
                  f"{period.cost_per_member:11.2f}  "
                  f"{costs:7.2f}")

        print()

        balance = 0.0
        print("Events:")
        print(f"{'Date':10}  {'Event':40}  {'Amount':>7}  Balance")
        for date, event_text, amount in events[name]:
            balance += amount
            print(f"{date.isoformat()}  {event_text:40}  {amount:7.2f}  {balance:7.2f}")


        print()

        debt = costs - balance
        if debt < 0:
            print(f"{name} is owed: {abs(debt):.2f} {CURRENCY}")
        else:
            print(f"{name} owes: {abs(debt):.2f} {CURRENCY}")



        # print events and running sum
        # diff between costs and events.
        # if positive, you are owed that amount, if negative, you owe that amount

        print()


if __name__ == "__main__":
    family = Family("Joel", transform_family_members_date([
        ("Joel", "2022-09-13"),
        ("Humla", "2022-09-13"),
        ("Sophie", "2023-02-15"),
        ("Olle", "2023-04-23"),
    ]))
    print(family.members)
    #print_events(family.calculate_events())
    print_costs(family.calculate_costs())

    print_individual_reports(family)
