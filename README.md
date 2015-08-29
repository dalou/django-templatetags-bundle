# django-fontforge-watcher
======================

This add a command .

Usage
=====

Put ``'stylus_fontforge'`` into ``INSTALLED_APPS``.

Set settings ``FONTFORGE_WATCHER = [
    ('relative/path/to/main/stylus/file.styl', 'relative/path/to/compiled/file.css'), # A compilation rules
    ('relative/path/to/main/stylus/file.styl', 'relative/path/to/compiled/file.css'), # Antoher compilation rules
    ...etc
]

The watcher listen changes in every installed apps ``styl`` folder

Then run ``python manage.py stylus_fontforge``




# django-fontforge-watcher
