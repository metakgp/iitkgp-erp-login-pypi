# CHANGELOG

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
