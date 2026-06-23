from uuid import uuid4


class TempIndex:
    @staticmethod
    def generate_collection_name():
        return f"benchmark_{uuid4().hex}"