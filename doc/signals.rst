Signals
=======

Signals are the heart of inter-module communication in GlorIRCd.  Using this
system, new modules can be added quickly, and replacement modules you write
yourself can take advantage of all the messages that the core modules use.

Signals are namespaced in the following form:

* A **category name**.  A list of the built-in categories appears later in this
  documentation.

* A **module name**.  This must be unique within the signal's category.

* A **signal name**.  This must be unique to the category/module pair.


Built-in categories
-------------------

core
````

This category is reserved for core GlorIRCd modules.  As such, you should never
define your own signals within the core category.  You may, of course, listen
on any documented core signal.  Additionally, if you are reimplementing a core
module for your own use, you may call any applicable defined core signal.
However, you must never create your own or use (listen on or call) any
undocumented core signal.

io
``

This category is used by the various GlorIRCd I/O backends.  They are generally
very low-level and have a limited scope for custom modules.  Nevertheless, they
are a part of the public GlorIRCd API and the global signals are guaranteed to
be available on any official GlorIRCd I/O backend.

store
`````

This category is used by the Data Store.

user
````

This category is "free" for use by any custom user module.  GlorIRCd will never
conflict with signals in this category; however, care should still be taken to
ensure that custom modules you use and write don't conflict amongst themselves.
