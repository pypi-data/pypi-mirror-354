
## ⚠️ Deprecation Notice
This SDK is deprecated and no longer actively maintained.

Docusign has launched a new IAM SDK, which includes support for Maestro, Navigator and Connected Fields API families in a single, unified package.

👉 We recommend migrating to the IAM SDK for the latest updates, support, and a streamlined developer experience.

🔗 [Learn more and get started](https://developers.docusign.com/docs/sdks/) 

# The Official Docusign Maestro Python Client SDK

[![PyPI version][pypi-image]][pypi-url]
![Deprecated](https://img.shields.io/badge/status-deprecated-red.svg)
<!--[![PyPI downloads][downloads-image]][downloads-url]-->

The Docusign SDK makes integrating Docusign into your apps and websites a seamless experience.

## Table of Contents
- [The Official Docusign Maestro Python Client SDK](#the-official-docusign-maestro-python-client-sdk)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Installation](#installation)
    - [Version Information](#version-information)
  - [Requirements](#requirements)
  - [Compatibility](#compatibility)
    - [Path setup:](#path-setup)
    - [Install via PIP:](#install-via-pip)
  - [SDK Dependencies](#sdk-dependencies)
  - [API Reference](#api-reference)
  - [Code examples](#code-examples)
  - [OAuth implementations](#oauth-implementations)
  - [Changelog](#changelog)
  - [Support](#support)
  - [License](#license)
    - [Additional resources](#additional-resources)

<a id="introduction"></a>
## Introduction
Leverage the power of Docusign workflows. Enjoy greater flexibility to manage your agreements using your own code in concert with the Maestro Workflow Designer.

<a id="installation"></a>
## Installation
This client SDK is provided as open source, which enables you to customize its functionality to suit your particular use case. To do so, download or clone the repository. If the SDK’s given functionality meets your integration needs, or if you’re working through our [code examples](https://developers.docusign.com/docs/maestro-api/how-to/) from the [Docusign Developer Center](https://developers.docusign.com/), you merely need to install it by following the instructions below.

<a id="versionInformation"></a>
### Version Information
- **API version**: 1.0.0
- **Latest SDK version**: 3.0.0

<a id="requirements"></a>
## Requirements
*   Python 2.7 (3.7+ recommended)
*   Free [developer account](https://go.docusign.com/o/sandbox/?postActivateUrl=https://developers.docusign.com/)

<a id="compatibility"></a>
## Compatibility
*   Python 2.7+

<a id="pathSetup"></a>
### Path setup:
1. Locate your Python installation, also referred to as a **site-packages** folder. This folder is usually labeled in a format of **Python{VersionNumber}**.  
    **Examples:**
    *   Unix/Linux: **/usr/lib/python2.7**
    *   Mac: **/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7**
    *   Windows: **C:\Users\{username}\AppData\Local\Programs\Python\Python37**
2. Add your Python folder’s path to your system as an environment variable.  
    **Unix/Linux:**
    1. Type the following command into your console: \
        **export PYTHONPATH = "${PYTHONPATH}:.:/_path_/_to_/_site-packages_"**
    2. Optionally, you can add this command to your system profile, which will run the command each time Python is launched.  

    **Windows:**
    <ol>
      <li>Open the Windows <strong>Control Panel.</strong></li>
      <li>Under the System and Security category, open the <strong>System</strong> information panel.</li>
      <li>Select <strong>Advanced System Settings</strong> to open the <strong>System Properties</strong> dialog box.</li>
      <li>On the <strong>Advanced</strong> tab, select the <strong>Environment Variables</strong> button at the lower-right corner.
          <ol style="list-style-type: lower-alpha">
              <li>Check to see whether <strong>PYTHONPATH</strong> has been added as a <strong>system variable.</strong></li>
              <li>If it has not, select <strong>New</strong> to add it. The variable you add is the path to the <strong>site-packages</strong> folder.</li>
          </ol>
      </li>
    </ol>


**Note:** If you are still unable to reference Python or pip via your command console, you can also add the path to the **site-packages** folder to the built-in environment variable labeled **Path**, which will take effect the next time you start your machine.

<a id="pip"></a>
### Install via PIP:
In your command console, type: **pip install docusign_maestro**  
    **Note:** This may require the command console to be elevated. You can accomplish this via sudo in Unix/Linux, or by running the command console as an administrator in Windows.

<a id="dependencies"></a>
## SDK Dependencies
This client has the following external dependencies:
*   certifi v14.05.14+
*   six v1.8.0+
*   python_dateutil v2.5.3+
*   setuptools v21.0.0+
*   urllib3 v1.15.1+
*   PyJWT v2.0.0+
*   cryptography v2.5+

<a id="apiReference"></a>
## API Reference
You can refer to the API reference [here](https://developers.docusign.com/docs/maestro-api/reference/).

<a id="codeExamples"></a>
## Code examples
Explore our GitHub repository for the [Launcher](https://github.com/docusign/code-examples-python/), a self-executing package housing code examples for the Maestro Python SDK. This package showcases several common use cases and their respective source files. Additionally, you can download a version preconfigured for your Docusign developer account from [Quickstart](https://developers.docusign.com/docs/esign-rest-api/quickstart/). These examples support both the [Authorization Code Grant](https://developers.docusign.com/platform/auth/authcode/) and [JSON Web Token (JWT)](https://developers.docusign.com/platform/auth/jwt/) authentication workflows.

## OAuth implementations
For details regarding which type of OAuth grant will work best for your Docusign integration, see [Choose OAuth Type](https://developers.docusign.com/platform/auth/choose/) in the [Docusign Developer Center](https://developers.docusign.com/).

For security purposes, Docusign recommends using the [Authorization Code Grant](https://developers.docusign.com/platform/auth/authcode/) flow.

<a id="changeLog"></a>
## Changelog
You can refer to the complete changelog [here](https://github.com/docusign/docusign-maestro-python-client/blob/master/CHANGELOG.md).

<a id="support"></a>
## Support
Log issues against this client SDK through GitHub. You can also reach out to us through [Docusign Community](https://community.docusign.com/developer-59) and [Stack Overflow](https://stackoverflow.com/questions/tagged/docusignapi).

<a id="license"></a>
## License
The Docusign Maestro Python Client SDK is licensed under the [MIT License](https://github.com/docusign/docusign-maestro-python-client/blob/master/LICENSE).

<a id="additionalResources"></a>
### Additional resources
*   [Docusign Developer Center](https://developers.docusign.com/)
*   [Docusign API on Twitter](https://twitter.com/docusignapi)
*   [Docusign For Developers on LinkedIn](https://www.linkedin.com/showcase/docusign-for-developers/)
*   [Docusign For Developers on YouTube](https://www.youtube.com/channel/UCJSJ2kMs_qeQotmw4-lX2)

[pypi-image]: https://img.shields.io/pypi/v/docusign_maestro.svg?style=flat
[pypi-url]: https://pypi.python.org/pypi/docusign_maestro
[downloads-image]: https://img.shields.io/pypi/dm/docusign_maestro.svg?style=flat
[downloads-url]: https://pypi.python.org/pypi/docusign_maestro