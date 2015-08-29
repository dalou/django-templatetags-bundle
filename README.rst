django-stylus-watcher
======================

This add a command .

Usage
=====

Put ``'stylus_watcher'`` into ``INSTALLED_APPS``.

Set settings ``STYLUS_WATCHER = [
    ('relative/path/to/main/stylus/file.styl', 'relative/path/to/compiled/file.css'), # A compilation rules
    ('relative/path/to/main/stylus/file.styl', 'relative/path/to/compiled/file.css'), # Antoher compilation rules
    ...etc
]

The watcher listen changes in every installed apps ``styl`` folder

Then run ``python manage.py stylus_watcher``




