# -*- coding: UTF-8 -*-

if __name__ == '__main__' :

    from importlib import reload
    from app import app_qt
    app_qt = reload(app_qt)
    app_qt.main()