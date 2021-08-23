<a href="https://openx.com/">
    <img src="https://openx-prod.s3.amazonaws.com/uploads/2016/09/OX_Logo_1024x512.png" alt="OpenX logo" title="OpenX" align="right" height="60" />
</a>

# ox-api-client-py

[![standard-readme compliant](https://img.shields.io/badge/standard--readme-OK-green.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
**TODO**: Put more badges here, such as [Cloud Build Status](https://github.com/leg100/cloud-build-badge)

> The new client for OpenX API, for Python apps

This package supersedes the `ox3apiclient` and contains a rewritten client 
of OpenX API (OX API) for Python applications. It provides a wrapper for OAuth autenthication process
to log in into the OX API, and then wraps around standard requests, adding the auth headers.

In the future, we want to add some API autodiscovery to the client, and maybe a CLI app as a demo.

## Table of Contents
<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Background](#background)
- [Install](#install)
    - [Installed environments](#installed-environments)
    - [Logs and reports](#logs-and-reports)
- [Development](#development)
    - [Secrets](#secrets)
    - [Testing](#testing)
- [Usage](#usage)
- [API](#api)
- [Maintainers](#maintainers)
- [Contribute](#contribute)
    - [Contributors](#contributors)
- [License](#license)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Background

In order to use the OpenX Exchange API, which is a standard REST service,
you need to authenticate through OAuth 
(as described in [the docs](https://docs.openx.com/developers/about-topics-api/index.html)).
This library automates the process and simplifies it down to two things:

* instantiating the client with your client key/secret
* logging in as a user - either programatically or *interactively* (new!)


It makes the API usage as simple as:

```py
import OXApiClient

api = OXApiClient('abc123def456ghi789jklABCmnoDEFpqrGHIstuJ', '987abc654def321ghi123abc234def567ghi890a',
                  'sso.openx.com', 'your_realm', 'your-ui.openx.net')
api.login()  # interactive

# get root network account
example = api.get(f"/account?account_id=null").json()
master_id = example.get('objects')[0]['id']

print(f"My instance master network is under id {master_id}.")
```


## Install

```
pip install oxapiclient  # we've dropped the '3' from the name
```

**Requirements:**
- Code block illustrating how to install.

**Subsections:**
- `Dependencies`. Required if there are unusual dependencies or dependencies that must be manually installed.
- `Updating`. Optional.

**Suggestions:**
- Link to prerequisite sites for programming language: [npmjs](https://npmjs.com), [godocs](https://godoc.org), etc.
- Include any system-specific information needed for installation.
- If there is no code in the module - for instance, a document-based module - this section is not required.


### Logs and reports

The client does not log much by default, only some SimpleHTTPRequestHandler logs if using interactive login.
If you want to debug your OAuth1 login, you can do

```py
import logging

log = logging.getLogger("oauth1_session")
log.setLevel("DEBUG")
```


## Development

Describe the development process.


### Testing

`make test`

Describe how to test your project here, what test frameworks it uses and how would you like the tests to be written.


## Usage

```
npm run
```

**Requirements:**
- Code block illustrating common usage.
- If CLI compatible, code block indicating common usage.
- If importable, code block indicating both import functionality and usage.


## API

**Status:** Optional. Should be a separate document.

**Requirements:**
- Describe exported functions and objects.

**Suggestions:**
- Describe signatures, return types, callbacks, and events.
- Cover types covered where not obvious.
- Describe caveats.
- If using an external API generator (like go-doc, js-doc, or so on), point to an external `API.md` file. This can be the only item in the section, if present.


## Maintainers

* **Core developer**: [Cezar Pokorski](https://github.com/ikari-pl/) — This is the main project code owner, every major/architectural change should be agreed with them. Also consult for these scopes: project README, project python code.
* **Backup developer**: [TheOther Person](https://openx.com/people/theother.person/) — Secondary contact for the project.


## Contribute

PRs accepted. General PR guidelines:
 * x


### Contributors

* 🍻 Grzegorz Łyczba (kudos for Makefile template and standarization)


## License

Commercial License © 2021 OpenX
