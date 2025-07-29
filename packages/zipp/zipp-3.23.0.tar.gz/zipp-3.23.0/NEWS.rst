v3.23.0
=======

Features
--------

- Add a compatibility shim for Python 3.13 and earlier. (#145)


v3.22.0
=======

Features
--------

- Backported simplified tests from python/cpython#123424. (#142)


Bugfixes
--------

- Fixed ``.name``, ``.stem``, and other basename-based properties on Windows when working with a zipfile on disk. (#133)


v3.21.0
=======

Features
--------

- Improve performances of :meth:`zipfile.Path.open` for non-reading modes. (1a1928d)
- Rely on cached_property to cache values on the instance.
- Rely on save_method_args to save method args.


v3.20.2
=======

Bugfixes
--------

- Make zipp.compat.overlay.zipfile hashable. (#126)


v3.20.1
=======

Bugfixes
--------

- Replaced SanitizedNames with a more surgical fix for infinite loops, restoring support for names with special characters in the archive. (python/cpython#123270)


v3.20.0
=======

Features
--------

- Made the zipfile compatibility overlay available as zipp.compat.overlay.


v3.19.3
=======

Bugfixes
--------

- Also match directories in Path.glob. (#121)


v3.19.2
=======

No significant changes.


v3.19.1
=======

Bugfixes
--------

- Improved handling of malformed zip files. (#119)


v3.19.0
=======

Features
--------

- Implement is_symlink. (#117)


v3.18.2
=======

No significant changes.


v3.18.1
=======

No significant changes.


v3.18.0
=======

Features
--------

- Bypass ZipFile.namelist in glob for better performance. (#106)
- Refactored glob functionality to support a more generalized solution with support for platform-specific path separators. (#108)


Bugfixes
--------

- Add special accounting for pypy when computing the stack level for text encoding warnings. (#114)


v3.17.0
=======

Features
--------

- Added ``CompleteDirs.inject`` classmethod to make available for use elsewhere.


Bugfixes
--------

- Avoid matching path separators for '?' in glob.


v3.16.2
=======

Bugfixes
--------

- In ``Path.match``, Windows path separators are no longer honored. The fact that they were was incidental and never supported. (#92)
- Fixed name/suffix/suffixes/stem operations when no filename is present and the Path is not at the root of the zipfile. (#96)
- Reworked glob utilizing the namelist directly. (#101)


v3.16.1
=======

Bugfixes
--------

- Replaced the ``fnmatch.translate`` with a fresh glob-to-regex translator for more correct matching behavior. (#98)


v3.16.0
=======

Features
--------

- Require Python 3.8 or later.


v3.15.0
=======

* gh-102209: ``test_implied_dirs_performance`` now tests
  measures the time complexity experimentally.

v3.14.0
=======

* Minor cleanup in tests, including #93.

v3.13.0
=======

* In tests, add a fallback when ``func_timeout`` isn't available.

v3.12.1
=======

* gh-101566: In ``CompleteDirs``, override ``ZipFile.getinfo``
  to supply a ``ZipInfo`` for implied dirs.

v3.12.0
=======

* gh-101144: Honor ``encoding`` as positional parameter
  to ``Path.open()`` and ``Path.read_text()``.

v3.11.0
=======

* #85: Added support for new methods on ``Path``:

  - ``match``
  - ``glob`` and ``rglob``
  - ``relative_to``
  - ``is_symlink``

v3.10.0
=======

* ``zipp`` is now a package.

v3.9.1
======

* Removed 'print' expression in test_pickle.

* bpo-43651: Apply ``io.text_encoding`` on Python 3.10 and later.

v3.9.0
======

* #81: ``Path`` objects are now pickleable if they've been
  constructed from pickleable objects. Any restored objects
  will re-construct the zip file with the original arguments.

v3.8.1
======

Refreshed packaging.

Enrolled with Tidelift.

v3.8.0
======

Removed compatibility code.

v3.7.0
======

Require Python 3.7 or later.

v3.6.0
======

#78: Only ``Path`` is exposed in the public API.

v3.5.1
======

#77: Remove news file intended only for CPython.

v3.5.0
======

#74 and bpo-44095: Added ``.suffix``, ``.suffixes``,
and ``.stem`` properties.

v3.4.2
======

Refresh package metadata.

v3.4.1
======

Refresh packaging.

v3.4.0
======

#68 and bpo-42090: ``Path.joinpath`` now takes arbitrary
positional arguments and no longer accepts ``add`` as a
keyword argument.

v3.3.2
======

Updated project metadata including badges.

v3.3.1
======

bpo-42043: Add tests capturing subclassing requirements.

v3.3.0
======

#9: ``Path`` objects now expose a ``.filename`` attribute
and rely on that to resolve ``.name`` and ``.parent`` when
the ``Path`` object is at the root of the zipfile.

v3.2.0
======

#57 and bpo-40564: Mutate the passed ZipFile object
type instead of making a copy. Prevents issues when
both the local copy and the caller's copy attempt to
close the same file handle.

#56 and bpo-41035: ``Path._next`` now honors
subclasses.

#55: ``Path.is_file()`` now returns False for non-existent names.

v3.1.0
======

#47: ``.open`` now raises ``FileNotFoundError`` and
``IsADirectoryError`` when appropriate.

v3.0.0
======

#44: Merge with v1.2.0.

v1.2.0
======

#44: ``zipp.Path.open()`` now supports a compatible signature
as ``pathlib.Path.open()``, accepting text (default) or binary
modes and soliciting keyword parameters passed through to
``io.TextIOWrapper`` (encoding, newline, etc). The stream is
opened in text-mode by default now. ``open`` no
longer accepts ``pwd`` as a positional argument and does not
accept the ``force_zip64`` parameter at all. This change is
a backward-incompatible change for that single function.

v2.2.1
======

#43: Merge with v1.1.1.

v1.1.1
======

#43: Restored performance of implicit dir computation.

v2.2.0
======

#36: Rebuild package with minimum Python version declared both
in package metadata and in the python tag.

v2.1.0
======

#32: Merge with v1.1.0.

v1.1.0
======

#32: For read-only zip files, complexity of ``.exists`` and
``joinpath`` is now constant time instead of ``O(n)``, preventing
quadratic time in common use-cases and rendering large
zip files unusable for Path. Big thanks to Benjy Weinberger
for the bug report and contributed fix (#33).

v2.0.1
======

#30: Corrected version inference (from jaraco/skeleton#12).

v2.0.0
======

Require Python 3.6 or later.

v1.0.0
======

Re-release of 0.6 to correspond with release as found in
Python 3.8.

v0.6.0
======

#12: When adding implicit dirs, ensure that ancestral directories
are added and that duplicates are excluded.

The library now relies on
`more_itertools <https://pypi.org/project/more_itertools>`_.

v0.5.2
======

#7: Parent of a directory now actually returns the parent.

v0.5.1
======

Declared package as backport.

v0.5.0
======

Add ``.joinpath()`` method and ``.parent`` property.

Now a backport release of the ``zipfile.Path`` class.

v0.4.0
======

#4: Add support for zip files with implied directories.

v0.3.3
======

#3: Fix issue where ``.name`` on a directory was empty.

v0.3.2
======

#2: Fix TypeError on Python 2.7 when classic division is used.

v0.3.1
======

#1: Fix TypeError on Python 3.5 when joining to a path-like object.

v0.3.0
======

Add support for constructing a ``zipp.Path`` from any path-like
object.

``zipp.Path`` is now a new-style class on Python 2.7.

v0.2.1
======

Fix issue with ``__str__``.

v0.2.0
======

Drop reliance on future-fstrings.

v0.1.0
======

Initial release with basic functionality.
