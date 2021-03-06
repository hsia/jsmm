#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import commons

if __name__ == "__main__":
    print("Starting...")
    import tornado_utils
    from handlers import *
    from member_importer import import_info

    tornado_utils.registered_handlers += [
        (r'/members/upload/?', member_upload.UploadHandler, dict(callback=import_info))
        , (r'/image/upload/?', member_image.UploadImage, dict(callback=member_image.imageCallBack))
        # ,(r'/doc/upload/?', member_doc.UploadDoc, dict(callback=member_doc.docCallBack))
    ]
    tornado_utils.serve(2063, debug=True)
