PyConZA Funding application form
================================

Intended to integrate with `wafer`_.

.. _wafer: https://github.com/CTPUG/wafer

About
=====

This is a funding application that can be used with wafer. It is fairly minimal
and specific to how PyCon ZA handles funding, but can be adapted for other
conferences.

This is intended to automate the data related parts of the application - gathering
budgets, making offers and recording delegates decisions on whether to accept funding
offers. It is not intended to handle the decision making process, nor does it handle
the communictation between applicants and the funding committee.

Installing
==========

This is not a standalone application, but intended to extend wafer.

1. Add pyconza-funding to the requirements.txt file of the conference application.
2. Add ``pyconza.funding`` to the ``INSTALLED_APPS`` of your site, before any of the ``wafer`` applications.
3. Add ``pyconza.funding.urls`` to the ``urls.py`` of your site. By default, funding lives under ``/funding/`` .
