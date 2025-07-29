class Helpers:
    @staticmethod
    def isIterable(obj):
        if isinstance(obj, str):
            return False
        try:
            iter(obj)
            obj[0]
            return True
        except Exception:
            return False