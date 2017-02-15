#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import commons
if __name__ == "__main__":
    print("Starting...")
    import tornado_utils
    import handlers.jsmm
    tornado_utils.serve(2063, debug=True)
