#!/usr/bin/python
# -*- coding: utf-8 -*-
from bot import ReportBot
import sys


# Entry Point
if __name__ == '__main__':
    bot = ReportBot(sys.argv[1] if len(sys.argv) > 1 else None)
    print(bot.post())
