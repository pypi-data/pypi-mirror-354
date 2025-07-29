Achtung!
========

Achtung is a "PANIC compatible" (not 100%, but the basic features should be the same) Tango alarm device. The idea is that it could be pretty much dropped in as a replacement for `PyAlarm`. This holds as long as you don't rely on more "dynamic" features of PyAlarm. 

The main purpose is to use less system resources, as well as being a simpler code base using modern async python and PyTango APIs.


## Installation

Achtung expects a python version no older than 3.9.

You can install it from PyPI:

    $ pip install tangods-achtung
    
It's also on conda-forge:

    $ conda install -c conda-forge tangods-achtung

For development you probably want to work in a virtual env, install optional deps for running tests, and use pre-commit.
    
    $ git clone <this repo>
    $ cd dev-maxiv-achtung
    $ python -m venv env
    $ . env/bin/activate
    $ pip install -e[tests]
    $ pytest
    $ pre-commit install


## Releasing a new version

Simply create a new tag with a bumped version number (use semantic versioning). This will trigger a pipeline, ending with upload to PyPI. After an hour or so, the conda-forge bot should automatically pick it up and create a MR in https://github.com/conda-forge/tangods-achtung-feedstock to build a new conda package.


## Main differences to PyAlarm

- Less powerful alarm formulas. Achtung formulas only allows *attributes* (including attribute "properties" like `quality`, `exception` etc) and *variables*, apart from basic logic, arithmetic and the usual math functions. No "dynamic" features. This allows the alarms to be fully parsed on startup - and checked for errors - and then efficiently evaluated during runtime.

- Achtung is more strict about configuration, and will go into FAULT at startup if it has problems parsing it. The Status attribute should give you enough information to fix the issues, then run Init to reload it.

- "HTTP consumers" which are basically "web hooks"; sending JSON encoded messages to some HTTP endpoint whenever there is an event (alarm on/off etc). This can be used to integrate with other services. 

- No support for "receivers" (e.g. sending emails), this can be replaced by HTTP consumers.

- Various less common settings are absent.

- Not well documented :)


## Configuration

