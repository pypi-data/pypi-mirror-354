"""A way to run the NCDLMUSE CLI with a Python call."""

from ncdlmuse.cli.run import main

if __name__ == '__main__':
    import sys

    from ncdlmuse import __name__ as module

    # `python -m <module>` typically displays the command as __main__.py
    if '__main__.py' in sys.argv[0]:
        sys.argv[0] = f'{sys.executable} -m {module}'
    main()
