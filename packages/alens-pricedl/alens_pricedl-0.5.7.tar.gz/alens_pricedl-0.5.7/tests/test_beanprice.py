"""
Test beanprice directly.
"""
import os
import dotenv


dotenv.load_dotenv()

BOOK_FILE = os.getenv("BEANCOUNT_FILE")


def test_vanguard_au():
    """
    Test Vanguard AU price source.
    This is a test for debugging.
    """
    from beanprice import price

    import sys
    sys.argv = ["price.py", BOOK_FILE, "--clobber"]

    price.main()
