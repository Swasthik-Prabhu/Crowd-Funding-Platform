from passlib.context import CryptContext
pwd_cxt = CryptContext(schemes=["bcrypt"],deprecated = "auto")

class Hash:
    @staticmethod
    def bcrypt(password : str) -> str:
        hashedPassword = pwd_cxt.hash(password)
        return hashedPassword