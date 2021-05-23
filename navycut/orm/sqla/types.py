from sqlalchemy.types import TypeDecorator, String

class ImageType(TypeDecorator):
    """
    Custom sqlalchemy type to store image.
    """
    impl = String
    
    cache_ok = True
    
    def process_bind_param(self, value, dialect):
        try: return value
        except: return None

    def process_result_value(self, value, dialect):
        try: return f"/static_upload/images/{value}/"
        except: return None

    def copy(self, **kw):
        return ImageType(self.impl.length)