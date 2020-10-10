PyConZA Funding application form
================================

Intended to integrate with `wafer`_.

.. _wafer: https://github.com/CTPUG/wafer

|funding-ci-badge|

.. |funding-ci-badge| image:: https://travis-ci.org/CTPUG/pyconza-funding.svg?branch=master
    :alt: Travis CI build status
    :scale: 100%
    :target: https://travis-ci.org/CTPUG/pyconza-funding

About
=====

This is a funding application that can be used with wafer. It is fairly minimal
and specific to how PyCon ZA handles funding, but can be adapted for other
conferences.

This is intended to automate the data related parts of the application - gathering
budgets, making offers and recording delegate's decisions on whether to accept funding
offers. It is not intended to handle the decision making process, nor does it handle
the communication between applicants and the funding committee.

Installing
==========

This is not a standalone application, but intended to extend wafer.

1. Add pyconza-funding to the requirements.txt file of the conference application.
2. Add ``pyconza.funding`` to the ``INSTALLED_APPS`` of your site, before any of the ``wafer`` applications.
3. Add ``pyconza.funding.urls`` to the ``urls.py`` of your site. By default, funding lives under ``/funding/`` .


Intended Workflow
=================

When an applicant creates their application, it is in the 'Submitted' state. The funding committee
is responsible for changing the state to 'Under Consideration', to indicate that they've acknowledged
the application. If there are any questions that need to be addressed, the committee should
communicate with the applicant and resolve them. During this period, the applicant is free
to edit the application (to tweak figures, expand on motivation, etc.). They can also cancel
the application at this point,

Once the funding commitee is happy with the application, the status should be set to 'Final Review'.
If, after review, the decision is to not award the funding, the application should be set to
'Funding not granted', otherwise an offer should be specified and the status set to 'Request Granted'.

While the status of the application will be updated, the applicant should also be informed
of the decision by whatever communication channel the funding committee is using to communicate.

The applicant must then decide whether or not to accept the offer on the site, and the application
status will be updated to reflect that decision.
