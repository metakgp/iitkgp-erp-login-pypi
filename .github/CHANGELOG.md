# CHANGELOG

 ## [2.4.0](https://github.com/proffapt/iitkgp-erp-login-pypi/compare/v2.3.7...v2.4.0) (2024-06-24)


### Features

* added erp package logging in api ([aad8d00](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/aad8d004a46b64244ba7bdf3367d9d625a617b5a))
* **format:** prettier ([f24fb23](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/f24fb239b417d4b310340d5aa63bc09b2605ec9e))
* improved code quality ([8e1ba6b](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/8e1ba6b37cb1b486616945ce98aacfa788c11e0f))


### Bug Fixes

* it works now :) ([aec6b9b](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/aec6b9be9cbd9597d7942d7e1c3351dc8efc0278))

 
 ### [2.3.7](https://github.com/proffapt/iitkgp-erp-login-pypi/compare/v2.3.6...v2.3.7) (2024-05-25)


### Bug Fixes

* request_otp() for manual login wasn't called ([#25](https://github.com/proffapt/iitkgp-erp-login-pypi/issues/25)) ([6255252](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/6255252b0624b85c8d5e0c22bb6b5182f33f21b6))

 
 ### [2.3.6](https://github.com/proffapt/iitkgp-erp-login-pypi/compare/v2.3.5...v2.3.6) (2024-03-01)


### Bug Fixes

* requires signin parameters to get OTP now ([533621b](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/533621bcefbce518467d3379880fc752a4a19474))

 
 ### [2.3.5](https://github.com/proffapt/iitkgp-erp-login-pypi/compare/v2.3.4...v2.3.5) (2023-11-25)


### Bug Fixes

* handling otp ([68ede04](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/68ede04e3b941e69896c26972903a68f36fa22d7))

 
 ### [2.3.4](https://github.com/proffapt/iitkgp-erp-login-pypi/compare/v2.3.3...v2.3.4) (2023-11-24)


### Bug Fixes

* **otp:** OTP is required on campus network as well ([8c97124](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/8c97124eb4bbff83978294971b36aaf6306b01ca))

 
 ### [2.3.3](https://github.com/proffapt/iitkgp-erp-login-pypi/compare/v2.3.2...v2.3.3) (2023-11-16)


### Bug Fixes

* Logout after sign in resulted in false positive for session_alive() ([f84840f](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/f84840f1a1a41046e36a6b80d939921beaefb706))

 
 ### [2.3.2](https://github.com/proffapt/iitkgp-erp-login-pypi/compare/v2.3.1...v2.3.2) (2023-09-11)


### Bug Fixes

* **session-check:** Bug in session and token validity check ([231eeb9](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/231eeb9e07930080a918eda8c737516d32a318a9))

 
 ### [2.3.1](https://github.com/proffapt/iitkgp-erp-login-pypi/compare/v2.3.0...v2.3.1) (2023-09-04)


### Features

* Adding all the cookies to session when building from file ([37dee5b](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/37dee5ba5e885809795ba8a2d3b5fe8be017ae47))
* Integrated session alive check ([1f58545](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/1f585459074f19d512769a9ee245eb2ec6d75f56))

 
 ## [2.3.0](https://github.com/proffapt/iitkgp-erp-login-pypi/compare/v2.2.1...v2.3.0) (2023-08-15)


### Features

* **better-code:** Modularised the login workflow ([5e48e55](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/5e48e55d7285eb542253b66c6a00a911241b5dba))
* Modular code capable of being used in backend for WebApps ([b64ca12](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/b64ca12a28a76b4850dbc342e30b7b8fc8a95346))
* modularised writing and fetching of tokens from file ([cde9ff7](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/cde9ff7e18e0149a0af707eb31b82f3d647ad96f))

 
 ### [2.2.1](https://github.com/proffapt/iitkgp-erp-login-pypi/compare/v2.2.0...v2.2.1) (2023-08-11)


### Features

* **minor:** Providing developer access to ROLL_NUMBER ([e5eec6f](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/e5eec6fb74ea30baca3e55b150283739ecf32e23))

 
 ## [2.2.0](https://github.com/proffapt/iitkgp-erp-login-pypi/compare/v2.1.3...v2.2.0) (2023-07-28)


### Bug Fixes

* OTP fetching wasn't handled when on campus network ([1bafd8b](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/1bafd8bd0bbf53004fd89ab0cc0e0af39abb8ed9))

 
 ### [2.1.3](https://github.com/proffapt/iitkgp-erp-login-pypi/compare/v2.1.2...v2.1.3) (2023-07-23)


### Features

* Fetch tokens from a file, created by the pacakge itself ([c51a4fa](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/c51a4fa7855bc945e2751d2d9c6c14d35fa3a5c6))


### Bug Fixes

* Updating cookies for re-using session rather than SSOToken ([8036028](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/8036028192a1485f553becc9b377bd3bdcdf21d2))

 
 ### [2.1.2](https://github.com/proffapt/iitkgp-erp-login-pypi/compare/v2.1.1...v2.1.2) (2023-07-22)


### Bug Fixes

* Failed when SESSION_STORAGE_FILE(optional) wasn't provided ([9c9941f](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/9c9941fab926195916506ae7101c07b045d9d579))

 
 ### [2.1.1](https://github.com/proffapt/iitkgp-erp-login-pypi/compare/v2.1.0...v2.1.1) (2023-07-22)


### Features

* **multithreading-support:** Patched frame call back specially for MFTP ([87cb67d](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/87cb67daeafddf97f2b687d92c776627448b0b99))


### Bug Fixes

* **logs:** Condition for logging 'Not Valid!' status of saved SSOToken ([c6e0771](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/c6e077115823cb83482ac298caed727c98fdeb47))

 
 ## [2.1.0](https://github.com/proffapt/iitkgp-erp-login-pypi/compare/v2.0.1...v2.1.0) (2023-07-21)


### Features

* Function to check the validity of SSOToken ([5623308](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/56233081c5334b6205dba2f8a8abbc6368b32191))
* **login:** Integrated token storage & validity check in login func ([3198cae](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/3198cae185af06b4e14dfd0fc1bf8a16b7d35d26))
* **utils:** Separated-out utility functions from read_mail.py ([bd0613f](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/bd0613f8908ce4ebc96cf3648570b55ad44df31a))


### Bug Fixes

* **workflow:** Version in pyproject.toml wasn't updating ([99b743d](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/99b743dc113ff386945604e839efdb433eb4a9d9))


 ## [2.0.1](https://github.com/proffapt/iitkgp-erp-login-pypi/compare/v2.0.0...v2.0.1) (2023-07-20)
 
 
### Features

* **workflow:** added workflow to draft a release, publish on pypi ([66cf0c8](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/66cf0c8ff0d309499cb91110a369ae4dcfba5a63))

### Bug Fixes

* **otp-fetch:** Updated OTP request to add `pass` parameter ([4d8c6b9](https://github.com/proffapt/iitkgp-erp-login-pypi/commit/4d8c6b93ade4720b6daaf0876483a08722702bc5))
