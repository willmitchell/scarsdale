# Scarsdale: A Smart Contract Synopsis Language

![Build Status](https://travis-ci.org/willmitchell/scarsdale.svg?branch=master "Build Status")

# Synopsis

- who: Will Mitchell
- what: A YAML based language for summarizing Smart Contracts as well as regular Contracts IRL
- where: https://github.com/willmitchell/scarsdale
- when: Created December 2017 
- how: Python 3, various libraries
- why: I want to build a bridge between cryptos and new online services that deliver business value, privacy, and security

# Introduction

The goal is to be able to model the most important facets of arbitrary business relationships.  We achieve this by combining a well known conceptual framework with a fairly simple file-based modeling technique.

The conceptual framework is based on the [Six W's](https://en.wikipedia.org/wiki/Five_Ws).  This general approach has been used in journalism for many years.

The reason why the framework has relevance to journalism is the same reason why we want to use it for describing contracts.  People need to be able to review contracts *with the same mindset and time frame* that they use when they read a newspaper.  In this sense, summary level information is important.  Predictable conventions for presenting information in a hierarchal manner are essential to readers and participants.

Contracts and newspaper articles are alike, in that the *who, what, where, when, why, and how* of each should be briefly stated.

The Scarsdale library provides a way to model, validate, and present contracts.  Goals:

- simplicity of modeling approach
- value breadth of applicability over depth in any specific problem domain
- support contract rendering and visualization
- support higher level analysis and modeling

# Example 1: Simple

In the example below, we have a kid in a candy store.  This is obviously a real world scenario.

```
contract:                            # Note 1: All contracts begin with a 'contract' node
    who:                             # Note 2: 'who' is an optional (but important) section within any contract
        kid:                         # Note 3: parties to a contract have unique names within the contract
            wants:                   # Note 4: parties to a contract generally want something
                - /what/food/candy   # Note 5: /what/food/candy can be used from other contracts like a URL
            has:
                - /what/money
        candystore:
            wants:
                - /what/money
            has:
                - /what/food/candy
```

# Example 2: Smart Contract for Third Party Identity Services

With Scarsdale, we can use the same notation for capturing the highlights of a Smart Contract as well.  In the example below, a subscriber wants to purchase third party identity services from a seller.  Note the following:

- who, what, where, and when are treated in the contract synopsis
- the state is party to the contract, as they have real world identification requirements
- the resulting identity could be used to provide a minimum-age assertion that might be required within the context of a purchase of alcohol (at least in the USA).

```
contract:
  who:
    subscriber:
      roles:
        - /who/roles/subscriber
        - /who/roles/buyer
      has:
        - /what/money
      wants:
        - /what/services/identity

    seller:
      roles:
        - /who/roles/seller
        - /who/roles/identity/authenticator
      wants:
        - /what/money
        - /what/legal/compliance
      has:
        - /what/internet/website
        - /what/identity/types/clear
        - /what/license/state/identity_services
        - /what/services/identity

    state:
      roles:
        - /what/authority/state

      wants:
        - /what/money
        - /what/legal/compliance
      has:
        - /what/identity/types/clear
        - /what/authority/state

  what:
    summary: /who/subscriber purchases a subscription for state-sanctioned identity services from /who/seller.

    categories:
      - /what/authority/state
      - /what/services/identity

  where:
    jurisdiction: /where/jurisdictions/state

    who:
      subscriber:
        - /where/places/types/addressable

      seller:
        - /where/places/types/addressable

  when:
    -
      name: purchase
      who:
        -
          name: subscriber
          actions:
            - /when/actions/choose
            - /when/actions/checkout
            - /when/actions/payment/pay
        -
          name: seller
          actions:
            - /when/actions/payment/accept

    -
      name: performance
      who:
        -
          name: subscriber
          actions:
            - /when/actions/identity/respond
            - /when/actions/identity/delegate
        -
          name: seller
          actions:
            - /when/actions/identity/handle
            - /when/actions/identity/validate
            - /when/actions/identity/minimize
            - /when/actions/identity/prove
            - /when/actions/identity/audit

```

# Status

This project is in the alpha stage.  If you would like to participate, please ping will.mitchell@app3.com or submit a PR, etc.  Thanks.

# Want to learn more?

Documentation is a work in progress.  More details can be found [here](https://github.com/willmitchell/scarsdale/blob/master/docs/index.md).

