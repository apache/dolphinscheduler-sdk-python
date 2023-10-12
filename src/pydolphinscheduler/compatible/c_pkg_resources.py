try:
    from pkg_resources import parse_requirements
except ImportError:
    # Python 3.12 compatibility
    from pip._vendor.pkg_resources import parse_requirements
