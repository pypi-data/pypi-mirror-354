# FreeOTP-Export
[![PyPi Version](https://img.shields.io/pypi/v/freeotp-export.svg)](https://pypi.org/project/freeotp-export/)

Rescue your OTP tokens from FreeOTP

# Not compatible with modern FreeOTP

FreeOTP was finally updated and now uses a different storage format, which
this tool does not yet support. See #1


## Installing
You can install directly through pip: `pip install freeotp-export`

Alternatively, to install from source, clone the repo or download and unpack a
tarball, then...

- If you already have [poetry](https://python-poetry.org/) installed, you can
  just run:
  ```sh
  $ poetry run freeotp-export tokens.xml
  ```
- Otherwise, use pip: `pip install --upgrade .`
- If you must, running `__main__.py` may work if you have the dependencies
  installed.


## Usage
### Acquire the File
If your phone is rooted, you can just grab the file from
`/data/data/org.fedorahosted.freeotp/shared_prefs/tokens.xml`

Otherwise, start by enabling debugging on the phone and setting up the android
platform tools. Grab a backup off the app data by running
`adb backup org.fedorahosted.freeotp`, and when asked for a password, don't
enter one.

To read the resulting Android backup file, `backup.ab`, you can either use
[android-backup-extractor](https://github.com/nelenkov/android-backup-extractor):
```sh
$ abe unpack backup.ab - | tar xv --strip-components=3
```

Or yolo it by adding the tar header yourself:
```sh
$ ( printf "\x1f\x8b\x08\x00\x00\x00\x00\x00" ; tail -c +25 backup.ab ) | tar zxv --strip-components=3
```

You should then have the token file, `tokens.xml`.

### Read the File
Just run this tool, and it'll give you both the OTP URIs (`otpauth://...`) and
scannable QR codes. Note that Google Authenticator
[ignores](https://github.com/google/google-authenticator/wiki/Key-Uri-Format)
the `digits` parameter, so it does not work for issuers like Blizzard that use
lengths other than 6.

If you used `pip install`: `$ freeotp-export tokens.xml`

Or with Poetry: `$ poetry run freeotp-export tokens.xml`

After importing everything to a new app, be sure to delete `tokens.xml` and
`backup.ab`, since they contain all of your tokens!


## See Also
[freeotp-export](https://github.com/viljoviitanen/freeotp-export), an HTML/JS
tool to do the same thing, which I discovered after writing and publishing this.
