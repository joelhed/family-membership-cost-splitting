# family-membership-cost-splitting

This is a program that calculates how to split the costs of any collective membership/subscription fee fairly.

One person, the Payer, pays for one period of family membership.
The cost for every day of membership is shared equally across all family members at that date.
When a new family member joins, they pay for their part of the rest of the year to the Payer. 
You cannot stop being a member until the end of the family membership.

At the end of the membership period, the Payer will have some surplus money, given that new family members joined within the year, and some people will be owed money they already paid, thinking that the bill would be split between fewer people.

By supplying the program with the names and dates where membership started, as well as the price and length of the family membership, you will get reports for every member of how much the person should pay when becoming a member, and how much they owe or are owed at the end of the year.

## TODO

- [ ] Make an interface for creating family memberships
  - [ ] Include global vars in the model
  - [ ] Create json serialization/deserialization functions
