"""
Upwork API Automation Toolkit for Freelancers.

This Python package helps Upwork freelancers automate their daily workflows using the official
Upwork API. It is designed to boost efficiency and reduce manual effort by providing programmable
access to common tasks and events on the platform.

Features:
- Fetch and display public reviews from your Upwork profile for your personal portfolio
- Set up real-time alerts for:
  - New messages from clients with active contracts
  - Invitations to interview
  - General inbox messages
- Periodically scan job posts using custom filter logic and notify you with relevant links
- Retrieve and monitor personal data such as:
  - Earnings
  - Work diary
- Automate common actions via the command line

Whether you're an experienced freelancer or just starting out, this tool helps you stay responsive,
informed, and efficient — all while remaining compliant with Upwork’s terms of service.
"""

from upwork_cli.utils import __version__

__all__ = ['__version__']
