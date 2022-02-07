"""
원하는 클래스를 Singleton 패턴으로 바꾸기 위한 상속 클래스

LAST_UPDATE : 2021/11/08
AUTHOR      : SHY
"""

# Globals
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
TOTAL_SINGLETON_INSTANCE_COUNT  = 0
MAX_SINGLETON_INSTANCE_COUNT    = 0

# Singleton Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
class Singleton(object):
    _instance       = None
    _className      = ""
    _callCount      = 0
    def __new__(class_, *args, **kwargs):
        global TOTAL_SINGLETON_INSTANCE_COUNT, MAX_SINGLETON_INSTANCE_COUNT

        if not isinstance(class_._instance, class_):
            TOTAL_SINGLETON_INSTANCE_COUNT  += 1
            MAX_SINGLETON_INSTANCE_COUNT    += 1

            class_._instance                = object.__new__(class_)
            class_._className               = class_.__name__

        class_._callCount += 1
        return class_._instance

    def __del__(class_):
        class_.closeResult()

    def closeResult(class_):
        global TOTAL_SINGLETON_INSTANCE_COUNT
        if MAX_SINGLETON_INSTANCE_COUNT == TOTAL_SINGLETON_INSTANCE_COUNT:
            print('* Destroy Program & Instance Start')
            print('---------------------------------------------------------')

        TOTAL_SINGLETON_INSTANCE_COUNT -= 1
        print(f'- {class_._className:20} > Close Done [ CallCount {class_._callCount:2} ]')

        if TOTAL_SINGLETON_INSTANCE_COUNT == 0:
            print('---------------------------------------------------------')
            print('* All Program & Instance Close Done\n')