Generally Achtung is configured the same way as PyAlarm, with the same properties (see [here](https://tango-controls.readthedocs.io/projects/panic/en/latest/PyAlarmUserGuide.html#pyalarm-device-properties)). Achtung does not support all the settings on PyAlarm, however.

Some notable differences:

* `Actions` replaces `AlarmRecievers` with a mechanism intended to be a bit simpler. It takes lines on the form
    
        my_alarm_tag:reset:write_attribute:sys/tg_test/1/boolean_scalar:1
    
 This means that any time the `my_alarm_tag` alarm is reset, achtung will write a `1` (i.e. "true") to the attribute `boolean_scalar` on device `sys/tg_test/1`. Values/arguments are specified as JSON, so for a string argument, e.g. `"hello"`, a list `[1, 2, 3]`, etc. It's also possible to replace `write_attribute` with `run_command` which works in a similar way, running a device command. For commands that take no argument, just leave out the last `;`, e.g.
 
        my_alarm_tag:reset:run_command:sys/tg_test/1/switchstates
        
 Note: reset actions are run even if the alarm is still active! Furthermore, when running the ResetAll command, identical reset actions will only be run once.
 
* `HttpConsumers` which is a list of HTTP URLs where JSON reports will be POST:ed on alarm status changes. This is intended to replace the `AlarmReceivers` property of PyAlarm and enable integration with e.g. logstash (see below).

* `ReportExtras` is a JSON encoded string containing static key-values that will be added to the JSON reports sent to HTTP consumers.

* `AttributeSeparator` allows changing the default separator `:` used in attributes to separate fields, to something else, e.g. `;`.
* `PropertySeparator` same as above, but for configuration properties (e.g. `AlarmList`).

For the full list of supported properties, see `achtung/achtung.py`.


### Formula syntax

Formulas are how you express the conditions for an alarm to become active. A formula should result in a boolean value; `True` or `False`. The syntax is based on python syntax. Achtung does not support the dynamic fandango based features of PyTango.

It's recommended to always separate the parts of your formula with spaces, e.g. `a == 0` instead of `a==0`. It prevents some ambiguity and is also more readable. Longer formulas may use parentheses to clarify grouping.

Some examples of valid, but not very useful formulas:

- `True` This alarm will *always* be active
- `False` Similarly will *never* be active
- `1 != 2`  Always active
- `1 == 2`  Never active

In order to actually be useful, formulas must contain at least one device attribute:

- `sys/tg_test/1/ampli == 3` This alarm is active if the ampli attribute equals 3 exactly.
- `sys/tg_test/1/ampli < 5` ...less than 5.
- `sys/tg_test/1/ampli * 3 >= 10`  Basic math is allowed
- `abs(sys/tg_test/1/ampli) > 10e6`  Also some math functions (see below)
- `sys/tg_test/1/ampli < sys/tg_test/2/ampli` Comparing different attributes
- `sys/tg_test/1/state != ON` Active if device in any other state than ON
- `sys/tg_test/1/boolean_scalar` Directly use a value that is boolean

Hoefully you get the picture. More complex logical expressions are also possible:

- `(sys/tg_test/1/ampli >= 5) and (sys/tg_test/1/ampli < 10)` Attribute value in the given range.
- `not ((sys/tg_test/1/ampli < 2.0 and sys/tg_test/2/ampli < 0) or (sys/tg_test/2/ampli < 6))` Parentheses can be helpful.

More examples:

- `tango://some-other-csdb:10000/sys/tg_test/2/ampli == 0` Access to attributes in a different control system.
- `sys/tg_test/1/ampli.exception` Active if there's a problem accessing the attribute.
- `sys/tg_test/1/ampli.quality != ATTR_VALID` Active if the attribute is not valid, as reported by the device.
- `sys/tg_test/1/ampli.quality == ATTR_ALARM` Active if the attribute's value is outside its min/max_alarm settings.
- `"fault" in sys/tg_test/1/string_scalar` Checking if a substring is present

Operators allowed in formulas (they work like in python):
- `+ - * /`
- `**` power
- `== > < <= >=` for comparison
- `in` for checking for substrings
- `and`, `or`, `not` for logic
- `abs()`, `sin()`, `cos()`, `exp()`, `round()` for rounding to nearest integer

If you have a need for more advanced ways of writing formulas, please get in touch with the software team (or create an "issue" in this repo). 

You can find some more examples of formulas in `test/test_evaulator.py`.


### Usage with Logstash, Fluentbit, etc.

Achtung can be configured to write alarm reports to a local file, by setting the `ReportLogfile` property. Reports are generated whenever an alarm's status, and appended to the logfile.

The logfile is in ND-JSON (newline delimited) format, where each line is a separate JSON object. This format can easily be ingested by tools like fluentbit, to be sent to a database backend for example. The file is automatically rotated and the settings for rotation can be changed using the `ReportLogfileMaxBytes` and `ReportLogfileBackupCount` properties.

The http consumers feature (see above) is also using a format compatible with Logstash. Here's a logstash configuration example.

```
input {
    http {
        port => 8732
        codec => json
    }
}

filter {
    date {
        match => ["timestamp", "ISO8601"] 
        target => "@timestamp"
    }
}

output {
    elasticsearch {
        hosts => ["<some-es-host>", "..."]
        index => "tango-alarms-%{+YYYY.MM.dd}"
        document_type => "alarm"
    }
}
```
The port can of course be anything, and the output tailored to your needs. This pipeline must also be added to e.g. `/etc/logstash/pipelines.yml`.

Now just remains to add a line to the `HTTPConsumer` property in Achtung: `http://<logstash-host>:8732`.

If you want to play with the HttpConsumers feature locally, there is a small 
service in `tests/consumer.py` that will print out any reports it gets.

#### Filtering

The device can filter which alarms are to be sent to each HTTP consumer, currently only by
"severity". To do this, put a JSON string in the property instead of just a URL, e.g.

    {"url": "http://<logstash-host>:8732", "severity": ["ALARM"]}
    
This will configure a consumer with the given URL, which only receives reports for alarms of severity "ALARM".


### New evaluator

There's an *experimental* evaluator which supports all Python expression syntax, and is significantly
faster as a bonus. It changes the attribute read method to read all attributes from the same device
at once. This is a great improvement at MAX IV since almost all our alarms are based on PLC tags read as
attributes from a few centralized devices. But it's possible that it will cause differences in behavior
in some cases. In general, formulas that work with the old evaluator should still work with the new.

However, the new evaluator is based on `eval` and could therefore potentially open up security
holes if the device is run with wide permissions. We try to restrict the usage to only safe parts
of Python, but this is generally known as a hard problem. However, PyAlarm also uses `eval`.

For now, the property `UseNewEvaluator` must be set to `True` for the new evaluator to be used. 
If it's is deemed safe and reliable, it may become the default in the future.
